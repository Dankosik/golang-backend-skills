"""Fast evaluator contract tests. No model, network, or Go toolchain required."""

import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import evaluate


class OutcomeTests(unittest.TestCase):
    def run_record(self, events, code=0, error=None):
        return {"exit_code": code, "error": error,
                "output": "\n".join(json.dumps(e) for e in events)}

    def event(self, action, name=None, package="example.com/skill-eval"):
        event = {"Action": action, "Package": package}
        if name:
            event["Test"] = name
        return event

    def check(self, events, **kwargs):
        return evaluate.test_outcome(self.run_record(events, **kwargs), ["TestContractValue"])["passed"]

    def test_actual_test_and_package_pass(self):
        self.assertTrue(self.check([self.event("pass", "TestContractValue"), self.event("pass")]))

    def test_zero_exit_without_tests_is_not_pass(self):
        self.assertFalse(self.check([]))

    def test_package_pass_without_required_test_is_not_pass(self):
        self.assertFalse(self.check([self.event("pass")]))

    def test_required_skip_is_not_pass(self):
        self.assertFalse(self.check([self.event("skip", "TestContractValue"), self.event("pass")]))

    def test_skipped_subtest_is_not_pass(self):
        self.assertFalse(self.check([self.event("skip", "TestContractValue/edge"),
                                    self.event("pass", "TestContractValue"), self.event("pass")]))

    def test_wrong_package_is_not_pass(self):
        self.assertFalse(self.check([self.event("pass", "TestContractValue", "other"), self.event("pass")]))

    def test_nonzero_exit_overrides_pass_events(self):
        self.assertFalse(self.check([self.event("pass", "TestContractValue"), self.event("pass")], code=1))

    def test_runner_error_overrides_pass_events(self):
        self.assertFalse(self.check([self.event("pass", "TestContractValue"), self.event("pass")], error="timeout"))

    def test_printed_pass_is_not_execution(self):
        self.assertFalse(self.check([{"Action": "output", "Package": "example.com/skill-eval",
                                     "Output": "PASS TestContractValue"}, self.event("pass")]))

    def test_non_json_success_fails_closed(self):
        run = self.run_record([self.event("pass", "TestContractValue"), self.event("pass")])
        run["output"] += "\ncorrupted trace"
        self.assertFalse(evaluate.test_outcome(run, ["TestContractValue"])["passed"])

    def test_malformed_json_value_fails_closed(self):
        self.assertFalse(self.check([[], self.event("pass", "TestContractValue"), self.event("pass")]))


class FixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = evaluate.load_cases()
        cls.case = cls.cases["G01"]

    def test_all_fixture_graders_declare_required_tests(self):
        for case in self.cases.values():
            with self.subTest(case=case["id"]):
                text = evaluate.fixture_bytes(case, "grader/contract_test.go").decode()
                for name in case["required_tests"]:
                    self.assertIn("func " + name + "(t *testing.T)", text)
                self.assertNotEqual(evaluate.fixture_bytes(case, "input/task.go"),
                                    evaluate.fixture_bytes(case, "reference/task.go"))

    def test_prepare_does_not_expose_grader_or_reference(self):
        with tempfile.TemporaryDirectory() as temp:
            work = Path(temp) / "work"
            receipt = evaluate.prepare(self.case, work)
            self.assertEqual({p.name for p in work.iterdir()}, {"go.mod", "task.go", "TASK.md"})
            self.assertEqual(receipt["fixture_sha256"], evaluate.fixture_identity(self.case))
            self.assertEqual((work / "task.go").read_bytes(), evaluate.fixture_bytes(self.case, "input/task.go"))

    def test_prepare_refuses_existing_workspace(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(FileExistsError):
                evaluate.prepare(self.case, Path(temp))

    def test_prepare_refuses_evaluator_checkout(self):
        with self.assertRaises(ValueError):
            evaluate.prepare(self.case, evaluate.ROOT / "do-not-create")

    def test_changed_module_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            work = Path(temp) / "work"
            evaluate.prepare(self.case, work)
            (work / "go.mod").write_text("module other\n")
            self.assertEqual(evaluate.grade(self.case, work)["artifact_status"], "fail")

    def test_missing_source_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            work = Path(temp) / "work"
            evaluate.prepare(self.case, work)
            (work / "task.go").unlink()
            with self.assertRaises(ValueError):
                evaluate.snapshot(work)

    @unittest.skipUnless(os.name == "posix", "symlink fixture uses POSIX")
    def test_symlinked_source_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            work = Path(temp) / "work"
            evaluate.prepare(self.case, work)
            source = work / "task.go"
            source.unlink()
            source.symlink_to(work / "TASK.md")
            with self.assertRaises(ValueError):
                evaluate.snapshot(work)

    def test_missing_go_is_unavailable_not_pass(self):
        with tempfile.TemporaryDirectory() as temp:
            work = Path(temp) / "work"
            evaluate.prepare(self.case, work)
            with patch.object(evaluate.shutil, "which", return_value=None):
                result = evaluate.grade(self.case, work)
            self.assertEqual(result["artifact_status"], "unavailable")
            self.assertEqual(result["behavior_status"], "not_evaluated")

    def test_oversized_source_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            work = Path(temp) / "work"
            evaluate.prepare(self.case, work)
            (work / "task.go").write_bytes(b"x" * (evaluate.MAX_BYTES + 1))
            with self.assertRaises(ValueError):
                evaluate.snapshot(work)


class RoutingDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((evaluate.EVALS / "routing.json").read_text())

    def test_ids_are_unique(self):
        ids = [case["id"] for case in self.data["cases"]]
        self.assertEqual(len(ids), len(set(ids)))

    def test_not_run_is_explicit(self):
        self.assertEqual(self.data["status"], "not_run")

    def test_all_sixteen_domains_have_implicit_cases(self):
        implicit = [case for case in self.data["cases"] if case["kind"] == "implicit"]
        skills = {skill for case in implicit for skill in case["relevant_skills"]}
        self.assertEqual(len(skills), 16)
        for case in implicit:
            for skill in case["relevant_skills"]:
                self.assertNotIn(skill, case["prompt"])

    def test_negative_controls_do_not_request_go_skills(self):
        negative = [case for case in self.data["cases"] if case["kind"] == "negative"]
        self.assertEqual(len(negative), 4)
        self.assertTrue(all(case["relevant_skills"] == [] for case in negative))


@unittest.skipUnless(os.name == "posix", "bounded execution uses POSIX process groups")
class RunnerTests(unittest.TestCase):
    def test_timeout_is_recorded(self):
        result = evaluate.run_bounded([sys.executable, "-c", "import time; time.sleep(10)"],
                                      evaluate.ROOT, {}, seconds=0.05)
        self.assertIsNotNone(result["error"])
        self.assertNotEqual(result["exit_code"], 0)

    def test_output_is_bounded_and_not_passed(self):
        result = evaluate.run_bounded([sys.executable, "-c", "print('x' * 1200000)"],
                                      evaluate.ROOT, {}, seconds=5)
        self.assertIsNotNone(result["error"])
        self.assertLessEqual(len(result["output"]), evaluate.MAX_BYTES)


if __name__ == "__main__":
    unittest.main()
