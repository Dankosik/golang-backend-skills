#!/usr/bin/env python3
"""Prepare held-out Go fixtures and grade runtime evidence, not model quality.

Uses the standard library. Execute only in a disposable sandbox: a temporary
folder and offline Go module resolution are NOT a security boundary.
"""

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
ORACLE = "zz_skill_oracle_test.go"
MAX_BYTES = 2 * 1024 * 1024


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def load_cases(path=None):
    data = json.loads((path or ROOT / "evals/fixtures.json").read_text(encoding="utf-8"))
    if data.get("version") != 1 or not isinstance(data.get("cases"), list) or not data["cases"]:
        raise ValueError("expected nonempty version 1 fixture catalog")
    result = {}
    for case in data["cases"]:
        if not re.fullmatch(r"G\d{2}", case.get("id", "")) or case["id"] in result:
            raise ValueError("invalid or duplicate case ID")
        if set(case.get("files", {})) != {"go.mod", "app.go"}:
            raise ValueError("fixture must contain go.mod and app.go only")
        for value in [case.get("prompt"), case.get("oracle"), case.get("control"), *case["files"].values()]:
            if not isinstance(value, str) or not value.strip():
                raise ValueError("fixture content must be nonempty text")
        tests = case.get("tests", [])
        if not tests or len(set(tests)) != len(tests) or any(not re.fullmatch(r"TestOracle\w+", t) for t in tests):
            raise ValueError("unique named oracle tests are required")
        for field in ("expected_any", "trace_checks"):
            if not isinstance(case.get(field), list) or not case[field] or not all(isinstance(s, str) and s for s in case[field]):
                raise ValueError("missing evaluation rubric: " + field)
        result[case["id"]] = case
    return result


def prepare(case, destination):
    """Export inputs only. Never export expected skills, oracle or solution."""
    destination.mkdir(parents=True, exist_ok=False)
    for name, text in case["files"].items():
        (destination / name).write_text(text, encoding="utf-8")
    return {"case": case["id"], "fixture_sha256": digest(case), "prompt": case["prompt"]}


def snapshot(workspace, case):
    """These small flat fixtures support added Go files, not module changes."""
    if workspace.is_symlink() or not workspace.is_dir():
        raise ValueError("workspace must be a regular directory")
    files = {}
    total = 0
    for path in workspace.iterdir():
        if path.name == ".git":
            continue
        if path.is_symlink() or not path.is_file():
            raise ValueError("unexpected directory or symlink: " + path.name)
        if path.name == ORACLE or path.name.startswith((".", "_")):
            raise ValueError("reserved or ignored Go file: " + path.name)
        if path.name != "go.mod" and (not path.name.endswith(".go") or not re.fullmatch(r"[A-Za-z0-9_]+\.go", path.name)):
            raise ValueError("only go.mod and ordinary Go files belong in this fixture")
        size = path.stat().st_size
        total += size
        if total > MAX_BYTES:
            raise ValueError("fixture exceeds size budget")
        files[path.name] = path.read_text(encoding="utf-8")
    if files.get("go.mod") != case["files"]["go.mod"] or "app.go" not in files:
        raise ValueError("fixture module/signature source missing or module baseline changed")
    return files


def classify(returncode, text, expected):
    """Zero exit without each named oracle executing is not a pass."""
    ran, passed, failed, skipped = set(), set(), set(), set()
    package_pass = False
    for line in text.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(event, dict):
            continue
        name, action = event.get("Test"), event.get("Action")
        if action == "pass" and not name and event.get("Package") == "example.com/skillfixture":
            package_pass = True
        if name in expected and event.get("Package") == "example.com/skillfixture":
            target = {"run": ran, "pass": passed, "fail": failed, "skip": skipped}.get(action)
            if target is not None:
                target.add(name)
    evidence = {"ran": sorted(ran), "passed": sorted(passed), "failed": sorted(failed), "skipped": sorted(skipped)}
    if failed:
        return "runtime-fail", evidence
    if returncode == 0 and package_pass and set(expected) <= ran & passed and not skipped:
        return "runtime-pass", evidence
    return "inconclusive", evidence


def run_go(directory, go, timeout=45):
    """Bound time and captured output; callers supply an external sandbox."""
    env = {key: os.environ[key] for key in ("PATH", "HOME", "TMPDIR", "TEMP", "TMP", "SYSTEMROOT", "USERPROFILE") if key in os.environ}
    env.update(GOENV="off", GOWORK="off", GOFLAGS="", GOTOOLCHAIN="local", GOPROXY="off", GOMAXPROCS="2", CGO_ENABLED="0")
    command = [go, "test", "-json", "-count=1", "-timeout=10s", "./..."]
    with tempfile.TemporaryFile() as output:
        process = subprocess.Popen(command, cwd=directory, env=env, stdout=output, stderr=subprocess.STDOUT, start_new_session=(os.name == "posix"))
        started = time.monotonic()
        limit = None
        try:
            while process.poll() is None:
                if time.monotonic() - started > timeout:
                    limit = "wall-time budget exceeded"
                    break
                if os.fstat(output.fileno()).st_size > MAX_BYTES:
                    limit = "output budget exceeded"
                    break
                time.sleep(0.03)
        finally:
            if process.poll() is None:
                if os.name == "posix":
                    try:
                        os.killpg(process.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                else:
                    process.kill()
                process.wait()
        if os.fstat(output.fileno()).st_size > MAX_BYTES:
            limit = "output budget exceeded"
        output.seek(0)
        text = output.read(MAX_BYTES).decode("utf-8", errors="replace")
    return command, process.returncode, text, limit


def grade(case, workspace):
    report = {"case": case["id"], "fixture_sha256": digest(case), "status": "inconclusive", "trace_review": "not-run", "model_comparison": "not-run"}
    files = snapshot(workspace, case)
    report["candidate_sha256"] = digest(files)
    go = shutil.which("go")
    if not go:
        return dict(report, reason="Go toolchain unavailable")
    # The trusted evaluator owns the oracle; the candidate never supplies it.
    with tempfile.TemporaryDirectory(prefix="go-skill-grade-") as temporary:
        directory = Path(temporary)
        for name, text in dict(files, **{ORACLE: case["oracle"]}).items():
            (directory / name).write_text(text, encoding="utf-8")
        command, code, output, limit = run_go(directory, go)
        status, evidence = classify(code, output, case["tests"])
    report.update(command=command, exit_code=code, evidence=evidence, output=output)
    report["status"] = "inconclusive" if limit else status
    if limit:
        report["reason"] = limit
    return report


def self_test(cases):
    """Negative and positive controls validate oracles, never agent behavior."""
    results = []
    for case in cases.values():
        for label, expected in (("broken", "runtime-fail"), ("reference", "runtime-pass")):
            with tempfile.TemporaryDirectory(prefix="go-skill-control-") as temporary:
                work = Path(temporary) / "workspace"
                prepare(case, work)
                if label == "reference":
                    (work / "app.go").write_text(case["control"], encoding="utf-8")
                result = grade(case, work)
            result.update(control=label, expected=expected)
            results.append(result)
    return {"kind": "oracle-self-test", "model_comparison": "not-run", "ok": all(r["status"] == r["expected"] for r in results), "results": results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("check", "prepare", "grade", "self-test"))
    parser.add_argument("--case")
    parser.add_argument("--workspace", type=Path)
    parser.add_argument("--allow-execution", action="store_true", help="acknowledge that Go code executes with this process's permissions")
    args = parser.parse_args()
    try:
        cases = load_cases()
        if args.command in ("grade", "self-test") and not args.allow_execution:
            parser.error("execution requires --allow-execution inside a disposable sandbox")
        if args.command in ("prepare", "grade"):
            if args.case not in cases or args.workspace is None:
                parser.error("prepare/grade requires an existing --case and a --workspace")
            report = prepare(cases[args.case], args.workspace) if args.command == "prepare" else grade(cases[args.case], args.workspace)
        elif args.command == "self-test":
            report = self_test(cases)
        else:
            report = {"kind": "catalog-check", "cases": sorted(cases), "model_comparison": "not-run"}
        print(json.dumps(report, indent=2))
        if args.command == "self-test":
            return 0 if report["ok"] else 1
        if args.command == "grade":
            return {"runtime-pass": 0, "runtime-fail": 1, "inconclusive": 2}[report["status"]]
        return 0
    except (ValueError, OSError, subprocess.SubprocessError) as error:
        print(json.dumps({"status": "inconclusive", "reason": str(error)}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
