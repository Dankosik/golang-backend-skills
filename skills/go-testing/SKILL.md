---
name: go-testing
description: "Write or review Go unit tests, table tests, doubles, fuzz targets, and deterministic concurrent tests."
---

# Go Testing

**Behavior first.** Find the observable promise this change could break. Choose distinguishing fixtures and derive expectations independently of the production algorithm. Preserve contract distinctions in observations and assertions: decoding, normalization, or helpers must not conceal a violation. Honor requirements and preserve settled choices outside the requested change.

Use existing tests and the supported Go baseline to select APIs. Inspect module or runner settings when those choices are uncertain, not as a repeated prerequisite. Preserve assertion and mocking libraries. Start with ordinary values and direct calls; use doubles for meaningful collaborator boundaries and verify interactions only when required. Avoid interfaces created solely to mock internal steps.

Group cases sharing one rule with named subtests; keep distinct behaviors readable. Reuse fixtures and helpers before building a test framework. Register cleanup with the resource owner. Parallelize only isolated cases; process environment, working directory, and shared fixtures are not isolated by subtest names.

For concurrent behavior, use explicit synchronization. Supported `testing/synctest` can help self-contained time and goroutine tests, not external I/O. Bound waits, join workers, and return worker failures to the test goroutine before fatal assertions. Sleeping does not establish synchronization.

Use fuzzing when the task or a concrete input-property risk warrants it, with deterministic, independent invocations and a bounded run budget. Preserve discovered failures as regression cases; do not start an open-ended fuzz campaign for ordinary unit changes.

For a regression test, establish that it distinguishes the reported defect from the intended behavior, using the original reproducer or a controlled faulty variant where practical. A test that merely restates the implementation is not evidence of the contract.

Run the relevant project tests, confirm execution and skips, and use the race detector for affected shared-memory paths where supported or required. Reuse applicable results for the same revision and environment. Coverage and race results describe exercised behavior, not general correctness or liveness. Report unavailable checks; finish a test review with findings rather than unsolicited edits.
