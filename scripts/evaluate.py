#!/usr/bin/env python3
"""Prepare tiny Go fixtures and grade artifacts; never invoke a model or certify its trace."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
EVALS = ROOT / "evals"
MODULE = "module example.com/skill-eval\n\ngo 1.23.0\n"
MAX_BYTES = 1_048_576


def digest(data):
    return hashlib.sha256(data).hexdigest()


def load_cases():
    data = json.loads((EVALS / "cases.json").read_text(encoding="utf-8"))
    if data.get("schema_version") != 1:
        raise ValueError("unsupported case schema")
    cases = {}
    for case in data["cases"]:
        key = case["id"]
        if not re.fullmatch(r"G\d{2}", key) or key in cases:
            raise ValueError("invalid or duplicate case ID")
        tests = case["required_tests"]
        if not tests or len(tests) != len(set(tests)) or not all(re.fullmatch(r"TestContract\w+", t) for t in tests):
            raise ValueError("case must name distinct required tests")
        if not isinstance(case["prompt"], str) or not case["prompt"].strip():
            raise ValueError("case needs a task prompt")
        for part in ("input/task.go", "grader/contract_test.go", "reference/task.go"):
            file = EVALS / "fixtures" / key / part
            if file.is_symlink() or not file.is_file():
                raise ValueError("missing or symlinked fixture: " + str(file))
        cases[key] = case
    if not cases:
        raise ValueError("no cases")
    return cases


def fixture_bytes(case, part):
    return (EVALS / "fixtures" / case["id"] / part).read_bytes()


def fixture_identity(case):
    files = {part: digest(fixture_bytes(case, part)) for part in
             ("input/task.go", "grader/contract_test.go", "reference/task.go")}
    encoded = json.dumps({"case": case, "files": files, "module": MODULE}, sort_keys=True).encode()
    return digest(encoded)


def prepare(case, workspace):
    workspace = Path(workspace).absolute()
    if workspace.resolve().is_relative_to(ROOT.resolve()):
        raise ValueError("prepare outside the evaluator checkout; keep graders out of agent context")
    workspace.mkdir(parents=True, exist_ok=False)
    (workspace / "go.mod").write_text(MODULE, encoding="utf-8")
    (workspace / "task.go").write_bytes(fixture_bytes(case, "input/task.go"))
    (workspace / "TASK.md").write_text(case["prompt"] + "\n", encoding="utf-8")
    return {"case": case["id"], "workspace": str(workspace), "fixture_sha256": fixture_identity(case)}


def snapshot(workspace):
    workspace = Path(workspace)
    if workspace.is_symlink() or not workspace.is_dir():
        raise ValueError("workspace must be a regular directory")
    files = {}
    for path in sorted(workspace.iterdir()):
        if path.name == "go.mod" or path.suffix == ".go":
            if path.is_symlink() or not path.is_file():
                raise ValueError("source must be a regular file: " + path.name)
            if path.stat().st_size > MAX_BYTES:
                raise ValueError("source exceeds size budget")
            files[path.name] = path.read_bytes()
    if len(files) > 32 or sum(map(len, files.values())) > MAX_BYTES:
        raise ValueError("workspace exceeds size budget")
    if files.get("go.mod") != MODULE.encode():
        raise ValueError("fixture module contract changed or missing")
    if "task.go" not in files:
        raise ValueError("task.go is missing")
    return files


def run_bounded(command, cwd, env, seconds=60):
    """Bound our child process and output. This is NOT an OS security sandbox."""
    if os.name != "posix":
        return {"exit_code": None, "error": "runner requires POSIX process-group cleanup", "output": ""}
    with tempfile.TemporaryFile() as output:
        try:
            child = subprocess.Popen(command, cwd=cwd, env=env, stdout=output,
                                     stderr=subprocess.STDOUT, start_new_session=True)
        except OSError as exc:
            return {"exit_code": None, "error": str(exc), "output": ""}
        deadline = time.monotonic() + seconds
        error = None
        try:
            while child.poll() is None:
                if time.monotonic() > deadline or os.fstat(output.fileno()).st_size > MAX_BYTES:
                    error = "time or output budget exceeded"
                    break
                try:
                    child.wait(timeout=0.05)
                except subprocess.TimeoutExpired:
                    pass
        finally:
            # Also clean up descendants after an early parent exit.
            try:
                os.killpg(child.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            child.wait()
        if os.fstat(output.fileno()).st_size > MAX_BYTES:
            error = "output budget exceeded"
        output.seek(0)
        return {"exit_code": child.returncode, "error": error,
                "output": output.read(MAX_BYTES).decode("utf-8", errors="replace")}


def test_outcome(run, required):
    """A zero exit, skipped test, or printed PASS is not enough."""
    terminal = {}
    package_passed = False
    malformed = False
    for line in run["output"].splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            # Non-JSON diagnostics cannot establish a passing execution trace.
            malformed = True
            continue
        if not isinstance(event, dict):
            malformed = True
            continue
        if event.get("Package") != "example.com/skill-eval":
            continue
        action, test = event.get("Action"), event.get("Test")
        if test and action in ("pass", "fail", "skip"):
            terminal[test] = action
        if not test and action == "pass":
            package_passed = True
    passed = (run["exit_code"] == 0 and not run["error"] and not malformed and package_passed
              and all(terminal.get(test) == "pass" for test in required)
              and not any(value in ("fail", "skip") for value in terminal.values()))
    return {"passed": bool(passed), "required_tests": {test: terminal.get(test, "not_executed") for test in required}}


def grade(case, workspace):
    report = {"case": case["id"], "fixture_sha256": fixture_identity(case),
              "artifact_status": "fail", "behavior_status": "not_evaluated"}
    try:
        files = snapshot(workspace)
    except ValueError as exc:
        return dict(report, error=str(exc))
    report["source_sha256"] = {name: digest(data) for name, data in files.items()}
    report["agent_test_files"] = [name for name in files if name.endswith("_test.go")]
    go = shutil.which("go")
    if go is None:
        return dict(report, artifact_status="unavailable", error="Go toolchain not found")
    env = {key: os.environ[key] for key in ("PATH", "HOME", "TMPDIR") if key in os.environ}
    env.update(GOTOOLCHAIN="local", GOWORK="off", GOENV="off", GOPROXY="off", GOFLAGS="",
               CGO_ENABLED="0", GOMAXPROCS="2")
    version = run_bounded([go, "version"], ROOT, env, 5)
    report["toolchain"] = version["output"].strip()
    match = re.search(r"go1\.(\d+)", version["output"])
    if version["error"] or version["exit_code"] != 0 or not match or int(match[1]) < 23:
        return dict(report, artifact_status="unavailable", error="Go 1.23+ local toolchain required")
    with tempfile.TemporaryDirectory(prefix="go-skill-grade-") as temporary:
        target = Path(temporary)
        # Candidate tests are retained in the evidence, but cannot replace the trusted grader.
        # TestMain, Skip, and matching names in candidate test files must not fake this result.
        for name, content in files.items():
            if not name.endswith("_test.go"):
                (target / name).write_bytes(content)
        (target / "zz_contract_test.go").write_bytes(fixture_bytes(case, "grader/contract_test.go"))
        command = [go, "test", "-json", "-count=1", "-timeout=5s", "-p=2", "."]
        run = run_bounded(command, target, env)
    report.update(command=command, run=run, checks=test_outcome(run, case["required_tests"]))
    report["artifact_status"] = "pass" if report["checks"]["passed"] else "fail"
    return report


def self_test(cases):
    """Test the evaluator with authored controls, not models or skill variants."""
    results = []
    for case in cases.values():
        with tempfile.TemporaryDirectory(prefix="go-skill-control-") as temporary:
            workspace = Path(temporary) / "work"
            prepare(case, workspace)
            broken = grade(case, workspace)
            (workspace / "task.go").write_bytes(fixture_bytes(case, "reference/task.go"))
            corrected = grade(case, workspace)
            results.append({"case": case["id"], "seeded": broken, "reference": corrected})
    passed = all(r["seeded"]["artifact_status"] == "fail" and
                 r["reference"]["artifact_status"] == "pass" and
                 any(value == "fail" for value in r["seeded"].get("checks", {}).get("required_tests", {}).values())
                 for r in results)
    return {"self_test_passed": passed, "behavior_status": "not_evaluated", "controls": results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("list", "prepare", "grade", "self-test"))
    parser.add_argument("case", nargs="?")
    parser.add_argument("workspace", nargs="?", type=Path)
    parser.add_argument("--allow-code-execution", action="store_true",
                        help="acknowledge that Go code executes; use an externally isolated, secret-free sandbox")
    args = parser.parse_args()
    try:
        cases = load_cases()
        if args.command == "list":
            result = {"runnable_cases": list(cases), "behavior_status": "not_evaluated"}
        elif args.command == "self-test":
            if not args.allow_code_execution:
                parser.error("self-test requires --allow-code-execution")
            result = self_test(cases)
        else:
            if args.case not in cases or args.workspace is None:
                parser.error("provide an existing case ID and workspace")
            if args.command == "prepare":
                result = prepare(cases[args.case], args.workspace)
            else:
                if not args.allow_code_execution:
                    parser.error("grade requires --allow-code-execution")
                result = grade(cases[args.case], args.workspace)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(2, str(exc) + "\n")
    print(json.dumps(result, indent=2))
    if result.get("artifact_status") == "unavailable":
        return 2
    if result.get("artifact_status") == "fail" or result.get("self_test_passed") is False:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
