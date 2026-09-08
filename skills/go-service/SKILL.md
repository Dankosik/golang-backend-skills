---
name: go-service
description: "Composition. Use when Go backend construction, configuration, startup, health, resource ownership, or graceful shutdown needs implementation or diagnosis."
---

# Go Service

**Composition.** Make construction and lifetime visible. Trace how the affected component receives its dependencies and configuration, starts serving, and releases resources. Honor supplied requirements and settled technical choices; resolve only what the task leaves open.

Prefer explicit wiring and ordinary constructors in the existing composition root. Reuse the project's lifecycle machinery before adding a container or generic application framework. Keep hidden I/O, goroutine startup, mutable globals, and process exits out of reusable packages. Request context belongs to the operation, not a shared service field.

Parse related settings into typed configuration at the boundary. Distinguish missing, empty, invalid, and deliberately defaulted values. Validate required relationships before accepting work; never make an invalid deployment appear healthy with placeholder credentials. Clean up resources already acquired when later initialization fails.

Separate stopping admission, draining accepted work, cancellation, joining workers, and closing dependencies. Keep dependencies available until their users finish. Give cleanup its own bounded context when the initiating context is already canceled. Wait for actual shutdown completion before returning from main; a server's serving loop can return before draining finishes.

Where health checks exist, distinguish readiness to accept work from process liveness. Account for long-lived or hijacked connections separately when the server does not drain them.

Exercise the relevant invalid configuration, partial startup failure, or shutdown ordering with observable resource cleanup. Preserve the existing deployment contract.
