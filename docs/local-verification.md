# Local verification of the reference-driven candidate

Date: 2026-09-16. Reviewed parent: `4f5223a3e1a721b4af682e2da873e4cd3ae0d9de`.
Environment: Linux/amd64, Python 3.13.5, Go 1.23.2. This record concerns the
[evaluator](eval-runner.md), not model behavior or an independent agent review.

| Check actually executed | Result | What it establishes |
| --- | --- | --- |
| `python scripts/evaluate.py check` | Four fixture records accepted | Catalog validity, not model routing |
| `python -m unittest discover -s scripts/tests -p test_evaluate.py` | 17 tests passed | Input export, fixture identities, protected module/oracle, symlink rejection, and result classification |
| `python scripts/evaluate.py self-test --allow-execution` | Four negative controls failed their named oracle; four reference controls passed | Each oracle distinguishes its supplied broken and reference implementations |

| Case | Broken input | Reference control |
| --- | --- | --- |
| G01 | runtime-fail: TestOracleClamp | runtime-pass |
| G09 | runtime-fail: TestOracleMountedResponse | runtime-pass |
| G14 | runtime-fail: TestOracleNullMapping | runtime-pass |
| G17 | runtime-fail: TestOracleTenantEffect | runtime-pass |

The control result includes real Go test JSON events, not a compile-failure proxy.
Control sources and tests were formatted with the installed `gofmt`. No timing,
token-saving or generalization claim follows from these outcomes.

Full distribution validation, native install smoke and release-archive checks
were not executed locally: this environment had no complete clone or `skills_ref`
installation. The pre-existing repository CI remains the authority for those
checks; its status must be read on the actual PR rather than inferred here.
The new lightweight evaluator unit tests use that CI's existing test discovery.

**Not run:** no-pack/baseline/candidate model comparisons; implicit or explicit
activation trials; independent subagents; external trace grading; real database,
network, gRPC or performance evaluation. The other 16 G-scenarios and eight
negative probes remain specifications. No release-readiness or perfection claim
is made by this record.
