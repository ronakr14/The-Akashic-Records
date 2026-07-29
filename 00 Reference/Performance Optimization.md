# AI Summary
None. How would you investigate?

```table-of-contents
```
## A Spark batch job slowed from 45 minutes to 3 hours.
How would you investigate?
Potential areas:
* Data growth
* Skew
* Shuffle size
* Join strategy
* Cluster changes

Investigation order (cheap signals first):
1. **Compare yesterday's run to today's.** Same input volume? Same partition count? Same input bytes? If today's input doubled, mystery solved — check upstream for new source or filter that no longer prunes.
2. **Check Spark UI for the new bottleneck.** Stage durations, task time distribution (median vs p95 — large gap = skew), shuffle spill (disk spill = bad), GC time.
3. **Skew** — one task takes 10x longer than peers. Look at partition sizes; repartition on a more uniform key or use salting for the heavy join.
4. **Shuffle size** — did shuffle bytes grow? Usually because of broadcast-vs-shuffle join change, or new column being shuffled. Check `spark.sql.adaptive.enabled` and broadcast threshold.
5. **Join strategy** — did a previously-broadcast join (small dimension) now exceed broadcast threshold (default 10MB)? Look at plan; if so, either increase threshold, bucket the dimension, or filter before join.
6. **Data skew on a join key** — one customer has 80% of rows. Mitigate with salting, skewed join hints, or pre-aggregation.
7. **File layout** — too many small files explode planning time; check `input_files_count` in metrics, compact if needed.
8. **Cluster changes** — did executor count, executor memory, or runtime version change? Did autoscaler pick a different instance type? Check YARN/K8s logs.
9. **Schema drift** — new column treated as string instead of typed, exploding row size.
10. **UDFs** — Python UDFs serialize per-row; replace with Pandas UDFs or built-in functions.

Quick win ranking: data growth > skew > shuffle > file layout > UDF > cluster config.

---
## A batch job processes:
```text
1 billion records
20 joins
10 aggregations
```
How would you optimize it?

Optimization layers (cheapest first):
1. **Push computation early** — filter before joining (predicate pushdown, partition pruning). Most "20 joins" jobs join data that turns out to be irrelevant; trimming inputs is the highest-leverage move.
2. **Reduce shuffle** — every join/aggregation shuffles. Skew + shuffle is usually the dominant cost. Salting, broadcast joins, pre-aggregating, or `groupByKey` → `reduceByKey` style restructuring.
3. **Broadcast small dimensions** — flag dimensions <100MB; Spark's `autoBroadcastJoinThreshold` (default 10MB) is conservative. Bump it or hint broadcasts.
4. **Pre-aggregate where possible** — most "20 joins" patterns have a hub table; aggregate once at the hub, join summaries downstream. Cuts downstream cost.
5. **Reorder joins** — join the most selective, smallest dimension first; build a smaller intermediate; then join larger.
6. **Bucketing** — pre-bucket hot tables on join keys (Spark/Databricks `bucketBy`) to eliminate shuffle on repeated joins.
7. **AQE** — `spark.sql.adaptive.enabled=true`, plus `coalescePartitions` and `skewJoin` enabled. Spark 3.2+ does this well.
8. **File format & layout** — Parquet/Delta with ZSTD or Snappy; partition + cluster on filter columns. Avoid small files.
9. **Compute sizing** — match executor count to partition count; right-size memory for shuffle-heavy stages.
10. **Replace UDFs** — built-in functions are 10–100x faster; Pandas UDFs for vectorized cases.
11. **DataFrame vs RDD** — always DataFrame API; Catalyst optimizer can do whole-stage codegen.
12. **Incremental recompute** — if most rows are unchanged, compute only the delta and merge.

For 1B rows, 20 joins: expect to spend most time on join ordering, broadcast-vs-shuffle, and skew — not on compute size.

---
## How do you identify bottlenecks in a batch workload?
Expected:
* CPU
* Memory
* Network
* Disk I/O
* Shuffle

How to tell which is the bottleneck:
* **CPU** — task CPU time is high and GC time is low; spark stage durations grow with executor count (CPU-bound scales). Profile with `spark.ui.profile`, or async-profiler for JVM.
* **Memory** — GC time > 10% of task time; OOMs; shuffle spill. Look for skewed partitions, large broadcasted tables, UDFs holding references.
* **Network** — shuffle read/write bytes are huge; data transfer dominates stage time. Often a join or aggregation that should have been pre-aggregated.
* **Disk I/O** — shuffle spill to disk; reading many small files; Parquet/ORC decoding dominates. Compaction, broadcast, or repartition needed.
* **Shuffle** — almost always the primary bottleneck in batch. Check shuffle read/write/spill; optimize with broadcast joins, salting, pre-aggregation.

Methodology:
1. Look at Spark UI stage summary: which stage is slowest, and why? CPU time vs shuffle time vs GC time per task.
2. Median vs p95 task duration: big gap = skew.
3. Shuffle read/write ratio: high write = recomputing; high read = receiving too much.
4. Correlate with infrastructure metrics from the cluster: node CPU%, network throughput, disk I/OPS.

Rule of thumb: in batch, **shuffle and skew are bottlenecks ~70% of the time**. Compute sizing is rarely the issue.

---
## Explain predicate pushdown and why it matters in batch processing.

Predicate pushdown = the engine pushes a `WHERE` filter **down to the storage layer** so that unread data is never read.
* **At scan time** — instead of reading a 1TB Parquet file then filtering, the engine reads only the row groups / pages where the filter could match. Uses Parquet/ORC column statistics (min/max per row group).
* **At partition pruning** — when a query has `WHERE dt='2026-06-18'`, the engine skips all other date partitions entirely. Partition-level pushdown.
* **At column pruning** — `SELECT a, b` reads only columns `a, b`, not the rest. Column-level pushdown.

Why it matters in batch:
* **Cost** — every byte read = cost. Pushdown turns "scan 10TB to return 100 rows" into "scan 100MB."
* **Speed** — orders-of-magnitude less I/O, less decode, less shuffle downstream.
* **SLA** — many batch jobs miss SLA *only* because pushdown failed (e.g. function on partition column disables it).
* **Failure mode** — `WHERE DATE(dt) = '2026-06-18'` looks like pruning but disables partition pruning. Always filter on raw column, not transformed.

How to verify: `EXPLAIN` shows the plan; the `Scan` operator should include `PushedFilters:`. If not, your predicate wasn't pushed.

Refer: [[Partition Strategy]]