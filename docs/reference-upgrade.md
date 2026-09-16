# Reference-driven instruction refinement

Reviewed base: `4f5223a3e1a721b4af682e2da873e4cd3ae0d9de`.
This follows the [first audit](instruction-audit.md); it does not replace it or
claim that previously merged changes were made again. The runtime remains 16
independent skills, each containing only `SKILL.md` and `LICENSE`.

## Source decisions

| Reference | Adopted here | Not imported |
| --- | --- | --- |
| [Matt Pocock code review](https://github.com/mattpocock/skills/blob/959a8e9f1edc3adbe2f7e3054bb6fbefa6696260/skills/engineering/code-review/SKILL.md) | Separate requirements and standards judgments; grounded findings; independent review contexts when available | Mandatory issue-tracker setup, generic OO smell prescriptions, global router |
| [Matt Pocock TDD](https://github.com/mattpocock/skills/blob/959a8e9f1edc3adbe2f7e3054bb6fbefa6696260/skills/engineering/tdd/SKILL.md) | Observable slices, behavior-focused tests, independent expectations, meaningful failing controls | Approval before every test boundary, universal TDD, prohibition on independent committed-state reads |
| [Alibaba Open Code Review](https://github.com/alibaba/open-code-review/blob/f1101fd7f51304c82e4a4f292bbee88aea0823cf/README.md) | Deterministic inventories/checks; relevant context; verify findings against existing protections before reporting | An OCR dependency, its model configuration, benchmark claims, or a file-review CLI rebuilt inside skills |
| [OpenAI eval-skills](https://developers.openai.com/blog/eval-skills) | Natural tasks, negative controls, captured evidence, independent artifact checks, separate behavioral grading | A command mention or a successful formatter treated as behavioral success |
| [OpenAI rethinking skills](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) | Task-discriminating descriptions, contextual reading, explicit completion boundaries | Mandatory context tours, repeated full-suite checks, blanket assertions that users' environments are safe |
| [Anthropic context engineering](https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models) | Keep runtime guidance small; use concrete references and rubrics at the relevant boundary | Repeated system-level instructions or long compulsory recipes |

Sources were accessed on 2026-09-16. The supplied Alibaba URL had an extra Cyrillic
character; the verified repository is `alibaba/open-code-review`. The supplied
[X article](https://x.com/trq212/article/2080710971228918066) did not expose its body.
The official Anthropic article is supplementary reading, not a verified
transcription of that X article. No claims depend on unseen X content.

## Changes and falsifiable expectations

Descriptions now lead with the applicable action and Go decision instead of a
concept label. The concept still anchors each skill body. Expected benefit: less
ambiguous selection. This is a routing hypothesis until measured, not an observed
quality gain.

Standalone concurrency, HTTP, data, and integration skills now explicitly keep
review-only tasks read-only. Review guidance checks concrete synchronization,
mounted middleware, constraints/isolation, or deduplication before alleging a
missing guarantee. Existing review-capable specialists clarify their own evidence
boundary without depending on a shared review file. Expected benefit: fewer
unsolicited edits and unsupported findings. A clean review is a valid outcome;
do not invent a defect to fill a quota.

Implementation can progress in observable slices without imposing planning or
TDD on settled tasks. Testing makes the regression's intended failure explicit;
an unavailable dependency is not a successful negative control. These changes
retain nil/aliasing and error contracts, cancellation versus joining, mounted
versus transport evidence, transaction handles, and uncertain external effects.

The [executable evaluator](executable-evaluation.md) materializes five small
artifact cases. It deliberately does not call a model, grade prose by keywords,
replace real DB/RPC evidence with mocks, or declare an unexecuted routing case
passed. Maintainer evaluation files remain outside release archives and runtime
skill context. Packaging, versions, installation pins, and releases are unchanged.

## Review protocol for future iterations

Pin the base, candidate, affected files, requirements, and selected cases before
review. When the host actually supports subagents, give read-only reviewers
separate contexts and bounded scopes:

- Requirements/scope: missing requested outcomes, invented work, mode and completion conflicts.
- Go semantics/standards: concrete caller, ownership, transport, persistence, or trust-boundary failures; separate documented rules from preferences.
- Evaluation integrity: whether the test can reject the defect, conceal a contract difference, leak its oracle, or pass without executing the mechanism.

Each finding needs a file/line or exact passage, the violated contract, a
reachable failing condition, inspected counterevidence, and a minimal correction.
Unconfirmed conditions remain hypotheses. Keep requirements and standards results
separate; neither cancels the other. The integrating agent validates findings,
deduplicates the same cause, rejects unsupported preferences, and owns edits.
Reviewers do not all mutate the same checkout or rerun identical tests.

After a justified edit, recheck affected contracts and the nearest regression
risks. A prior check is reusable only for the same relevant content/environment.
Preselect a review budget. Stop when no supported material finding remains and
the applicable checks pass, or report the specific open blocker/evidence gap.
Repeated agreement, reviewer count, and exhausted budget are not proof of
perfection. Do not make this review protocol a required runtime skill sequence.

## Work performed in this session

All 16 skill texts and the existing distribution/evaluation contracts were read.
A text/scope pass identified the standalone review gaps. A separate evaluator
pass checked missing/skipped execution, source integrity, hidden grader exposure,
time/output limits, and meaningful positive/negative controls. These were
same-session manual passes, **not independent subagent reviews**: no subagent
execution facility was available. No model A/B runs, speedups, or cross-model
improvements are asserted. A proposed simplified G04 grader accepted an uncoordinated premature-completion
variant. It was rejected rather than shipped as proof of joining; G04 remains
in the broader specification plan. G08 supplies a deterministic ownership
control instead. The executable control results are recorded separately from
behavioral evaluation in the pull request.
