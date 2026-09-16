"""Fast evaluator contract tests; no Go runtime or model invocation."""

import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "evaluate.py"
spec = importlib.util.spec_from_file_location("evaluate", SCRIPT)
evaluate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(evaluate)


def events(*actions):
    return "\n".join(json.dumps(dict(Package="example.com/skillfixture", **a)) for a in actions)


class EvaluatorTest(unittest.TestCase):
    def setUp(self):
        self.case = evaluate.load_cases()["G01"]
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.workspace = self.directory / "workspace"

    def check_catalog_rejection(self, change):
        case = copy.deepcopy(self.case)
        change(case)
        file = self.directory / "bad.json"
        file.write_text(json.dumps({"version": 1, "cases": [case]}))
        with self.assertRaises(ValueError):
            evaluate.load_cases(file)

    def test_catalog_contains_materialized_subset_only(self):
        self.assertEqual(set(evaluate.load_cases()), {"G01", "G09", "G14", "G17"})

    def test_rejects_path_traversal(self):
        self.check_catalog_rejection(lambda c: c["files"].update({"../oracle.go": "bad"}))

    def test_requires_named_oracle(self):
        self.check_catalog_rejection(lambda c: c.update(tests=[]))

    def test_rejects_empty_source(self):
        self.check_catalog_rejection(lambda c: c.update(control=""))

    def test_prepare_exports_only_inputs(self):
        result = evaluate.prepare(self.case, self.workspace)
        self.assertEqual(set(p.name for p in self.workspace.iterdir()), {"app.go", "go.mod"})
        self.assertEqual(result["prompt"], self.case["prompt"])
        self.assertNotIn("expected_any", result)
        self.assertNotIn("oracle", result)
        self.assertNotIn("control", result)

    def test_prepare_never_overwrites_workspace(self):
        evaluate.prepare(self.case, self.workspace)
        with self.assertRaises(FileExistsError):
            evaluate.prepare(self.case, self.workspace)

    def test_snapshot_protects_module_baseline(self):
        evaluate.prepare(self.case, self.workspace)
        (self.workspace / "go.mod").write_text("module different\n")
        with self.assertRaises(ValueError):
            evaluate.snapshot(self.workspace, self.case)

    def test_candidate_cannot_supply_oracle(self):
        evaluate.prepare(self.case, self.workspace)
        (self.workspace / evaluate.ORACLE).write_text("package fixture")
        with self.assertRaises(ValueError):
            evaluate.snapshot(self.workspace, self.case)

    def test_rejects_symlink(self):
        evaluate.prepare(self.case, self.workspace)
        try:
            (self.workspace / "link.go").symlink_to(self.workspace / "app.go")
        except (NotImplementedError, OSError):
            self.skipTest("symlink creation unavailable")
        with self.assertRaises(ValueError):
            evaluate.snapshot(self.workspace, self.case)

    def test_accepts_added_go_tests(self):
        evaluate.prepare(self.case, self.workspace)
        (self.workspace / "app_test.go").write_text("package fixture")
        self.assertIn("app_test.go", evaluate.snapshot(self.workspace, self.case))

    def test_success_requires_named_execution_and_package_pass(self):
        text = events({"Action": "run", "Test": "TestOracleClamp"}, {"Action": "pass", "Test": "TestOracleClamp"}, {"Action": "pass"})
        self.assertEqual(evaluate.classify(0, text, self.case["tests"])[0], "runtime-pass")

    def test_empty_success_is_inconclusive(self):
        self.assertEqual(evaluate.classify(0, "", self.case["tests"])[0], "inconclusive")

    def test_skip_is_not_pass(self):
        text = events({"Action": "run", "Test": "TestOracleClamp"}, {"Action": "skip", "Test": "TestOracleClamp"}, {"Action": "pass"})
        self.assertEqual(evaluate.classify(0, text, self.case["tests"])[0], "inconclusive")

    def test_compile_error_is_not_negative_control_evidence(self):
        self.assertEqual(evaluate.classify(1, "build failed", self.case["tests"])[0], "inconclusive")

    def test_named_failure_is_runtime_failure(self):
        text = events({"Action": "run", "Test": "TestOracleClamp"}, {"Action": "fail", "Test": "TestOracleClamp"})
        self.assertEqual(evaluate.classify(1, text, self.case["tests"])[0], "runtime-fail")

    def test_other_package_cannot_supply_pass(self):
        text = events({"Action": "run", "Test": "TestOracleClamp"}, {"Action": "pass", "Test": "TestOracleClamp"}, {"Action": "pass"}).replace("example.com/skillfixture", "other")
        self.assertEqual(evaluate.classify(0, text, self.case["tests"])[0], "inconclusive")

    def test_fixture_fingerprint_changes_with_oracle(self):
        modified = copy.deepcopy(self.case)
        modified["oracle"] += "\n// changed expectation\n"
        self.assertNotEqual(evaluate.digest(self.case), evaluate.digest(modified))


if __name__ == "__main__":
    unittest.main()
