# Changelog

## 1.0.1 — Unreleased

- Clarify activation descriptions within the existing skill domains; these are behavioral routing corrections, not cosmetic edits.
- Separate review/diagnosis from editing and carry implementation through applicable checks and fixes for failures it introduces.
- Scope investigation and verification to the changed Go contract, preserving goroutine ownership, error/nil semantics, HTTP/RPC boundaries, and database evidence.
- Distinguish mounted-handler checks from network tests; make gRPC draining, data concurrency, fuzzing, and lifecycle checks conditional on the task.
- Keep settled choices outside the change and avoid reopening an explicitly agreed cache or migration.
- Refresh Go-specific starter prompts and native metadata; retain all 16 independently installable skill names and paths.
- Add an instruction audit, 20 behavioral evaluation specifications, and an unfilled results template. Model comparisons have not been run.
- Prepare the next PATCH candidate only; published v1.0.0 pins, tags, and marketplace entries are unchanged.

## 1.0.0 — 2026-09-08

- First versioned distribution of 16 independent Go skills.
- Portable Agent Plugins manifest plus native Claude Code and Codex adapters.
- Reproducible installation, explicit updates, and immutable GitHub release assets.
- Skill instructions are unchanged from the previously published main branch.
