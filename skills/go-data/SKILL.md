---
name: go-data
description: "Atomicity. Use when Go database queries, transactions, migrations, or data mappings affect persistence, consistency, concurrency, or access cost."
---

# Go Data

**Atomicity.** Identify the invariant that must survive competing requests or partial failure. Honor supplied requirements and settled technical choices; resolve only what the task leaves open.

Follow the operation through the project's actual driver, generated queries, or ORM. Identify the transaction handle, connection lifetime, and commit boundary. All participating work must use that handle and finish before it is released; a call through the shared pool can escape the transaction.

Keep rollback and resource release explicit on failure. Use the driver's actual cancellation semantics rather than assuming request cancellation ends a transaction. Observe row iteration errors and close rows and other owned resources. Reuse application-owned pools instead of creating one per operation.

Use constraints, conditional writes, or locks where the invariant needs arbitration. A preflight read cannot settle a race. Distinguish known rejection or rollback from an uncertain commit before retrying. An external effect cannot be undone by a database rollback.

Work backward from the required result to a bounded query and fetch plan. Parameterize values and constrain dynamic identifiers. Keep nulls, large integers, decimals, and time semantics honest across database and Go types. Use the existing migration owner and inspect generated SQL where query behavior matters.

Verify the claimed database property against the relevant engine and real transactions, observing committed state independently. Mocks can test orchestration but cannot establish constraints, isolation, or locking.
