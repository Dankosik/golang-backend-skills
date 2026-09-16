---
name: go-observability
description: "Operability. Use when Go logs, metrics, traces, probes, or lifecycle signals must explain and support backend behavior."
---

# Go Observability

**Operability.** Start with the operational question and choose the smallest signal that answers it. Honor requirements and preserve settled choices outside the requested change.

Follow the affected business operation through existing instrumentation. Reuse the project's logger, registries, and instrumented clients. Preserve its telemetry stack; a supported standard API can fill a gap without requiring a logging or tracing migration.

Use metrics for aggregate rates, latency, failures, and saturation; traces for an operation's path; logs for actionable events. Bound metric dimensions by their possible combinations. Prefer route templates and finite outcomes to raw paths, user IDs, or error messages. Distinguish logical outcomes from retry attempts and response completion from durable business completion.

Propagate correlation through the actual context and goroutine boundaries. Give spans an owner and an end on every exit. Keep structured errors useful while excluding secrets and sensitive payloads; caller-provided correlation is not trusted identity.

When probes change, treat them as control inputs: liveness describes local progress and readiness describes ability to serve. Consider the platform's response to a shared dependency failure. When diagnostic surfaces change, restrict access and account for profiling overhead.

When lifecycle signals or flushing change, observe admission, in-flight work, cleanup, and telemetry flushing within the shutdown budget. For an ordinary signal edit, verify its output, relevant failure behavior, cardinality, and absence of duplication without adding a lifecycle audit. Finish when the requested question is answerable, distinguishing local checks from deployment evidence; diagnosis alone does not authorize edits.
