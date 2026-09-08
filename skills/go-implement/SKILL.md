---
name: go-implement
description: "Execution. Use to turn clear requirements, a specification, a technical design, or a straightforward backend request into working Go code."
---

# Go Implement

**Execution.** When the intended behavior is clear, implement it directly. Treat supplied requirements and settled technical decisions as constraints, not invitations to redesign.

Read the affected code and callers, then extend the existing path. Resolve local details using the project's Go version, package conventions, and selected infrastructure.

**Reuse.** Before writing technical helpers, check existing project code, the supported standard library, and declared dependencies. Packages such as `strings`, `slices`, and `maps` already express many routine operations. Use a matching API directly. Custom mechanics need a concrete semantic or operational gap; wrappers should add domain meaning or adaptation.

**Clarity.** Write for the next reader: intention-revealing names, cohesive responsibilities, explicit control flow, and visible effects and failure paths. Keep changes local and idiomatic to Go. Apply SOLID, DRY, and YAGNI as heuristics: abstract shared knowledge, preserve distinct business rules, and add only structure justified by current requirements. Prefer the simplest implementation that remains easy to read and change.

New dependencies, configuration, and adjacent cleanup still need a present requirement. Preserve established contracts and technical choices.

If a concrete contradiction prevents correct implementation, identify it and continue independent work. Ask only for information that changes the required outcome; routine implementation choices remain yours.

Verify the requested behavior with focused checks, including the meaningful failure case, and respect existing required checks. Finish with working code, actual verification, and any specific unresolved requirement.
