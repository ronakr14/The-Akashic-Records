---
domain: data-engineering
subdomain: index
note_type: moc
source_type: self
status: curated
level: intermediate
---
# AI Summary

Map of content for the data-engineering knowledge area. Indexes every synthesized note by theme — ingestion patterns, storage and file layout, query and pipeline performance, reliability, and platform architecture — and acts as the hub the rest of the domain links back to.

---

# Data Engineering — Map of Content

Entry point for the data-engineering knowledge area. Grouped by theme, not folder.

## Ingestion & movement

- [[ETL]] — transform-before-load pattern, history, trade-offs
- [[ELT (Extract, Load, Transform)]] — load-then-transform, medallion, cloud-native motivation
- [[ETL vs ELT]] — concise decision reference between the two
- [[Incremental Data Loading Strategies]] — watermarks, CDC, MERGE, delete handling
- [[Stream Processing]] — events, Kafka/Flink, windowing, stateful processing
- [[Batch Processing]] — scheduled group execution, windows, load strategies

## Storage & file layout

- [[Parquet]] — columnar format internals: row groups, pages, footer, encoding
- [[Partitioning]] — partition types, pruning, key selection
- [[Z-Ordering]] — multi-column data skipping via space-filling curves
- [[Bloom Filters]] — probabilistic membership testing, sizing math
- [[Bloom Filters - Row Group Pruning]] — ADR: Bloom filters for equality pruning in Parquet lakes

## Performance

- [[Lakehouse Performance Optimization]] — file sizing, compaction, pruning mechanics
- [[Query Optimization]] — reading execution plans, skew, shuffles, scan reduction

## Reliability

- [[Idempotency in Data Pipelines]] — delivery semantics, MERGE, partition overwrite, watermarks
- [[Failure Recovery in Batch Data Pipelines]] — checkpointing, retry vs resume vs restart vs reprocess

## Compute engines

- [[PySpark]] — distributed computation model, Catalyst, DAG scheduling
- [[Polars]] — Arrow-backed lazy query engine, vectorized execution

## Platform architecture

- [[Data Mesh]] — domain ownership, data as a product, federated governance
- [[Data Engineering Playbook]] — fifteen foundational principles, quick reference

## See also

- [[_Architecture MOC]] — data modelling, dimensional modelling, database design
- [[_Python MOC]] — Python language and packaging notes
