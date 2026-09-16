---
name: go-design
description: "Cohesion. Use when deciding or reviewing Go responsibilities, package boundaries, consumer interfaces, or abstractions for a concrete change."
---

# Go Design

Design for **cohesion**: a business rule should have one natural home, and callers should need little knowledge of its implementation. Honor requirements and preserve settled choices outside the requested change.

Trace the requested behavior through existing callers before introducing structure. Put invariants where all relevant paths encounter them. Keep transport, business policy, and persistence distinguishable where their contracts differ; let the actual problem determine the packages and types required.

Prefer concrete types and ordinary functions. Introduce a narrow interface at the consumer when it isolates a real dependency or variation; a single implementation can justify that boundary. Do not mirror every struct with an interface or expose an interface only to manufacture mocks. A function parameter may express a single operation more directly.

Choose composition, explicit dependencies, meaningful package names, and the smallest exported surface. Keep internal details private. Avoid generic utility packages, speculative extension points, and layers that merely forward the same knowledge.

Apply SOLID, DRY, and YAGNI as judgment: centralize shared rules while preserving independent reasons to change. Evaluate abstractions by what their callers no longer need to understand, including mutation ownership, resource lifetime, and error contracts.

For analysis or review, explain the responsibility problem and smallest justified change without editing files. For refactoring, finish when the changed responsibility has a clear owner, each retained boundary earns its cost, and focused checks preserve caller-visible behavior and effect ordering. Do not make design a prerequisite for an already settled implementation task.
