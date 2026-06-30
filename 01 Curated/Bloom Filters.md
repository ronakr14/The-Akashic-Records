---
domain: Data Engineering
domain_suggested: null
category: Curated
category_suggested: null
source_type: obsidian
status: review
tags: [bloom-filter, data-skipping, parquet, data-structures, probabilistic]
---






```table-of-contents
```


A Bloom Filter is a memory-efficient probabilistic data structure that answers one question: **"Is this element possibly in the set, or definitely not?"**

| Query result | Meaning |
|---|---|
| **Definitely not present** | Element was never added — guaranteed correct |
| **Possibly present** | Element *may* have been added — could be a false positive |
| **Definitely present** | Never returned — Bloom Filters don't confirm presence with certainty |

This one-sided error guarantee makes them safe for filtering: they never miss real members, but may occasionally flag non-members.

## Why Not a [[Hash Set]]?

A [[Hash Set]] gives exact answers but is expensive at scale:

| | 10 Billion Customer IDs |
|---|---|
| **HashSet** | Hundreds of GB |
| **Bloom Filter** | Few GB |

When the only question is "skip or don't skip," that tradeoff is worth it.

## Internal Working

**Setup**: a bit array of size `m`, and `k` independent hash functions.

### Insert

For each element, compute `k` hash values and set those bit positions to `1`.

Example — inserting "Alice" with `k=3` into a 10-bit array:

```
Hashes: 2, 5, 8

Before: 0 0 0 0 0 0 0 0 0 0
After:  0 0 1 0 0 1 0 0 1 0
```

Inserting "Bob" (hashes: 1, 5, 9):

```
After:  0 1 1 0 0 1 0 0 1 1
```

### Query

Compute the same `k` hash values. If **any** bit is `0`, the element is **definitely not present**. If **all** bits are `1`, it is **possibly present**.

Query "David" (hashes: 3, 5, 8):

```
bit 3 = 0 → David NOT present (no further checks needed)
```

Query another value (hashes: 1, 5, 8):

```
bit 1 = 1, bit 5 = 1, bit 8 = 1 → Maybe present (could be a false positive)
```

## False Positive Rate

The probability of a false positive depends on three parameters:

- `m` — bit array size
- `n` — number of elements inserted
- `k` — number of hash functions

**Optimal hash count**: `k = (m / n) * ln(2)`

**False positive rate**: approximately `(1 - e^(-kn/m))^k`

In practice: a 1% FP rate requires ~9.6 bits per element. A 0.1% FP rate requires ~14.4 bits per element.

## Where Bloom Filters Are Used

| Domain | Systems | Use Case |
|---|---|---|
| **Databases** | [[Apache Cassandra]], [[Apache HBase]], [[PostgreSQL]] | Avoid reading SSTables/disk pages for non-existent keys |
| **Data Lakes** | [[Apache Iceberg]], [[Delta Lake]], [[Parquet]] | Row group pruning during queries |
| **Query Engines** | [[Apache Spark]], [[Apache Trino]] | Join optimization, partition pruning |
| **Caching** | CDNs, proxy caches | Avoid backend lookups for uncached keys |
| **Distributed Systems** | Google Bigtable, Meta, LinkedIn | Cross-node existence checks without network calls |

## Bloom Filters in Parquet

Row group metadata includes both statistics and Bloom Filters:

```
Row Group
    ├─ Min/Max per column
    ├─ Null Count
    ├─ Bloom Filter per column
```

Both are data-skipping mechanisms, but they complement each other:

| Scenario | Min/Max Statistics | Bloom Filter |
|---|---|---|
| `WHERE id = 250`, range is `[100, 500]` | Must read (250 is in range) | Can skip if 250 not in filter |
| `WHERE id = 999`, range is `[100, 500]` | Skip (999 > max) | Skip (not in filter) |
| High-cardinality columns | Limited value | Effective |

Bloom Filters handle point lookups on high-cardinality columns where min/max ranges are too wide to be useful.

Query engine pruning pipeline:

```
Footer Read → Statistics Check → Bloom Filter Check → Read Data
```

This stack — partition pruning → file pruning → statistics → Bloom Filters → scan — is what makes modern [[Data Lakehouse]] systems fast at petabyte scale.

## Decision Matrix — When to Use What

| Scenario | Best Option | Why |
|---|---|---|
| Range column, low cardinality | Min/Max stats | Range bounds are tight; cheap and exact |
| Equality filter, high cardinality, selective query | Bloom Filter | Eliminates most row groups; bounded memory |
| Equality filter, high cardinality, broad query | Min/Max only | FP ratio too high; filter adds cost without benefit |
| Need exact answers, memory available | Hash Set | Bloom Filter can't guarantee presence |
| Need frequency counts | Count-Min Sketch | Bloom Filter answers membership only |

## Code Example — Writing Bloom Filters into Parquet

Minimal PyArrow example: write a Bloom Filter on a high-cardinality column and verify it's present in metadata.

```python
import pyarrow as pa
import pyarrow.parquet as pq

# Sample data
customer_ids = pa.array([101, 202, 303, 404, 505])
table = pa.table({"customer_id": customer_ids, "value": [10, 20, 30, 40, 50]})

# Write Parquet with Bloom Filter on the high-cardinality column
pq.write_table(
    table,
    "/data/orders.parquet",
    write_statistics=True,
    # Column-level properties control Bloom Filter
    column_properties={
        "customer_id": {
            "bloom_filter_enabled": "true",
            "bloom_filter_fpp": "0.01",       # 1% false positive rate
        }
    },
)

# Verify: read back metadata
meta = pq.read_metadata("/data/orders.parquet")
col_meta = meta.row_group(0).column(0)
print(f"Bloom Filter present: {col_meta.bloom_filter_offset is not None}")
print(f"FP rate configured: 0.01 (9.6 bits/element)")
```

**Key points:**
- `bloom_filter_enabled` tells the writer to compute the filter for that column
- `bloom_filter_fpp` sets the target false positive rate (default 0.01)
- At read time, the engine consults the filter automatically — no query changes needed

## Scaling & Sizing Guidance

Back-of-envelope for common row group sizes (1% FP rate ≈ 9.6 bits/element):

| Row Group Size | Filter Size (1% FP) | Filter Size (0.1% FP) | Verdict |
|---|---|---|---|
| 1M elements | 1.2 MB | 1.8 MB | Trivial |
| 10M elements | 12 MB | 18 MB | Fine |
| 100M elements | 120 MB | 180 MB | Consider per-partition filters only |
| 1B elements | 1.2 GB | 1.8 GB | Too large — reduce FP tolerance or skip |

**Rule of thumb:** If the Bloom Filter exceeds 10% of the row group's data size, the I/O you save reading less data is offset by the I/O spent reading the filter itself. Either increase the FP tolerance or drop the filter on that column.

## Engine Compatibility & Gotchas

| Engine | Bloom Filter Support | Notes |
|---|---|---|
| Spark (3.x+) | Full | Enabled by default; `parquet.bloom.filter.enabled` config |
| Trino / Presto | Full | Uses Parquet and Iceberg Bloom Filters natively |
| DuckDB | Partial | Reads Parquet Bloom Filters; does not write them |
| Hive | Limited | Needs ORC/Parquet with proper settings; often ignored |
| Older readers | Not recognized | Silently skipped — no error, just no pruning benefit |

**Gotchas:**
- Bloom Filters are per-column-chunk. If your query filters on a column without a filter written, the engine falls back to min/max or full scan — no error, just silent degradation.
- Different engines may write filters with different FP targets. A file written at 0.1% FP by Spark may still be read by Trino, but Trino uses the *writer's* FP rate for its skip decision — not a configurable read-side threshold.
- Streaming writes (e.g., Flink → Parquet) often disable Bloom Filters by default because per-microbatch write overhead compounds. Verify your streaming framework's settings.

## Operational — Monitoring & Troubleshooting

**How to verify Bloom Filters are being used:**

- `EXPLAIN ANALYZE` in Spark/Trino — look for "row groups pruned" counts in the scan node
- `parquet-tools meta file.parquet` — inspect column metadata for Bloom Filter offset (non-null = filter present)
- Spark event log — compare scan task metrics before/after enabling filters on a column

**What to monitor in production:**

| Metric | What it tells you | Alert threshold |
|---|---|---|
| Row group skip ratio | % of row groups skipped before reading | Drop > 30% after enabling → filter not being consulted |
| Write latency | Overhead of computing filters | Increase > 15% → too many columns or row groups too large |
| Filter file size | Scaling sanity check | > 10% of row group data size → see Scaling section above |

**When to worry:**

- Skip ratio unchanged after enabling → engine doesn't support Bloom Filters for that column type, or the filter wasn't written. Check `parquet-tools meta` to confirm presence.
- Write latency spike → row group size too large for per-group filters. Either increase target row group size or enable filters on fewer columns.
- Silent degradation → older reader version. The engine skips the filter without error; you get full scans. Verify reader version supports Parquet Bloom Filters (Parquet 1.10+ spec).

## When NOT to Use Bloom Filters

- **Exact answers required** and memory is not constrained → use a [[Hash Set]] or hash table
- **Deletions needed** → use a Counting Bloom Filter (or another structure)
- **Counting occurrences** → use a Count-Min Sketch instead
- **Small datasets** where the overhead of hash functions isn't worth the I/O savings
- **Low-cardinality columns** where min/max statistics already prune effectively

## Interview Q&A

**Q1: Why can't a Bloom Filter give a definitive "yes"?**

A: Multiple hash functions can collide — different elements may set the same bit positions. A positive result ("all k bits are 1") means those positions *could* have been set by the element you're querying, or by a combination of other elements. Only a negative is certain.

**Q2: How do you choose k (number of hash functions)?**

A: Optimal k = (m / n) × ln(2), where m = bit array size and n = element count. In practice, 3–7 hash functions covers most workloads. More hashes = lower FP rate but slower inserts/queries. Most libraries auto-compute k from your target FP rate and element count.

**Q3: What's the cost of enabling Bloom Filters on writes?**

A: Each element requires k hash computations + k bit writes. Typically 5–10% write latency increase. For batch workloads this is usually acceptable; for streaming, evaluate per-microbatch overhead — some frameworks disable Bloom Filters by default for streaming writes.

**Q4: Can you delete an element from a Bloom Filter?**

A: No — clearing a bit would invalidate other elements that share it. If you need deletions, use a **Counting Bloom Filter** (each bit becomes a small counter; decrement on delete). Tradeoff: 4× memory per slot instead of 1 bit.

**Q5: Bloom Filter vs. Cuckoo Filter — which is better?**

A: Cuckoo Filters support deletions, have better cache locality, and achieve lower FP rates at the same space budget. But Bloom Filters are simpler, more widely supported in data systems (Parquet, RocksDB, Cassandra), and sufficient for read-heavy data lake workloads where deletions aren't needed. Choose Cuckoo only if you need delete support or extreme space efficiency.

## Related

- [[Parquet]]
- [[Data Lakehouse]]
- [[Data Skipping]]
- [[Hash Set]]
- [[Probabilistic Data Structures]]
- [[Apache Iceberg]]
- [[Delta Lake]]
- [[Apache Spark]]
