---
type: concept
---

Now we're getting into the performance engineering side of lakehouses.

Before learning Z-Ordering, challenge one assumption:

Many engineers think:

```text
Partitioning = Fast Queries
```

Not always.

At small scale, yes.

At TB/PB scale, partitioning alone becomes insufficient.

---

# The Problem

Suppose you have a Delta table:

```sql
sales
```

Partitioned by:

```sql
sale_date
```

Storage:

```text
2026-01-01/
2026-01-02/
2026-01-03/
...
```

Query:

```sql
SELECT *
FROM sales
WHERE customer_id = 12345
```

Partitioning doesn't help.

Because data inside each partition looks like:

```text
2026-01-01.parquet

CustomerID
-----------
100
200
12345
500
800
300
```

Customer IDs are scattered everywhere.

Spark still scans many files.

---

# What We Want

Imagine all records for customer 12345 are physically near each other.

```text
File 1
-------
100
101
102

File 2
-------
12340
12341
12345
12346
12348

File 3
-------
90000
90001
```

Now Spark can skip most files.

That's the idea behind Z-Ordering.

---

# Simple Definition

Z-Ordering reorganizes data so that records with similar values are stored physically close together.

Think:

```text
Sort Data
+
Optimize File Layout
+
Improve Data Skipping
```

---

# Single Column Example

Without Z-Order:

```text
CustomerID

500
12
900
123
8
400
```

After Z-Order on customer_id:

```text
8
12
123
400
500
900
```

Looks like sorting.

For one column, Z-Order behaves very similarly to sorting.

---

# Multi-Column Problem

Suppose queries are:

```sql
WHERE country='NL'
AND customer_id=12345
```

Which should we sort by?

```text
country ?
customer_id ?
```

Normal sorting can only prioritize one ordering effectively.

This is where Z-Order becomes clever.

---

# The Space-Filling Curve Idea

Imagine coordinates:

```text
(country, customer_id)
```

Example:

```text
(NL, 100)
(NL, 101)
(NL, 102)

(US, 500)
(US, 501)
```

Z-Ordering converts multiple dimensions into a single ordering.

Conceptually:

```text
2D Space
      ↓
1D Sequence
      ↓
Physical Storage Layout
```

The algorithm interleaves bits from multiple columns.

---

# Bit Interleaving Example

Suppose:

```text
Country = 01
CustomerID = 11
```

Interleave:

```text
0 1 1 1
```

Another row:

```text
Country = 00
CustomerID = 10
```

Becomes:

```text
0 1 0 0
```

Rows are then ordered using these generated values.

This creates a Z-shaped traversal pattern.

Hence:

```text
Z-Order
```

---

# Visual Representation

Imagine a grid:

```text
1   2   5   6
3   4   7   8
9  10  13  14
11 12  15  16
```

Traversal path:

```text
Z
```

instead of:

```text
Row by Row
```

Nearby points remain mostly nearby after conversion.

This is the magic.

---

# Why Delta Lake Uses It

Suppose:

```sql
OPTIMIZE sales
ZORDER BY (customer_id)
```

Delta rewrites files.

Before:

```text
File1
File2
File3
File4
File5
```

Customer IDs spread everywhere.

After:

```text
File1 -> IDs 1-1000
File2 -> IDs 1001-2000
File3 -> IDs 2001-3000
```

Now Parquet statistics become powerful.

Remember:

```text
Min ID
Max ID
```

stored in every file.

After Z-Order:

```text
File1
Min=1
Max=1000

File2
Min=1001
Max=2000
```

Query:

```sql
WHERE customer_id = 2500
```

Spark skips:

```text
File1
File2
```

Immediately.

---

# Why It's So Effective

Z-Order itself doesn't accelerate queries.

It improves:

```text
File Statistics
```

which improves:

```text
Data Skipping
```

which reduces:

```text
Disk Reads
```

which accelerates:

```text
Query Execution
```

Many engineers miss this chain.

---

# Partitioning vs Z-Ordering

Think architecturally:

|Technique|Scope|
|---|---|
|Partitioning|Directory Level|
|Z-Ordering|File Level|
|Bloom Filter|Row Group Level|
|Predicate Pushdown|Column Level|

Together:

```text
Partition
    ↓
File Skip
    ↓
Row Group Skip
    ↓
Column Skip
```

Each layer eliminates more work.

---

# Real Delta Lake Example

```sql
OPTIMIZE sales
ZORDER BY (
    customer_id,
    product_id,
    region
)
```

Best for columns frequently used in:

```sql
WHERE
JOIN
GROUP BY
```

Not ideal for:

```sql
Free text
High-cardinality random values
Rarely queried columns
```

---

# Architect Checklist

For a 100 TB lakehouse:

### Partition By

```text
date
year/month/day
region
```

Columns with low-to-medium cardinality.

---

### Z-Order By

```text
customer_id
account_id
device_id
product_id
```

Columns heavily used in filters.

---

### Avoid

```text
20 columns in ZORDER
```

The benefit rapidly diminishes.

Usually:

```text
1–4 columns
```

is the sweet spot.

---

# Mental Model

Think of a modern lakehouse optimization stack like this:

```text
Partitioning
    ↓
Compaction
    ↓
Z-Ordering
    ↓
Parquet Statistics
    ↓
Bloom Filters
    ↓
Predicate Pushdown
```

When someone says:

> "This Delta query scans only 3 GB out of a 2 PB table"

it's usually not one feature doing the work. It's all of these layers working together.

A useful next topic is **how Delta Lake's OPTIMIZE command actually rewrites files, chooses file sizes, and interacts with Z-Ordering**, because that's where many production Databricks performance issues originate.