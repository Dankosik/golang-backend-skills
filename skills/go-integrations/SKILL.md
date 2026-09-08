---
name: go-integrations
description: "Delivery semantics. Use when Go outbound calls, retries, messages, jobs, or caches must remain correct across delay, duplication, failure, or restart."
---

# Go Integrations

**Delivery semantics.** Determine what can repeat, disappear, or remain unknown across each process boundary. Honor supplied requirements and settled technical choices; resolve only what the task leaves open.

Trace intent through effect to acknowledgement. A lost response can leave a successful remote write unresolved. Tie replay to a stable operation identity and equivalent request meaning; a timeout is not proof that nothing happened.

Budget total time, attempts, active calls, queued work, and response consumption together. Reuse shared clients and transports. Propagate context through cooperating operations, classify transport failures separately from application responses, and close owned response bodies. Body-draining behavior depends on the actual transport and Go version; avoid unbounded cleanup of untrusted responses.

Put retries where effect semantics are known and account for nested attempts. Cancellation is a request to stop, not a reversal of an external effect. Keep recovery bounded and preserve unresolved outcomes when the provider cannot disambiguate them.

For messages and jobs, follow business commit, publication, acknowledgement, redelivery, and process death. Choose durability and coordination to match the promised outcome. A goroutine or local channel does not persist work, and broker guarantees have a defined boundary.

For caches, identify authoritative data, key identity, freshness, invalidation, and bounded origin fallback. Consider concurrent stale refill; let a concrete need justify the cache.

Challenge the consequential interruption point and observe the actual effect. Verify with the real dependency when its semantics are the claim.
