---
name: go-integration-testing
description: "Mechanism. Use when Go tests must establish HTTP or RPC composition, database behavior, migrations, or interaction with real infrastructure, including Testcontainers."
---

# Go Integration Testing

**Prove the mechanism.** Identify what makes the promised behavior true, then choose the smallest test boundary that includes it. Honor supplied requirements and settled technical choices; resolve only what the task leaves open.

Preserve the project's Go version, drivers, transport, and test infrastructure. Reuse existing harnesses and established Testcontainers modules where suitable. A container is an environment, not the assertion. Match the target engine and relevant configuration, apply real migrations, establish readiness, and isolate each test's data.

Exercise the actual router, middleware, or interceptor when their behavior matters. An `httptest` recorder covers handler output; use a real client/server transport for connection, TLS, streaming, or disconnect claims. Keep the mechanism under test real and replace only collaborators beyond it. A fabricated principal does not prove credential verification.

Database claims need the target engine. Exercise transaction boundaries and use independent connections for arbitration, locking, and visibility. Observe committed effects through a fresh read. Test-side rollback cannot undo independent application commits.

Coordinate races at a meaningful boundary; bound eventual assertions and surface worker errors. Own cleanup for connections, servers, containers, and committed fixtures, including partial setup failure. Finish workers before removing their resources.

Run the intended test command with its required configuration, confirm the selected tests actually executed, and report skipped or unavailable infrastructure explicitly. State the boundary proved; local integration success does not certify a deployed provider.
