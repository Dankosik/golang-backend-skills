---
name: go-build
description: "Resolution. Use for Go module or workspace problems, toolchain compatibility, generated code, dependency changes, or build and packaging failures."
---

# Go Build

**Resolution.** Explain what the build actually selects before changing its declarations. Inspect the affected module, workspace, replacements, vendoring, selected toolchain, build tags, target platform, cgo, and relevant generators. Reproduce the failing command in its real configuration. Honor supplied requirements and settled technical choices; resolve only what the task leaves open.

Distinguish the module's minimum Go and language version from the toolchain running the build. Newer local compilation does not establish compatibility with older standard-library APIs. Use modern forms available at the supported baseline; keep upgrades and modernization within the requested scope.

Trace dependency selection through the module graph. Minimal version selection chooses the highest requirement for each module path, not the newest published release. Declare directly imported libraries in the consuming module using Go tooling. Preserve existing version choices unless a concrete requirement warrants changing them.

Checksums establish artifact integrity, not dependency locks or security. Investigate download failures without disabling verification. Keep private-module settings narrowly scoped. Pin build tools through the project's supported mechanism; regenerate and review module metadata instead of fabricating it.

A workspace or local replacement can conceal a broken standalone module. Verify the configuration that CI or consumers actually use, including generation and packaging when affected.

Finish with relevant build and test evidence. For dependency changes, inspect resolved versions and applicable vulnerability findings; report scan coverage and remaining uncertainty honestly.
