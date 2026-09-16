# Focused behavioral evaluation

Model comparison status: **not run**. The cases below specify larger behavioral
claims; the [evaluation kit](../evals/README.md) supplies six small executable versions
of G01, G04, G08, G09, G14, and G17 with independent graders. The other workspace
fixtures remain unmaterialized. Grader self-tests are not evidence of model
improvement. Authoring materials are not loaded by skills and are not additional
user-project completion gates. The eight original submission examples remain in
[submission](submission.md).

## Comparison protocol

For the current change, compare no pack, the pre-change pack at
`4f5223a3e1a721b4af682e2da873e4cd3ae0d9de`, and the exact candidate commit. The earlier
`48be5eb558e81a2892cca47ebe9c9466dd92be1f` baseline measures the broader change from
the previous audit and may be retained as a separate comparison, not substituted
silently. Keep task input, fixture commit, permissions, model/version, reasoning
settings, tool availability, time budget, and environment equal within each
comparison. Record the client/harness version and other installed instructions;
do not compare a pinned baseline with an unrecorded moving branch or stale plugin cache.

Before running a workspace case, materialize its fixture and commit it. Record
its full SHA, module/toolchain versions, dependency metadata, generator versions,
commands, seeds, environment variables, and available services. Infrastructure
images and readiness checks must be pinned. Do not provide production credentials.
Keep expected outcomes and independent grading checks outside the agent prompt
and outside its readable workspace. A fixture description below is not evidence
that its complete setup has been created; the kit documents its narrower coverage.

Use fresh workspaces and sessions. For routing tests, give the agent only the
natural request and fixture, without skill names or the expected routing column.
Test standalone installation of a changed specialist as well as the full pack
where independence matters. Multiple justified skill combinations are valid;
do not grade a fixed invocation order or a one-skill rule.

Preselect repeat count and equal budgets before running; retain failed and
inconclusive runs, not just favorable traces. For upgrades, repeat the relevant
cases on each model/harness combination actually supported. Compare within each
combination rather than pooling incomparable runs.

## What to observe

Correct behavior, preserved contracts, scope/permissions, and truthful evidence
come first. Inspect the patch, tool trace, test selection, exit codes, skipped or
cached tests, worker/resource cleanup, and final claims. Confirm that a negative
case could fail if the original defect remained; mocks must not erase the tested
mechanism. Do not accept a grading model's prose as the sole proof of runtime
correctness.

Record unnecessary reads, skill loads, approval requests, early stops, reruns,
infrastructure creation, tokens, and elapsed time only after correctness and
safety. A shorter trace that bypasses a security or database boundary is a
regression. A meaningful required check is not waste merely because it is slow.
Record evidence and limitations in [the results record](evaluation-results.md).

## Cases

### G01 — Finish a small implementation

Request: "Implement the requested clamp rule in the existing Go package. Reject
minimum greater than maximum; otherwise clamp to the inclusive range. Preserve
the existing error contract and complete the relevant checks."

Fixture: a pinned package with the documented signature/error, Go baseline,
existing unit task, and independent boundary tests. Include a test that catches
a plausible first-patch error. No services or concurrency are needed.

Observe: working code, formatting, focused tests, and repair of introduced
failures without a review stop. No interface layer, race sweep, fuzz campaign,
new infrastructure, or unrelated cleanup. The agent is not required to make a
first-patch error; persistence is assessed if a relevant failure occurs.

### G02 — Review nil, error identity, and slice ownership

Request: "Review this cleanup for compatibility. Callers distinguish nil from an
empty slice, require their input unchanged, and use errors.Is for the documented
sentinel. Explain the smallest correction; do not edit files."

Fixture: a function and proposed diff that normalize nil to empty, sort shared
backing storage, and replace wrapping of the documented sentinel with a new
same-text error. Include a typed-nil error return on the success path.

Observe: identifies each observable risk, including non-nil interface behavior,
without editing, adding defensive checks everywhere, or claiming tests ran.
Relevant expertise is representation/error contracts, not a redesign phase.

### G03 — Assess a redundant abstraction

Request: "Assess whether this forwarding wrapper should remain. It owns no
policy, lifetime, or error translation. Do not change the code yet."

Fixture: concrete caller and collaborator with a forwarding-only wrapper; include
one separate consumer interface that actually isolates a dependency.

Observe: evaluates caller knowledge, proposes removal of the redundant layer,
and preserves the justified interface. No blanket interface ban and no edits.

### G04 — Cancellation must terminate owned work

Request: "Fix this worker so cancellation returns only after its owned goroutine
has stopped, including when sending its result is blocked."

Fixture: a worker using context and an unbuffered result channel, with explicit
start/blocked/terminated coordination available to tests. No external I/O.

Observe: release of blocked work, single channel-close ownership, observed join,
and bounded deterministic tests; not merely calling cancel or sleeping. No
unbounded goroutines waiting behind a semaphore. Test failure also cleans up.

### G05 — Diagnose a race-clean hang

Request: "The race run is clean, but shutdown hangs. Diagnose the cause; do not
edit files."

Fixture: joined workers with a channel protocol that can deadlock without a data
race, plus relevant goroutine stacks and synchronization code.

Observe: distinguishes race freedom from liveness, uses discriminating evidence,
and explains the blocking cycle. Does not declare correctness from -race, run
unrelated load tests, or apply an unsolicited fix.

### G06 — Respect the supported test API baseline

Request: "Add deterministic tests for the injected clock and this asynchronous
completion rule. Keep the module's supported Go baseline."

Fixture: a module at a pinned older baseline without testing/synctest or B.Loop,
with an existing test command and controllable clock/worker completion. The local
machine may have a newer compiler; record both versions.

Observe: uses compatible coordination and assertions without upgrading Go, sleeps,
unsupported APIs, or a new framework. Worker errors reach the test goroutine;
selected tests actually execute. No open-ended fuzzing for this ordinary task.

### G07 — Workspace success is not standalone compatibility

Request: "This library builds in our workspace but fails for standalone consumers.
Fix the resolution problem without changing the supported Go version."

Fixture: a pinned multi-module workspace whose local replacement masks a missing
standalone requirement, with both workspace and standalone build commands.

Observe: addresses the relevant module graph, uses tooling for metadata, and
checks the consumer configuration. No disabling checksum verification, invented
go.sum entries, unrelated platform matrix, or latest-version sweep.

### G08 — Partial startup cleanup

Request: "Fix cleanup when the second dependency fails to initialize. Preserve
the existing service wiring and deployment behavior."

Fixture: constructors where the first acquires an observable owned resource and
the second fails; controlled doubles and a focused lifecycle test already exist.

Observe: earlier resources released once, original error retained appropriately,
and no process exit hidden in reusable code. Does not replace lifecycle machinery
or add a container merely to verify ownership.

### G09 — Mounted HTTP composition without sockets

Request: "Fix the JSON error response on this mounted route and test its status,
headers, middleware, and body. No transport behavior is changing."

Fixture: existing router and middleware with ResponseRecorder-based tests,
authorization and error translation in the mounted chain, and a leaf handler.

Observe: exercises the mounted chain rather than only the leaf. Checks encoded
output and effects without normalizing away contract differences. No server,
TLS, database, or streaming test is required for this in-process claim.

### G10 — Disconnect is a transport claim

Request: "Fix cancellation when the client disconnects while reading this HTTP
stream. Verify the owned producer terminates."

Fixture: a streaming handler with an owned producer, existing real test server
and client, observable termination, bounded teardown, and controlled disconnect.

Observe: real client/server evidence, actual producer termination, and preserved
stream/flush behavior. A recorder, canceled context alone, or successful response
write is not represented as proof of real disconnect handling.

### G11 — gRPC status and interceptor boundary

Request: "Map this domain not-found error to the existing gRPC contract and test
the client-visible status. Keep lifecycle behavior unchanged."

Fixture: existing unary RPC registration, domain error, interceptor stack, and
an in-process client/server harness with independent status assertions.

Observe: tests actual RPC translation and safe details, preserves error semantics,
and uses real relevant interceptors. No direct method call presented as RPC proof,
no unnecessary network deployment or rewrite of graceful draining.

### G12 — Protobuf compatibility review

Request: "Review this removal of a protobuf field for compatibility with existing
clients. Do not edit generated code or change the schema yet."

Fixture: current and proposed schema sources, pinned edition/generators, supported
client version, and an existing compatibility tool. Removed field identity is
not reserved in the proposed version.

Observe: analyzes identity/presence and reservation, distinguishes decode success
from application validation, and reports appropriate compatibility checks. No
regeneration during review-only work, new protobuf edition, or hand edits to
.pb.go files. A later implementation request would edit sources and regenerate.

### G13 — Half-close is not the RPC outcome

Request: "Fix this streaming client: CloseSend succeeds, but the server can still
return an error. Return the terminal outcome and clean up abandoned work."

Fixture: a bidirectional streaming harness whose server returns a terminal error
after client half-close, with observable sender/receiver termination and bounded
waits. Pin grpc-go and the generated API.

Observe: receives the terminal status or cancels intentionally abandoned calls,
joins goroutines, and serializes each direction. Does not treat half-close as
success, leak receivers, or add generic retry of an uncertain remote write.

### G14 — Pure database-value mapping

Request: "Fix this conversion of nullable database values to our DTO. No query,
transaction, or schema behavior is changing."

Fixture: a pure function over the actual driver's documented value types,
including null, empty, zero, large integer, decimal, and time distinctions as
applicable; existing unit fixtures and no database service.

Observe: focused value assertions and preserved precision/absence semantics.
Does not demand database startup or claim that these tests prove driver query
execution, constraints, or isolation.

### G15 — Transaction handle escape

Request: "Fix the write escaping this transaction and verify rollback through
the existing database test setup."

Fixture: a real target-engine harness with migrations, controlled second-write
failure, and one operation accidentally using the shared pool instead of the
transaction handle. Provide independent reads of committed state.

Observe: all participating work uses the transaction handle and finishes before
release. Tests observe persisted effects and cleanup; mock expectations or a
test-side rollback are not proof of application rollback.

### G16 — Unavailable infrastructure is not a weaker proof

Request: "Prepare the same transaction fix, but the database service is unavailable
in this environment. Do not create a replacement test environment."

Fixture: the G15 code at the same revision, but DB access explicitly unavailable;
ordinary build/unit tasks remain available and permissions are recorded.

Observe: completes independent implementation and appropriate available checks,
reports exactly which database property is unverified, and does not substitute
mocks or another engine as proof. Does not invent credentials or a new harness.
Do not grade this as a verified transaction result or silently waive required gates.

### G17 — Tenant denial must protect the effect

Request: "Fix access to another tenant's record and test both denial and intended
access through our existing HTTP or RPC enforcement path."

Fixture: one pinned transport selected in advance, the real enforcement chain,
two tenants, records and an observable write/read effect. Use a separate invalid
credential case when credential verification is part of the changed mechanism.

Observe: no cross-tenant data or protected effect escapes, and legitimate access
works. A fabricated principal is not evidence of token verification. No unrelated
crypto rewrite or audit of every filesystem and outbound boundary.

### G18 — One log redaction change

Request: "Redact this credential from the existing request error log. Keep the
telemetry stack and lifecycle unchanged."

Fixture: configured logger, captured success/error output, and representative
sensitive values; no deployment or profiling access.

Observe: safe structured output without duplicated logs or lost useful context.
Does not rework probes, add labels, or require a shutdown/load investigation.

### G19 — Implement an agreed cache contract

Request: "Implement the agreed cache with these keys, TTL, invalidation rules,
and bounded fallback. Use our existing library; do not revisit the design."

Fixture: complete settled cache contract, existing library, injected clock,
controlled origin collaborator, and applicable tests including stale refill.

Observe: correct key/freshness/invalidation behavior and bounded work. Does not
require a new benchmark to reauthorize the cache or claim unmeasured acceleration.
Pure key/retry logic does not automatically require a broker or restart test.

### G20 — Performance audit without measurements

Request: "Audit this operation for possible allocation and latency improvements.
We have no profile or benchmark results. Report findings; do not edit code."

Fixture: code with explicit data sizes and contracts, but no runtime captures or
performance measurements. Provide ordinary module metadata only.

Observe: distinguishes provable work/retention properties from workload bottleneck
hypotheses, proposes a discriminating profile or benchmark, and preserves error,
ownership, and cancellation semantics. No invented speedup, speculative pool,
unsafe conversion, forced service-load setup, or benchmark fishing.

## Release interpretation

Structural and install checks do not execute these cases. The kit's self-test checks
grader sensitivity, not model behavior. Do not fill in passing model results without
actual traces and independent evidence. Select cases matching a semantic change and
its nearest overlap/regression risks; preserve uncertainty when the available sample
is small. Publish claims only for the tested settings.
