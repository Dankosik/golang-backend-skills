# Reference adoption and review boundaries

Reviewed base: `4f5223a3e1a721b4af682e2da873e4cd3ae0d9de`.
Date: 2026-09-16. This follows the [earlier instruction audit](instruction-audit.md).
Scope: all 16 skills, activation descriptions, review/implementation boundaries,
maintainer evaluation material, and the existing distribution contract.

This is a source-grounded authoring review plus deterministic fixture validation.
Independent subagents and model A/B runs were not available or executed during this
change. Separate review perspectives below describe a reusable protocol, not a claim
that parallel agents endorsed this revision. Inferred model failure modes remain
hypotheses until observed in actual traces.

## Sources and selective adoption

### OpenAI: evaluation

[Testing Agent Skills Systematically with Evals](https://developers.openai.com/blog/eval-skills)
was read directly. Adopt task-level outcome checks, explicit and natural invocation
cases, negative controls, captured traces and artifacts, independent graders, and
separate correctness/process/efficiency observations. The new kit materializes six
small Go fixtures and validates that their graders reject known defects and accept
reference corrections. A passing structural check, grader self-test, or prose rubric
is not a passing model comparison.

### OpenAI: instruction scope

[Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra)
was read directly. Shorten all 16 descriptions to discriminating work; retain the
engineering concepts in the bodies rather than spending discovery context on labels.
Preserve contextual reading, settled project choices, permissions, and completion
through relevant checks and repair. Do not add an unconditional whole-repository read,
new ceremony, or a stop after the first patch.

The existing single-purpose files are already compact and independently installed.
Progressive disclosure does not justify a router or a shared mandatory reference
library here. Keep authoring and evaluation docs outside runtime skills. Do not copy
an assertion that an arbitrary user's local tests have no production access.

### Matt Pocock: decisions, review axes, and behavioral slices

Reviewed [code-review](https://github.com/mattpocock/skills/blob/959a8e9f1edc3adbe2f7e3054bb6fbefa6696260/skills/engineering/code-review/SKILL.md),
[tdd](https://github.com/mattpocock/skills/blob/959a8e9f1edc3adbe2f7e3054bb6fbefa6696260/skills/engineering/tdd/SKILL.md),
and [repository guidance](https://github.com/mattpocock/skills/blob/959a8e9f1edc3adbe2f7e3054bb6fbefa6696260/CLAUDE.md)
at commit `959a8e9f1edc3adbe2f7e3054bb6fbefa6696260`.

Adopt separate specification and standards judgments: satisfying one does not erase
a failure on the other. Keep documented rules distinct from design heuristics, locate
the relevant source and diff, and make findings specific. For multi-part implementation
and requested test-first work, prefer small verifiable behavior slices and independent
expected values instead of speculative layers or tautological tests.

Do not import the entire router/setup/issue-tracker workflow, mandatory approval of
every test boundary, a fixed number of reviewers, or generic object-oriented smell
remedies. Go package and consumer-interface decisions remain contextual. Independent
database reads are valid evidence for committed state; a blanket prohibition on such
observations would weaken this pack's transaction tests. Test-first is not mandated
for every unrelated task, and behavior-preserving refactoring is not categorically banned.

### Alibaba: deterministic coverage and verified findings

Reviewed the [Open Code Review README](https://github.com/alibaba/open-code-review/blob/f1101fd7f51304c82e4a4f292bbee88aea0823cf/README.md)
and repository search at commit `f1101fd7f51304c82e4a4f292bbee88aea0823cf`.
The supplied repository link had a trailing Cyrillic character; the canonical
repository is `alibaba/open-code-review`.

Adopt the separation of deterministic responsibilities from judgment: maintain an
explicit coverage inventory, validate fixtures and test execution mechanically, and
use contextual review to assess real failures. Review findings need the affected path,
trigger, consequence, and existing guards. Look for a middleware guard, transaction
constraint, worker join, or idempotency guarantee before declaring it absent. Treat
related reports of the same cause as one finding; do not impose a finding quota.

Do not add this external CLI, provider setup, bundled rule engine, or benchmark claims
to an instruction-only Go pack. A prompt cannot guarantee the hard coverage or line
positioning properties of a dedicated tool. Our runner covers a small deterministic
grading boundary, not Alibaba's entire review architecture.

### X article: unavailable

[The supplied X article](https://x.com/trq212/article/2080710971228918066) did not expose
its article body through the available reader. No recommendation or quantitative
claim is attributed to its unread contents, and third-party summaries were not used
as a substitute. Incorporation of that specific reference remains unverified.

## Reusable reviewer briefs

These are optional maintainer briefs for a host that actually supports subagents.
They are not loaded by the 16 skills and do not create a new required runtime process.
Give each reviewer the same pinned base/candidate, requested scope, relevant evidence,
and actual permissions. Start with isolated reviews, without other reviewers' opinions.

| Perspective | Question and required evidence |
| --- | --- |
| Specification | Which requested outcomes are missing, incorrect, or expanded without authorization? Cite the requirement and affected instruction or patch. |
| Instruction design | Do descriptions discriminate nearby tasks? Does standalone use still work? Identify exact wording that broadens scope, duplicates mandatory work, or stops authorized implementation early. |
| Go semantics and evidence | Which caller-visible invariant could fail? Name the triggering value, schedule, boundary, or version, inspect existing protection, and identify the smallest discriminating check. |
| Evaluation integrity | Could the test pass without exercising the defect? Check seeded failure, reference success, hidden-grader isolation, observed execution, skips, clean teardown, and unsupported final claims. |

For each actionable finding record location, requirement or invariant, trigger,
consequence, evidence, and uncertainty. A stylistic preference is not a defect.
Separate specification failures from standards violations and from hypotheses.
Do not duplicate findings already settled by applicable deterministic tooling.

The maintainer verifies each candidate finding against the actual files and rejects
false positives with a concrete reason. Apply the smallest supported correction and
rerun only checks whose inputs or claims changed. On later review passes, focus on
unresolved findings and regressions introduced by the correction rather than forcing
another full read or identical test sweep.

Stop when the requested scope is covered, verified material findings are addressed,
applicable gates pass, and remaining gaps are explicitly recorded. Do not rewrite
until reviewers run out of opinions, or treat unanimous approval as proof of
perfection. A model-quality claim additionally needs the recorded paired runs in the
[evaluation protocol](behavioral-evaluation.md); no such claim is made by this change.

## Preserved contracts

The pack remains 16 independent `SKILL.md` files with their existing names, paths,
licenses, Go-domain distinctions, and native manifests. No shared runtime file,
application framework, infrastructure dependency, model-specific API recipe, release,
tag, or marketplace change is introduced. Existing authoring checks discover the new
Python tests; executing Go fixtures is explicit and is not a new mandatory user-project
completion gate. See the [evaluation kit](../evals/README.md) for coverage and limits.
