Given a query plan, how would you identify:
* Expensive joins
* Full table scans
* Data skew
* Excessive shuffles
This is a very common **Spark, Databricks, Snowflake, BigQuery, and Lakehouse optimization interview question**.

The interviewer wants to see whether you can read a query plan and quickly identify the operators that dominate cost.

---

# Step 1: Start with EXPLAIN

Examples:

```sql
EXPLAIN
SELECT ...
```

or

```sql
EXPLAIN ANALYZE
SELECT ...
```

Look for:

```text
Scan
Filter
Join
Exchange
Aggregate
Sort
```

These operators usually consume most resources.

---

# 1. Identifying Expensive Joins

## What to Look For

### Large Inputs

```text
Hash Join
  Left: 2 TB
  Right: 500 GB
```

Large join inputs usually mean:

```text
High CPU
High memory
Large shuffle
```

---

### Join Type

Cost ranking (roughly):

```text
Broadcast Join      Cheapest
Hash Join
Merge Join
Nested Loop Join    Most Expensive
```

If you see:

```text
Nested Loop Join
```

that's an immediate red flag.

---

### Many-to-Many Joins

Example:

```text
Customers: 100M rows
Orders: 1B rows
```

Join output:

```text
50B rows
```

This indicates join explosion.

Look for:

```text
Output Rows >> Input Rows
```

---

### Missing Filters Before Join

Bad:

```text
Scan Orders (5 TB)
Scan Customers (1 TB)
Join
Filter region='APAC'
```

Better:

```text
Filter Orders
Filter Customers
Join
```

---

### Interview Signal

Ask:

```text
Can predicates be pushed before the join?
Can a broadcast join be used?
Can the join cardinality be reduced?
```

---

# 2. Identifying Full Table Scans

Look for:

```text
Table Scan
```

or

```text
Seq Scan
```

or

```text
Parquet Scan
```

with:

```text
PartitionFilters: []
PushedFilters: []
```

Example:

```text
Scan orders
Rows: 10 billion
```

while query asks for:

```sql
WHERE order_date='2026-06-01'
```

This suggests:

```text
No partition pruning
No predicate pushdown
```

---

### Common Symptoms

```text
Bytes Read = Huge
Rows Returned = Tiny
```

Example:

```text
20 TB scanned
100 rows returned
```

Major optimization opportunity.

---

# 3. Identifying Data Skew

Data skew occurs when some partitions are much larger than others.

---

## Query Plan Clues

Example:

```text
200 tasks

199 tasks = 20 seconds
1 task = 45 minutes
```

Classic skew.

---

### Runtime Metrics

Look for:

```text
Max task duration
Median task duration
```

Example:

```text
Median = 15 sec
Max = 3200 sec
```

Huge skew.

---

### Partition Size Imbalance

```text
Partition 1 = 2 GB
Partition 2 = 3 GB
Partition 3 = 500 GB
```

One worker becomes the bottleneck.

---

### Join Skew

Example:

```text
customer_id = 123
```

represents:

```text
40% of dataset
```

during join.

This creates:

```text
Hot partition
Long-running task
```

---

### Spark Indicators

Look for:

```text
Skewed partition detected
```

or:

```text
Task duration variance
```

in Spark UI.

---

# 4. Identifying Excessive Shuffles

Shuffles are often the biggest performance killer.

---

## Query Plan Clues

Look for operators such as:

```text
Exchange
Shuffle Exchange
Repartition
Sort Merge Join
```

Example:

```text
Scan
 ↓
Exchange
 ↓
Join
 ↓
Exchange
 ↓
Aggregate
 ↓
Exchange
```

Many exchanges indicate heavy data movement.

---

### Shuffle Metrics

Look at:

```text
Shuffle Read
Shuffle Write
```

Example:

|Metric|Value|
|---|---|
|Input|500 GB|
|Shuffle|8 TB|

Huge warning sign.

---

### Large GROUP BY

```sql
GROUP BY customer_id
```

on:

```text
5 billion rows
```

usually causes large shuffles.

---

### Large JOIN

```sql
JOIN customers
```

without broadcast.

Likely:

```text
Shuffle left side
Shuffle right side
Join
```

---

### Symptoms

```text
High network traffic
Disk spills
Long stage durations
```

often point directly to shuffle issues.

---

# Practical Query Plan Review Checklist

When reading any plan, ask:

### Scan Layer

```text
Are partitions being pruned?
Are filters pushed down?
Are full scans occurring?
```

---

### Join Layer

```text
Join type?
Broadcast possible?
Join explosion?
Large input sizes?
```

---

### Shuffle Layer

```text
How many exchanges?
Shuffle volume?
Sort operations?
```

---

### Skew Layer

```text
Task imbalance?
Partition imbalance?
Long tail tasks?
```

---

# Interview Answer

> When reviewing a query plan, I first look at scan operators to identify full table scans and verify partition pruning and predicate pushdown. Next, I examine joins, focusing on join type, input cardinality, and whether a broadcast join could replace a shuffle join. For data skew, I compare partition sizes and task durations, looking for large variance or long-running straggler tasks. Finally, I inspect Exchange or Shuffle operators and runtime metrics such as shuffle read/write volume, spills, and network I/O to identify excessive data movement. The operators with the highest scan volume, shuffle volume, or cardinality growth usually represent the primary optimization opportunities.