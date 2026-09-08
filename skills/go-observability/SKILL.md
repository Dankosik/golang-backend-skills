---
name: go-observability
description: "Operability. Use when Go logs, metrics, traces, probes, or lifecycle signals must explain and support backend behavior."
---

# Go Observability

**Operability.** Start with the operational question and choose the smallest signal that answers it. Honor supplied requirements and settled technical choices; resolve only what the task leaves open.

Follow the affected business operation through existing instrumentation. Reuse the project's logger, registries, and instrumented clients. Preserve its telemetry stack; a supported standard API can fill a gap without requiring a logging or tracing migration.

Use metrics for aggregate rates, latency, failures, and saturation; traces for an operation's path; logs for actionable events. Bound metric dimensions by their possible combinations. Prefer route templates and finite outcomes to raw paths, user IDs, or error messages. Distinguish logical outcomes from retry attempts and response completion from durable business completion.

Propagate correlation through the actual context and goroutine boundaries. Give spans an owner and an end on every exit. Keep structured errors useful while excluding secrets and sensitive payloads; caller-provided correlation is not trusted identity.

Treat probes as control inputs. Liveness describes local progress; readiness describes ability to serve the contract. Consider the platform's response to a shared dependency failure. Restrict diagnostic endpoints and account for profiling overhead.

Observe lifecycle changes through admission, in-flight work, cleanup, and telemetry flushing within the shutdown budget. Verify emitted signals and relevant failure behavior. Finish when the question is answerable with bounded signals, distinguishing local checks from deployment evidence.
