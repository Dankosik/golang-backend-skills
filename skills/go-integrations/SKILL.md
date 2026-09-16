---
name: go-integrations
description: "Implement or review Go outbound calls, retries, messages, jobs, and caches under delay, duplication, or failure."
---

# Go Integrations

**Delivery semantics.** Determine what can repeat, disappear, or remain unknown at the process boundary affected by this task. Honor requirements and preserve settled choices outside the requested change.

For outbound effects, trace intent through effect to acknowledgement. A lost response can leave a successful remote write unresolved. Tie replay to a stable operation identity and equivalent request meaning; a timeout is not proof that nothing happened.

Budget total time, attempts, active calls, queued work, and response consumption together. Reuse shared clients and transports. Propagate context through cooperating operations, classify transport failures separately from application responses, and close owned response bodies. Body-draining behavior depends on the actual transport and Go version; avoid unbounded cleanup of untrusted responses.

Put retries where effect semantics are known and account for nested attempts. Cancellation is a request to stop, not a reversal of an external effect. Keep recovery bounded and preserve unresolved outcomes when the provider cannot disambiguate them.

For messages and jobs, follow business commit, publication, acknowledgement, redelivery, and process death. Choose durability and coordination to match the promised outcome. A goroutine or local channel does not persist work, and broker guarantees have a defined boundary.

For caches, identify authoritative data, key identity, freshness, invalidation, and bounded origin fallback. Consider concurrent stale refill. Do not propose speculative caching, but implement an explicitly agreed cache contract without reopening its justification or claiming an unmeasured speedup.

Verify the changed delivery or freshness property at its consequential failure point, observing the actual effect. Use the real dependency when its semantics are the claim; pure retry policy or key logic can use controlled collaborators. Do not require a broker or restart test for every integration change. State unavailable evidence and do not expand the task to invent infrastructure.

For review-only work, report the affected path, triggering failure, and consequence without edits. Check existing idempotency, acknowledgement, and invalidation guarantees before declaring them missing; distinguish a proven violation from a provider-dependent uncertainty.
