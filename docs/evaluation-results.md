# Behavioral evaluation results

**Model comparisons: not run.** No model runs, speedups, or cross-model quality
gains are asserted here. Four fixtures now exist in the [executable subset](eval-runner.md).
Their broken/reference controls and evaluator unit tests are recorded in
[local verification](local-verification.md), not as behavioral comparison results.
Distribution/CI success must also be recorded separately. Copy this template per
actual comparison; never replace missing evidence with an expected result.

## Run identity

| Field | Recorded value |
| --- | --- |
| Date and evaluator | Not recorded for a model run |
| Case IDs | Not recorded |
| Fixture commit and source | Not pinned for a model run; G01/G09/G14/G17 available through the runner |
| Baseline pack for this change | 4f5223a3e1a721b4af682e2da873e4cd3ae0d9de |
| Historical prior pack | 48be5eb558e81a2892cca47ebe9c9466dd92be1f |
| Candidate commit | Not recorded |
| No-pack configuration | Not recorded |
| Model, settings, harness/client version | Not recorded |
| Other instructions and installation mode | Not recorded |
| Go baseline, executing toolchain, dependencies, generators | Not recorded |
| Permissions and infrastructure availability | Not recorded |
| Preselected repeats, budgets, order, seeds | Not recorded |

## Observations

| Case / variant / repeat | Correctness and contract evidence | Scope and permissions | Checks, skips, cleanup, claims | Trace / patch / grader evidence | Result |
| --- | --- | --- | --- | --- | --- |
| Not run | — | — | — | — | Not run |

Record actual loaded skills, useful versus unnecessary reads/checks, approval
requests, first-patch stops, tokens, and elapsed time with each trace. Separate
unavailable checks from failures and preserve inconclusive outcomes. Summarize
quality first, efficiency second; do not select only favorable repetitions.

## Conclusion

Not evaluated. Record supported improvements, regressions, uncertainty, and the
exact configurations to which conclusions apply. Use the
[evaluation protocol](behavioral-evaluation.md) and [runner instructions](eval-runner.md);
structural checks and oracle controls are not model behavior evidence.
