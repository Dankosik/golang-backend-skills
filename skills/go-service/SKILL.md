---
name: go-service
description: "Implement or review Go dependency wiring, configuration, partial startup cleanup, and graceful shutdown."
---

# Go Service

**Composition.** Make construction and lifetime visible for the affected component. Trace the dependency, configuration, or lifecycle boundary changed by the task rather than re-auditing the whole service. Honor requirements and preserve settled choices outside the requested change.

Prefer explicit wiring and ordinary constructors in the existing composition root. Reuse the project's lifecycle machinery before adding a container or generic application framework. Keep hidden I/O, goroutine startup, mutable globals, and process exits out of reusable packages. Request context belongs to the operation, not a shared service field.

For configuration and startup, parse related settings into typed configuration. Distinguish missing, empty, invalid, and deliberately defaulted values. Validate required relationships before accepting work; never hide invalid deployment settings with placeholder credentials. Clean up resources already acquired when later initialization fails.

For shutdown changes, separate stopping admission, draining accepted work, cancellation, joining workers, and closing dependencies. Keep dependencies available until their users finish. Give cleanup a bounded context when the initiating context is already canceled. Wait for shutdown completion before returning from main; a serving loop can return before draining finishes.

When health or server lifetime is affected, distinguish readiness from liveness and account for long-lived or hijacked connections the server does not drain. Preserve the deployment contract.

Verify the changed configuration, startup, or shutdown property with observable cleanup at the relevant boundary. Do not require all lifecycle scenarios for unrelated wiring changes. For diagnosis or review-only work, report the supported explanation without editing; check the actual resource owner and shutdown ordering before claiming cleanup is missing.
