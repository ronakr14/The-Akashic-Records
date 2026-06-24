#bloom-filter #data-structures #probabilistic #parquet #data-engineering #data-skipping

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

## Bloom Filters vs. Min/Max Statistics

Both are data-skipping mechanisms used in [[Parquet]] row groups, but they complement each other:

| Scenario | Min/Max Statistics | Bloom Filter |
|---|---|---|
| `WHERE id = 250`, range is `[100, 500]` | Must read (250 is in range) | Can skip if 250 not in filter |
| `WHERE id = 999`, range is `[100, 500]` | Skip (999 > max) | Skip (not in filter) |
| High-cardinality columns | Limited value | Effective |

Bloom Filters handle point lookups on high-cardinality columns where min/max ranges are too wide to be useful.

## Where Bloom Filters Are Used

| Domain | Systems | Use Case |
|---|---|---|
| **Databases** | [[Apache Cassandra]], [[Apache HBase]], [[PostgreSQL]] | Avoid reading SSTables/disk pages for non-existent keys |
| **Data Lakes** | [[Apache Iceberg]], [[Delta Lake]], [[Parquet]] | Row group pruning during queries |
| **Query Engines** | [[Apache Spark]], [[Apache Trino]] | Join optimization, partition pruning |
| **Caching** | CDNs, proxy caches | Avoid backend lookups for uncached keys |
| **Distributed Systems** | Google Bigtable, Meta, LinkedIn | Cross-node existence checks without network calls |

## In Parquet

Row group metadata includes both statistics and Bloom Filters:

```
Row Group
    ├─ Min/Max per column
    ├─ Null Count
    ├─ Bloom Filter per column
```

Query engine pruning pipeline:

```
Footer Read → Statistics Check → Bloom Filter Check → Read Data
```

This stack — partition pruning → file pruning → statistics → Bloom Filters → scan — is what makes modern [[Data Lakehouse]] systems fast at petabyte scale.

## When NOT to Use Bloom Filters

- **Exact answers required** and memory is not constrained → use a [[Hash Set]] or hash table
- **Deletions needed** → use a Counting Bloom Filter (or another structure)
- **Counting occurrences** → use a Count-Min Sketch instead
- **Small datasets** where the overhead of hash functions isn't worth the I/O savings
- **Low-cardinality columns** where min/max statistics already prune effectively

## Related

- [[Parquet]]
- [[Data Lakehouse]]
- [[Data Skipping]]
- [[Hash Set]]
- [[Probabilistic Data Structures]]
- [[Apache Iceberg]]
- [[Delta Lake]]
- [[Apache Spark]]
