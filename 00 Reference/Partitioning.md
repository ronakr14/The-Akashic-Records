```table-of-contents
```

Partitioning is one of those concepts that sounds simple ("split data into pieces"), but has implications across storage, query execution, distributed systems, and data modeling.

Let's build it from first principles.

---

## What is Partitioning?

Imagine a library with 1 billion books.

Without partitioning:

```text
Library
 └── 1,000,000,000 books
```

To find all books published in 2025, you must inspect every shelf.

With partitioning:

```text
Library
 ├── 2022 shelf
 ├── 2023 shelf
 ├── 2024 shelf
 └── 2025 shelf
```

Now a query for 2025 only visits one shelf.

That's partitioning.

**Definition:**

Partitioning = dividing data into smaller logical or physical chunks based on a key.

Common keys:

- Date
- Region
- Customer
- Country
- Device type
- Hash of user ID

---

## Why Partition Data?

Three main reasons:

### Read Less Data

Without partitioning:

```sql
SELECT *
FROM sales
WHERE sale_date='2026-06-01';
```

Database scans:

```text
10 TB
```

With partitioning:

```text
2026-06-01 partition only
```

Maybe:

```text
50 GB
```

Huge savings.

---

### Parallel Processing

Instead of:

```text
1 worker processes 1 billion rows
```

You can do:

```text
Worker1 -> Partition A
Worker2 -> Partition B
Worker3 -> Partition C
Worker4 -> Partition D
```

All run simultaneously.

---

### Operational Benefits

Delete old data:

Instead of:

```sql
DELETE FROM sales
WHERE year=2022;
```

Drop partition:

```sql
DROP PARTITION 2022;
```

Seconds instead of hours.

---

## Types of Partitioning

### Range Partitioning

Example:

```text
2023
2024
2025
```

Based on ranges.

Good for:

- Time-series data
- Logs
- Events

Most common.

---

### Hash Partitioning

Example:

```text
hash(user_id)%4
```

Results:

```text
Partition 0
Partition 1
Partition 2
Partition 3
```

Distributes data evenly.

Good for:

- Distributed databases
- Large joins

---

### List Partitioning

Example:

```text
US
UK
IN
DE
```

Country-specific partitions.

---

### Composite Partitioning

Example:

```text
year
  └── country
```

```text
2025
 ├── US
 ├── UK
 └── IN
```

Used heavily in large data warehouses.

---

## Partitioning vs Indexing

Many beginners confuse these.

### Index

```text
Table
 └── Index
```

Data remains together. Index acts like a map.

---

### Partition

```text
Partition A
Partition B
Partition C
```

Data physically separated.

Think:

```text
Index = book index
Partition = separate bookshelves
```

You often need both.

---

## Architect Perspective

Think of partitioning as operating at **two different layers**:

|Layer|PostgreSQL|Delta Lake|Databricks|DuckDB|DuckLake|
|---|---|---|---|---|---|
|Table Partitioning|Yes|No|No|Limited/No|Logical metadata|
|File Partitioning|Hidden|Yes|Yes|Yes (Parquet layout)|Yes|
|Partition Pruning|Yes|Yes|Yes|Yes|Yes|
|Distributed Processing|Limited|Yes|Yes|Single-node|Depends on execution engine|

The mental model:

```text
OLTP databases
    -> Table partitioning

Lakehouses
    -> File partitioning

Distributed engines
    -> Execution partitions
```

Those are three related but distinct concepts. Once you separate them mentally, most partitioning discussions become much easier to understand.

---

## Partitioning in PostgreSQL

Postgres supports true table partitioning.

Example:

```sql
CREATE TABLE sales (
    sale_id BIGINT,
    sale_date DATE
)
PARTITION BY RANGE (sale_date);
```

Partitions:

```sql
CREATE TABLE sales_2025
PARTITION OF sales
FOR VALUES FROM ('2025-01-01')
TO ('2026-01-01');
```

Storage:

```text
sales_2025
sales_2026
sales_2027
```

Separate physical tables.

### Layer

Partitioning occurs at:

```text
Table layer
```

Not file layer. Postgres hides internal files.

### Query Execution

Query:

```sql
WHERE sale_date='2025-06-01'
```

Planner performs:

**Partition Pruning**

```text
Read sales_2025 only
```

instead of:

```text
Read all partitions
```

### Tradeoffs

Too many partitions:

```text
100,000 partitions
```

Planner slows down.

Practical recommendation:

```text
Hundreds -> fine
Thousands -> caution
Tens of thousands -> often bad
```

---

## Partitioning in Databricks / Delta Lake

Completely different world.

Partitioning happens primarily at:

```text
File layer
```

Example:

```python
df.write.format("delta") \
.partitionBy("event_date") \
.save(...)
```

Storage:

```text
table/

event_date=2026-06-20/
    file1.parquet
    file2.parquet

event_date=2026-06-21/
    file1.parquet
```

Partition is actually a folder.

### Query

```sql
WHERE event_date='2026-06-21'
```

Spark reads:

```text
event_date=2026-06-21 folder
```

only.

This is called:

**Partition Pruning**

---

### Delta Lake Improvements

Delta adds metadata.

Instead of scanning folders manually:

```text
Delta Log
```

knows:

- files
- partitions
- statistics
- min/max values

This enables:

- Partition pruning
- Data skipping
- Z-ordering

---

## What About DuckDB?

DuckDB itself doesn't really have table partitioning like Postgres.

Internally:

```text
Row groups
```

are used.

When querying Parquet:

DuckDB uses:

- Predicate pushdown
- Row group pruning

### Example

Parquet file:

```text
row group 1
2024

row group 2
2025

row group 3
2026
```

Query:

```sql
WHERE year=2026
```

DuckDB skips earlier row groups.

### Layer

Mostly:

```text
File layer
```

through Parquet organization.

Not traditional database partitioning.

---

## DuckLake

DuckLake combines:

- DuckDB query engine
- Lakehouse storage

Similar to Delta Lake conceptually.

Partitioning is primarily:

```text
File/folder layer
```

Example:

```text
country=US/
country=IN/
country=DE/
```

Query engine prunes partitions.

---

## Distributed Processing Perspective

Suppose:

```text
10 TB table
```

Without partitioning:

```text
Worker1 reads everything
```

Bad.

---

With partitioning:

```text
Partition A -> Worker1
Partition B -> Worker2
Partition C -> Worker3
Partition D -> Worker4
```

Parallel execution.

This is why Spark loves partitioned datasets.

---

## Storage Partition vs Processing Partition

This is where many engineers get confused.

These are different.

### Storage Partition

Physical organization.

```text
country=US/
country=IN/
```

Stored on disk.

---

### Processing Partition

Execution-time split.

Spark:

```python
df.repartition(100)
```

Creates:

```text
100 processing partitions
```

for execution.

May have nothing to do with storage partitions.

---

Example:

```text
Storage partitions = 12
Processing partitions = 500
```

Perfectly valid.

---

## Good Partition Keys

Usually:

### Event Data

```text
event_date
```

### IoT

```text
date
device_region
```

### Retail

```text
date
country
```

### Finance

```text
trade_date
```

Rule:

> Partition on columns commonly used in filters and having moderate cardinality.

---

## When NOT to Partition

Avoid partitioning when:

### Small Tables

```text
5 GB
```

No benefit.

---

### High Cardinality

```text
customer_id
email
uuid
```

Bad.

---

### Queries Touch Everything

If every query scans all data:

```sql
SELECT SUM(amount)
FROM sales
```

Partitioning provides little benefit.

---

## Partition Troubleshooting — Step-by-Step

When queries are slow despite partitioning, investigate systematically:

### Step 1: Investigate the Root Cause

Questions to ask:

- Is the table partitioned?
- What is the partition column?
- Is the query filtering on the partition column?
- Are files organized correctly?
- Is the storage format columnar (Parquet/ORC) or row-based (CSV/JSON)?
- Are query plans showing partition pruning?

A common anti-pattern:

```sql
SELECT *
FROM sales
WHERE DATE(transaction_ts) = '2026-06-01';
```

Even if data is partitioned by `transaction_dt`, wrapping the column in a function can prevent pruning.

---

### Step 2: Enable Partition Pruning

#### Current Layout

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

#### Better Layout

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

#### Impact

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

### Step 3: Use Predicate Pushdown

#### Bad

```sql
SELECT *
FROM sales
WHERE UPPER(region) = 'US';
```

Engine may need to read all rows first.

#### Better

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

### Step 4: Optimize File Layout

Even with partitions, poor file layout hurts performance.

#### Small File Problem

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

#### Appropriate File Sizes

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

#### Clustering / Sorting

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

### Step 5: Read Only Required Columns

#### Bad

```sql
SELECT *
FROM sales
WHERE dt='2026-06-01';
```

#### Better

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

### Step 6: Verify Using Query Plans

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

---

## Modern Lakehouse Best Practice

For most analytics systems today:

```text
Partition by date
```

and then use:

- Delta statistics
- Data skipping
- Z-Ordering
- Clustering

instead of creating hundreds of thousands of partitions.

---

## See Also

- [[Data Modelling]]
- [[Delta Lake & Iceberg]]
- [[00 Reference/DuckDB]]
- [[Distributed Systems — Storage]]
- [[Data Lake]]
- [[Parquet]]
- [[Incremental Load Strategy]]
