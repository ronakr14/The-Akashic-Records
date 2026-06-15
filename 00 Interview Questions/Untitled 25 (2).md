A batch pipeline that normally processes 500 GB suddenly receives 20 TB.
What happens?
How would you prevent failures?

This is really a question about **capacity planning, scalability, and graceful degradation**.

The interviewer wants to know whether you understand what breaks when data volume increases by **40x**.

---

# What Happens When 500 GB Becomes 20 TB?

## 1. Runtime Explodes

A job that normally takes:

```text
500 GB → 1 hour
```

may become:

```text
20 TB → 20–50+ hours
```

depending on:

- Parallelism
    
- Cluster size
    
- Shuffle volume
    
- Data skew
    

The SLA is usually missed first.

---

## 2. Shuffle Becomes Massive

Suppose the pipeline contains:

```text
Joins
Aggregations
Sorts
```

Shuffle may grow from:

```text
100 GB
```

to

```text
4–8 TB+
```

Symptoms:

- Executors spill to disk
    
- Network saturation
    
- Long GC pauses
    
- Task failures
    

---

## 3. Memory Pressure

Hash tables used for:

```text
Joins
Aggregations
Deduplication
```

may no longer fit in memory.

Result:

```text
OutOfMemoryError
Executor lost
Container killed
```

---

## 4. Data Skew Gets Worse

A skewed key that was manageable at 500 GB becomes catastrophic at 20 TB.

Example:

```text
customer_id=123
```

contains:

```text
5% of total data
```

At 20 TB:

```text
1 TB of data
```

can land in a single partition.

---

## 5. Storage Issues

Temporary data grows dramatically.

Examples:

```text
Shuffle files
Checkpoint files
Intermediate datasets
```

Local disks may fill up.

---

## 6. Metadata Problems

If ingestion creates many files:

```text
50,000 files
```

becomes

```text
2 million files
```

Now:

- Planning slows
    
- Metadata operations dominate
    
- Listing files becomes expensive
    

---

# How Would I Prevent Failures?

## 1. Detect Volume Anomalies Early

Before processing:

```text
Input row count
Input size
Partition count
```

Compare against historical baselines.

Example:

```text
Normal: 500 GB
Today: 20 TB
```

Immediately trigger alerts.

---

## 2. Implement Data Quality / Volume Gates

Pipeline should fail fast.

Example:

```python
if input_size > expected_size * 5:
    raise Exception("Abnormal input volume")
```

Prevent wasting hours of compute.

---

## 3. Autoscale Compute

Increase:

```text
Executors
Workers
CPU
Memory
```

before processing begins.

Cloud platforms make this relatively easy.

---

## 4. Partition More Aggressively

Example:

Instead of:

```text
200 partitions
```

use:

```text
8000 partitions
```

to maintain parallelism.

In Spark:

```python
spark.sql.shuffle.partitions
```

may need adjustment.

---

## 5. Process Incrementally

Instead of:

```text
20 TB all at once
```

split into:

```text
Daily chunks
Hourly chunks
Partition batches
```

This limits blast radius.

---

## 6. Use Checkpointing

Avoid restarting from zero.

Pipeline:

```text
Stage 1 ✓
Stage 2 ✓
Stage 3 fails
```

Resume from Stage 3.

Not:

```text
Restart entire 20 TB workload
```

---

## 7. Protect Critical Joins

Review:

- Broadcast thresholds
    
- Join order
    
- Skew handling
    

Enable adaptive execution where available.

For Spark:

```text
Adaptive Query Execution (AQE)
Skew Join Optimization
```

---

## 8. Control Spill Behavior

Ensure:

```text
Sufficient local disk
Object storage spill
External shuffle service
```

so jobs degrade gracefully instead of crashing.

---

## 9. Optimize Data Layout

Use:

- Partition pruning
    
- Predicate pushdown
    
- Clustering
    
- Compaction
    

If only:

```text
500 GB
```

is actually needed from the 20 TB arrival, avoid scanning everything.

---

## 10. Build Backpressure Mechanisms

Don't allow ingestion to overwhelm downstream systems.

Example:

```text
Ingestion → Queue → Processing
```

rather than:

```text
Ingestion → Immediate processing
```

This smooths spikes.

---

# What a Strong Senior Answer Sounds Like

> A 40x increase from 500 GB to 20 TB would likely cause SLA violations, excessive shuffle, memory pressure, skew amplification, and potentially executor or storage failures. I would first detect the anomaly through volume monitoring and fail-fast guardrails. To handle legitimate growth, I'd rely on autoscaling, increased partition parallelism, incremental processing, checkpointing, and adaptive query execution. The goal is to ensure the pipeline either scales predictably or fails early with clear diagnostics rather than consuming hours of compute before crashing.

A strong follow-up is:

> "I'd also ask whether the 20 TB is expected business growth or a data-quality issue. In production, abnormal volume is often caused by upstream duplication, replayed data, or partitioning mistakes rather than genuine growth."

That answer shows operational maturity, not just Spark tuning knowledge.