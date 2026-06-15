## 7. A daily batch job scans 30 TB but only processes one day of data.

How would you optimize it?

Expected:

* Partition pruning

* Predicate pushdown

* File layout optimization
For a Data Engineering interview, I'd answer this by first identifying **why 30 TB is being scanned when only one day is needed**.

---

## Step 1: Investigate the Root Cause

Questions I'd ask:

- Is the table partitioned?
    
- What is the partition column?
    
- Is the query filtering on the partition column?
    
- Are files organized correctly?
    
- Is the storage format columnar (Parquet/ORC) or row-based (CSV/JSON)?
    
- Are query plans showing partition pruning?
    

A common anti-pattern is:

```sql
SELECT *
FROM sales
WHERE DATE(transaction_ts) = '2026-06-01';
```

Even if data is partitioned by `transaction_dt`, wrapping the column in a function can prevent pruning.

---

## Step 2: Enable Partition Pruning

### Current Layout

```text
sales/
   year=2025/
   year=2026/
```

Query:

```sql
SELECT *
FROM sales
WHERE transaction_dt = '2026-06-01';
```

If partitioning is only by year, the engine may still scan an entire year's worth of data.

### Better Layout

```text
sales/
  year=2026/
    month=06/
      day=01/
      day=02/
```

or

```text
sales/
  dt=2026-06-01/
  dt=2026-06-02/
```

Then:

```sql
WHERE dt = '2026-06-01'
```

allows the engine to read only the required partition.

### Impact

Instead of:

```text
30 TB scanned
```

you may scan:

```text
100 GB scanned
```

or less.

---

## Step 3: Use Predicate Pushdown

### Bad

```sql
SELECT *
FROM sales
WHERE UPPER(region) = 'US';
```

Engine may need to read all rows first.

### Better

```sql
SELECT *
FROM sales
WHERE region = 'US';
```

With Parquet statistics:

```text
min_region = 'APAC'
max_region = 'EU'
```

Entire row groups can be skipped.

Predicate pushdown allows filtering:

- At storage layer
    
- Before rows are loaded into memory
    

Reducing:

```text
I/O
CPU
Memory
Network
```

---

## Step 4: Optimize File Layout

Even with partitions, poor file layout hurts performance.

### Small File Problem

```text
100,000 files
300 MB total partition
```

Problems:

- Metadata overhead
    
- Excessive file opens
    
- Scheduler overhead
    

Compaction:

```text
100,000 files
→
100 files
```

greatly improves scan efficiency.

---

### Appropriate File Sizes

Typical target:

```text
128 MB – 1 GB per file
```

depending on engine:

- Spark
    
- Trino
    
- Snowflake
    
- Databricks
    
- DuckDB
    

---

### Clustering / Sorting

If queries often filter by:

```sql
WHERE region='US'
```

sort data by:

```text
region
```

or use:

- Z-Ordering (Databricks)
    
- Clustering Keys (Snowflake)
    
- Sorting/Bucketing (Hive/Spark)
    

This improves data skipping.

---

## Step 5: Read Only Required Columns

### Bad

```sql
SELECT *
FROM sales
WHERE dt='2026-06-01';
```

### Better

```sql
SELECT
    customer_id,
    amount
FROM sales
WHERE dt='2026-06-01';
```

Columnar formats read only needed columns.

Example:

```text
200 columns table
Need 3 columns

Scan drops dramatically
```

---

## Step 6: Verify Using Query Plans

Check:

```sql
EXPLAIN
```

or

```sql
EXPLAIN ANALYZE
```

Look for:

```text
Partition Filters Applied
Files Pruned
Row Groups Skipped
Bytes Scanned
```

If the plan still shows:

```text
30 TB scanned
```

pruning is not working.

---

## Interview-Ready Answer

> If a daily batch job scans 30 TB but only processes one day's data, I'd first check whether partition pruning is working. The table should be partitioned on the date column being filtered. Next, I'd ensure predicates are pushdown-friendly and avoid functions on partition columns. I'd optimize file layout by using Parquet, compacting small files, and clustering data on frequently filtered columns. I'd also avoid `SELECT *` and verify improvements using EXPLAIN plans and scan metrics. The goal is to reduce data scanned from tens of terabytes to only the partitions, files, and columns required for that day's processing.

### Key Optimization Levers

|Optimization|Benefit|
|---|---|
|Partition Pruning|Skip irrelevant partitions|
|Predicate Pushdown|Skip irrelevant row groups|
|Column Pruning|Read only needed columns|
|File Compaction|Reduce file overhead|
|Clustering/Sorting|Improve data skipping|
|Parquet/ORC|Efficient columnar reads|
|EXPLAIN Analysis|Validate optimization works|

A strong senior-level follow-up is: **"What is the scan-to-output ratio?"** If you're scanning 30 TB to produce 100 GB of output, that's usually a sign that partitioning, pruning, or file organization is not aligned with the access pattern.