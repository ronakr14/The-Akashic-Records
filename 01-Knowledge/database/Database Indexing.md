---
domain: database
subdomain: indexing
note_type: concept
source_type: self
status: draft
level: intermediate
---
# AI Summary

DRAFT — scaffold only. Synthesis pending. How database indexes work and when to add one: B-tree vs LSM, covering/composite indexes, selectivity, and the write-amplification cost.

---

## Why indexes

- Turn O(n) scan into O(log n) lookup / range
- The cost side: extra writes, storage, planner choices

## B-tree indexes

- Structure, page splits, fan-out, clustered vs secondary
- Range scans, sort avoidance, index-only scans

## LSM-tree indexes

- Memtable → SSTable → compaction; write-optimised
- Read amplification, bloom filters — see [[Bloom Filters]]
- Where LSM engines fit (RocksDB, Cassandra, [[Turso]]-style)

## Index design

- Selectivity, cardinality, leading-column rule for composites
- Covering indexes, partial/filtered indexes
- When NOT to index (low selectivity, write-heavy, small tables)

## Cost

- Write amplification, index maintenance on update/delete
- Planner: when it ignores an index

## Open questions

- B-tree vs LSM decision for this project's workloads?
- Composite index column order for the common query shapes?

## Reference

- [[Milvus]] — ANN indexes for vectors (contrast with B-tree)
- [[_Database Reference Index]]

## See also

- [[_Database MOC]] · [[Database Design]] · [[Vector Database]] · [[Query Optimization]] · [[Partitioning]]
