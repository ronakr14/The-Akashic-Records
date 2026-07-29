# AI Summary
None. Why might this happen?

```table-of-contents
```
## A query reads 10 TB to return 100 rows.
Why might this happen?

Common causes (from most to least likely):
* **No partition pruning** — `WHERE` not on the partition column, or partition column wrapped in a function (`DATE(dt)` disables pruning).
* **Predicate not pushed down** — filter applied at engine level instead of in the storage layer.
* **No column pruning** — `SELECT *` reads all columns.
* **Join before filter** — joined first, filtered second. Reorder.
* **Cartesian or many-to-many join** — planner thinks it'll return few rows, but explodes.
* **Cross join** — implicit cross join on missing join condition.
* **Self-join on large table** — unbounded.
* **Subquery not decorrelated** — runs once per outer row, scans 10TB each time.
* **OR conditions across columns** — sometimes defeats predicate pushdown.
* **Function on partition/cluster column** — `WHERE CAST(dt AS STRING) = ...` blocks pruning.
* **Stats missing** — planner assumes worst case, scans everything.
* **Views stacked** — view definition itself has `SELECT *`; deep view chains accumulate.
* **Multi-statement transaction scan** — feature in some engines.

Fix recipe: rewrite filter on raw partition column → drop `SELECT *` → reorder join/filter → add explicit `LIMIT` → check `EXPLAIN` for `PushedFilters` and `PartitionFilters`. Verify with metrics: bytes_scanned before/after.

---
## Given a query plan, how would you identify:
* Expensive joins
* Full table scans
* Data skew
* Excessive shuffles

Reading a plan (Spark-style; applies to Trino/BigQuery with different naming):
* **Expensive joins** — look for `Exchange` (shuffle) before a join, especially `SortMergeJoin` over `BroadcastHashJoin`. Large estimated row counts at the join input. A join that should have been broadcast (small dim × large fact) wasn't.
* **Full table scans** — `Scan` operator with no `PushedFilters` or `PartitionFilters`. `PartitionCount` = total table partitions, not pruned. Compare estimated rows vs total table rows.
* **Data skew** — `Sort` or `Exchange` with skewed partition sizes; or check stage metrics: any task takes 10x the median. Look at the join's `Estimated rows` vs `Actual rows` — large gap = bad stats or skew.
* **Excessive shuffles** — count the `Exchange` operators. Every shuffle = cost. Multiple shuffles in one pipeline = often a `groupByKey` pattern or a chain that should have been combined.

Tooling:
* **Spark UI** — DAG, stage timeline, per-task metrics.
* **EXPLAIN EXTENDED / EXPLAIN ANALYZE** — compare estimated vs actual rows; gap = bad stats or skew.
* **Per-stage metrics** — shuffle read/write bytes, spill, GC, task duration distribution.
* **BigQuery / Snowflake plan viewers** — same ideas, different naming.
---
## What information would you extract from query plans to build an AI optimization engine?
Interesting for your lakehouse optimization work.
Possible features:
```json
{
  "join_count": 3,
  "join_types": ["inner", "left"],
  "estimated_rows": 1000000,
  "scan_bytes": 50000000000,
  "group_by_count": 2
}
```

Feature engineering from plans:
* **Structural** — operator tree shape: depth, join count, group-by count, window count, exchange count, sort count, distinct count, subquery nesting.
* **Operator types** — `SortMergeJoin` vs `BroadcastHashJoin` vs `ShuffleNestedLoopJoin`; `HashAggregate` vs `SortAggregate`; presence of `Sort`, `Window`, `Expand`.
* **Cardinality** — estimated input/output rows per operator. Estimated vs actual ratio is itself a feature (estimator error).
* **Cost** — planner-reported cost per operator; cumulative cost by subtree.
* **Data sizes** — bytes scanned, files scanned, partitions scanned, rows scanned. Ratio `bytes_output / bytes_input` = selectivity.
* **Filter info** — pushed filter count, partition filter count, predicate type (equality, range, IN, LIKE).
* **Join keys & cardinality** — many-to-one vs many-to-many vs one-to-one; key uniqueness stats.
* **Skew indicators** — partition size stddev, max/median ratio, presence of `skewed partition` hints.
* **Shuffle pattern** — number of distinct `Exchange` operators; shuffle bytes; spill bytes.
* **Plan fingerprint** — canonical hash of the operator tree (after normalization) for clustering similar plans.
* **Context** — table size, table age, owner team, recent DDL changes on referenced tables.

Modeling approach:
* **Supervised** — train on (plan features) → (runtime, cost, error) labels from historical runs.
* **RL / bandit** — recommend config (broadcast threshold, partition count, file format) and learn from observed outcome.
* **Pattern matching** — rule-based: "SortMergeJoin on a table <100MB should be BroadcastHashJoin" → explicit recommendation.
* **Outcome prediction** — predict runtime and cost given plan features; flag outliers before they run.
* **Anti-pattern classifier** — labeled dataset of bad plans (small files, broadcast exceeded, join-before-filter); supervised classifier on plan features.

Why this is tractable: plans are structured (graphs), feature-extractable, and labeled by historical outcomes. Less unsupervised ML than feature engineering + classical models + rules.