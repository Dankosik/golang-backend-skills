# Executable evaluation support

This is maintainer tooling, not a runtime skill dependency or a required check in
users' Go projects. Model comparisons and routing evaluations are **not run**.
The [20 behavioral specifications](behavioral-evaluation.md) remain the broader
coverage plan; five small variants now have executable artifact graders.

## What is materialized

| Case | Checked artifact property | Deliberate limit |
| --- | --- | --- |
| G01 | Inclusive clamp and sentinel error identity | No application integration |
| G08 | Partial-startup cleanup exactly once, original error, successful ownership transfer | Controlled resources; no service shutdown claim |
| G09 | Mounted route, middleware, status, content type, JSON, fallback | No sockets or deployment transport |
| G14 | Null versus zero, exact int64 conversion, independent result | No database query or transaction |
| G17 | Cross-tenant denial, no protected body, legitimate access, missing record | Trusted tenant is injected; no credential verification |

Each fixture has separate `input`, `grader`, and `reference` directories under
[evals/fixtures](../evals/fixtures). [cases.json](../evals/cases.json) contains the
natural requests and required grader test names. Reference implementations are
authored positive controls, **not outputs from evaluated agent runs**. The broken inputs are negative
controls: their intended assertions must fail, not merely fail to compile.

[routing.json](../evals/routing.json) adds natural activation requests and
near-miss/no-finding controls. They are data for captured agent sessions, not
executed model tests. Relevant skills are guidance for a reviewer, not a required
invocation sequence or a ban on justified combinations.

## Commands

Python 3.12+ handles preparation and metadata tests. Artifact execution additionally
requires POSIX (Linux/macOS) and a local Go 1.23+ toolchain. The fixture baseline is
1.23.0; no toolchain or module downloads are performed by the runner.

```sh
python scripts/evaluate.py list
python scripts/evaluate.py prepare G01 /tmp/go-skill-g01
# Run the selected agent in this workspace, with TASK.md as its task.
# Capture its actual trace, patch, final answer, and configuration outside it.
python scripts/evaluate.py grade G01 /tmp/go-skill-g01 --allow-code-execution

# Maintainer controls, not a model evaluation:
python scripts/evaluate.py self-test --allow-code-execution
python -m unittest discover -s scripts/tests -p test_evaluate.py
```

Use a fresh, previously nonexistent workspace for each variant and repeat. The
prepare command refuses the evaluator checkout and emits only `go.mod`, `task.go`,
and `TASK.md`. Keep the evaluator checkout, graders, reference corrections, and
routing expectations **outside the agent's accessible sandbox**, not just out of
the prompt. This tool does not install skills, choose a model, call an API, alter
agent permissions, or implement an agent sandbox.

`grade` executes code. The acknowledgement flag is not a security control. Run it
inside a disposable, externally isolated environment with no production access,
credentials, sensitive mounts, or network egress. `GOPROXY=off` and local-toolchain
settings prevent Go dependency downloads; they do **not** prevent arbitrary Go
code from accessing a network or filesystem. POSIX process-group cleanup and time
and output budgets limit ordinary runaway children, not hostile sandbox escapes.

## Evidence and interpretation

The grader copies the candidate's root production Go files into a temporary
single-package module and adds trusted contract tests. It preserves source hashes
and records candidate test filenames, but **does not execute agent-authored tests**:
those could replace `TestMain`, skip assertions, or conflict with grader names.
Review the agent tests, complete patch, added directories, and trace separately.
The grader is intentionally not a whole-project scope, test-quality, or security
certifier. Additional package structures are outside these tiny fixtures.

The original `go.mod` must remain unchanged. Tests use `-count=1`, a five-second Go
test timeout, and an outer time/output budget. A zero exit, printed PASS, missing
test, skipped case, wrong package, or malformed trace cannot pass. The emitted
JSON records required test outcomes, source/fixture hashes, toolchain, command,
exit status and bounded output. A missing/unsupported toolchain is `unavailable`,
not a passing or failed model run. Exit codes are 0 for successful artifact/control
checks, 1 for failed checks, and 2 for unavailable tools or invalid invocation.

`artifact_status: pass` never implies `behavior_status: pass`. The latter remains
`not_evaluated`: routing, scope, permissions, tool use, first-patch persistence,
test selection, honesty, token use, and elapsed agent time require the captured
session and independent review. This is a grader, not an inference runner.

## Comparing this revision

Use the same tasks, fresh sessions, supported model/harness/settings, permissions,
external isolation, and preselected repeats/budgets. Compare no pack, the immediate
baseline `4f5223a3e1a721b4af682e2da873e4cd3ae0d9de`, and the exact candidate commit.
The older baseline `48be5eb558e81a2892cca47ebe9c9466dd92be1f` belongs to the prior
audit; retain it as an additional variant only when assessing both changesets.
Do not attribute previously merged improvements to this patch.

Record fixture and pack commit IDs alongside the emitted content hashes; hashes
alone do not describe model settings. Record full-pack and standalone specialist
installation separately. Account for compiler-cache state before comparing
execution time. Keep failed and inconclusive runs. Use the
[results template](evaluation-results.md) for model comparisons, and keep control
self-tests separate. Full database, RPC, network, performance, and older-toolchain
cases still need their specified fixtures and actual evidence.
