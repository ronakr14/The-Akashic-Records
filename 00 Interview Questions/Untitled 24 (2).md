How would you compact files in a data lake?

This is a very common senior Data Engineering and Lakehouse interview question because **small files are one of the biggest performance killers** in data lakes.

---

# Why Compaction Is Needed

Over time, ingestion jobs create thousands or millions of small files.

Example:

```text
1 TB table

10,000 files × 100 MB  ✅

vs

5,000,000 files × 200 KB ❌
```

Problems:

- High metadata overhead
    
- Slow query planning
    
- Excessive file open/close operations
    
- Poor scan efficiency
    
- Higher cloud storage API costs
    
- Poor Spark parallelism
    

---

# My Approach

## Step 1: Identify Small-File Candidates

Collect metrics:

```text
File count
Average file size
Median file size
Partition file count
```

Example:

```text
sales/
├── dt=2026-06-01 (50,000 files)
├── dt=2026-06-02 (45,000 files)
├── dt=2026-06-03 (60,000 files)
```

A metadata scanner can flag:

```text
avg_file_size < 32 MB
```

for compaction.

---

# Step 2: Choose Target File Size

Typical targets:

|Engine|Recommended|
|---|---|
|Spark|128–512 MB|
|Delta Lake|~256 MB|
|Iceberg|256–1024 MB|
|Hudi|128–512 MB|

Rule:

```text
Large enough for efficient scans
Small enough for parallelism
```

---

# Step 3: Compact Within Partitions

Never compact across partition boundaries.

Bad:

```text
dt=2026-06-01
dt=2026-06-02
```

merged together.

Good:

```text
Compact files only inside
dt=2026-06-01
```

This preserves partition pruning.

---

# Step 4: Rewrite Files

Read:

```text
1000 files × 1 MB
```

Write:

```text
4 files × 250 MB
```

Spark example:

```python
df = spark.read.parquet(path)

df.repartition(4) \
  .write.mode("overwrite") \
  .parquet(path)
```

---

# Delta Lake

Use:

```sql
OPTIMIZE sales;
```

or

```sql
OPTIMIZE sales
WHERE dt='2026-06-01';
```

Delta automatically:

- Combines files
    
- Rewrites data
    
- Preserves table semantics
    

Entity: Delta Lake

---

# Apache Iceberg

Use:

```sql
CALL system.rewrite_data_files(
  table => 'sales'
);
```

Iceberg rewrites small files into larger files.

Entity: Apache Iceberg

---

# Apache Hudi

Use:

```sql
RUN COMPACTION
```

or scheduled compaction services.

Entity: Apache Hudi

---

# Step 5: Preserve Data Correctness

During compaction:

- No records lost
    
- No duplicates introduced
    
- ACID guarantees maintained
    

Validation:

```text
Row counts before/after
Checksums
Partition totals
```

---

# Step 6: Automate Compaction

Production systems should not rely on manual compaction.

Common triggers:

### File Count Threshold

```text
files > 1000
```

---

### Average File Size

```text
avg_file_size < 64 MB
```

---

### Scheduled Job

```text
Daily
Weekly
```

---

### Growth-Based

```text
New files added > 20%
```

---

# Advanced Optimization

Compaction is often combined with:

## Clustering

Rewrite files ordered by:

```text
customer_id
region
date
```

Improves locality.

---

## Z-Ordering

Popular in Delta.

```sql
OPTIMIZE sales
ZORDER BY (customer_id);
```

Improves data skipping.

---

## Sorting

Iceberg example:

```text
Sort by customer_id
```

before rewriting files.

This improves scan efficiency.

---

# Things to Watch Out For

### Over-Compaction

Bad:

```text
1 file = 5 TB
```

Now only one task can read it.

---

### Competing With Ingestion

Compaction can interfere with writers.

Solutions:

- ACID table formats
    
- Off-peak scheduling
    
- Snapshot isolation
    

---

### Rewriting Hot Partitions Repeatedly

Avoid compacting partitions that are still receiving data.

Example:

```text
Compact only partitions older than 2 days
```

---

# Senior-Level Answer

> I would first identify partitions suffering from the small-file problem using metadata metrics such as file count and average file size. Then I would rewrite files within each partition to a target size, typically 128–512 MB depending on the engine. For modern lakehouse formats such as Delta Lake, Apache Iceberg, or Apache Hudi, I would use their native compaction mechanisms because they maintain transactional correctness. Finally, I would automate compaction based on thresholds such as file count, average file size, or partition growth, and combine it with clustering or sorting to improve future query performance.