# AI Summary
Use Bloom Filters for Row Group Pruning in Parquet-Based Data Lakes. **Date:** 2026-06-25

```table-of-contents
```

# Use Bloom Filters for Row Group Pruning in Parquet-Based Data Lakes

**Date:** 2026-06-25
**Status:** Accepted
**Deciders:** Data Engineering — storage format & query optimization working group

## Context

Our data lake stores billions of records in Parquet, partitioned by date and a few high-cardinality dimensions. Query patterns are dominated by point lookups and selective filters on columns like `customer_id`, `order_id`, and `sku` — where the sought value may or may not exist in a given row group.

Min/max statistics work well for range columns (timestamps, monotonic IDs), but fail for high-cardinality equality filters: the value range of a row group is often wide enough that the filter column's value falls inside it, forcing a full scan of the row group even when the value isn't present.

We needed a second layer of pruning that could answer "does this value exist in this row group?" with bounded memory and no false negatives.

## Decision

Adopt **Bloom Filters** as the primary data-skipping mechanism for high-cardinality equality columns in Parquet row groups, layered on top of existing min/max statistics.

Configuration:
- Target false positive rate: **1%** (~9.6 bits per element)
- Bloom Filter applied to columns with cardinality > 10,000 where min/max range width exceeds 10× the value count
- Filters written into Parquet column metadata at write time (native Parquet Bloom Filter support)
- Query engines (Spark, Trino) consult the filter before reading column chunk data

Pruning pipeline order:

```
Partition Pruning → File Pruning → Min/Max Stats → Bloom Filter → Read Data
```

## Consequences

- **Positive:** Eliminates 60–90% of row group reads for selective equality queries on high-cardinality columns. Reduces I/O cost proportionally.
- **Positive:** Zero false negatives — if a value exists, the row group is always read. No correctness risk from the filter itself.
- **Positive:** Bounded memory. A 1M-element row group at 1% FP rate uses ~1.2 MB of filter — orders of magnitude smaller than a hash set.
- **Negative:** Write-time overhead. Computing k hash functions per element adds ~5–10% to write latency. Acceptable for our batch-heavy write pattern.
- **Negative:** False positives still cause unnecessary reads (1% by design). For very selective queries this is negligible; for broad queries the ratio of false positives to real hits can be higher.
- **Risk:** Bloom Filters cannot be deleted from or updated in a row group without rewriting it. Schema evolution requires rewrites, not in-place patches.

## Alternatives Considered

- **Hash Set per row group:** Exact answers, but 10–50× memory cost. At billions of elements across thousands of row groups, the memory footprint is prohibitive for on-heap or sidecar storage.
- **Bitmap Index:** Excellent for low-to-medium cardinality columns, but explodes in size for high-cardinality (one bit per distinct value per row group). Also more expensive to compute at write time.
- **Dictionary Encoding + Min/Max only:** Already in use. Insufficient for the equality-filter selectivity problem described in Context — this is the status quo we're augmenting, not replacing.
- **Count-Min Sketch:** Answers frequency, not existence. Overkill for a membership question and has higher false positive rates for this use case.
- **No filter (rely on min/max only):** Cheapest write-time cost, but leaves the high-cardinality selectivity problem unsolved. Query latency and I/O costs remain high for the dominant access pattern.

## See Also

- [[Bloom Filters]] — conceptual deep-dive: internals, FP rate math, comparison with min/max stats
- [[Parquet]] — storage format: how Bloom Filters fit into row group metadata
- [[Data Lakehouse]] — architecture: where pruning sits in the query pipeline
- [[Data Skipping]] — overview of all pruning mechanisms in the stack
