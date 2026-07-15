```table-of-contents
```
## A daily batch job scans 30 TB but only processes one day of data.
How would you optimize it?
Expected: `Partition pruning, Predicate pushdown, File layout optimization`

If a daily batch job scans 30 TB but only processes one day's data, I'd first check whether partition pruning is working. The table should be partitioned on the date column being filtered. Next, I'd ensure predicates are pushdown-friendly and avoid functions on partition columns. I'd optimize file layout by using Parquet, compacting small files, and clustering data on frequently filtered columns. I'd also avoid `SELECT *` and verify improvements using EXPLAIN plans and scan metrics. The goal is to reduce data scanned from tens of terabytes to only the partitions, files, and columns required for that day's processing.

Refer: [[Partition Strategy]]

---
## How would you choose partition keys for:
* Orders table
* Customer table
* IoT sensor table
Why?

The note is an interview-prep answer for choosing partition keys per query patterns, cardinality, and skew: the Orders table should be partitioned by
  order_date (with region as secondary for very large datasets) because analytics are time-based and pruning collapses scans from 100 TB to a single day —
  never by order_id or customer_id (cardinality explosion); the Customer dimension table, typically only a few GB for ~10M rows, often shouldn't be
  partitioned at all and should rely on clustering/sorting/bucketing, or at most a low-cardinality key like country or signup_year, since customer_id would
  create 100M partitions and catastrophic metadata overhead; and the IoT sensor time-series table (~10B records/day, queried over recent time windows)
  should be partitioned by event_date or event_hour, optionally combined with hash(sensor_id) bucketing to keep a single day from becoming a 50 TB partition
  and to improve parallelism and write throughput — driven by access patterns, volume, cardinality, skew, and retention rather than schema alone.
  
---
## What problems occur when partitions become too small?

Very small partitions lead to the small-file problem. Query engines spend more time listing files, reading metadata, and scheduling tasks than processing data. Over-partitioning increases metastore overhead, reduces compression efficiency, weakens predicate pushdown effectiveness, and can significantly increase cloud storage request costs. The goal is to choose partition keys that maximize partition pruning while keeping partition sizes large enough—typically hundreds of MBs per file rather than thousands of tiny files.

---
## What problems occur when partitions become too large?
The note is an interview-prep answer on what breaks when partitions grow too large: queries lose partition pruning (a WHERE order_date='2026-06-03' filter
  scans a full year instead of a day, e.g. 100 GB vs 36 TB), data scans, network transfer, and CPU decompression costs balloon; parallelism collapses
  because engines fan out at the partition level, so 1 × 10 TB leaves workers idle while 100 × 100 GB fully utilizes them; failure recovery and restarts get
  expensive (reprocess a whole year, not a day); lakehouse rewrites in Delta/Iceberg/Hudi touch entire files even for tiny row updates; metadata hotspots
  form when one partition holds thousands of files, slowing planning; data skew (US = 20 TB vs Canada = 500 GB) creates straggler tasks and long-tail
  latency; maintenance jobs like OPTIMIZE/VACUUM/RECLUSTER/compaction stretch from minutes to hours; and large shuffles on multi-TB partitions cause
  executor OOM and disk spill — hence the standard targets of 1–100 GB per partition and 128 MB–1 GB per Parquet file, balancing metadata efficiency against
  query selectivity.

## See Also
- [[Partitioning 1]] — partitioning strategy deep-dive
- [[Delta Lake's OPTIMIZE]] — file compaction in Delta Lake
- [[Idempotency]] — making partition-scoped reruns safe
- [[Parquet]] — Parquet format details