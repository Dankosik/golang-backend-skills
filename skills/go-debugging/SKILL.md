---
name: go-debugging
description: "Causality. Use for an uncertain Go defect, panic, hang, startup failure, resource leak, or flaky behavior."
---

# Go Debugging

**Causality.** Find the first observable divergence between expected behavior and the real execution path. Honor supplied requirements and settled technical choices; resolve only what the task leaves open.

Build the smallest repeatable signal for the reported symptom. Read the error chain or panic stack, affected callers, actual input, build configuration, and running version. Distinguish observed facts from explanations that merely fit them.

Follow values and ownership across boundaries. Inspect the concrete value behind an interface, the backing storage behind a slice or map, and the context actually passed to the blocking operation. A nil check, retry, or recovered panic can hide the mechanism without repairing it.

Choose the next observation for its ability to reject a plausible hypothesis. Use goroutine stacks for blocked work, the race detector for exercised shared-state conflicts, and the matching profile or trace for a runtime resource question. Account for the overhead and sensitivity of diagnostic captures.

Control time, scheduling, fixtures, and external dependencies enough to expose intermittent failures. Change one causal variable at a time and make every diagnostic goroutine terminate.

Fix the cause at its owner, replay the original case, and check relevant neighboring callers. Keep a regression check that detects the mechanism and remove temporary instrumentation. Finish with a supported explanation and actual verification; if evidence is incomplete, identify the next discriminating check.
