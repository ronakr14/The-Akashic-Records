A query reads 10 TB to return 100 rows.

This is a classic data engineering and query optimization interview question.

## Immediate Observation

A query reading **10 TB** and returning **100 rows** indicates extremely poor selectivity and/or inefficient data access.

The key metric is:

```text
Read:     10 TB
Output:   100 rows
Efficiency: Terrible
```

The result size is tiny, but the engine is forced to scan almost everything.

---

# How I Would Investigate

## 1. Check Execution Plan

First step:

```sql
EXPLAIN
```

or

```sql
EXPLAIN ANALYZE
```

Questions:

- Is the engine performing a full table scan?
    
- Are filters being pushed down?
    
- Is partition pruning happening?
    
- Are indexes being used?
    
- Is there a large join causing the scan?
    

---

# 2. Check Predicate Pushdown

Example:

Bad:

```sql
SELECT *
FROM sales
WHERE YEAR(order_date)=2025;
```

The function prevents pushdown.

Better:

```sql
SELECT *
FROM sales
WHERE order_date >= '2025-01-01'
AND order_date < '2026-01-01';
```

Now the engine can eliminate partitions/files early.

---

# 3. Check Partition Pruning

Suppose table is partitioned by:

```text
year/month/day
```

Query:

```sql
WHERE customer_id = 123
```

The engine may scan every partition.

Better:

```sql
WHERE year=2025
  AND month=6
  AND customer_id=123
```

Only relevant partitions are read.

---

# 4. Verify Column Pruning

Bad:

```sql
SELECT *
```

The engine reads every column.

Good:

```sql
SELECT customer_id, revenue
```

For Parquet/Delta/Iceberg:

- only required columns are read
    
- scan volume drops dramatically
    

---

# 5. Examine File Format

If data is stored as:

```text
CSV
JSON
```

the engine must read everything.

Better:

- Parquet
    
- Iceberg
    
- Delta
    
- ORC
    

These support:

- predicate pushdown
    
- statistics
    
- column pruning
    

---

# 6. Look for Missing Data Skipping

Modern lakehouse formats maintain file statistics.

Example:

```text
File A:
customer_id min=1
customer_id max=1000

File B:
customer_id min=1001
customer_id max=2000
```

Query:

```sql
WHERE customer_id=1500
```

Engine should skip File A entirely.

If not:

```text
10 TB scan
```

becomes inevitable.

---

# 7. Investigate Join Strategy

Sometimes the 10 TB comes from a join.

Example:

```sql
customers
JOIN orders
JOIN transactions
```

before filtering.

Bad plan:

```text
Join huge tables
Then filter
```

Good plan:

```text
Filter first
Then join
```

This reduces intermediate data massively.

---

# 8. Check Statistics

Optimizers rely on table statistics.

Missing stats often cause:

```text
Bad join order
Bad join type
Unnecessary scans
```

Refresh stats:

```sql
ANALYZE TABLE
```

(or equivalent)

---

# 9. Look for Data Skew

Example:

```sql
WHERE country='US'
```

If 80% of rows are US:

```text
Huge scan
Large shuffle
```

despite a small final result.

---

# 10. Evaluate Indexing / Clustering

In OLTP systems:

- B-tree indexes
    
- Bitmap indexes
    

In lakehouses:

- Z-ordering
    
- Clustering
    
- Sorting
    
- Bloom filters
    

Example:

```text
Cluster by customer_id
```

allows selective reads.

---

# Root Causes I Would Suspect First

Ranked by likelihood:

1. Full table scan
    
2. Missing partition pruning
    
3. Predicate pushdown failure
    
4. Poor file format (CSV/JSON)
    
5. Bad join order
    
6. Missing statistics
    
7. Lack of clustering/data skipping
    
8. Data skew
    

---

# Interview-Style Answer

> If a query reads 10 TB to return 100 rows, I would first inspect the execution plan to determine why the scan volume is so high. I would verify partition pruning, predicate pushdown, column pruning, and file statistics usage. Then I would examine join ordering, clustering strategy, and optimizer statistics. My goal would be to reduce data scanned as early as possible, because the biggest performance gains usually come from eliminating unnecessary I/O rather than adding compute resources. A well-optimized query returning 100 rows should typically read MBs or GBs, not tens of terabytes.