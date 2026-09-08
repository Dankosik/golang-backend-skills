---
name: go-performance
description: "Evidence. Use for a reported Go latency, throughput, CPU, memory, allocation, or contention problem, or a requested backend benchmark."
---

# Go Performance

**Evidence.** Identify the affected workload, metric, toolchain, and resource limits. Establish comparable conditions before changing code. Honor supplied requirements and settled technical choices; resolve only what the task leaves open.

Separate computation from waiting on dependencies, synchronization, queues, and scheduling. Choose a CPU profile for active execution, allocation and retained-heap evidence for memory, and blocking, mutex, or execution traces for waiting. High allocation volume is not a retained-memory leak. Account for diagnostic overhead and restrict access to captured data and profiling endpoints.

Form a falsifiable hypothesis and measure what distinguishes plausible causes. Remove demonstrated waste before introducing pools, caches, goroutines, unsafe conversions, or runtime tuning. Reuse suitable library operations and preserve ownership, ordering, errors, and cancellation. A faster path that changes the contract is a different implementation.

Use representative inputs and verify that benchmarks measure the intended operation. Keep setup outside the measured region; prefer `B.Loop` where the project's Go baseline supports it. Compare repeated samples with `benchstat` under consistent build and machine conditions. Choose the sample plan before measuring; do not rerun until noise produces a favorable result.

Measure service behavior under representative concurrency and saturation, including latency distributions, throughput, errors, and resource use. A microbenchmark gain does not establish an endpoint gain.

Report the cause, change, before-and-after evidence, and remaining uncertainty. When evidence is inconclusive, retain the simpler correct implementation rather than claiming a speedup.
