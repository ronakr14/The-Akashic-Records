What problems do small files create?
Expected:
* Metadata overhead
* Slow planning
* Inefficient scans
This is a very common lakehouse and Spark interview question.

## What Problems Do Small Files Create?

Small files are one of the biggest performance killers in distributed data systems.

Imagine:

```text
1 TB data
```

stored as:

### Good

```text
1000 files × 1 GB
```

vs

### Bad

```text
1,000,000 files × 1 MB
```

The amount of data is identical, but performance can be dramatically worse.

---

## 1. Metadata Overhead

Before reading data, the engine must:

```text
List files
Read file metadata
Read Parquet footers
Build execution plan
```

For a few hundred files this is cheap.

For millions of files:

```text
1,000,000 metadata operations
```

becomes expensive.

Common symptoms:

- Slow query startup
    
- Slow partition discovery
    
- Increased catalog pressure
    

In systems like:

- Hive Metastore
    
- AWS Glue
    
- Unity Catalog
    

metadata operations can become a bottleneck.

---

## 2. Slow Query Planning

Query execution begins with planning.

Example:

```sql
SELECT COUNT(*)
FROM sales
WHERE dt='2026-06-01';
```

Spark first needs to determine:

```text
Which files exist?
Which partitions exist?
Which files should be read?
```

With:

```text
100 files
```

planning is fast.

With:

```text
500,000 files
```

planning can take minutes before any data is processed.

Sometimes:

```text
Planning Time > Execution Time
```

which is a major red flag.

---

## 3. Inefficient Scans

Distributed engines prefer reading large contiguous chunks.

Large files:

```text
512 MB
1 GB
```

allow efficient sequential reads.

Tiny files cause:

```text
Open file
Read 1 MB
Close file

Open next file
Read 1 MB
Close file
```

Repeated thousands of times.

Result:

- More I/O operations
    
- More network requests
    
- Lower throughput
    

The engine spends more time opening files than reading data.

---

## 4. Task Scheduling Overhead

In Spark:

```text
1 file ≈ 1 task
```

(roughly speaking)

Example:

### Good

```text
1000 files
1000 tasks
```

### Bad

```text
500,000 files
500,000 tasks
```

Each task has overhead:

```text
Task creation
Serialization
Scheduling
Monitoring
Cleanup
```

If processing takes:

```text
5 ms
```

and scheduling takes:

```text
50 ms
```

most time is wasted on orchestration.

---

## 5. Reduced Compression Efficiency

Compression works better with larger datasets.

Example:

```text
1 GB Parquet file
```

allows:

- Better dictionary encoding
    
- Better run-length encoding
    
- Better compression ratios
    

Tiny files:

```text
1 MB
```

contain limited data.

Result:

- Larger storage footprint
    
- More data read from disk
    

---

## 6. Poor Predicate Pushdown Effectiveness

Parquet stores statistics per row group:

```text
min value
max value
null count
```

Large files usually contain:

```text
many row groups
```

providing rich statistics.

Tiny files often have:

```text
very few rows
```

which reduces the effectiveness of:

- Predicate pushdown
    
- Data skipping
    

The engine ends up reading more files than necessary.

---

## 7. Higher Cloud Storage Costs

Object stores charge per request.

Examples:

- Amazon S3
    
- Google Cloud Storage
    
- Microsoft Azure ADLS
    

Small files increase:

```text
LIST requests
GET requests
Metadata operations
```

Example:

```text
100 files
```

vs

```text
1,000,000 files
```

can create a noticeable cost difference.

---

## 8. Poor Parallelism Efficiency

More files does not always mean better parallelism.

Example:

```text
500,000 files
1 MB each
```

creates excessive scheduling overhead.

Conversely:

```text
1000 files
256 MB each
```

typically provides enough parallelism without overwhelming the scheduler.

---

## How to Fix Small File Problems

### Compaction

Merge:

```text
100,000 files
```

into:

```text
500 files
```

---

### Appropriate File Sizes

Typical targets:

|Engine|Recommended Size|
|---|---|
|Spark|128 MB – 1 GB|
|Databricks|256 MB – 1 GB|
|Trino|128 MB – 1 GB|
|DuckDB|100 MB+|

---

### Avoid Over-Partitioning

Bad:

```text
year/month/day/hour/minute
```

for low-volume datasets.

Better:

```text
date
```

or

```text
date/hour
```

when justified.

---

## Interview Answer

> Small files create three major problems. First, they increase metadata overhead because the engine must track and open a large number of files. Second, they slow query planning since partition discovery and file enumeration become expensive. Third, they make scans inefficient because the engine spends more time opening and managing files than reading data. Additional effects include excessive Spark task scheduling, poorer compression, reduced predicate pushdown effectiveness, and higher object storage request costs. The typical solution is file compaction and choosing partition strategies that produce files in the 128 MB–1 GB range rather than thousands of tiny files.