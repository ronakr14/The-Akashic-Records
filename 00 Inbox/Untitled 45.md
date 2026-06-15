Why is file size important in batch processing?

File size is one of the biggest factors affecting batch processing performance in data lakes and lakehouses. Even with perfect SQL and cluster sizing, poor file sizing can make jobs 10–100× slower.

## The Core Idea

Processing cost isn't just:

```text
Data Size
```

It's:

```text
Data Size
+
Number of Files
+
Metadata Operations
+
Task Scheduling Overhead
```

Two datasets may both contain 1 TB of data:

```text
Dataset A:
10 files × 100 GB

Dataset B:
1,000,000 files × 1 MB
```

Same data volume, vastly different performance.

---

# Problem 1: Small Files ("Small File Problem")

Suppose:

```text
1 TB
=
1,000,000 files
=
1 MB each
```

Before reading data, the engine must:

```text
List files
Open files
Read metadata
Schedule tasks
Create readers
```

The overhead becomes enormous.

### Symptoms

- Slow query planning
    
- High metadata latency
    
- Long startup times
    
- Excessive task creation
    

Example:

```text
Actual data processing: 5 minutes
Metadata handling: 30 minutes
```

---

# Problem 2: Excessive Task Scheduling

Many engines create tasks per file or file split.

Example:

```text
500,000 files
```

can lead to:

```text
500,000 tasks
```

The scheduler becomes the bottleneck.

Common symptoms:

```text
High driver CPU
Task scheduling delays
Executor idle time
```

---

# Problem 3: Object Storage Penalties

With cloud storage:

- Amazon Web Services S3
    
- Google Cloud Storage
    
- Microsoft Blob Storage
    

every file operation requires:

```text
LIST
GET
HEAD
```

calls.

Example:

```text
10 files
```

vs

```text
1,000,000 files
```

The second can spend significant time just talking to storage.

---

# Problem 4: Large Files Reduce Parallelism

The opposite extreme is also bad.

Example:

```text
1 file = 5 TB
```

Only a few workers can process it at once.

Result:

```text
Cluster: 100 workers
Workers utilized: 2
```

Most resources sit idle.

---

# Problem 5: Skewed Processing

Suppose:

```text
File A = 1 GB
File B = 500 GB
```

One task finishes quickly:

```text
1 minute
```

Another takes:

```text
45 minutes
```

This creates stragglers and poor cluster utilization.

---

# Problem 6: Poor Predicate Pushdown Efficiency

Columnar formats such as:

- Parquet
    
- ORC
    

store statistics per file and row group.

If files are poorly sized:

```text
Huge files
```

the engine may still need to read substantial data.

Properly sized files improve:

- Data skipping
    
- Predicate pushdown
    
- Partition pruning effectiveness
    

---

# Problem 7: Compaction Costs

Small files accumulate over time.

Example:

```text
1000 daily jobs
↓
100 files per job
↓
100,000 files
```

Eventually you must run:

```text
OPTIMIZE
COMPACT
REWRITE DATA FILES
```

Maintenance becomes expensive.

Common in:

- Delta Lake
    
- Apache Iceberg
    
- Apache Hudi
    

---

# Ideal File Sizes

Typical recommendations:

|Format|Recommended Size|
|---|---|
|Parquet|128 MB – 1 GB|
|ORC|128 MB – 1 GB|
|Delta/Iceberg/Hudi|256 MB – 1 GB|

Many lakehouse teams target:

```text
256–512 MB
```

as a practical sweet spot.

---

# Real Example

Imagine:

```text
10 TB dataset
```

### Bad

```text
10 million files
1 MB each
```

Problems:

- Metadata explosion
    
- Scheduling overhead
    
- Slow planning
    

---

### Bad

```text
2 files
5 TB each
```

Problems:

- Low parallelism
    
- Long-running tasks
    

---

### Good

```text
20,000 files
500 MB each
```

Benefits:

- Efficient parallelism
    
- Low metadata overhead
    
- Good storage throughput
    

---

# Interview Answer

> File size directly affects metadata overhead, task scheduling, parallelism, and storage efficiency. Very small files create excessive metadata operations and scheduling overhead, while very large files reduce parallelism and can create straggler tasks. In modern lakehouses, the goal is to maintain files large enough to avoid the small-file problem but small enough to enable efficient parallel processing. For Parquet-based workloads, file sizes around 128 MB to 1 GB are typically recommended, with many organizations targeting 256–512 MB as a balance between throughput and scalability.