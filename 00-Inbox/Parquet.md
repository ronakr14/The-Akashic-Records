# AI Summary
A comprehensive deep dive into Apache Parquet from a storage-engine perspective. The note explains Parquet's internal architecture, including row groups, column chunks, pages, footer metadata, encoding strategies, compression codecs, statistics, Bloom filters, predicate pushdown, nested data storage, and Spark's read pipeline. It also compares Parquet with ORC and Avro, provides practical tuning recommendations, discusses performance trade-offs, and explains why Parquet underpins modern lakehouse technologies such as Spark, Delta Lake, Iceberg, and Snowflake.

---
# Parquet

```table-of-contents
```

> Since you're already thinking like a Data Engineer and aiming toward Architect-level understanding, I'll explain Parquet from the storage-engine perspective rather than the usual "it's a columnar file format" definition.

---

## What Parquet Is

Apache Parquet is an open-source, columnar storage format designed for efficient analytics workloads. Created in 2013 as a joint project between Twitter and Cloudera, it was inspired by Google's Dremel paper (which also inspired Protocol Buffers' columnar cousin, Arrow).

Parquet is not a database — it's a file format. But it embeds enough structure (schema, statistics, compression, encoding) that it functions as a "mini database inside a file."

---

## Why Parquet Exists

Imagine a table:

|CustomerID|Name|City|Salary|
|---|---|---|---|
|1|John|London|50000|
|2|Alice|Paris|60000|
|3|Bob|London|55000|

Traditional CSV stores data row by row:

```text
1,John,London,50000
2,Alice,Paris,60000
3,Bob,London,55000
```

If your query is:

```sql
SELECT AVG(Salary)
FROM customers
```

CSV must read all columns. Parquet only reads:

```text
Salary Column
50000
60000
55000
```

This is why Parquet became the standard for Data Lakes.

---

## Architect View

Think of Parquet as:

```text
Dataset
    ↓
Parquet Files
    ↓
Row Groups
    ↓
Column Chunks
    ↓
Pages
```

---

## Level 1: Parquet File Structure

A Parquet file looks like:

```text
+----------------+
| File Header    |
+----------------+
| Row Group 1    |
+----------------+
| Row Group 2    |
+----------------+
| Row Group 3    |
+----------------+
| Metadata       |
+----------------+
| PAR1           |
+----------------+
```

The metadata is stored at the end. Why? Because writers don't know final statistics until writing completes.

At the end Parquet writes:

```text
Column Names
Data Types
Compression
Statistics
Offsets
Encoding
```

Readers first jump to footer. This is called **Footer Metadata Architecture**. Very important interview topic.

---

## Level 2: Row Groups

Suppose file contains 100 million rows. Parquet doesn't store one giant block.

Instead:

```text
File
 ├─ Row Group 1 (10M rows)
 ├─ Row Group 2 (10M rows)
 ├─ Row Group 3 (10M rows)
 ...
```

Each row group is independently readable. Benefits:

- Parallel processing
- Predicate pushdown
- Better distribution

Spark executors can process row groups independently.

```text
Row Group = Unit of Parallelism
```

### Row Group Sizing

| Size | When to Use |
|---|---|
| 64 MB | Small tables, high parallelism needed |
| 128 MB | Default. Good balance for most workloads |
| 256 MB | Large tables, fewer files preferred |
| 512 MB | Very large tables, sequential scan-heavy |
| 1 GB | Extreme scan workloads, but reduces parallelism |

→ **Risk:** Too small = too many files (small-file problem). Too large = wasted I/O on selective queries and reduced parallelism.

---

## Level 3: Column Chunks

Inside each row group:

```text
Row Group
    ├─ CustomerID Column Chunk
    ├─ Name Column Chunk
    ├─ City Column Chunk
    └─ Salary Column Chunk
```

Instead of:

```text
1 John London 50000
2 Alice Paris 60000
```

It becomes:

```text
CustomerID:
1
2

Name:
John
Alice

City:
London
Paris

Salary:
50000
60000
```

This is why analytical queries become fast.

---

## Level 4: Pages

Column chunks are further divided:

```text
Salary Chunk
    ├─ Page 1
    ├─ Page 2
    ├─ Page 3
```

Page is the smallest unit Parquet reads. Typical page sizes:

```text
8 KB
16 KB
64 KB
```

depending on configuration.

---

## Internal Hierarchy

```text
Parquet File
│
├── Row Group
│     │
│     ├── Column Chunk
│     │       │
│     │       ├── Page
│     │       ├── Page
│     │       └── Page
│     │
│     └── Column Chunk
│
└── Footer Metadata
```

This diagram alone explains 70% of Parquet internals.

---

## Encoding Strategies

Parquet applies multiple encodings per column. Understanding these is key to predicting compression ratios and read performance.

### Dictionary Encoding

CSV:

```text
London
London
London
London
London
```

Parquet sees repetition. Stores:

```text
Dictionary

0 -> London
1 -> Paris
```

Actual data:

```text
0
0
0
1
0
```

Huge reduction for low-cardinality columns.

### Run-Length Encoding (RLE)

For sorted or sequential data:

```text
1, 1, 1, 1, 2, 2, 2, 3, 3
```

Becomes:

```text
1 × 4, 2 × 3, 3 × 2
```

Best when combined with dictionary encoding (RLE-Dictionary hybrid).

### Bit-Packing

For small integer ranges (e.g., values 0–7 need only 3 bits):

```text
Standard: 8 bytes per int
Bit-packed: 3 bits per int
```

Reduces storage by ~95% for small-range integers.

### Delta Encoding

For monotonically increasing values (timestamps, IDs):

```text
Original:  1000, 1005, 1010, 1015
Delta:     1000, 5, 5, 5
```

Stores base + small deltas. Very effective for timestamps and sorted numeric columns.

### Choosing Encodings

| Column Type | Best Encoding |
|---|---|
| Low-cardinality strings (city, status) | Dictionary |
| Sorted sequential (timestamps) | Delta + RLE |
| Small integers (age, count) | Bit-packing |
| High-cardinality random (UUID) | None (or plain) |
| Floating point | Plain + compression |

→ **Risk:** Parquet auto-detects encodings, but you can override. Forcing dictionary on high-cardinality columns wastes memory and slows reads.

---

## Compression

Parquet supports:

| Codec | Compression Ratio | Speed | Use Case |
|---|---|---|---|
| Snappy | Medium (~1.5×) | Very fast | Default, balanced |
| Gzip | High (~3×) | Slow | Archival, cold storage |
| Brotli | High (~3.5×) | Slow | Archival, web delivery |
| ZSTD | High (~2.5–4×) | Fast | Modern default, good balance |
| LZO | Low (~1.3×) | Fast | Legacy compatibility |

Most common today: **Snappy** (legacy default) or **ZSTD** (modern default in Spark 3.x+).

### Column-Level Compression

You can mix codecs per column:

```python
df.write.option("parquet.compression", "zstd") \
  .option("parquet.compression.column", "snappy:name, gzip:archived_col") \
  .parquet("/path/to/output")
```

→ **Risk:** Gzip on frequently-read columns kills performance. Use Snappy/ZSTD for hot data, Gzip only for archival.

---

## Statistics Stored in Footer

For each column:

```text
Salary
Min = 50000
Max = 70000
Nulls = 100
```

Stored per row group. Example:

```sql
SELECT *
FROM employee
WHERE salary > 100000
```

Row Group Stats:

```text
RG1
Min=10000
Max=50000

RG2
Min=60000
Max=90000

RG3
Min=110000
Max=150000
```

Spark immediately skips RG1 and RG2. Reads only RG3. This is called **Predicate Pushdown** — one of the biggest performance wins.

---

## Bloom Filters

Parquet v2 supports per-column Bloom filters — probabilistic data structures that answer "does this value exist in this row group?" with no false negatives.

### How They Work

```text
Query: WHERE user_id = 12345

Bloom Filter for RG1: "Definitely not here" → Skip file
Bloom Filter for RG2: "Maybe here" → Read pages
Bloom Filter for RG3: "Definitely not here" → Skip file
```

### When to Enable

- High-cardinality columns frequently used in equality filters (user_id, email)
- When predicate pushdown alone isn't enough (many row groups have overlapping ranges)

### When to Skip

- Low-cardinality columns (Bloom filter overhead > benefit)
- Range queries (Bloom filters only help equality)
- Columns rarely filtered

### Cost

- ~1–5% storage overhead per column with Bloom filter
- Write time increases (filter construction)
- Read time decreases (fewer pages read)

→ **Risk:** Enabling Bloom filters on all columns wastes storage and slows writes. Only enable on columns that benefit from equality skip.

---

## Why Spark Loves Parquet

Query:

```sql
SELECT salary
FROM employee
WHERE city='London'
```

Spark performs:

```text
1. Read footer
2. Check statistics
3. Skip irrelevant row groups
4. Read only City and Salary columns
5. Ignore all others
```

Result:

```text
Less I/O
Less Network
Less CPU
```

---

## Nested Data Support

Parquet handles:

```json
{
  "customer": {
    "name": "John",
    "address": {
      "city": "London"
    }
  }
}
```

using **Definition Levels** and **Repetition Levels**. This is one of the most complex parts of Parquet internals. That's how Parquet efficiently stores structs, arrays, maps, and nested JSON without flattening everything.

---

## What Happens During a Spark Read?

```text
spark.read.parquet()
        │
        ▼
Read Footer
        │
        ▼
Schema Discovery
        │
        ▼
Predicate Pushdown
        │
        ▼
Column Pruning
        │
        ▼
Row Group Selection
        │
        ▼
Page Reads
        │
        ▼
DataFrame
```

This pipeline is worth understanding deeply because it explains many Spark optimization behaviors.

---

## Parquet vs ORC vs Avro

| Dimension | Parquet | ORC | Avro |
|---|---|---|---|
| Creator | Twitter / Cloudera | Hortonworks / Facebook | Apache |
| Storage | Columnar | Columnar | Row-based |
| Best for | Analytics (read-heavy) | Hive workloads | Streaming, serialization |
| Compression | Good (multiple codecs) | Excellent (ZLIB default) | Good |
| Predicate pushdown | Yes (stats + Bloom) | Yes (stats + Bloom) | No |
| Nested data | Yes (Dremel encoding) | Limited | Full schema evolution |
| Schema evolution | Limited | Limited | Excellent |
| Spark support | Native (default) | Good | Library required |
| Hive support | Good | Native (best) | Library required |
| Interoperability | Excellent | Hive-centric | Language-agnostic |

→ **Risk:** Choosing ORC in a non-Hive ecosystem or Avro for analytical workloads leads to suboptimal performance. Parquet is the safe default for analytics.

---

## Practical Tuning

### Key Configuration Knobs

| Parameter | Default | Recommendation |
|---|---|---|
| `parquet.block.size` | 128 MB | Match to HDFS block size or S3 part size |
| `parquet.page.size` | 1 MB | 64 KB–1 MB; smaller for selective queries |
| `parquet.enable.dictionary` | true | Disable only for high-cardinality columns |
| `parquet.bloom.filter.enabled` | false | Enable for high-cardinality equality columns |
| `parquet.compression` | snappy | Use ZSTD for modern Spark |
| `parquet.enable.summary` | true | Keep true; needed for schema discovery |

### Write Optimization

- Sort data within row groups before writing (better compression, better pushdown)
- Use `sortWithinPartitions()` in Spark before write
- Avoid too many small files — coalesce before read

### Read Optimization

- Push filters down (don't filter in Spark when Parquet can skip)
- Select only needed columns (don't `SELECT *`)
- Use partition pruning on top of Parquet's row group pruning

---

## Architect-Level Mental Model

Think of Parquet as a mini database inside a file. A Parquet file contains:

```text
Data
+
Schema
+
Indexes (statistics)
+
Compression
+
Column Storage
```

which means:

```text
CSV  = Raw Data
Parquet = Smart Data
```

That's why modern platforms such as Apache Spark, Databricks, Snowflake, Apache Iceberg, and Delta Lake all use Parquet as their underlying storage format.

---

## Learning Path: Beyond Parquet

The next topics to study:

1. Row Groups sizing (128 MB vs 512 MB vs 1 GB)
2. Predicate Pushdown internals
3. Dictionary Encoding vs Run-Length Encoding
4. Bloom Filters in Parquet
5. How Delta Lake and Iceberg build transaction layers on top of Parquet
6. Small-file problem and file compaction

Those topics are where Data Engineer knowledge starts transitioning into Architect-level lakehouse design.
