A Spark batch job slowed from 45 minutes to 3 hours.
How would you investigate?
Potential areas:
* Data growth
* Skew
* Shuffle size
* Join strategy
* Cluster changes
This is a strong troubleshooting question because interviewers want to see a **systematic approach**, not random guessing.

# First Principle

I'd compare:

```text
Previous Successful Run (45 min)
vs
Current Run (3 hours)
```

The key question is:

> What changed?

Could be:

- Data volume
    
- Data distribution
    
- Query plan
    
- Cluster resources
    
- Upstream data quality
    
- Storage layout
    

---

# 1. Check Data Growth

First thing I'd verify:

```sql
SELECT COUNT(*)
FROM orders;
```

Compare with previous runs.

Example:

|Date|Rows|
|---|---|
|Yesterday|500M|
|Today|2B|

A 4× increase in data can easily increase runtime.

Also check:

```text
Input files
File sizes
Partition sizes
```

Questions:

- Did a backfill accidentally run?
    
- Did partition pruning stop working?
    
- Is more data being scanned?
    

In Spark UI:

```text
Input Size
Records Read
```

are good indicators.

---

# 2. Check for Data Skew

One of the most common causes.

Example:

```sql
SELECT *
FROM orders o
JOIN customers c
ON o.customer_id = c.customer_id;
```

Suppose:

```text
customer_id = 123
```

appears:

```text
500 million times
```

while other IDs appear normally.

Now:

```text
199 tasks finish quickly
1 task runs for 2 hours
```

Entire stage waits for one executor.

Symptoms in Spark UI:

```text
Task duration imbalance
```

Example:

```text
Average Task = 20 sec
One Task = 7000 sec
```

Huge red flag.

Check:

```sql
SELECT customer_id,
       COUNT(*)
FROM orders
GROUP BY customer_id
ORDER BY COUNT(*) DESC;
```

---

# 3. Check Shuffle Size

Shuffles are often the biggest bottleneck.

Look in Spark UI:

```text
Shuffle Read
Shuffle Write
```

Example:

```text
Yesterday: 500 GB
Today: 8 TB
```

Something changed.

Common causes:

### Extra GROUP BY

```sql
GROUP BY customer_id, region
```

instead of

```sql
GROUP BY customer_id
```

### Additional Join

A new join may explode intermediate data.

---

# 4. Check Join Strategy

Open Spark physical plan.

```python
df.explain("formatted")
```

Look for:

```text
BroadcastHashJoin
SortMergeJoin
ShuffleHashJoin
```

---

### Example

Yesterday:

```text
BroadcastHashJoin
```

Today:

```text
SortMergeJoin
```

Why?

Small dimension table grew.

Example:

```text
50 MB
→
2 GB
```

No longer eligible for broadcast.

Result:

```text
Massive shuffle
```

and runtime increases dramatically.

---

# 5. Check Cluster Changes

Maybe the code didn't change.

Infrastructure changed.

Questions:

- Fewer executors?
    
- Smaller executor memory?
    
- Different instance type?
    
- Autoscaling issue?
    
- Spot/preemptible node losses?
    

Compare:

```text
Executors
CPU cores
Memory
```

between runs.

Example:

```text
Yesterday: 50 executors
Today: 10 executors
```

Runtime increase becomes obvious.

---

# 6. Check Garbage Collection

In Spark UI:

```text
GC Time
```

Example:

```text
Execution = 3 hours
GC = 1 hour
```

Indicates:

- Memory pressure
    
- Excessive spilling
    
- Poor executor sizing
    

---

# 7. Check Spill to Disk

Spark UI:

```text
Memory Spill
Disk Spill
```

Example:

```text
Yesterday: 0 GB spill
Today: 3 TB spill
```

This often causes massive slowdowns.

Potential causes:

- Bigger shuffle
    
- Less memory
    
- Skew
    

---

# 8. Check Partitioning Issues

Maybe someone changed:

```python
repartition(5000)
```

or

```python
coalesce(1)
```

---

### Too Few Partitions

```text
2 TB data
4 partitions
```

Low parallelism.

---

### Too Many Partitions

```text
2 TB data
100,000 partitions
```

Scheduler overhead dominates.

Check:

```python
df.rdd.getNumPartitions()
```

---

# 9. Check Storage/Layout Changes

Questions:

- Are files still Parquet?
    
- Did someone switch to JSON?
    
- Did compaction stop?
    
- Are there thousands of tiny files?
    

Example:

```text
Yesterday:
500 files

Today:
500,000 files
```

Spark spends significant time opening files.

---

# 10. Compare Query Plans

This is often the fastest way.

Generate:

```python
df.explain("formatted")
```

for:

- Previous version
    
- Current version
    

Look for:

```text
Extra join
Extra aggregation
Missing partition filter
Changed join strategy
Additional shuffle stage
```

---

# What I'd Check First (Priority Order)

1. **Spark UI → Stage Timeline**
    
    - Identify which stage became slow.
        
2. **Input Size**
    
    - Did data volume increase?
        
3. **Shuffle Read/Write**
    
    - Did shuffle explode?
        
4. **Task Distribution**
    
    - Is there skew?
        
5. **Physical Plan**
    
    - Did join strategy change?
        
6. **Executor Metrics**
    
    - Memory spill, GC, CPU utilization.
        
7. **Cluster Configuration**
    
    - Any infrastructure changes?
        

---

## Interview Answer

> I would start by comparing the current run against a previous healthy run. First I'd check whether data volume increased or partition pruning stopped working. Next I'd analyze Spark UI to identify the slow stage and review shuffle read/write metrics. I'd look for data skew by checking task duration distribution and key frequency distributions. Then I'd inspect the physical plan to see if join strategies changed, such as a broadcast join becoming a sort-merge join. Finally, I'd review executor utilization, memory spills, GC time, and cluster configuration changes. The goal is to determine whether the slowdown is caused by data growth, skew, excessive shuffling, a query plan regression, or infrastructure changes.

A senior-level addition is:

> "I wouldn't tune Spark settings first. I'd use Spark UI and execution metrics to isolate the bottleneck before making any configuration changes."

That shows you're diagnosing based on evidence rather than guessing.