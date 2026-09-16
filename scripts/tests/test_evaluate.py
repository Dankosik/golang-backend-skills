"""Fast authoring checks; no model, Go process, network, or service is started."""

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("evaluate", ROOT / "scripts/evaluate.py")
evaluate = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(evaluate)


def events(*pairs):
    return "\n".join(json.dumps({"Action": action, **({"Test": test} if test else {})}) for action, test in pairs)


class EvaluationTests(unittest.TestCase):
    def test_catalog(self):
        self.assertEqual(set(evaluate.catalog(ROOT)), {"G01", "G04", "G08", "G09", "G14", "G17"})

    def test_reference_requires_one_match(self):
        for source in ["absent", "old old"]:
            with self.assertRaises(ValueError):
                evaluate.reference(source, [{"old": "old", "new": "new"}])

    def test_reference_applies(self):
        self.assertEqual(evaluate.reference("old", [{"old": "old", "new": "new"}]), "new")

    def test_empty_test_selection_never_passes(self):
        self.assertFalse(evaluate.parse_results(events(("pass", None)), set(), 0)["passed"])

    def test_missing_hidden_tests_never_pass(self):
        self.assertFalse(evaluate.parse_results(events(("pass", None)), {"TestEvalX"}, 0)["passed"])

    def test_skip_never_passes(self):
        self.assertFalse(evaluate.parse_results(events(("skip", "TestEvalX"), ("pass", None)), {"TestEvalX"}, 0)["passed"])

    def test_nonzero_exit_never_passes(self):
        self.assertFalse(evaluate.parse_results(events(("pass", "TestEvalX"), ("pass", None)), {"TestEvalX"}, 1)["passed"])

    def test_requires_package_completion(self):
        self.assertFalse(evaluate.parse_results(events(("pass", "TestEvalX")), {"TestEvalX"}, 0)["passed"])

    def test_success_requires_all_tests(self):
        log = events(("pass", "TestEvalX"), ("pass", "TestEvalY"), ("pass", None))
        self.assertTrue(evaluate.parse_results(log, {"TestEvalX", "TestEvalY"}, 0)["passed"])

    def test_malformed_events_are_not_evidence(self):
        self.assertFalse(evaluate.parse_results("not-json\n[]\n42", {"TestEvalX"}, 0)["passed"])

    def test_prepare_does_not_leak_graders(self):
        with tempfile.TemporaryDirectory() as temporary:
            work = Path(temporary) / "new"
            evaluate.prepare(ROOT, "G01", work)
            self.assertEqual({p.name for p in work.iterdir()}, {"clamp.go", "go.mod"})
            with self.assertRaises(ValueError):
                evaluate.prepare(ROOT, "G01", work)

    def test_snapshot_rejects_metadata_change(self):
        with tempfile.TemporaryDirectory() as temporary:
            work = Path(temporary) / "new"
            evaluate.prepare(ROOT, "G01", work)
            (work / "go.mod").write_text("module replacement\ngo 1.23\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                evaluate.snapshot(work, ROOT / "evals/fixtures/G01", "clamp.go")

    def test_reserved_grader_cannot_be_supplied(self):
        with tempfile.TemporaryDirectory() as temporary:
            work = Path(temporary) / "new"
            evaluate.prepare(ROOT, "G01", work)
            (work / evaluate.RESERVED).write_text("package fixture\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                evaluate.snapshot(work, ROOT / "evals/fixtures/G01", "clamp.go")

    def test_candidate_source_is_copied_unchanged(self):
        with tempfile.TemporaryDirectory() as temporary:
            work = Path(temporary) / "new"
            evaluate.prepare(ROOT, "G01", work)
            source = evaluate.snapshot(work, ROOT / "evals/fixtures/G01", "clamp.go")
            self.assertEqual(source["clamp.go"], (work / "clamp.go").read_bytes())

    def test_routing_controls(self):
        rows = evaluate.routing(ROOT)
        self.assertEqual(len(rows), 29)
        self.assertEqual(sum(r["mode"] == "no-go-skill" for r in rows.values()), 8)
        self.assertIn("$go-implement", rows["E01"]["prompt"])

    def test_checkpoint_retains_partial_and_final_status(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "report.json"
            path.write_text("{}", encoding="utf-8")
            evaluate.write_checkpoint(path, {"complete": False, "passed": False, "cases": ["G01"]})
            self.assertFalse(json.loads(path.read_text())["complete"])
            evaluate.write_checkpoint(path, {"complete": True, "passed": True})
            self.assertTrue(json.loads(path.read_text())["passed"])
            self.assertEqual(list(path.parent.iterdir()), [path])

    def test_wrong_event_types_are_not_evidence(self):
        self.assertFalse(evaluate.parse_results('{"Action": "pass", "Test": []}', {"TestEvalX"}, 0)["passed"])


if __name__ == "__main__":
    unittest.main()
