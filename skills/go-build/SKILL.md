---
name: go-build
description: "Resolution. Use for Go module or workspace problems, toolchain compatibility, generated code, dependency changes, or build and packaging failures."
---

# Go Build

**Resolution.** Identify the affected build command or requested build change. Inspect the module, workspace, replacements, vendoring, toolchain, tags, target platform, cgo, or generators when they can explain that layer. Reproduce failures in their actual configuration, not by first auditing the entire toolchain. Honor requirements and preserve settled choices outside the requested change.

Distinguish the module's minimum Go and language version from the toolchain running the build. Newer local compilation does not establish compatibility with older standard-library APIs. Use modern forms available at the supported baseline; keep upgrades and modernization within the requested scope.

Trace dependency selection through the module graph. Minimal version selection chooses the highest requirement for each module path, not the newest published release. Declare directly imported libraries in the consuming module using Go tooling. Preserve existing version choices outside the requested update.

Checksums establish artifact integrity, not dependency locks or security. Investigate download failures without disabling verification. Keep private-module settings narrowly scoped. Pin build tools through the project's supported mechanism; regenerate and review module metadata instead of fabricating it.

A workspace or local replacement can conceal a broken standalone module. Verify the configuration CI or consumers actually use, including generation and packaging when affected; do not impose a standalone-release claim on a workspace-only change.

Report the explained failure or implemented change and the affected build/test results. For dependency changes, inspect resolved versions and applicable vulnerability findings; state scan coverage and unavailable checks honestly. For diagnosis-only requests, report findings without modifying the build.
