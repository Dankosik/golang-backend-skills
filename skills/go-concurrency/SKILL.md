---
name: go-concurrency
description: "Ownership. Use when Go goroutines, channels, shared state, or parallel work need correct synchronization, cancellation, capacity bounds, or cleanup."
---

# Go Concurrency

**Ownership.** Account for every goroutine from admission to termination: who observes failure, requests cancellation, releases blocking operations, and waits for completion? Honor supplied requirements and settled technical choices; resolve only what the task leaves open.

Keep sequential work sequential unless overlap serves a current need. Reuse standard synchronization and existing coordination libraries. A mutex often expresses shared state more clearly than a channel protocol; channels fit communication and ownership transfer. Name the synchronization edge that makes shared reads and writes safe. Concurrent containers and atomics do not make a compound business operation atomic.

Propagate context through dependent calls and release derived contexts. Cancellation is a signal, not a join or proof that an external effect stopped. Give every send, receive, wait, and I/O operation an exit story. Give channel closure one owner who can establish that all sends have finished. Do not detach request work without a deliberate lifetime and failure owner.

Bound pending work as well as active work. A semaphore acquired inside an unlimited number of goroutines still permits unlimited waiting. When using errgroup, account for blocking admission and the derived context ending when Wait returns.

Verify the relevant race, cancellation, saturation, or shutdown case with controlled coordination. The race detector finds exercised races; it does not prove liveness. Leave no test goroutines running.
