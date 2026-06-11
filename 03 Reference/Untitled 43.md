What telemetry signals would help predict SLA violations before they happen?

This is a strong **senior/staff-level observability question**. The key is that you're not looking for signals that explain why an SLA was missed—you want **leading indicators** that predict a miss while there's still time to act.

---

# 1. Runtime Trend vs Historical Baseline

Track:

```text
Current Runtime
Historical Runtime
P95 Runtime
P99 Runtime
```

Example:

|Metric|Normal|Today|
|---|---|---|
|Step 1|10 min|12 min|
|Step 2|15 min|22 min|
|Step 3|20 min|35 min|

The pipeline is progressively slowing.

A simple prediction:

```text
Current progress rate
+
Remaining workload
=
Estimated completion time
```

If ETA exceeds SLA, raise an alert immediately.

---

# 2. Input Data Volume Growth

One of the most common causes.

Track:

```text
Rows processed
Files processed
Bytes scanned
```

Example:

|Day|Input Size|
|---|---|
|Monday|5 TB|
|Tuesday|5.2 TB|
|Wednesday|8.7 TB|

An 80% growth spike is a strong predictor of longer runtimes.

---

# 3. Scan-to-Output Ratio

Track:

```text
Bytes scanned
Bytes produced
```

Example:

```text
100 TB scanned
50 GB output
```

Often indicates:

- Missing partition pruning
    
- Predicate pushdown failure
    
- Bad query plan
    

This frequently causes sudden SLA breaches.

---

# 4. Shuffle Volume

For Spark/Flink-style engines:

Track:

```text
Shuffle Read
Shuffle Write
Spill Size
```

Example:

|Day|Shuffle|
|---|---|
|Avg|500 GB|
|Today|6 TB|

The job is likely heading toward trouble.

Large shuffles usually precede:

- Long runtimes
    
- Executor failures
    
- OOM events
    

---

# 5. Data Skew Metrics

Monitor:

```text
Largest partition
Median partition
Task duration variance
```

Example:

```text
Median partition = 1 GB
Largest partition = 400 GB
```

A few straggler tasks can dominate runtime.

Common symptom:

```text
95% tasks complete
Job still running 1 hour later
```

---

# 6. Executor/Worker Utilization

Track:

```text
CPU utilization
Memory utilization
Disk I/O
Network I/O
```

Example:

```text
Memory = 95%
Disk Spill = Increasing
```

Often predicts:

```text
OOM
GC pressure
Slowdown
```

before failure occurs.

---

# 7. Queue Wait Time

In shared clusters:

```text
Job Submitted
↓
Resources Allocated
```

Track:

```text
Queue time
Resource acquisition time
```

Example:

|Metric|Normal|Today|
|---|---|---|
|Queue Time|2 min|45 min|

Even a perfectly optimized job may miss SLA.

---

# 8. Stage-Level Critical Path

Not all stages matter equally.

Track:

```text
Longest stage duration
Critical path duration
```

Example:

```text
20-stage pipeline

Stage 7 = 3 hrs
All others = 5 mins
```

Stage 7 becomes the SLA risk.

---

# 9. Late or Missing Upstream Data

Many pipelines are blocked by dependencies.

Monitor:

```text
Source freshness
File arrival delays
Kafka lag
CDC lag
```

Example:

```text
Expected arrival: 01:00
Actual arrival: 03:00
```

The SLA clock is already under pressure.

---

# 10. Error Rate Trends

Track:

```text
Retry count
Failed tasks
Transient errors
```

Example:

```text
Normal retries = 5

Today:
Retries = 500
```

The job may still be running, but failure risk is increasing rapidly.

---

# 11. Throughput Degradation

Measure:

```text
Rows/sec
Files/sec
GB/sec
```

Example:

|Metric|Normal|Today|
|---|---|---|
|Rows/sec|10M|2M|

ETA can be projected long before the SLA is missed.

---

# 12. Cost-Based Query Signals

For warehouse systems, collect:

```text
Estimated scan size
Join count
Join type
Partition pruning %
Broadcast join eligibility
```

Example:

```text
Yesterday:
Scan 500 GB

Today:
Scan 20 TB
```

This often predicts an SLA miss before execution even starts.

---

# Building an SLA Prediction Model

A mature platform combines:

```text
Input growth
+
Current progress
+
Resource availability
+
Historical runtimes
+
Query complexity
```

to compute:

```text
Predicted Finish Time
```

and compare it against:

```text
SLA Deadline
```

Example:

```text
Current time: 03:00
Predicted finish: 06:30
SLA: 05:00

Risk Score: HIGH
```

This enables:

- Auto-scaling
    
- Priority escalation
    
- Early alerts
    
- Query optimization recommendations
    

---

## Interview Answer

> To predict SLA violations proactively, I would monitor leading indicators such as runtime trends versus historical baselines, input data growth, scan volume, shuffle size, task skew, resource utilization, queue wait times, upstream data freshness, retry rates, and throughput degradation. I would continuously estimate completion time based on current progress and remaining workload. If the predicted completion time exceeds the SLA threshold, I would trigger alerts or automated remediation such as scaling resources, prioritizing workloads, or optimizing execution plans before the violation occurs. This shifts monitoring from reactive alerting to predictive observability.