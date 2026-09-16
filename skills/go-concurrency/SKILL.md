---
name: go-concurrency
description: "Implement or review Go goroutines, channels, shared-state synchronization, cancellation, joining, and work bounds."
---

# Go Concurrency

**Ownership.** Account for each goroutine in the affected path from admission to termination: who observes failure, requests cancellation, releases blocking operations, and waits for completion? Honor requirements and preserve settled choices outside the requested change.

Keep sequential work sequential unless overlap serves a current need. Reuse standard synchronization and existing coordination libraries. A mutex often expresses shared state more clearly than a channel protocol; channels fit communication and ownership transfer. Name the synchronization edge that makes shared reads and writes safe. Concurrent containers and atomics do not make a compound business operation atomic.

Propagate context through dependent calls and release derived contexts. Cancellation is a signal, not a join or proof that an external effect stopped. Give every affected send, receive, wait, and I/O operation an exit story. Give channel closure one owner who can establish that all sends have finished. Do not detach request work without a deliberate lifetime and failure owner.

Bound pending work as well as active work. A semaphore acquired inside an unlimited number of goroutines still permits unlimited waiting. When using errgroup, account for blocking admission and the derived context ending when Wait returns.

Verify the changed race, cancellation, capacity, or shutdown property with controlled coordination and bounded waits. Use the race detector for affected shared-memory paths where supported; it finds exercised races, not liveness failures. Observe worker termination separately and leave no test goroutines running. Report unsupported checks rather than substituting a weaker proof.

For review-only work, do not edit files. Ground each finding in the affected synchronization or blocking path and a concrete failing interleaving; check for an existing exit or join before claiming it is absent.
