Explain how partition pruning works in a lakehouse.

This is one of the most important performance concepts in modern lakehouses. A strong answer should connect **partitioning → metadata → file elimination → reduced I/O**.

---

# What is Partition Pruning?

Partition pruning is a query optimization technique where the engine **skips reading partitions that cannot satisfy the query filter**.

Instead of:

```text
Read all data
Filter later
```

the engine does:

```text
Identify relevant partitions
Read only those partitions
```

This dramatically reduces:

- Data scanned
    
- Disk I/O
    
- Network transfer
    
- Query execution time
    
- Compute cost
    

---

# Example

Suppose we have a sales table partitioned by date:

```text
sales/
   sale_date=2026-06-01/
   sale_date=2026-06-02/
   sale_date=2026-06-03/
   sale_date=2026-06-04/
```

Each partition contains:

```text
1 TB
```

Total table size:

```text
4 TB
```

---

## Query Without Pruning

```sql
SELECT *
FROM sales
WHERE amount > 100;
```

The engine doesn't know which partitions contain matching rows.

Result:

```text
Read all 4 TB
```

---

## Query With Pruning

```sql
SELECT *
FROM sales
WHERE sale_date = '2026-06-04';
```

The engine examines partition metadata:

```text
sale_date=2026-06-01
sale_date=2026-06-02
sale_date=2026-06-03
sale_date=2026-06-04
```

It immediately knows only one partition can match.

Result:

```text
Read 1 TB
Skip 3 TB
```

---

# How It Works Internally

Consider a table stored in:

- Apache Iceberg
    
- Delta Lake
    
- Apache Hudi
    

The table metadata contains information such as:

```text
Partition Key
Partition Values
File Locations
Statistics
```

When a query arrives:

```sql
WHERE sale_date='2026-06-04'
```

The optimizer:

1. Reads metadata
    
2. Finds matching partitions
    
3. Builds a reduced scan plan
    
4. Opens only relevant files
    

No need to inspect every file.

---

# Visual Example

Without pruning:

```text
sales
│
├── 2026-06-01
├── 2026-06-02
├── 2026-06-03
└── 2026-06-04

Read all partitions
```

With pruning:

```text
sales
│
├── 2026-06-01  SKIP
├── 2026-06-02  SKIP
├── 2026-06-03  SKIP
└── 2026-06-04  READ
```

---

# Why It Matters

Imagine:

```text
100 TB table
365 daily partitions
```

Query:

```sql
WHERE sale_date='2026-06-04'
```

Without pruning:

```text
Scan 100 TB
```

With pruning:

```text
Scan ~274 GB
```

Huge reduction in cost and runtime.

---

# Partition Pruning vs Predicate Pushdown

These concepts are related but different.

### Partition Pruning

Eliminates partitions.

Example:

```sql
WHERE sale_date='2026-06-04'
```

Engine skips entire directories/files.

---

### Predicate Pushdown

Eliminates rows within files.

Example:

```sql
WHERE customer_id=100
```

Using Parquet statistics, the engine may skip row groups inside a file.

---

Think of it as:

```text
Partition Pruning
    ↓
Choose files

Predicate Pushdown
    ↓
Choose row groups
```

Both work together.

---

# Good Partition Keys

Partition pruning is only effective when queries filter on the partition column.

### Good

Orders table:

```text
sale_date
```

Common query:

```sql
WHERE sale_date BETWEEN ...
```

Excellent pruning.

---

### Bad

Partition by:

```text
customer_name
```

Queries rarely filter on it.

Pruning provides little value.

---

# Common Mistakes

## Filtering on Non-Partition Columns

Partitioned by:

```text
sale_date
```

Query:

```sql
WHERE product_id=123
```

Result:

```text
No partition pruning
```

All partitions may be scanned.

---

## Over-Partitioning

Example:

```text
customer_id
```

Millions of partitions.

Problems:

- Metadata explosion
    
- Small files
    
- Slow planning
    

---

## Under-Partitioning

Example:

```text
country
```

Only 3 partitions.

One partition may contain tens of terabytes.

Pruning becomes ineffective.

---

# Lakehouse Improvements

Modern table formats improve pruning beyond directory structures.

### Iceberg Hidden Partitioning

In Apache Iceberg, users can query:

```sql
WHERE order_timestamp >= '2026-06-01'
```

while Iceberg automatically maps that to partition metadata.

This avoids exposing partition implementation details.

---

### File-Level Statistics

Modern lakehouses store:

```text
min value
max value
record count
null count
```

per file.

This enables additional pruning even within a partition.

---

# Interview Answer (2-Minute Version)

> Partition pruning is a query optimization technique that reduces the amount of data scanned by eliminating partitions that cannot satisfy a query filter. In a lakehouse, tables are often partitioned by columns such as date, region, or event time. When a query includes a filter on the partition key, the optimizer uses table metadata to identify relevant partitions and skips the rest. For example, if a 100 TB sales table is partitioned by `sale_date` and a query requests one day of data, the engine may scan only a few hundred gigabytes instead of the entire table. This significantly reduces I/O, network traffic, compute usage, and query runtime. Modern lakehouse formats like Apache Iceberg and Delta Lake enhance partition pruning with metadata and file-level statistics, allowing even more efficient data skipping.