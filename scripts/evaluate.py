#!/usr/bin/env python3
"""Prepare and grade six small Go fixtures; never launches a model or claims a sandbox."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
RESERVED = "skill_eval_hidden_test.go"
TEST_NAME = re.compile(r"^func (TestEval\w+)\(t \*testing\.T\)", re.MULTILINE)
LOG_LIMIT = 1024 * 1024


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def required_tests(root, case):
    return set(TEST_NAME.findall((root / "evals/graders" / (case + "_test.go")).read_text(encoding="utf-8")))


def reference(source, replacements):
    for change in replacements:
        if not change["old"] or source.count(change["old"]) != 1:
            raise ValueError("reference replacement must match exactly once")
        source = source.replace(change["old"], change["new"], 1)
    return source


def routing(root=ROOT):
    rows = read_json(root / "evals/routing.json")
    identifiers = [row["id"] for row in rows]
    if not rows or len(identifiers) != len(set(identifiers)):
        raise ValueError("empty or duplicate routing cases")
    for row in rows:
        if not re.fullmatch(r"[GEN]\d{2}", row["id"]) or not row["prompt"].strip():
            raise ValueError("invalid routing case")
        if row["mode"] not in {"implement", "review", "diagnose", "no-go-skill"}:
            raise ValueError("invalid routing mode")
        if (row["mode"] == "no-go-skill") != (not row["suggested_skills"]):
            raise ValueError("routing labels contradict the case mode")
        for name in row["suggested_skills"]:
            if not re.fullmatch(r"go-[a-z-]+", name):
                raise ValueError("invalid skill label")
    return {row["id"]: row for row in rows}


def catalog(root=ROOT):
    cases = read_json(root / "evals/fixtures.json")
    if not set(cases) <= routing(root).keys():
        raise ValueError("fixture has no natural request")
    if not cases:
        raise ValueError("empty fixture catalog")
    if set(cases) != {p.name for p in (root / "evals/fixtures").iterdir()}:
        raise ValueError("fixture inventory differs from catalog")
    if {case + "_test.go" for case in cases} != {p.name for p in (root / "evals/graders").iterdir()}:
        raise ValueError("grader inventory differs from catalog")
    for case, config in cases.items():
        if not re.fullmatch(r"G\d{2}", case) or not re.fullmatch(r"[a-z_]+\.go", config["editable"]):
            raise ValueError("invalid fixture path")
        folder = root / "evals/fixtures" / case
        if folder.is_symlink() or any(p.is_symlink() or not p.is_file() for p in folder.iterdir()):
            raise ValueError("fixtures must be flat regular files")
        if {p.name for p in folder.iterdir()} != {"go.mod", config["editable"]}:
            raise ValueError("unexpected fixture files")
        tests = required_tests(root, case)
        if not tests or not config["seed_failures"] or not set(config["seed_failures"]) <= tests:
            raise ValueError("seed failures must name actual hidden tests")
        reference((folder / config["editable"]).read_text(encoding="utf-8"), config["reference_replacements"])
    return cases


def prepare(root, case, destination):
    if case not in catalog(root):
        raise ValueError("unknown fixture: " + case)
    if destination.exists() or destination.is_symlink():
        raise ValueError("workspace must not already exist")
    shutil.copytree(root / "evals/fixtures" / case, destination)


def snapshot(workspace, fixture, editable):
    """Copy only the flat Go package; instructions and run logs are not compiled."""
    if workspace.is_symlink() or not workspace.is_dir():
        raise ValueError("workspace must be a regular directory")
    selected = {}
    for path in workspace.iterdir():
        if path.name == "go.mod" or path.suffix == ".go":
            if path.is_symlink() or not path.is_file() or path.stat().st_size > LOG_LIMIT:
                raise ValueError("invalid candidate file: " + path.name)
            selected[path.name] = path.read_bytes()
    if RESERVED in selected:
        raise ValueError("reserved hidden-grader filename")
    if selected.get("go.mod") != (fixture / "go.mod").read_bytes():
        raise ValueError("fixture Go baseline and module must remain unchanged")
    if editable not in selected:
        raise ValueError("candidate removed the requested implementation")
    return selected


def parse_results(log, expected, returncode):
    outcomes = {}
    package_pass = False
    for line in log.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(event, dict):
            continue
        action, test = event.get("Action"), event.get("Test")
        if not isinstance(action, str) or (test is not None and not isinstance(test, str)):
            continue
        if test in expected and action in {"pass", "fail", "skip"}:
            outcomes[test] = action
        if not test and action == "pass":
            package_pass = True
    passed = returncode == 0 and package_pass and all(outcomes.get(t) == "pass" for t in expected) and bool(expected)
    return {"passed": passed, "tests": {t: outcomes.get(t, "not-observed") for t in sorted(expected)}}


def execute(command, cwd, environment, timeout):
    """Bound the process and captured report. This is NOT a security boundary."""
    started = time.monotonic()
    with tempfile.TemporaryFile() as log:
        process = subprocess.Popen(command, cwd=cwd, env=environment, stdout=log, stderr=subprocess.STDOUT, start_new_session=os.name == "posix")
        timed_out = False
        try:
            process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
        finally:
            if os.name == "posix":
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
            elif process.poll() is None:
                process.kill()
            process.wait(timeout=5)
        log.seek(0)
        raw = log.read(LOG_LIMIT + 1)
    return {"returncode": process.returncode, "timed_out": timed_out, "log_truncated": len(raw) > LOG_LIMIT, "elapsed_seconds": round(time.monotonic() - started, 3), "log": raw[:LOG_LIMIT].decode("utf-8", errors="replace")}


def grade(root, case, workspace, cache):
    config = catalog(root)[case]
    fixture = root / "evals/fixtures" / case
    files = snapshot(workspace, fixture, config["editable"])
    grader = (root / "evals/graders" / (case + "_test.go")).read_bytes()
    hashes = {name: hashlib.sha256(data).hexdigest() for name, data in sorted(files.items())}
    result = {"kind": "fixture-grade-not-model-evaluation", "case": case, "source_sha256": hashes, "grader_sha256": hashlib.sha256(grader).hexdigest()}
    go = shutil.which("go")
    if go is None:
        return dict(result, passed=False, unavailable="Go executable not found")
    with tempfile.TemporaryDirectory(prefix="go-skill-grade-") as temporary:
        work = Path(temporary)
        for name, data in files.items():
            (work / name).write_bytes(data)
        (work / RESERVED).write_bytes(grader)
        # Disable implicit dependency/toolchain downloads, NOT the program's network access.
        environment = os.environ.copy()
        environment.update(GOWORK="off", GOENV="off", GOTOOLCHAIN="local", GOPROXY="off", GOSUMDB="off", GOFLAGS="", CGO_ENABLED="0", GOMAXPROCS="2", GOCACHE=str(cache.resolve()))
        version = subprocess.run([go, "version"], env=environment, text=True, capture_output=True, timeout=10, check=True).stdout.strip()
        command = [go, "test", "-p=2", "-json", "-count=1", "-timeout=10s", "."]
        execution = execute(command, work, environment, timeout=90)
    result.update(execution)
    result.update(parse_results(execution["log"], required_tests(root, case), execution["returncode"]))
    result.update(toolchain=version, command=command)
    if result["timed_out"] or result["log_truncated"]:
        result["passed"] = False
    return result


def self_test(root, cache, checkpoint=None):
    report = {"kind": "grader-self-test-not-model-evaluation", "complete": False, "passed": False, "cases": []}
    for case, config in catalog(root).items():
        entry = {"case": case, "passed": False}
        report["cases"].append(entry)
        with tempfile.TemporaryDirectory(prefix="go-skill-reference-") as temporary:
            workspace = Path(temporary) / "work"
            prepare(root, case, workspace)
            seeded = grade(root, case, workspace, cache)
            entry["seed"] = seeded
            if checkpoint:
                checkpoint(report)
            source = workspace / config["editable"]
            source.write_text(reference(source.read_text(encoding="utf-8"), config["reference_replacements"]), encoding="utf-8")
            fixed = grade(root, case, workspace, cache)
            entry["reference"] = fixed
        observed = seeded.get("tests", {})
        discriminates = not seeded["passed"] and not seeded.get("timed_out", False) and not seeded.get("log_truncated", False) and all(observed.get(t) == "fail" for t in config["seed_failures"])
        entry["passed"] = discriminates and fixed["passed"]
        if checkpoint:
            checkpoint(report)
        print(case + ": " + ("grader self-test passed" if entry["passed"] else "failed or unavailable"), file=sys.stderr, flush=True)
    report.update(complete=True, passed=all(r["passed"] for r in report["cases"]))
    return report


def write_checkpoint(path, result):
    # The CLI reserves this new report before execution. Replace only that run's file.
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent, delete=False) as temporary:
        temporary.write(json.dumps(result, indent=2) + "\n")
        name = temporary.name
    try:
        os.replace(name, path)
    finally:
        Path(name).unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["check", "prepare", "grade", "self-test"])
    parser.add_argument("case", nargs="?")
    parser.add_argument("--workspace", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--cache", type=Path, help="Optional reusable Go build cache; never changes the test-result cache policy")
    parser.add_argument("--allow-execution", action="store_true", help="Acknowledge execution of Go code outside a security sandbox")
    args = parser.parse_args()
    try:
        cases = catalog()
        if args.command in {"grade", "prepare"} and (args.case not in cases or args.workspace is None):
            parser.error("prepare/grade require a known case and --workspace")
        if args.command in {"grade", "self-test"} and not args.allow_execution:
            parser.error("Go execution requires --allow-execution; use a disposable environment without secrets")
        if args.output and args.output.exists():
            parser.error("output already exists; retain earlier evidence")
        if args.output:
            with args.output.open("x", encoding="utf-8") as output:
                output.write(json.dumps({"complete": False, "passed": False, "status": "started"}) + "\n")
        if args.command == "check":
            result = {"kind": "catalog-check-not-model-evaluation", "passed": True, "cases": sorted(cases)}
        elif args.command == "prepare":
            prepare(ROOT, args.case, args.workspace)
            result = {"kind": "prepared-not-evaluated", "workspace": str(args.workspace), "case": args.case, "prompt": routing()[args.case]["prompt"]}
        else:
            with tempfile.TemporaryDirectory(prefix="go-skill-cache-") as cache:
                build_cache = args.cache or Path(cache)
                build_cache.mkdir(parents=True, exist_ok=True)
                checkpoint = (lambda report: write_checkpoint(args.output, report)) if args.output else None
                result = self_test(ROOT, build_cache, checkpoint) if args.command == "self-test" else grade(ROOT, args.case, args.workspace, build_cache)
        encoded = json.dumps(result, indent=2) + "\n"
        if args.output:
            write_checkpoint(args.output, result)
            print(json.dumps({"report": str(args.output), "passed": result.get("passed")}))
        else:
            print(encoded, end="")
        return 0 if result.get("passed", True) else 1
    except (ValueError, KeyError, OSError, subprocess.SubprocessError) as error:
        parser.exit(2, "evaluation unavailable: " + str(error) + "\n")


if __name__ == "__main__":
    raise SystemExit(main())
