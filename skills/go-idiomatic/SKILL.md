---
name: go-idiomatic
description: "Review or improve Go value, error, interface, and collection semantics while preserving caller contracts."
---

# Go Idiomatic

**Contracts.** Make the caller's expectations visible in ordinary Go. Identify values, absence, mutation, ordering, effects, and failures before changing their representation. Follow the module's supported Go version and conventions. Honor requirements and preserve settled choices outside the requested change.

Use useful zero values where they fit; distinguish an invalid state from an empty result. Preserve nil versus empty where callers or serialization observe it. A typed nil inside an interface is not a nil interface. Choose receivers for mutation, identity, and method sets. Make aliasing explicit when copying reference fields; synchronization primitives must not be copied after use.

Treat slices and maps as shared storage unless ownership proves otherwise. Cloning is shallow; map iteration is unordered. Keep effects and branching explicit instead of hiding them inside clever expressions or transformation pipelines.

Use errors as values. Add meaningful context, preserve intentional error identity, and inspect wrapped errors with the supported standard matching APIs. Wrapping exposes a cause as part of the caller's contract; routine failures do not need panics.

**Reuse.** Prefer existing project, standard-library, and established dependency operations when their semantics match. Generics should express a real shared algorithm or type relationship. Keep wrappers only for domain meaning or adaptation.

For review-only work, cite the affected code, caller-visible contract, and triggering value; explain the smallest justified change without editing files. For implementation, finish with formatted code and focused checks for the observable contract the change could disturb; avoid unrelated style churn.
