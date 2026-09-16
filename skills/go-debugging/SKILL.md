---
name: go-debugging
description: "Causality. Use for an uncertain Go defect, panic, hang, startup failure, resource leak, or flaky behavior."
---

# Go Debugging

**Causality.** Find the first observable divergence between expected behavior and the real execution path. Honor requirements and preserve settled choices outside the requested change.

Build the smallest repeatable signal for the reported symptom. Inspect the error chain or panic stack and the input, caller, build setting, or running version that can explain it; do not audit every source before testing a hypothesis. Distinguish observed facts from explanations that merely fit them.

Follow values and ownership across the implicated boundaries. Inspect the concrete value behind an interface, backing storage behind a slice or map, or context passed to a blocking operation when relevant. A nil check, retry, or recovered panic can hide the mechanism without repairing it.

Choose the next observation for its ability to reject a plausible hypothesis. Use goroutine stacks for blocked work, the race detector for exercised shared-state conflicts, and the matching profile or trace for a runtime resource question. Account for the overhead and sensitivity of diagnostic captures.

Control time, scheduling, fixtures, and external dependencies enough to expose intermittent failures. Change one causal variable at a time and make every diagnostic goroutine terminate.

For diagnosis, finish with the supported cause or the next discriminating observation; do not edit files merely because a fix is possible. When fixing is requested, repair the cause at its owner, replay the original case, and check relevant neighboring callers. Keep a regression check for the mechanism, remove temporary instrumentation, and report actual verification or its specific limits.
