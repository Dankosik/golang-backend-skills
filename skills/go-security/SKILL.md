---
name: go-security
description: "Authorization. Use when Go identity, resource permissions, tenancy, untrusted input, outbound destinations, filesystem access, or secrets cross a trust boundary."
---

# Go Security

**Authorization.** Follow the caller from untrusted input through verified identity to the protected operation. Honor supplied requirements and settled technical choices; resolve only what the task leaves open.

Model subject, action, resource, and context. Authentication does not grant access to every object a caller can name. Enforce ownership and tenant scope at the operation that can protect the effect, using identity established by the real authentication path.

Reuse the project's established security integrations and supported standard-library mechanisms. Preserve token verification and TLS peer checks; use cryptographic APIs for security properties rather than custom algorithms or noncryptographic randomness. Keep credentials and sensitive payloads out of errors, logs, and diagnostic responses.

Trace untrusted data to its interpreter or destination. Parameterized SQL, bounded decoding, controlled outbound authorities, and filesystem containment address different boundaries. Check redirects, resolution, symlinks, and time-of-check races where relevant; lexical sanitization alone may not enforce the intended authority.

Choose browser and proxy protections from the actual deployment. Automatically attached credentials can require CSRF defenses; CORS does not authorize server operations. Trust forwarding metadata only through the known proxy boundary. Bound caller-controlled work and resource consumption.

Exercise the denial that would expose the flaw through the real enforcement path. Assert that the protected data or effect did not escape, alongside intended successful access. Report the verified boundary and remaining gaps.
