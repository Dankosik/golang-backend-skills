---
name: go-testing
description: "Behavior. Use when writing or improving Go unit tests, table tests, test doubles, fuzz targets, or deterministic tests of concurrent code."
---

# Go Testing

**Behavior first.** Find the observable promise this change could break. Choose fixtures whose values and relationships distinguish correct behavior from a plausible defect; derive expectations independently of the production algorithm. Preserve relevant contract distinctions through observation and assertion: decoding, normalization, or helpers must not make incorrect results appear correct. Honor supplied requirements and settled technical choices; resolve only what the task leaves open.

Read the existing tests and module before choosing APIs. Preserve the Go baseline and established assertion or mocking libraries. Start with ordinary values and direct calls. Use a fake or mock for a meaningful collaborator boundary; verify interactions when the interaction itself is required. Avoid interfaces created solely to mock internal steps.

Group cases sharing one rule with named subtests; keep distinct behaviors readable. Reuse existing fixtures and testing helpers before building a test framework. Register cleanup with the resource owner. Parallelize only isolated cases; process environment, working directory, and shared fixtures are not isolated by subtest names.

Control concurrency with explicit synchronization. Use supported `testing/synctest` for self-contained time and goroutine behavior, not external I/O. Bound waits, join workers, and return worker failures to the test goroutine before fatal assertions. Sleeping does not establish synchronization.

Use fuzzing for meaningful properties and input boundaries, keeping each invocation deterministic and independent. Preserve discovered failures as regression cases. Run relevant tests, confirm execution and skips, and use the race detector for concurrent paths. Coverage and race results describe exercised behavior; they do not establish correctness by themselves.
