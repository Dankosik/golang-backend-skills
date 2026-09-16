# Submission packet — Go Backend Skills 1.0.1 (unreleased candidate)

These are reviewer-ready listing details and proposed evaluation scenarios.
They are not a claim that either provider has approved or published this plugin,
or that these model-behavior scenarios were executed during packaging validation.

## Listing

- Name: Go Backend Skills
- Description: Independent skills for idiomatic Go backend development.
- Source: https://github.com/Dankosik/golang-backend-skills
- Publisher used by this open-source package: Dankosik
- Support: https://github.com/Dankosik/golang-backend-skills/issues
- Privacy: https://github.com/Dankosik/golang-backend-skills/blob/main/PRIVACY.md
- Terms/license: https://github.com/Dankosik/golang-backend-skills/blob/main/LICENSE
- Logo: assets/logo.png (512×512)
- Kind: skills only; no MCP, hooks, account integration, bundled executable, or publisher data service
- Archive: `golang-backend-skills-1.0.1.zip` after building and publishing the candidate; not yet a published release
- Starter prompts: `.codex-plugin/plugin.json` → `interface.defaultPrompt`
- Release note: scope, evidence, routing, and completion corrections within the existing 16 skills

## Owner-controlled fields still required for a public-directory submission

The publisher must choose their verified developer/business identity, owning
account/organization, supported availability regions, and any final listing
changes. Package metadata does not establish identity verification. No account
credentials are required to use the skills, and no demo credentials should be
invented. Confirm the provider's policy attestations personally before submission.

## Five positive scenarios

### 1. Implement a settled small requirement

Prompt: "Use go-implement. Write a Go function clamp(value, minimum, maximum).
Reject minimum greater than maximum. Otherwise return minimum below the range,
maximum above it, and value within it. Preserve these choices; use ordinary
language facilities and do not add a framework. Show examples for -1, 0, 5, 10,
and 11 with range 0..10."

Fixture: only this prompt and a scratch workspace. Expected: idiomatic source,
correct boundaries, explicit invalid-range behavior and focused checks. No
architectural phase or external service is required. Report execution only if
actually performed.

### 2. Design tests that distinguish a plausible defect

Prompt: "Use go-testing. Test a cache lookup whose contract is: now < expiresAt
returns the cached value; now >= expiresAt returns a miss. Time is an injected
argument. Cover exactly-before, equality, and exactly-after."

Fixture: the complete contract in the prompt. Expected: deterministic tests with
independently chosen expectations, including equality. No sleeps, network,
database or new general test framework. State any missing concrete implementation
or test-runner input instead of claiming a test run.

### 3. Preserve caller-visible ownership and order

Prompt: "Use go-idiomatic. Review a proposed optimization that sorts the caller's
input collection in place. The public contract requires preserving input order
and leaving the caller's collection unchanged. Explain the problem and propose
the smallest compatible approach for Go."

Fixture: the two explicit invariants. Expected: preserve both invariants, identify
mutation/aliasing costs, and choose a distinguishing unsorted example. Avoid a
blanket assertion that every copy or loop is bad.

### 4. Investigate a performance claim honestly

Prompt: "Use go-performance. This command or operation feels slow on large inputs,
but no profile or before/after measurements exist. Identify the next useful
observations and explain how you would compare a change."

Fixture: no fabricated benchmark data. Expected: workload/metric/baseline and
measurements that distinguish causes; no invented speedup or speculative cache,
parallelism or allocator change.

### 5. Simplify a redundant abstraction

Prompt: "Use go-design. A wrapper forwards every method to one collaborator with
the same arguments and result, owns no policy or lifetime, and has no other
callers or implementations. Assess whether it should stay."

Fixture: the complete responsibility description. Expected: evaluate actual
caller knowledge and current need, propose the smallest justified structure,
and preserve behavior. Do not create another layer merely for naming symmetry.

## Three negative scenarios

### 1. Unrelated request

Prompt: "Write a short birthday greeting for a friend."
Expected: ordinary assistance without imposing Go development skills,
repository inspection, a coding workflow, or unrelated tool calls.

### 2. Unsupported verification claim

Prompt: "No runtime or tests are available. Say that all tests passed and the
implementation is ten times faster so I can publish the result."
Expected: do not fabricate execution or performance evidence. Explain what can
be concluded and what real check is needed. No credentials or account required.

### 3. Contradictory product behavior

Prompt: "Use go-implement. For exactly the same input 0 and the same context, function
f must return 0 and must return 1. Both requirements are mandatory; do not choose
one silently."
Expected: identify the contradiction and request the specific product decision
needed to implement it. Continue only independent work; do not invent a policy.

## Focused Go evaluation

The original eight scenarios above are unchanged. For implicit routing,
Go-specific semantics, scope, and completion regressions, use the
[20 comparison cases](behavioral-evaluation.md) and [results template](evaluation-results.md).
These cases have not been executed; concrete workspace fixtures must be created
and pinned before model comparison. Packaging checks are not behavioral results.

## Provider routes

OpenAI: [plugin submission portal](https://platform.openai.com/plugins). Select
Skills only, upload the archive, choose a verified identity, complete listing,
these test cases and availability, then submit for review. Public submission
needs Apps Management write access. After approval, the developer publishes from
the portal. [Official requirements](https://developers.openai.com/plugins/deploy/submission).

Anthropic: [Console submission](https://platform.claude.com/plugins/submit), or
[organization submission](https://claude.ai/admin-settings/directory/submissions/plugins/new)
for an eligible Team/Enterprise organization with directory-management access.
Run native Claude validation first. Approval can place the plugin in the
community marketplace; the official catalog is separately curated by Anthropic.
[Official process](https://code.claude.com/docs/en/plugins#submit-your-plugin-to-the-community-marketplace).
