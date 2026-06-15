If you could collect only 10 metrics from every batch job, which would you choose and why?

If I were building a batch observability platform and could collect **only 10 metrics per job**, I'd choose metrics that help answer four critical questions:

1. **Did it succeed?**
    
2. **How long did it take?**
    
3. **How much data did it process?**
    
4. **Why did it become slow or expensive?**
    

## Top 10 Batch Job Metrics

|#|Metric|Why It Matters|
|---|---|---|
|1|Job Status (Success/Failed/Partial)|Most fundamental KPI. Enables SLA, reliability, and incident reporting.|
|2|Execution Duration|Detects regressions, SLA violations, and performance trends.|
|3|Input Records Processed|Normalizes performance against workload growth.|
|4|Output Records Produced|Detects data loss, duplication, and unexpected volume changes.|
|5|Data Read (GB/TB)|Measures scan efficiency and storage access cost.|
|6|Data Written (GB/TB)|Indicates output growth, compaction issues, and storage cost.|
|7|Shuffle Volume|One of the strongest predictors of Spark/Flink performance problems.|
|8|Peak Memory Usage|Identifies memory pressure, spills, and sizing issues.|
|9|CPU Time / Executor Utilization|Distinguishes compute-bound from I/O-bound workloads.|
|10|Data Quality Score / Failed Checks|A fast job producing bad data is still a failed job.|

---

## Why These 10?

Imagine a job suddenly increases from:

```text
45 min → 3 hours
```

These metrics immediately tell you:

|Observation|Likely Cause|
|---|---|
|Input records doubled|Data growth|
|Read GB increased 20x|Missing partition pruning|
|Shuffle increased 50x|Join or aggregation issue|
|Memory maxed out|Spill or skew|
|CPU low but duration high|Waiting on I/O|
|Output records dropped|Data quality issue|
|DQ failures increased|Bad upstream data|

Without these metrics, you're mostly guessing.

---

## If Running Spark Specifically

I would slightly modify the list:

1. Duration
    
2. Status
    
3. Input rows
    
4. Output rows
    
5. Input data size
    
6. Shuffle read bytes
    
7. Shuffle write bytes
    
8. Spill bytes (memory + disk)
    
9. Skew ratio (largest partition / median partition)
    
10. Executor CPU utilization
    

The addition of **spill bytes** and **skew ratio** dramatically improves root-cause analysis for Spark workloads.

---

## If Building an AI Optimization Engine

I'd prioritize optimization signals rather than pure operational metrics:

1. Duration
    
2. Input rows
    
3. Input bytes
    
4. Output rows
    
5. Shuffle bytes
    
6. Spill bytes
    
7. Join count
    
8. Largest partition size
    
9. Small file count
    
10. Scan efficiency
    

These features are highly predictive for:

- SLA violations
    
- Cost overruns
    
- Query regressions
    
- Auto-tuning recommendations
    

For an AI-powered lakehouse optimization platform, I'd argue the most valuable metric is **shuffle volume**, because excessive shuffling is responsible for a surprisingly large percentage of batch job slowdowns across Spark, Databricks, and modern lakehouse environments.