Your nightly batch SLA is 3 hours.
Business now requires 1 hour.
What architectural changes would you consider?

This is a classic **Senior/Staff Data Engineer system design question**.

The interviewer is testing whether you can move beyond tuning individual jobs and rethink the architecture.

---

# Step 1: Quantify the Gap

Current:

```text
Runtime = 3 hours
SLA = 3 hours
```

New requirement:

```text
Runtime ≤ 1 hour
```

Need:

```text
3x improvement
```

First question:

> Is the workload growing, or did the SLA simply become stricter?

The answer influences whether optimization alone is enough.

---

# 2. Optimize Before Re-Architecting

Before changing architecture:

### Check

- Partition pruning
    
- Predicate pushdown
    
- Join strategies
    
- Data skew
    
- Small files
    
- Cluster sizing
    

Sometimes:

```text
3 hours
→
50 minutes
```

is achievable through optimization alone.

I would quantify:

```text
CPU utilization
Shuffle volume
Spill volume
Scan volume
```

before proposing a redesign.

---

# 3. Move from Full Refresh to Incremental Processing

This is often the highest ROI change.

Current:

```text
Every night:
Read 20 TB
Recompute everything
```

Better:

```text
Read only new data
```

Example:

```text
20 TB total
50 GB new/day
```

Now process:

```text
50 GB
instead of
20 TB
```

Techniques:

- CDC
    
- Watermarks
    
- Incremental MERGE
    
- Change tables
    

Often delivers orders-of-magnitude improvements.

---

# 4. Introduce Multi-Stage Data Layers

Bad:

```text
Raw
 ↓
Huge nightly transformation
 ↓
Business table
```

Better:

```text
Raw
 ↓
Incremental Bronze
 ↓
Incremental Silver
 ↓
Incremental Gold
```

Each stage processes smaller deltas.

Common in:

- Databricks Lakehouse
    
- Modern data platforms
    

---

# 5. Parallelize the Workflow

Many pipelines are accidentally sequential.

Current:

```text
Step A (30 min)
↓
Step B (40 min)
↓
Step C (50 min)
↓
Step D (60 min)

Total = 180 min
```

Analyze dependencies.

Possible redesign:

```text
      B
     /
A
     \
      C

B + C run simultaneously

Then D
```

Runtime drops significantly.

---

# 6. Scale Out Compute

Sometimes the architecture is fine.

The cluster is simply undersized.

Example:

```text
20 executors
```

becomes:

```text
80 executors
```

Questions:

- Is workload CPU-bound?
    
- Memory-bound?
    
- Shuffle-bound?
    

Blindly adding compute doesn't always help.

---

# 7. Reduce Shuffle-Heavy Operations

Many long-running batch jobs spend most time shuffling.

Common offenders:

```sql
GROUP BY
DISTINCT
ORDER BY
Large joins
```

Possible redesign:

### Pre-Aggregation

Instead of:

```text
5 TB shuffle nightly
```

Create intermediate aggregates throughout the day.

---

### Better Partitioning

Align partitioning with:

```text
Join keys
Aggregation keys
```

to reduce data movement.

---

# 8. Introduce Materialized Aggregates

Current:

```text
Nightly recompute
365 days of history
```

Better:

```text
Maintain daily aggregates
```

Then:

```text
Today's aggregate
+
Historical aggregate
```

instead of recalculating everything.

---

# 9. Move Toward Near-Real-Time Processing

If business wants:

```text
3 hours
→
1 hour
```

today,

tomorrow they may want:

```text
15 minutes
```

At some point batch becomes the wrong model.

Architecture shift:

```text
Batch
↓
Micro-batch
↓
Streaming
```

Using:

- Apache Kafka
    
- Apache Flink
    
- Apache Spark Structured Streaming
    

Instead of processing:

```text
24 hours of data
```

process:

```text
5-minute windows
```

continuously.

Then the nightly workload becomes tiny.

---

# 10. Storage Layout Improvements

A surprisingly common issue.

Example:

```text
20 TB scanned nightly
```

because:

```text
No partition pruning
No clustering
Millions of small files
```

Architectural improvements:

- Better partitioning strategy
    
- File compaction
    
- Clustering/Z-ordering
    
- Data skipping indexes
    

Can cut runtime dramatically.

---

# 11. Build an Optimization Feedback Loop

For large platforms:

```text
Pipeline
↓
Telemetry
↓
Optimization Engine
↓
Recommendations
↓
Continuous Improvement
```

This is where metadata-driven optimization platforms become valuable.

Monitor:

```text
Runtime
Shuffle
Spill
Scan ratio
Skew
```

and continuously identify bottlenecks.

---

# How I'd Answer in an Interview

> I would first determine whether the 3-hour runtime is due to inefficiencies or simply workload size. I'd optimize partition pruning, joins, shuffles, skew, and file layout before redesigning anything. If the workload still cannot meet the SLA, I'd move from full-refresh processing to incremental processing using CDC or watermarks, increase parallelism, and introduce pre-aggregations or materialized intermediate datasets. If the business requirement continues to tighten, I'd evaluate a transition from nightly batch processing to micro-batch or streaming architectures so that most computation happens continuously throughout the day rather than during a single nightly window.

### Staff-Level Prioritization

|Change|Expected Impact|Effort|
|---|---|---|
|Partition pruning & query optimization|High|Low|
|Incremental processing|Very High|Medium|
|Parallel workflow redesign|High|Medium|
|Cluster scaling|Medium|Low|
|Pre-aggregations/materialized views|High|Medium|
|Streaming/micro-batch architecture|Very High|High|

A strong staff-level observation is:

> If the business wants a 3× SLA improvement, I would first ask whether we're solving a compute problem or a data architecture problem. Reprocessing less data is usually far more effective than processing the same data faster.