# Go instruction audit and candidate changes

Reviewed base: `48be5eb558e81a2892cca47ebe9c9466dd92be1f`.
Scope: all 16 SKILL.md files, README, canonical/native metadata, submission
examples, versioning/distribution documentation, and the existing checks and
packaging contract. This is a text/structure audit; inferred agent failure modes
are hypotheses, not observed model failures. Behavioral comparisons are not run.

## Interpretation

The [OpenAI article](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra)
supports discriminating descriptions, contextual reading, and explicit completion
boundaries instead of accumulated compulsory process. The Go pack already has
compact independent skills and no compulsory global AGENTS.md/CLAUDE.md layer.
Do not add a router skill, shared mandatory file, or extra roles merely to apply
the article. Do not assume any user's local tests have no production access.

Keep the technical distinctions that make these skills useful: nil and aliasing,
intentional error identity, ownership and joining, real middleware/interceptor
paths, transport versus in-process tests, and database transaction handles.
The changes scope those judgments; they do not replace them with slogans or
weaker checks. Shorter text or fewer commands is not itself a quality result.

## Findings and implemented decisions

| Skill | Finding in the reviewed text | Candidate change |
| --- | --- | --- |
| go-implement | Clear-task execution exists, but completion does not explicitly cover repairing introduced failures; overlap with broad idiomatic trigger. | More discriminating description, proportional reuse search, applicable build/tests, continuation through fixes, explicit stopping boundary. |
| go-idiomatic | Writing any Go function can match; finishing presumes edited/formatted code even for review. | Focus on representation/error/collection decisions; review reports rather than edits; retain nil, shallow copy, error and receiver contracts. |
| go-design | Strong consumer-interface guidance; finish presumes a changed responsibility. | Distinguish analysis from refactoring, without making design mandatory for settled implementation. |
| go-concurrency | Strong cancellation/join and exercised-race distinctions. | Restrict ownership trace to affected work and observe bounded termination separately from supported race checks. |
| go-debugging | Initial source list and unconditional fixing can overrun diagnosis requests. | Hypothesis-led inspection and distinct diagnosis/fix outcomes. |
| go-performance | Default path presumes measurement and intervention, including service load. | Separate audit, measurement, isolated benchmark, and service-level optimization; retain B.Loop baseline, benchstat and anti-fishing guidance. |
| go-build | Initial inventory includes every build concern. | Inspect the implicated layer; distinguish workspace-only changes from a standalone-consumer claim; preserve checksum/toolchain facts. |
| go-service | Lifecycle material can be read as universal work for a local wiring change. | Conditional configuration/startup/shutdown paths and evidence; preserve partial-failure cleanup and drain ordering. |
| go-http | Testing boundary can be made more precise than just direct calls versus a server. | Mounted chain plus ResponseRecorder for in-process routing/middleware; actual network for network claims. |
| go-grpc | Review is in the trigger but final instructions require tests and graceful-drain work unconditionally. | Distinct review result, schema checks versus RPC checks, and draining only for shutdown changes; retain stream termination and generated-code constraints. |
| go-data | Pure mapping is routed through an atomicity-first introduction and real-transaction finish. | Separate mapping, query, transaction and migration claims; real engine when the claim needs it, not for pure value conversion. |
| go-security | Strong enforcement/effect test; breadth may invite unrelated boundary audits. | Scope to affected trust boundary; distinguish fabricated identity from credential verification and review from editing. |
| go-integrations | Interruption/dependency proof can overrun pure key/policy work. | Verify changed delivery or freshness property; retain bounded response cleanup, uncertainty, and explicitly agreed cache scope. |
| go-observability | Useful narrow operational goal but broad probes/lifecycle material. | Conditional probe, diagnostic and shutdown checks; ordinary signal edits remain local. |
| go-testing | Good test-discrimination/worker rules; fuzz/race wording can imply a campaign for routine tests. | Match test technique to the claim, bound fuzzing, preserve required gates, reuse applicable evidence and distinguish unavailable checks. |
| go-integration-testing | Opening setup can imply infrastructure for every composition test. | Conditional real infrastructure, precise mounted HTTP/in-process RPC/network boundaries, honest unavailable evidence and no invented completion harness. |

## Package and evaluation

README explains decision-based selection and composition without an invocation
sequence or skill-count cap. Standalone skills retain their own useful boundaries.
Canonical plugin metadata prepares 1.0.1 and supplies Go-specific starter prompts;
the two native manifests remain derived views. Published install examples stay
on v1.0.0. No tag, marketplace change, release publication, dependency update, or
application-code change is included.

The existing validator permits SKILL.md and LICENSE only inside each skill.
Keep that contract and the installation/packaging scripts unchanged; additional
references are not justified by current size. The release archive excludes
authoring docs/scripts/CI, so this document and evaluation materials are not
runtime prerequisites.

The original five positive and three negative submission scenarios are retained.
They do not cover implicit routing or most Go-specific boundaries. Add
[20 natural-request cases](behavioral-evaluation.md), a no-pack/prior/candidate
comparison protocol, and an explicitly unfilled [result record](evaluation-results.md).
Workspace fixtures must be materialized and pinned before execution; these files
are specifications, not an evaluation runner or measured results.

1.0.1 is a PATCH correction within the existing domains, not a claim that
activation changes are cosmetic. Names, paths, independent use, licenses, and
required environments remain unchanged. Review behavioral evidence before release.

## Technical references checked

These are rationale sources for maintainers, not required agent reading before
every edit. Use the target project's versions when applying library APIs.

- [context](https://pkg.go.dev/context): cancellation signals do not wait for work to stop.
- [Race detector](https://go.dev/doc/articles/race_detector): detects races on executed paths, not a universal correctness proof.
- [httptest](https://pkg.go.dev/net/http/httptest): recorder and real-server tools support different evidence boundaries.
- [testing/synctest](https://pkg.go.dev/testing/synctest): self-contained concurrency testing has a version and I/O scope.
- [Go transactions](https://go.dev/doc/database/execute-transactions): transaction operations must not accidentally use non-transaction DB methods.
- [gRPC Go](https://grpc.io/docs/languages/go/basics/): generated services, client/server calls, and stream outcome handling.
- [gRPC graceful shutdown](https://grpc.io/docs/guides/server-graceful-stop/): bounded graceful shutdown and forceful fallback are lifecycle concerns.

Distribution validation confirms packaging, not these behavioral outcomes. No
universal acceleration or model-quality claim is made by this audit.
