# Evaluation results and remaining evidence

## Model comparisons

**Not run.** No model traces, paired behavior outcomes, speedups, or cross-model gains
are asserted. Distribution/CI validation and grader self-tests are different evidence.
The [evaluation kit](../evals/README.md) materializes six small fixtures; the remaining
Go workspace cases are specifications. Their existence does not demonstrate skill
activation, instruction following, or improved task completion.

Independent subagents were not available during this authoring change. Separate
review perspectives in [reference adoption](reference-adoption.md) are maintainer
briefs, not executed independent reviews. The X article body was inaccessible.

## Deterministic grader validation, 2026-09-16

The local authoring environment ran Python 3.13.5 and Go 1.23.2 on Linux/amd64.
The fixture modules declare Go 1.22; minimum-version execution is not claimed.
The runner's static catalog check and 17 Python unit tests passed. A completed
self-test ran each of the six seeded fixtures and its explicit reference correction.

| Case | Seeded defect observed | Reference correction |
| --- | --- | --- |
| G01 | Sentinel identity assertion failed; ordinary clamp bounds passed | Both assertions passed |
| G04 | Blocked sender failed cancellation/termination assertion and was released during test cleanup | Termination assertion passed |
| G08 | Partial-startup cleanup failed; successful ownership transfer passed | Both assertions passed |
| G09 | Mounted JSON error contract failed on escaped input | Contract assertion passed |
| G14 | Absence/valid-zero mapping assertion failed | Mapping assertion passed |
| G17 | Cross-tenant denial and intended-access assertions failed; missing credentials were denied | All three assertions passed |

These are six seed/reference pairs and ten named grader tests, not six agent runs.
Reference corrections are explicit text replacements in `evals/fixtures.json`, not
model-generated solutions. Go results are from actual `go test -p=2 -json -count=1
-timeout=10s .` executions with compiler/runtime parallelism bounded to two.

Two early authoring invocations exceeded the surrounding execution limit before a
complete report was saved. This exposed a tooling gap, not an agent failure. The
runner now checkpoints after each seed/reference execution. The completed validation
used a warmed explicit build cache; its durations are not comparative performance
results. All expected original defects still failed and all reference assertions
passed in that completed run. No failing model run was discarded because no model
comparison was performed.

The full distribution/install suite was not run in this local partial authoring
workspace. Check the actual pull request CI for its independent distribution result;
this document does not predeclare it passing. Runtime Go self-tests are explicit and
not added as a mandatory application or release gate.

## Record for a real comparison

Copy this section for each executed comparison; never replace missing observations
with intended outcomes.

| Field | Recorded value |
| --- | --- |
| Date and evaluator | Not recorded |
| Case IDs and repetitions | Not recorded |
| Fixture commit, source hashes, grader hashes | Not recorded for a model comparison |
| Pre-change pack for this change | 4f5223a3e1a721b4af682e2da873e4cd3ae0d9de |
| Earlier audit baseline, optional separate comparison | 48be5eb558e81a2892cca47ebe9c9466dd92be1f |
| Candidate commit | Record the exact tested commit, not a moving branch |
| No-pack isolation and other installed instructions | Not recorded |
| Model, settings, harness/client version | Not recorded |
| Installation mode and actual loaded skills | Not recorded |
| Go baseline, executing toolchain, dependencies, generators | Not recorded for a model comparison |
| Permissions and infrastructure availability | Not recorded |
| Preselected repeats, budgets, order, seeds | Not recorded |

| Case / variant / repeat | Correctness and contract evidence | Scope and permissions | Checks, skips, cleanup, claims | Trace / patch / grader evidence | Result |
| --- | --- | --- | --- | --- | --- |
| Not run | — | — | — | — | Not run |

Record actual loaded skills, useful versus unnecessary reads/checks, approval
requests, first-patch stops, tokens, and elapsed time with each trace. Separate
unavailable checks from failures and preserve inconclusive outcomes. Summarize
quality first, efficiency second; do not select only favorable repetitions.
Use the [evaluation protocol](behavioral-evaluation.md) and the
[kit's isolation requirements](../evals/README.md). Publish conclusions only for
configurations actually tested; structural or grader success is not model behavior.
