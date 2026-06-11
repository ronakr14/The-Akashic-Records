What problems occur when partitions become too small?

This is a very common interview follow-up because **over-partitioning** can be just as bad as under-partitioning.

## What Happens When Partitions Become Too Small?

Imagine a 30 TB table partitioned by:

```text
year/month/day/hour/minute
```

Now a single day's data may be spread across thousands of tiny partitions and files.

---

## 1. Small File Problem

Instead of:

```text
dt=2026-06-01
  ├── file1.parquet (512 MB)
  ├── file2.parquet (512 MB)
```

you get:

```text
dt=2026-06-01/hour=01
  ├── file1.parquet (2 MB)

dt=2026-06-01/hour=02
  ├── file2.parquet (3 MB)

...
```

Thousands of tiny files create overhead:

- File open/close operations
    
- Metadata lookups
    
- Object storage API calls
    
- Task scheduling overhead
    

The engine spends more time managing files than processing data.

---

## 2. Query Planning Becomes Expensive

Before reading data, engines must:

```text
List partitions
Read metadata
Build execution plan
```

Example:

```text
10 partitions → milliseconds
100,000 partitions → seconds/minutes
```

Planning time can exceed execution time.

---

## 3. Metadata Explosion

In systems like:

- Hive Metastore
    
- AWS Glue
    
- Unity Catalog
    

every partition generates metadata.

Example:

```text
1,000 partitions → OK

1,000,000 partitions → painful
```

Problems:

- Slow partition discovery
    
- Catalog bottlenecks
    
- Longer query compilation
    

---

## 4. Reduced Parallelism Efficiency

At first glance more partitions sounds good.

But:

```text
10,000 partitions
1 MB each
```

creates:

```text
10,000 Spark tasks
```

Each task may spend:

```text
50 ms scheduling
5 ms processing
```

Most time is wasted on orchestration.

---

## 5. Poor Compression Ratios

Compression algorithms work better on larger datasets.

Example:

```text
500 MB Parquet file
```

compresses efficiently.

Versus:

```text
500 files × 1 MB
```

Compression effectiveness drops.

Result:

- More storage
    
- More I/O
    

---

## 6. Worse Column Statistics

Parquet stores statistics per row group:

```text
min value
max value
null count
```

Small files contain fewer rows.

This means:

- Less useful statistics
    
- Less effective predicate pushdown
    
- Less effective data skipping
    

---

## 7. Increased Cloud Storage Costs

For object stores such as:

- Amazon S3
    
- Azure ADLS
    
- Google Cloud Storage
    

every operation costs money.

Example:

```text
1 file read
```

vs

```text
100,000 file reads
```

More:

- LIST requests
    
- GET requests
    
- Metadata operations
    

Higher cost.

---

## 8. Partition Skew

A common mistake:

Partitioning by high-cardinality columns.

Example:

```text
customer_id
```

with:

```text
10 million customers
```

creates millions of partitions.

Many contain:

```text
0 rows
10 rows
100 rows
```

which is highly inefficient.

---

## Rule of Thumb

A good partition should:

- Eliminate large amounts of irrelevant data
    
- Still contain enough data to justify a file read
    

Typical targets:

|Engine|Recommended File Size|
|---|---|
|Spark|128 MB – 1 GB|
|Databricks|256 MB – 1 GB|
|Trino/Presto|128 MB – 1 GB|
|DuckDB|100 MB+|
|Snowflake|Managed automatically|

---

## Interview Answer

> Very small partitions lead to the small-file problem. Query engines spend more time listing files, reading metadata, and scheduling tasks than processing data. Over-partitioning increases metastore overhead, reduces compression efficiency, weakens predicate pushdown effectiveness, and can significantly increase cloud storage request costs. The goal is to choose partition keys that maximize partition pruning while keeping partition sizes large enough—typically hundreds of MBs per file rather than thousands of tiny files.