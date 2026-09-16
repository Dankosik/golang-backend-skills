---
name: go-performance
description: "Evidence. Use to audit or improve Go latency, throughput, CPU, memory, allocation, or contention, or to design a backend benchmark."
---

# Go Performance

**Evidence.** Identify the requested outcome: audit, measurement, or optimization. Honor requirements and preserve settled choices outside the requested change. For an audit without runtime data, separate code-supported properties from bottleneck hypotheses and propose discriminating measurements; do not require a new load harness just to provide the analysis.

Separate computation from waiting on dependencies, synchronization, queues, and scheduling. Choose a CPU profile for active execution, allocation and retained-heap evidence for memory, and blocking, mutex, or execution traces for waiting. High allocation volume is not a retained-memory leak. Account for diagnostic overhead and restrict access to captured data and profiling endpoints.

For optimization, establish the workload, metric, toolchain, resource limits, and comparable baseline. Form a falsifiable hypothesis. Remove demonstrated waste before introducing pools, caches, goroutines, unsafe conversions, or runtime tuning. Reuse suitable library operations and preserve ownership, ordering, errors, and cancellation.

For isolated operations, verify that benchmarks measure the intended work with representative inputs. Keep setup outside the measured region; prefer `B.Loop` where supported. Compare repeated samples with `benchstat` under consistent conditions. Choose the sample plan before measuring; do not rerun until noise produces a favorable result.

For service-level claims, measure representative concurrency and saturation, including latency distributions, throughput, errors, and resource use. A microbenchmark gain does not establish an endpoint gain. Do not require both benchmark levels for every task.

Finish an audit with supported findings and explicit hypotheses, without unsolicited edits. Finish an optimization with the change, before-and-after evidence, and remaining uncertainty. If evidence is unavailable or inconclusive, say so and favor the simpler correct implementation over an invented speedup.
