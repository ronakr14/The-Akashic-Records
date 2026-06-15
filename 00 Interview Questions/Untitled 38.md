What problems occur when partitions become too large?

When partitions become **too large**, you lose many of the performance benefits that partitioning was supposed to provide.

### 1. Poor Partition Pruning

The query engine has to scan a large amount of data even when you're interested in a small subset.

**Example**

Instead of:

```
orders/
 ├── date=2026-06-01
 ├── date=2026-06-02
 └── date=2026-06-03
```

You have:

```
orders/
 ├── year=2026
```

Query:

```sql
SELECT *
FROM orders
WHERE order_date = '2026-06-03';
```

The engine may need to scan a huge yearly partition instead of a single day.

**Result:** Higher I/O and slower queries.

---

### 2. Large Data Scans

Large partitions increase:

- Storage reads
    
- Network transfer
    
- CPU decompression costs
    

Example:

|Partition Strategy|Data Read|
|---|---|
|Daily partition|100 GB|
|Yearly partition|36 TB|

Same query, dramatically different scan volume.

---

### 3. Reduced Parallelism

Most distributed engines parallelize work at the partition/file level.

If you have:

```
1 partition = 10 TB
```

only a limited number of tasks can work simultaneously.

Better:

```
100 partitions = 100 GB each
```

Many workers can process in parallel.

---

### 4. Longer Job Recovery

Suppose a Spark job fails after processing:

```
date=2026-06-01
```

If the partition is:

```
year=2026
```

you may need to reprocess huge amounts of data.

Large partitions increase recovery time and restart costs.

---

### 5. Expensive Updates and Rewrites

Many lakehouse formats rewrite data at file/partition granularity.

Example:

```
year=2026 partition = 10 TB
```

Updating a small percentage of rows may trigger substantial file rewrites.

Common with:

- Delta Lake
    
- Iceberg
    
- Hudi
    

---

### 6. Metadata Hotspots

Large partitions often contain thousands of files.

Example:

```
date=2026-06-01
 ├── file1.parquet
 ├── file2.parquet
 ...
 ├── file50000.parquet
```

The engine spends time:

- Listing files
    
- Reading metadata
    
- Planning queries
    

before actual execution begins.

---

### 7. Data Skew

One partition may become disproportionately large.

Example:

```
country=US      20 TB
country=India    3 TB
country=Canada  500 GB
```

Queries involving the US partition become bottlenecks.

Symptoms:

- Straggler tasks
    
- Uneven executor utilization
    
- Long tail latency
    

---

### 8. Slow Compaction and Maintenance

Operations such as:

- OPTIMIZE
    
- VACUUM
    
- RECLUSTER
    
- File compaction
    

must process huge partitions.

A maintenance job that should take minutes may take hours.

---

### 9. Memory Pressure

Large partitions often create large shuffle blocks.

Example:

```sql
GROUP BY customer_id
```

against a multi-terabyte partition.

Can lead to:

- Executor OOM
    
- Spill to disk
    
- Slow shuffles
    

---

## Rule of Thumb for Data Engineering Interviews

You generally want partitions that are:

- **Not too small** → avoid millions of tiny files.
    
- **Not too large** → avoid scanning terabytes per partition.
    

A commonly cited target is:

|Metric|Recommended|
|---|---|
|Partition size|1–100 GB|
|Parquet file size|128 MB–1 GB|
|Rows per partition|Depends on row width and workload|

---

### Interview Sound Bite

> Small partitions create metadata overhead and tiny-file problems. Large partitions reduce partition pruning, increase scan costs, create skew, and limit parallelism. The goal is to balance metadata efficiency with query selectivity, typically targeting partitions that are large enough to avoid tiny files but small enough to enable effective pruning and parallel execution.