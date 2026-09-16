---
name: go-implement
description: "Execution. Implement requested Go backend behavior within the project's existing contracts and technical choices."
---

# Go Implement

**Execution.** When the intended behavior is clear, implement it directly. Honor the requirements; preserve settled choices outside the requested change. An explicitly requested technical change is not an invitation to redesign unrelated parts.

Read the affected code and callers, then extend the existing path. Resolve local details using the project's Go version, package conventions, and selected infrastructure.

**Reuse.** Before adding a technical helper, look for a matching operation in nearby project code, the supported standard library, or declared dependencies. Keep the search proportional to the helper. Packages such as `strings`, `slices`, and `maps` cover many routine operations. Custom mechanics need a concrete semantic or operational gap; wrappers should add domain meaning or adaptation.

**Clarity.** Write intention-revealing names, cohesive responsibilities, explicit control flow, and visible effects and failure paths. Keep changes local and idiomatic. Apply SOLID, DRY, and YAGNI as heuristics: abstract shared knowledge, preserve distinct business rules, and add only structure justified by current requirements. New dependencies, configuration, and adjacent cleanup need a present requirement.

If a concrete contradiction prevents correct implementation, identify it and continue independent work. Ask only for information that materially changes the required outcome; routine implementation choices remain yours.

Format changed Go code. Use the project's build and focused tests for the affected behavior, including a meaningful failure case. Add race, transport, database, fuzz, or performance checks only for a concrete claim or required project gate. Reuse applicable results for the same revision and environment; loading another skill is not a reason to rerun them.

Within the environment's permissions, fix failures introduced by the change and rerun affected checks without stopping for review after the first patch. Finish when the requested outcome and required checks are satisfied, or state the concrete blocker and unavailable verification. Do not invent infrastructure, unrelated cleanup, or speculative checks as new completion gates.
