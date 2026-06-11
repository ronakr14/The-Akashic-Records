How do you identify bottlenecks in a batch workload?
Expected:
* CPU
* Memory
* Network
* Disk I/O
* Shuffle
This is a classic troubleshooting and performance-engineering question.

The interviewer wants to know whether you can systematically diagnose a slow batch job instead of saying:

> "Add more nodes."

A strong answer starts with:

> First, identify **where time is being spent** before scaling resources.

---

# A Framework for Finding Bottlenecks

When a batch job slows down, I analyze five resource categories:

```text
CPU
Memory
Disk I/O
Network
Shuffle
```

Then I correlate them with:

```text
Execution plan
Stage timings
Task metrics
Resource utilization
```

---

# 1. CPU Bottleneck

## Symptoms

```text
CPU Utilization = 90-100%
Memory = Normal
Disk = Normal
Network = Normal
```

Executors spend most of their time computing.

---

## Common Causes

### Expensive Transformations

```sql
REGEX
UDFs
Complex aggregations
```

---

### Excessive Serialization

```text
JSON parsing
Object conversion
Compression
```

---

### Large Aggregations

```sql
GROUP BY customer_id
```

on billions of rows.

---

## How to Detect

Spark UI:

```text
Executor CPU Time
Task Duration
```

Linux:

```text
top
htop
```

---

## Fixes

- Optimize transformations
    
- Replace UDFs with native functions
    
- Increase parallelism
    
- Scale CPU resources
    

---

# 2. Memory Bottleneck

## Symptoms

```text
OOM Errors
Frequent GC
Executor Crashes
```

---

## Common Causes

### Large Joins

```sql
fact_table
JOIN
large_dimension
```

---

### Data Skew

One partition:

```text
500 GB
```

Others:

```text
5 GB
```

---

### Large Caches

```python
cache()
persist()
```

without enough memory.

---

## How to Detect

Spark UI:

```text
GC Time
Spill Metrics
Executor Failures
```

---

## Fixes

- Broadcast joins
    
- Repartition data
    
- Increase executor memory
    
- Remove unnecessary caching
    

---

# 3. Disk I/O Bottleneck

## Symptoms

CPU remains low:

```text
20%
```

while job is still slow.

---

## Common Causes

### Reading Massive Data

```text
100 TB scan
```

for a 1 TB workload.

---

### Small File Problem

Instead of:

```text
100,000 files
```

you have:

```text
10,000,000 files
```

---

### Spill-to-Disk

Insufficient memory causes:

```text
Sort Spill
Shuffle Spill
```

---

## How to Detect

Metrics:

```text
Read MB/s
Write MB/s
Spilled Bytes
```

---

## Fixes

### Partition Pruning

```sql
WHERE order_date='2026-06-01'
```

---

### File Compaction

Target:

```text
256MB–1GB files
```

---

### Better Formats

Use:

- Apache Parquet
    
- Apache ORC
    

instead of CSV.

---

# 4. Network Bottleneck

## Symptoms

Executors spend time:

```text
Waiting
```

rather than computing.

---

## Common Causes

### Large Data Movement

```sql
JOIN
```

between huge datasets.

---

### Cross-Region Reads

```text
Cluster in Region A
Storage in Region B
```

---

### Distributed Shuffle

Large partition exchanges.

---

## How to Detect

Metrics:

```text
Network Throughput
Shuffle Read Time
Shuffle Write Time
```

---

## Fixes

- Co-locate storage and compute
    
- Broadcast small tables
    
- Reduce shuffle operations
    

---

# 5. Shuffle Bottleneck (Most Common)

For Spark, this is often the biggest performance killer.

---

## What Is Shuffle?

Data redistribution across executors.

Example:

```sql
GROUP BY
JOIN
DISTINCT
ORDER BY
```

usually triggers shuffle.

---

## Example

Before:

```text
Executor A
Executor B
Executor C
```

After GROUP BY:

```text
Move data across all nodes
```

---

## Symptoms

Spark UI shows:

```text
Shuffle Read = Huge
Shuffle Write = Huge
```

---

## Common Causes

### Large Joins

```sql
sales
JOIN customers
```

---

### Skewed Keys

```text
customer_id=123
contains 80% of rows
```

One executor becomes overloaded.

---

### High Cardinality Aggregations

```sql
GROUP BY user_id
```

for billions of users.

---

## Fixes

### Broadcast Join

Instead of shuffling both sides:

```python
broadcast(dim_table)
```

---

### Repartition

```python
repartition()
```

on join keys.

---

### Salting

Mitigate skew:

```text
customer_id + random_bucket
```

---

# Practical Investigation Workflow

When a job goes from:

```text
4 hours
```

to

```text
7 hours
```

I typically check:

### Step 1

Execution DAG

```text
Which stage is slow?
```

---

### Step 2

Resource Utilization

```text
CPU
Memory
Disk
Network
```

---

### Step 3

Shuffle Metrics

```text
Shuffle Read
Shuffle Write
Spill
```

---

### Step 4

Data Changes

```text
Input size increase?
Partition skew?
Small files?
```

---

### Step 5

Query Plan

Look for:

```text
Full scans
Large joins
Expensive aggregations
```

---

# Interview Summary Answer

> To identify bottlenecks in a batch workload, I first analyze execution metrics and stage-level timings. I check CPU utilization to identify compute-heavy transformations, memory metrics for garbage collection, spills, and out-of-memory conditions, disk I/O for excessive scans or small-file problems, and network utilization for data movement across nodes. In distributed systems such as Spark, I pay particular attention to shuffle metrics because joins, aggregations, and sorting often trigger expensive data redistribution. I correlate resource metrics with the execution plan to determine whether the bottleneck is compute, memory, storage, network, or shuffle related. Once identified, I apply targeted optimizations such as partition pruning, broadcast joins, repartitioning, file compaction, skew mitigation, or resource scaling rather than blindly adding more compute.