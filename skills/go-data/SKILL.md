---
name: go-data
description: "Implement or review Go query shape, database-value mapping, transactions, and migration compatibility."
---

# Go Data

**Atomicity.** Identify the property being changed: query shape, Go value conversion, transaction consistency, or schema compatibility. For competing requests or partial failure, state the invariant that must survive. Honor requirements and preserve settled choices outside the requested change.

For transactional work, follow the actual driver, generated queries, or ORM. Identify the transaction handle, connection lifetime, and commit boundary. All participating work must use that handle and finish before release; a call through the shared pool can escape the transaction.

Keep rollback and resource release explicit on failure. Use the driver's actual cancellation semantics rather than assuming request cancellation ends a transaction. Observe row iteration errors and close rows and other owned resources. Reuse application-owned pools instead of creating one per operation.

Use constraints, conditional writes, or locks where an invariant needs arbitration. A preflight read cannot settle a race. Distinguish known rejection or rollback from an uncertain commit before retrying. An external effect cannot be undone by a database rollback.

For queries and mappings, work backward from the required result to a bounded fetch plan. Parameterize values and constrain dynamic identifiers. Preserve nulls, large integers, decimals, and time semantics across database and Go types; inspect generated SQL when query behavior matters. For migrations, use the existing schema owner and consider application versions that must coexist.

Test pure conversion with representative driver values; do not invent a database harness for a mapping-only claim. Query execution, constraints, isolation, and locking need the relevant engine and real mechanism; observe committed state independently when commitment or visibility is the claim. Mocks can test orchestration, not those database properties. Report unavailable evidence without claiming a weaker check proves it.

For review-only work, do not edit files. Tie each finding to the query or transaction path and a concrete invariant violation; check existing constraints and isolation before claiming a race.
