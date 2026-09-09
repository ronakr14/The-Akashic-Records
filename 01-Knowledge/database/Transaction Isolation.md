---
domain: database
subdomain: transactions
note_type: concept
source_type: self
status: draft
level: advanced
---
# AI Summary

DRAFT — scaffold only. Synthesis pending. ACID, the SQL isolation levels, the anomalies each permits, and how MVCC implements them.

---

## ACID

- Atomicity, consistency, isolation, durability — what each actually guarantees
- Where "consistency" is the application's job, not the DB's

## Isolation levels

- Read uncommitted / read committed / repeatable read / serializable
- Anomalies: dirty read, non-repeatable read, phantom, write skew, lost update
- Which level blocks which anomaly (the standard table)

## Implementation

- Lock-based vs MVCC (snapshot isolation)
- Postgres/Oracle snapshot model; serializable snapshot isolation (SSI)
- Read/write conflict detection, first-committer-wins

## Practical

- Default level per engine; when to raise it
- Long transactions, bloat, retry-on-serialization-failure
- Connects to [[Idempotency in Data Pipelines]] (retry-safe writes)

## Distributed angle

- Cross-shard transactions, 2PC, consistency vs availability — see [[Distributed System]]

## Open questions

- Is read-committed enough for this project, or is write skew a real risk?
- Retry strategy for serialization failures?

## Reference

- [[Neon]] — serverless Postgres (MVCC)
- [[_Database Reference Index]]

## See also

- [[_Database MOC]] · [[Database Design]] · [[Distributed System]] · [[Idempotency in Data Pipelines]]
