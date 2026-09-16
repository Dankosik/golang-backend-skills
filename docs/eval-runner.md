# Executable evaluation subset

The [20 behavioral scenarios](behavioral-evaluation.md) describe what to evaluate.
[fixtures.json](../evals/fixtures.json) materializes four small cases: G01 clamp,
G09 mounted HTTP response, G14 nullable mapping, and G17 tenant authorization.
G14 covers only `sql.NullString`, not every driver's numeric/time representation.
G17 covers downstream authorization, not credential verification. The remaining
16 scenario fixtures and the eight [negative probes](reference-driven-review.md)
are not materialized here.

[scripts/evaluate.py](../scripts/evaluate.py) uses Python's standard library.
Fixture code requires Go 1.23 or a compatible newer local compiler and no external
modules or services. This fixture baseline does not change the Go versions
supported by the skills. Unit tests of the evaluator require no Go installation.

## Commands

From a trusted checkout, validate the catalog without running Go or a model:

```sh
python scripts/evaluate.py check
python -m unittest discover -s scripts/tests -p test_evaluate.py
```

Within a disposable sandbox, verify each oracle against the deliberately broken
input and the known-correct control:

```sh
python scripts/evaluate.py self-test --allow-execution > oracle-controls.json
```

Self-test failure means an oracle, fixture, toolchain, or execution problem. A
compile failure is not accepted as evidence that the intended defect was caught.
These are oracle controls, not agent runs or instruction-quality comparisons.

Prepare only one case's input files in a new workspace:

```sh
python scripts/evaluate.py prepare --case G01 --workspace /tmp/go-eval-G01
```

The JSON response supplies the natural task and fixture fingerprint, but not
expected skills, hidden assertions or reference code. The workspace contains
only `app.go` and `go.mod`. The agent may edit/add ordinary top-level Go source
and test files without changing the module baseline or introducing dependencies.
Nested packages and unrelated files are outside these deliberately small fixtures.
Use an external location suitable for the platform instead of `/tmp` on Windows.

Give the agent only that prompt, prepared workspace, and the selected installation
variant. Keep this repository, fixture catalog, oracles, reference controls,
expected skills and grading rubrics outside the agent's accessible sandbox. A
separate directory alone does not prevent an agent reading neighboring files.
Capture the complete tool trace, patch, final answer, model/version and settings.
No model invocation is performed by this script.

After the agent session has stopped, snapshot its workspace and grade from the
trusted evaluator checkout in an execution sandbox:

```sh
python scripts/evaluate.py grade --case G01 --workspace /tmp/go-eval-G01 --allow-execution > G01-runtime.json
```

The grader copies the candidate into a temporary directory, installs the oracle
from the trusted catalog, and runs `go test -json -count=1 -timeout=10s ./...`.
A 45-second outer limit bounds compilation plus tests; output is limited to 2 MiB.
Cold/slow environments may reach that budget: retain the inconclusive result,
and preselect an equal larger budget for a later comparison rather than giving
only a favored candidate extra attempts. The script does not expose a budget
flag; changing it creates a new evaluator revision that must be recorded.

`runtime-pass` requires every named oracle to run and pass, a package pass, and
exit zero. A named failing oracle is `runtime-fail`. Skips, missing execution,
build/toolchain failure, timeout or missing Go are `inconclusive`, never success.
CLI exit codes are 0 for runtime-pass, 1 for runtime-fail, and 2 for inconclusive.
Self-test uses 0 only when all eight expected control outcomes match.

Results record fixture and candidate SHA-256 identities, command, exit code,
test evidence and bounded output. They always leave `trace_review` and
`model_comparison` as `not-run`: the script cannot infer those from passing tests.
Record actual Go version, OS/architecture and evaluator commit alongside the JSON.

## Compare instructions, not environments

For this change, compare no pack, the merged baseline
`4f5223a3e1a721b4af682e2da873e4cd3ae0d9de`, and the exact candidate commit.
The older `48be5eb...` in the original protocol remains a historical comparison,
not a substitute for testing this patch against its immediate parent.

Use the same fixture fingerprints, model/settings, client, tools, permissions,
other instructions and preselected repetitions/budgets. Use fresh sessions and
workspaces and retain every failure and inconclusive result. Pin the pack commit
and record actually loaded skills to catch stale installs. Evaluate natural
activation without revealing expected names, and explicit invocation separately.
Test changed specialists alone as well as in the full pack where independence
matters; multiple justified selections can be valid.

After runtime grading, inspect each case's `trace_checks` against the actual tool
trace and final claims. Examples: did the agent test the mounted chain; did it
create needless infrastructure; did it call a fabricated principal proof of
credential verification; did it stop with an introduced failure? Passing an
external oracle does not show the agent ran appropriate tests itself. Unauthorized
edits or false verification claims remain failures even when runtime checks pass.
Use [the results template](evaluation-results.md) for the model comparison.

Do not grade general code review, transport behavior, SQL isolation, arbitrary
Go programs or performance gains with this small suite. Expand with concrete
fixtures and independent oracles for newly observed failures, not token-heavy
rules for imagined problems.

## Execution boundary

Go test executes candidate code. `--allow-execution` acknowledges that fact; it
is not a sandbox. Temporary folders, filtered environment variables, process-group
cleanup and `GOPROXY=off` do not block filesystem or network access from Go code.
Use OS/container isolation with no secrets, production connectivity or credentials,
with external CPU, memory, filesystem and network limits. Stop the agent before
grading to avoid concurrent mutation. On Windows the runner cannot guarantee
termination of arbitrary descendant processes; external isolation owns cleanup.

Keep fixtures, controls and graders outside installed skills. The existing release
packager excludes `evals/`, `scripts/` and `docs/`; no user-project test gate or
model/API dependency is added. Existing CI discovery runs the lightweight Python
evaluator tests; the Go control run remains an explicit maintainer command.
