---
domain: Data Engineering
domain_suggested: null
category: Learning
category_suggested: null
source_type: obsidian
status: review
tags: [lakehouse, interview, data-architecture]
---




```table-of-contents
```
## Why is file size important in batch processing?

File size sits in a sweet spot — too small or too large both hurt.

* **Too small** (Parquet/ORC files < ~32MB) — file-listing overhead explodes, planning time grows, every scan opens thousands of files. Driver OOMs on metadata.
* **Too large** (> ~1GB) — single tasks run too long, can't parallelize, stragglers dominate stage time, partial file failures hard to retry. Compression efficiency also plateaus.
* **Sweet spot** — 128MB–1GB per file is the usual target. Most engines (Spark, Trino, BigQuery) tune for ~256MB–512MB.

In a lakehouse, file size is a direct lever on every read path. It's also one of the few knobs you control purely from batch-side, without changing source data.
## What problems do small files create?
Expected:
* Metadata overhead
* Slow planning
* Inefficient scans

Operational symptoms:
* **Driver OOM** — Hive/Spark driver reads file metadata before scheduling. 100K+ files can OOM the driver.
* **Planning latency** — `Listing leaf files and dirs` takes minutes; query sits there.
* **Task overhead** — every file = one task. 10K files × 50ms task overhead = 500 seconds wasted per stage.
* **Inefficient I/O** — many small reads instead of few large ones. Throughput per disk drops; cloud storage bills rise on per-request charges.
* **Commit overhead** — table formats (Iceberg/Delta/Hudi) need a manifest entry per file; manifests grow, commit slows.
* **Join/aggregate amplification** — small files mean many tiny tasks; shuffle explodes.
* **Cost** — S3 GET request costs add up; GCS/Azure Blob charge per operation.

Root causes: streaming writers without rolling, frequent micro-batches, row-level CDC creating one file per row, partition over-pruning.

---
## How would you compact files in a data lake?

Compaction = rewriting many small files into fewer larger ones. Two flavors:
* **Bin-pack** — rewrite files into ~target-size files, preserving row order. Used when files exist but are too small.
* **Sort + Z-order** — rewrite with global ordering on hot columns; smaller scan footprint due to data skipping.

Mechanics:
* **Engine job** — Spark/Databricks reads matching partition, repartitions, writes back. Target 128MB–1GB per file.
* **Native compaction** — Delta `OPTIMIZE`, Iceberg `rewrite_data_files`, Hudi `clustering`/`compaction`. Do it in-place atomically (no orphan files).
* **Schedule** — nightly or weekly on hot tables; on-demand after a small-file storm.
* **Incremental** — only compact partitions that need it (file count threshold, e.g. >100 files <32MB).
* **Vacuum** — after rewrite, remove old files past retention. Otherwise storage cost stays the same.
* **Pitfalls:**
  * Don't compact while readers are mid-scan — use snapshot isolation (Delta/Iceberg).
  * Don't compact hot tables during peak read time.
  * Don't compact when files are already optimal (waste of compute).
  * Be careful with partition-level compaction on huge partitions; chunk it.

---
## Explain how partition pruning works in a lakehouse.

Partition pruning = the engine skips whole partitions at scan time based on a `WHERE` clause.
* **Hive-style** — files live under `dt=2026-06-18/`. Metastore knows partition keys. Query with `WHERE dt='2026-06-18'` lists only that directory; everything else is skipped at the storage layer.
* **Hidden partitioning** (Iceberg) — partition spec is in table metadata, not file path. `WHERE date(event_ts) = '2026-06-18'` can be rewritten to the underlying partition column transparently. Big advantage: no brittle path-coupled partition logic.
* **Storage layer** — engine asks catalog/manifest for "partitions matching this predicate," gets back a subset of manifest entries, reads only those files.
* **Where it fails:**
  * Filter on a *non-partition* column.
  * Filter uses a function on the partition column (`DATE(dt)` if partitioned by `dt`).
  * Partition column has high cardinality (e.g. partitioned by `user_id`); pruning rarely helps.
  * Statistics missing; planner falls back to full scan.

Verify pruning: `EXPLAIN` shows `PartitionFilters: [dt=2026-06-18]`. If absent or `PartitionCount = total`, pruning didn't work.

Refer: [[Partition Strategy]]

---
## How would you detect that a table requires compaction?

Signals:
* **File count per partition** — alert when partition has >1000 files or >10x target count.
* **Average file size** — alert when <32MB (the lower bound for healthy Parquet/ORC).
* **p99 file size** — wide spread = mixed legacy and recent.
* **Plan time** — `Listing leaf files` time growing week-over-week.
* **Driver memory** — `OpenCostBasedPlanner` or similar taking long; risk of OOM.
* **Query scan time / bytes scanned ratio** — disproportionately high scan time per byte = small-file overhead.
* **Metadata size** — Iceberg manifest count, Delta `_delta_log` JSON count; growth rate signals compaction debt.

Implementation:
* Nightly scan of catalog stats.
* Per-table thresholds (small fact table ≠ large fact table).
* **Auto-create compaction job** for any partition that breaches; surface dashboard for human review on hot tables.

## See Also
- [[Data Lake]] — data lake fundamentals
- [[Delta Lake & Iceberg]] — format comparison
- [[Delta Lake's OPTIMIZE]] — compaction deep-dive
- [[Data Vault & Lakehouse Modelling]] — modelling patterns