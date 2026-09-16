# Go skill evaluation kit

Maintainer tooling, not a skill dependency. **Model comparisons have not been run.**
The kit separates routing, instruction review, runtime correctness, and grading-tool
validation. A passing fixture self-test is not evidence that a model improved.

## Coverage

[routing.json](routing.json) contains 20 natural Go requests, one explicit invocation,
and eight negative controls. `suggested_skills` are review hints, not an exact-match
oracle: several justified combinations are valid, and no invocation order or skill
count is prescribed. The negative controls expose activation based on repository
language or nearby keywords rather than the requested work.

Six small executable versions of the [behavioral cases](../docs/behavioral-evaluation.md)
are checked in. They require only the Go standard library; their module baseline is
Go 1.22. Actual validation used Go 1.23.2 on Linux, not every supported Go version.

| Case | Independent observation |
| --- | --- |
| G01 | Inclusive clamp boundaries and sentinel identity, not just matching error text |
| G04 | Cancellation releases a blocked sender and completion follows worker termination |
| G08 | Partial initialization closes once; successful initialization transfers an open resource |
| G09 | Valid JSON with preserved message, status, and middleware headers through the mounted route |
| G14 | Validity flags preserve absence, empty strings, zero, and int64 precision without a database |
| G17 | Cross-tenant denial protects state, intended access works, missing credentials are denied |

These deliberately small fixtures do not cover all requirements in the larger case
specifications. G17 uses fixed test tokens as a controlled authentication collaborator;
it does not prove JWT verification or a production identity provider. G04 exercises
one coordinated failure path, not all possible schedules. The other 14 Go cases still
need pinned workspaces and independent evidence, especially gRPC, real transport,
transaction isolation, migrations, and provider behavior.

## Commands

Run from the repository root with Python 3.12 or later. No Python package, inference
service, new infrastructure, or paid model is needed for this kit.

```sh
# Static catalog checks; does not start Go or a model.
python scripts/evaluate.py check
python -m unittest discover -s scripts/tests -p test_evaluate.py

# New workspace containing only the source fixture; JSON output includes its request.
python scripts/evaluate.py prepare G01 --workspace /tmp/go-eval-g01

# After an authorized agent has changed that workspace, grade its actual code.
python scripts/evaluate.py grade G01 --workspace /tmp/go-eval-g01 \
  --allow-execution --output /tmp/go-eval-g01-result.json

# Validate the graders against seeded defects and explicit reference corrections.
python scripts/evaluate.py self-test --allow-execution \
  --output /tmp/go-grader-self-test.json
```

Use fresh paths. Existing workspaces and report files are not overwritten. `self-test`
checkpoints its report after each seed and reference execution; an interrupted report
has `complete: false` and must not be scored as a completed run. Optional `--cache`
selects a reusable Go build cache. Tests still use `-count=1`, so a cached test result
cannot masquerade as a new execution. Compilation is limited to two parallel packages;
each Go test binary has a 10-second timeout and each complete Go command a 90-second
outer limit. Reports preserve exit codes, named test outcomes, hashes, toolchain,
commands, timings, and bounded log excerpts. A truncated or timed-out run cannot pass.

`grade` copies the flat root Go package to a temporary directory and adds the trusted
grader there. It rejects changed `go.mod`, missing implementation files, symlinks in
compiled inputs, and a supplied reserved grader filename. The checked-in grader and
fixture are not modified. This narrow runner is not a general multi-module harness.
The `passed` field means the observed fixture assertions passed, not that scope,
formatting, test quality, skill selection, or all task requirements were satisfied.

## Execution and isolation

`--allow-execution` acknowledges executing Go code, including candidate tests. This
Python tool is **not a security sandbox**. It inherits the process environment.
Run candidate code in an externally isolated disposable environment without secrets,
production credentials, or access to valuable files. Set filesystem, network, CPU,
memory, and disk limits outside this script. Go module/toolchain downloads are disabled;
that does not prevent application code from making network calls. On POSIX the runner
cleans up its process group; Windows or escaping child processes require executor-level
cleanup. Captured output is capped in the report, not by a disk quota on the process.

Do not let the evaluated agent read this repository's `evals/graders`, reference
replacements in `fixtures.json`, expected routing labels, or prior results. `prepare`
excludes them, but a neighboring readable checkout is still leakage. Restrict the
agent filesystem to its fixture and installed skill variant. Run the grader separately.
Keep grader access and review observations outside the agent prompt.

## Real model comparisons

Use the full [comparison protocol](../docs/behavioral-evaluation.md). For the current
change, compare no pack, the pre-change pack at
`4f5223a3e1a721b4af682e2da873e4cd3ae0d9de`, and the exact candidate commit. The earlier
`48be5eb558e81a2892cca47ebe9c9466dd92be1f` reference in the original audit measures a
different, broader change and may be an additional baseline, not a silent substitute.
Pin the fixture to the candidate repository commit; use identical fixture bytes and
hidden graders for every pack variant. Record their hashes from the grader report.

Choose the model/harness versions, settings, permissions, seeds, budgets, repetitions,
and ordering before execution. Use fresh sessions and isolated workspaces, and verify
what skills were actually loaded. A no-pack run must not inherit globally installed
skills or stale plugin caches. Natural routing runs receive only the request and
fixture; E01 separately tests explicit invocation against G01. Run a changed specialist
standalone as well as the full pack when independence matters.

Capture actual agent traces, resulting diffs, test output, and final claims. For Codex,
[the official eval guide](https://developers.openai.com/blog/eval-skills) describes
`codex exec --json` and structured grading. Use the installed client's supported
invocation and least necessary permissions; this kit neither invokes that client nor
assumes credentials or a model name. Routing cannot be inferred from the final prose
alone; retain evidence of actual skill loading.

Judge outcome correctness, safety, scope, and truthful claims before efficiency.
Review the diff and trace for untouched requirements, unauthorized edits, unnecessary
infrastructure, skipped tests, and test assertions coupled to the implementation.
The hidden Go tests are one source of evidence, not an autonomous final reviewer.
Record disagreements and unavailable checks rather than manufacturing a single
favorable score. Retain failures and inconclusive runs; publish only claims supported
by the tested model/harness configurations. Use the [results record](../docs/evaluation-results.md).
