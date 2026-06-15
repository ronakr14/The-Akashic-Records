Explain predicate pushdown and why it matters in batch processing.

**Predicate pushdown** is an optimization where filters are applied **as close to the data source as possible**, so unnecessary data is never read in the first place.

Instead of:

```text
Storage
  ↓
Read 100 TB
  ↓
Filter 99.9 TB
  ↓
Process 100 GB
```

You want:

```text
Storage
  ↓
Filter at source
  ↓
Read 100 GB
  ↓
Process 100 GB
```

---

## Simple Example

Suppose you have a 100 TB orders table:

```sql
SELECT *
FROM orders
WHERE order_date = '2026-06-01';
```

Without predicate pushdown:

```text
Read entire 100 TB
↓
Apply filter in Spark
↓
Keep 100 GB
```

With predicate pushdown:

```text
Storage engine reads only matching data
↓
100 GB scanned
↓
100 GB processed
```

The query result is identical, but the cost and runtime are dramatically lower.

---

## Why It Matters in Batch Processing

### 1. Reduces I/O

In large batch jobs, reading data is often the most expensive operation.

Example:

|Scenario|Data Read|
|---|---|
|No pushdown|100 TB|
|Pushdown|100 GB|

That's a **1000x reduction** in data scanned.

---

### 2. Faster Job Execution

Less data read means:

- Less network traffic
    
- Less decompression
    
- Less CPU work
    
- Less memory consumption
    

A job that takes:

```text
4 hours
```

might complete in:

```text
15 minutes
```

after effective pushdown.

---

### 3. Lower Cloud Costs

Many systems charge based on bytes scanned.

Examples include:

- Amazon Athena
    
- Google BigQuery
    
- Snowflake
    

Scanning:

```text
100 TB
```

vs

```text
100 GB
```

can mean a huge cost difference.

---

### 4. Reduces Shuffle Volume

If filtering happens early:

```sql
SELECT region, SUM(amount)
FROM sales
WHERE region = 'APAC'
GROUP BY region;
```

Only APAC records participate in downstream operations.

This reduces:

- Shuffle size
    
- Memory pressure
    
- Spill-to-disk risk
    

---

## How Predicate Pushdown Works

### Row-Based Databases

The database applies:

```sql
WHERE customer_id = 123
```

before returning rows.

```text
Database
  ↓
Matching rows only
  ↓
Application
```

---

### Columnar Formats (Parquet)

Parquet stores statistics per row group:

```text
Row Group 1
min_date = 2026-01-01
max_date = 2026-01-31

Row Group 2
min_date = 2026-02-01
max_date = 2026-02-28
```

Query:

```sql
WHERE order_date = '2026-06-01'
```

The engine can skip entire row groups whose min/max ranges don't match.

This is sometimes called **data skipping** and is a major reason Parquet performs so well.

---

## Predicate Pushdown vs Partition Pruning

These are related but different.

### Partition Pruning

Uses folder/partition metadata.

Example:

```text
orders/
 ├── dt=2026-06-01
 ├── dt=2026-06-02
 └── dt=2026-06-03
```

Query:

```sql
WHERE dt='2026-06-01'
```

Only one partition is read.

---

### Predicate Pushdown

Occurs inside files.

Example:

```sql
WHERE customer_id = 1001
```

The engine uses file metadata/statistics to avoid reading irrelevant blocks.

---

### Best Case

Both happen together:

```sql
SELECT *
FROM orders
WHERE dt='2026-06-01'
  AND customer_id=1001;
```

1. Partition pruning skips most folders.
    
2. Predicate pushdown skips most row groups.
    
3. Very little data is actually read.
    

---

## When Pushdown Doesn't Work

### Functions on Columns

Bad:

```sql
WHERE YEAR(order_date) = 2026
```

Engine often cannot push this efficiently.

Better:

```sql
WHERE order_date >= '2026-01-01'
  AND order_date < '2027-01-01'
```

---

### Non-Pushdownable Expressions

Bad:

```sql
WHERE UPPER(region) = 'APAC'
```

Better:

```sql
WHERE region = 'APAC'
```

---

### Complex UDFs

```sql
WHERE custom_python_function(col)
```

The storage layer doesn't understand the UDF, so pushdown is typically impossible.

---

## How to Verify

In Spark:

```sql
EXPLAIN
SELECT *
FROM orders
WHERE dt='2026-06-01';
```

Look for:

```text
PushedFilters
PartitionFilters
```

In query plans.

---

## Interview Answer

> Predicate pushdown is an optimization where filter conditions are executed as close to the data source as possible, allowing irrelevant data to be skipped before it is read. In batch processing, this significantly reduces I/O, network transfer, memory usage, and execution time. For large datasets, predicate pushdown can reduce scans from terabytes to gigabytes. It works especially well with columnar formats like Parquet, where file and row-group statistics allow entire blocks of data to be skipped. It's often used alongside partition pruning to minimize the amount of data processed.