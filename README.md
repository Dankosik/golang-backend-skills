# Golang Backend Skills

Small, independent skills for clean, idiomatic Go backend development.

Each skill starts with a familiar engineering concept and directs a decision: what to inspect, how to reason, and what would make the result convincing. The model brings its language and ecosystem knowledge. Your project supplies the versions, conventions, and constraints.

One `SKILL.md` per skill. No reference libraries, setup ceremony, mandatory process, or dependencies between skills.

## Install

Use the [Agent Skills CLI](https://github.com/vercel-labs/skills) and choose your coding agent and desired skills:

```sh
npx skills add Dankosik/golang-backend-skills
```

Install only the testing skills:

```sh
npx skills add Dankosik/golang-backend-skills --skill go-testing go-integration-testing
```

Or install from a local checkout:

```sh
npx skills add ./golang-backend-skills
```

You can also copy an individual skill folder into the skills directory supported by your agent. Each folder is self-contained. The skills have no runtime dependencies; Node.js is needed if you choose the CLI installer. Go is needed when the agent builds or tests your application.

## Choose the decision

| Skill | Leading concept | Use it for |
| --- | --- | --- |
| [go-implement](skills/go-implement/SKILL.md) | Execution, Reuse, Clarity | Turn clear requirements or an agreed technical design into working Go |
| [go-idiomatic](skills/go-idiomatic/SKILL.md) | Contracts | Values, errors, interfaces, ownership, and behavior-preserving cleanup |
| [go-design](skills/go-design/SKILL.md) | Cohesion | Responsibilities, packages, consumer interfaces, and useful abstractions |
| [go-concurrency](skills/go-concurrency/SKILL.md) | Ownership | Goroutines, channels, synchronization, cancellation, bounds, and joining |
| [go-debugging](skills/go-debugging/SKILL.md) | Causality | Bugs, panics, hangs, startup failures, and flaky behavior |
| [go-performance](skills/go-performance/SKILL.md) | Evidence | Measured latency, throughput, CPU, allocation, memory, and contention |
| [go-build](skills/go-build/SKILL.md) | Resolution | Modules, workspaces, toolchains, dependencies, generation, and packaging |
| [go-service](skills/go-service/SKILL.md) | Composition | Dependency wiring, configuration, startup, resource lifetime, and shutdown |
| [go-http](skills/go-http/SKILL.md) | Translation | Routes, middleware, request decoding, responses, errors, and streaming |
| [go-grpc](skills/go-grpc/SKILL.md) | Contract | Protobuf evolution, interceptors, status, deadlines, and stream ownership |
| [go-data](skills/go-data/SKILL.md) | Atomicity | Queries, transactions, migrations, data mapping, and competing writes |
| [go-security](skills/go-security/SKILL.md) | Authorization | Identity, resource permissions, tenancy, untrusted input, and secrets |
| [go-integrations](skills/go-integrations/SKILL.md) | Delivery semantics | Outbound calls, retries, messages, jobs, and caches |
| [go-observability](skills/go-observability/SKILL.md) | Operability | Logs, metrics, traces, probes, and lifecycle signals |
| [go-testing](skills/go-testing/SKILL.md) | Behavior | Unit tests, tables, doubles, fuzzing, and deterministic concurrency tests |
| [go-integration-testing](skills/go-integration-testing/SKILL.md) | Mechanism | HTTP/RPC composition, database behavior, and infrastructure tests |

Use `go-implement` when the task is clear and the work is to implement it. Use a specialist when its particular decision needs attention. Each preserves supplied requirements and settled technical choices; none requires a design phase. Debugging identifies an uncertain cause; performance work measures a resource claim. Unit tests isolate ordinary behavior; integration tests retain the mechanism being tested.

## Use

Ask naturally, or select a skill through your agent's explicit skill invocation:

- “Use go-implement to implement this specification without changing its technical design.”
- “Use go-idiomatic to simplify this package while preserving errors and nil semantics.”
- “Use go-concurrency to fix cancellation and shutdown in this worker.”
- “Use go-http to implement this endpoint with our existing router.”
- “Use go-data to fix the duplicate reservation race.”
- “Use go-testing to cover this rule with deterministic tests.”

The pack preserves your Go baseline, router or framework, database driver or ORM, generation tools, and test libraries. The standard library is a starting point for reuse; existing dependencies remain valid choices where they fit. No skill prescribes an upgrade, a utility megadependency, a replacement framework, or a layered architecture. Provider-specific deployment and specialist infrastructure remain project concerns.

## Contribute

Keep each skill independent and decision-focused. Prefer an established concept over a new glossary, a discriminating trigger over a capability catalog, and an observable outcome over a long checklist. Improve wording against a realistic task that exposed a weakness. Keep version lookups and API tutorials out of the skill.

The pack uses the [Agent Skills format](https://agentskills.io/specification). Structural validity and a few useful examples do not establish a universal improvement across models.

## Acknowledgements

Follows the compact style of [Dankosik/java-backend-skills](https://github.com/Dankosik/java-backend-skills) and [Dankosik/fastify-backend-skills](https://github.com/Dankosik/fastify-backend-skills), with inspiration from [Dankosik/go-service-template-rest](https://github.com/Dankosik/go-service-template-rest) and [mattpocock/skills](https://github.com/mattpocock/skills). The instructions are written for Go semantics and work independently of those repositories.

[MIT license](LICENSE).
