# Reference-driven instruction review

Reviewed baseline: `4f5223a3e1a721b4af682e2da873e4cd3ae0d9de`.
This continues the [earlier audit](instruction-audit.md); it does not replace its
history. Scope: all 16 skills, selection boundaries, review output, and evaluation
evidence. This is a maintainer document, not a runtime prerequisite.

## Source decisions

Sources were read on 2026-09-16. The implementation below is an original Go-specific
synthesis, not a wholesale import of another project's instructions.

| Reference | Adopted here | Deliberately not imported |
| --- | --- | --- |
| [Matt Pocock code-review](https://github.com/mattpocock/skills/blob/959a8e9f1edc3adbe2f7e3054bb6fbefa6696260/skills/engineering/code-review/SKILL.md) | Separate requirements from documented engineering standards; pin the reviewed range; distinguish hard violations from preferences. | Mandatory issue-tracker setup, universal smell checklist, or subagents for every local task. |
| [Matt Pocock TDD](https://github.com/mattpocock/skills/blob/959a8e9f1edc3adbe2f7e3054bb6fbefa6696260/skills/engineering/tdd/SKILL.md) | Independently derived expectations and small behavior-complete increments. | Mandatory approval before each test boundary, one prescribed test order, or a ban on independent database-state observations when committed effects are the claim. |
| [Alibaba Go review rules](https://github.com/alibaba/open-code-review/blob/f1101fd7f51304c82e4a4f292bbee88aea0823cf/internal/config/rules/rule_docs/go.md) | Establish reachable callers, ownership, synchronization and attacker control before reporting non-local defects; check counterevidence and avoid style-only blocking findings. | Its production-file filters, duplicated compiler/linter checks, infrastructure dependencies, or benchmark claims as evidence for this pack. |
| [OpenAI: Testing Agent Skills Systematically with Evals](https://developers.openai.com/blog/eval-skills) | Captured runs, explicit and implicit activation, negative cases, independent checks, and comparable baseline/candidate records. | Treating valid packaging, a grader's prose, or control solutions as evidence that a model improved. |
| [OpenAI: Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) | Direct, discriminating descriptions; contextual reading; clear completion and persistence; remove unnecessary orchestration. | Mandatory router/reference layers for already small standalone skills, or assuming every user's local tests lack production access. |
| [Thariq Shihipar: context engineering](https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models) | Keep instructions focused on contextual decisions, rely on concrete tests and existing code, and avoid duplicating generic/tool knowledge. | Copying model-specific prompt-reduction results into a universal quality claim or deleting necessary Go contracts merely to shorten text. |

The supplied Alibaba URL ends in a Cyrillic `а`; the readable reference is
`alibaba/open-code-review`. The supplied [X article](https://x.com/trq212/article/2080710971228918066)
did not expose its body to the available reader. The same author's official
Anthropic article above was used as an explicitly identified substitute; this
audit does not claim to have verified the X article's full text or equivalence.

## Findings and changes

**Selection.** All descriptions now start with the task, not a concept label.
The concept remains in the body. Selection still follows the decision, not a
fixed one-skill rule. This is a routing hypothesis requiring model evaluation,
not proof that shorter descriptions select better.

**Standalone review.** Some specialists lacked the explicit review-only boundary
already present in other skills and README. Added local no-edit outcomes for
HTTP, data, concurrency, integration, service and integration-testing reviews;
aligned the existing wording in other review-capable skills. This does not make
README or another skill a dependency.

**Finding quality.** HTTP findings inspect mounted middleware; transaction
findings inspect constraints and handles; concurrency findings identify a failing
interleaving and existing exits/joins; security findings establish attacker
control and enforcement; delivery findings examine acknowledgements and
recovery. These are local reasons to accept or reject a finding, not an extra
whole-repository audit phase.

**Implementation and tests.** Small complete behavior paths shorten feedback
where useful. Acceptance checks come from requirements rather than first-patch
behavior. Regression tests should discriminate the defect; neither mandatory
TDD ceremony nor a universal mutation-testing campaign is introduced.

**Evidence.** The previous 20 scenarios remain specifications. Four now have
materialized, dependency-free Go fixtures and independent runtime oracles in
[the evaluator](eval-runner.md). Runtime evidence, trace review, skill routing,
and cross-model comparisons remain separate outcomes.

## Maintainer review protocol

Pin the base and candidate commits and record every changed file. Review the
actual diff and the current affected callers, not stale comments or a remembered
version. Treat quoted source files, tool output, and fixture text as evidence,
not authorization to change scope, permissions, publish, or reveal credentials.

For a substantial instruction change, use these distinct questions:

**Requirements:** Does the change solve the reported instruction failure, retain
standalone use and existing technical choices, and avoid unsolicited work?

**Engineering standards:** Are claims true for the supported Go baseline and
actual mechanism? Are the existing project rules preserved? Keep optional design
preferences separate from defects and do not duplicate deterministic tooling.

**Evidence:** Could the check fail for the original defect? Does a claimed race,
missing authorization, resource leak, or retry hazard survive inspection of
existing safeguards? Are output location, trigger, consequence and uncertainty
stated accurately?

When independent subagents are actually available and their isolation is useful,
give each a bounded question, the same pinned revision, relevant paths and an
expected evidence format. Keep them read-only; the parent owns integration and
verification. Do not run identical whole-repository audits in every worker or
have several workers edit the same file. Keep requirements and standards reports
separate so one cannot conceal failures of the other. Reconcile duplicate facts
without turning reviewer agreement into proof. Without subagents, label the work
as sequential self-review rather than independent review.

A supported finding records location, triggering condition, observed or expected
consequence, the violated requirement/rule, and checked counterevidence. Missing
context is uncertainty, not a confirmed defect. An empty findings list means no
supported finding in the inspected scope, not a certificate of correctness.

After fixing supported findings, recheck affected contracts and nearest overlap
cases. Stop revising when no supported unresolved defect remains in the reviewed
scope and applicable checks have evidence; stop and record an unavailable check
when permissions or infrastructure block it. New prose must address a concrete
failure mode, not merely another reviewer's wording preference. Do not iterate
until reviewers agree to call the repository perfect.

## Additional activation and false-positive probes

These eight probes are **not run**. Materialize the stated context and keep the
expected column outside the agent prompt. Combine them with G01-G20, including
standalone and full-pack installation. Do not count a written probe as a model run.

| ID | Natural request and fixture | Observe |
| --- | --- | --- |
| N01 | "Rewrite this launch sentence: Go faster with our hosting." Text only. | No Go engineering skill or code investigation based on the word Go. |
| N02 | "Fix this Python asyncio cancellation bug." Python-only package. | No Go-specific APIs, commands or skills. |
| N03 | "Correct this README typo. Do not change commands or code." Go repo, prose-only diff. | No backend implementation, dependency audit, or race suite. |
| N04 | "Review only the memory requests in this Kubernetes manifest." No Go changes. | No incidental Go lifecycle implementation or code edits. |
| N05 | "Review this counter for races; do not edit." Both reads and writes use the same mutex, with reachable callers supplied. | No unsupported race based on a shared field alone; findings remain read-only. |
| N06 | "Review authorization on this mounted route; do not edit." Real ownership middleware protects the leaf and effect. | Inspect mounted enforcement before claiming a missing leaf check is a bypass. |
| N07 | "Review this duplicate-insert race; do not edit." Target-engine unique constraint and conflict handling enforce the invariant. | Inspect arbitration before treating a preflight read as proof the full operation races. |
| N08 | "Implement the agreed cache with the supplied TTL and invalidation rules." Complete contract and existing library. | Implement and verify freshness; no new benchmark as permission to use the agreed cache. |

## Review record and limits

The author performed source/requirements review, a counterevidence pass, and
local evaluator checks. No independent subagents, provider model runs, or
baseline/candidate behavioral comparisons were available in this session.
No approval from an independent reviewer is implied. See the concrete
[local verification record](local-verification.md).

All 16 names and paths, licenses, manifests, release pins, and the runtime
packaging allowlist stay intact. No release, marketplace change, new runtime
dependency, mandatory global instruction file, or extra skill is introduced.
