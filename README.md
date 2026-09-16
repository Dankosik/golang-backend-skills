# Golang Backend Skills

Small, independent skills for clean, idiomatic Go backend development.

Each skill starts with a familiar engineering concept and directs a decision: what to inspect, how to reason, and what would make the result convincing. The model brings its language and ecosystem knowledge. Your project supplies the versions, conventions, and constraints.

One `SKILL.md` per skill. No reference libraries, setup ceremony, mandatory process, or dependencies between skills.

## Install

The repository prepares 1.0.1; installation examples remain pinned to the published v1.0.0 until a new release exists.

Versioned release: [v1.0.0](https://github.com/Dankosik/golang-backend-skills/releases/tag/v1.0.0).
Install selected skills, or the entire pack, into your current project:

```sh
npx skills@1.5.25 add "Dankosik/golang-backend-skills#v1.0.0" --agent codex --skill '*' --copy
```

Use `--skill go-implement` for one skill, or `--agent claude-code` for Claude
standalone placement. Node.js >=22.20.0 is required by this installer, not by
the skill instructions.

For native Claude Code and Codex installation, add the
[Dankosik marketplace](https://github.com/Dankosik/agent-skills-marketplace), then
install `golang-backend-skills@dankosik-skills`. The author catalog is available independently
of review for either provider's public directory.

[All installation methods, updates and rollback](docs/distribution.md) ·
[Versioning](docs/versioning.md) · [Changelog](CHANGELOG.md)

## Choose the decision

| Skill | Leading concept | Use it for |
| --- | --- | --- |
| [go-implement](skills/go-implement/SKILL.md) | Execution, Reuse, Clarity | Turn clear requirements or an agreed technical design into working Go |
| [go-idiomatic](skills/go-idiomatic/SKILL.md) | Contracts | Values, errors, interfaces, ownership, and behavior-preserving cleanup |
| [go-design](skills/go-design/SKILL.md) | Cohesion | Responsibilities, packages, consumer interfaces, and useful abstractions |
| [go-concurrency](skills/go-concurrency/SKILL.md) | Ownership | Goroutines, channels, synchronization, cancellation, bounds, and joining |
| [go-debugging](skills/go-debugging/SKILL.md) | Causality | Bugs, panics, hangs, startup failures, and flaky behavior |
| [go-performance](skills/go-performance/SKILL.md) | Evidence | Audit or measure latency, throughput, CPU, allocation, memory, and contention |
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

Use `go-implement` when the task is clear and the work is to implement it. Use a specialist when its particular decision needs attention. Each preserves supplied requirements and settled technical choices; none requires a design phase. Debugging identifies an uncertain cause; performance work distinguishes an audit from measurement or optimization. Unit tests isolate ordinary behavior; integration tests retain the mechanism being tested.

Select skills for decisions that need their guidance, not merely because the repository contains Go. Specialists are not mandatory stages, and distinct decisions can justify several skills. A skill does not expand the requested scope or require every topic in its body to be investigated.

Review and diagnosis produce findings unless changes were requested. Implementation includes applicable verification and fixing failures it introduces, not a stop after the first patch. Preserve settled choices outside the requested change; an explicit migration or agreed cache is not a reason to reopen unrelated decisions.

Ground review findings in the affected code, triggering condition, and observable consequence. Inspect existing guards before declaring them missing. Distinguish a project-rule violation from a design preference, and a supported defect from a hypothesis. Correct implementation and conformance to conventions are separate judgments; neither substitutes for the other.

Match evidence to the changed claim: ordinary Go behavior, a mounted HTTP handler chain, an RPC path, real network transport, or database mechanisms. Build and focused tests are the ordinary starting point, not proof of every boundary. Keep required project checks, reuse still-applicable results, and report unavailable verification without inventing a new environment as a completion gate.

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

For maintainers: [instruction audit](docs/instruction-audit.md), [reference adoption and reviewer briefs](docs/reference-adoption.md), [behavioral evaluation](docs/behavioral-evaluation.md), and [results record](docs/evaluation-results.md). The [evaluation kit](evals/README.md) supplies 29 routing prompts and six small executable Go fixtures with independent graders. These are authoring materials, not prerequisites for using a skill. Grader self-tests are distinct from model comparisons; no behavioral comparison results are claimed by the candidate.

## Acknowledgements

Follows the compact style of [Dankosik/java-backend-skills](https://github.com/Dankosik/java-backend-skills) and [Dankosik/fastify-backend-skills](https://github.com/Dankosik/fastify-backend-skills), with inspiration from [Dankosik/go-service-template-rest](https://github.com/Dankosik/go-service-template-rest) and [mattpocock/skills](https://github.com/mattpocock/skills). Additional review and evaluation principles are traced to Open Code Review and the OpenAI articles in [reference adoption](docs/reference-adoption.md), including the limits of each transfer. The instructions are written for Go semantics and work independently of those repositories.

[MIT license](LICENSE).
