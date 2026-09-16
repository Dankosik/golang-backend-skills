---
name: go-integration-testing
description: "Mechanism. Use when Go tests must establish HTTP or RPC composition, database behavior, migrations, or interaction with real infrastructure, including Testcontainers."
---

# Go Integration Testing

**Prove the mechanism.** Identify what makes the promised behavior true, then choose the smallest test boundary that includes it and a scenario that exposes its failure. Honor requirements and preserve settled choices outside the requested change.

Preserve the Go baseline, drivers, transport, and test setup. Reuse existing harnesses. Use established Testcontainers modules when an infrastructure claim needs them; a container is an environment, not the assertion. For database cases, match the target engine and relevant configuration, apply real migrations, establish readiness, and isolate data.

Exercise the actual router, middleware, or interceptor when its behavior matters. A recorder with the mounted HTTP handler chain can cover routing, middleware, and response contracts; invoking only a leaf handler omits that composition. Reuse an in-process RPC client/server harness for RPC semantics. Use real network transport for connection, TLS, socket deadlines, backpressure, or disconnect claims. Do not require network or database setup for unrelated in-process contracts.

Keep the mechanism real and replace only collaborators beyond it. A fabricated principal tests downstream authorization, not credential verification. Preserve contract distinctions in observed responses and effects; decoding, normalization, or helpers must not conceal violations.

For transaction, constraint, locking, or isolation claims, use the target engine and real transactions. Use independent connections for arbitration and visibility, and fresh reads for committed effects. Test-side rollback cannot undo independent application commits.

Coordinate competing work, bound waits, and surface worker errors. Own cleanup for resources and committed fixtures, including partial setup failure; finish workers before removing resources.

Run the intended tests with their configuration and confirm execution. Reuse applicable evidence for the same revision/environment, while respecting required checks. Report skips and unavailable infrastructure without substituting weaker proof or inventing a new harness as an unsolicited completion gate. Local integration success does not certify a deployed provider.
