draft an answer for ## Design a batch pipeline that processes 50 TB of sales data every night within a 4-hour SLA.
Things interviewer expects:
* Partitioning strategy
* Parallelism
* Incremental processing
* Resource allocation
* Failure recovery
* Monitoring
Follow-up:
> What would you do if the job suddenly takes 7 hours?

For a system design or data engineering interview, I'd answer it in a structured way from ingestion → processing → reliability → operations.

---

### Processing 50 TB of Sales Data Nightly Within a 4-Hour SLA

#### 1. Understand the Scale

- Data Volume: 50 TB/day
    
- SLA: 4 hours
    
- Required throughput:
    

[  
50 \text{ TB} \div 4 \text{ hours} = 12.5 \text{ TB/hour}  
]

or roughly:

[  
3.5 \text{ GB/sec}  
]

This immediately tells me that a single-node solution is impossible, and I need a distributed architecture.

---

## Architecture

### Storage Layer

Store raw sales data in a data lake:

- S3 / ADLS / GCS
    
- Open table format:
    
    - Apache Iceberg
        
    - Delta Lake
        
    - Apache Hudi
        

Benefits:

- ACID transactions
    
- Partition pruning
    
- Schema evolution
    
- Time travel
    

---

## Partitioning Strategy

Partitioning is the first optimization lever.

For sales data:

```text
sales/
  sale_date=2026-06-04/
      region=APAC/
      region=EMEA/
      region=US/
```

Primary partition:

```text
sale_date
```

Secondary partition:

```text
region
```

For very large partitions:

```text
sale_date + region + hash(customer_id)
```

Goals:

- Minimize scans
    
- Maximize parallel reads
    
- Avoid partition skew
    

I would target file sizes around:

```text
256 MB – 1 GB
```

to optimize Spark execution.

---

## Incremental Processing

Processing all 50 TB every night is expensive.

I would design incremental pipelines.

### Bronze

Raw ingestion.

### Silver

Process only:

```text
new records
updated records
late arriving records
```

using:

- CDC (Change Data Capture)
    
- Watermarks
    
- MERGE operations
    

Example:

```sql
MERGE INTO sales_curated
USING sales_cdc
ON target.sale_id = source.sale_id
WHEN MATCHED THEN UPDATE
WHEN NOT MATCHED THEN INSERT
```

If only 5 TB changed, process 5 TB instead of 50 TB.

---

## Parallelism Strategy

I would horizontally scale the compute layer.

Example:

```text
Spark Cluster
```

- Driver Node
    
- 100–300 Worker Nodes
    

Parallelization dimensions:

### Data Parallelism

Each partition processed independently.

```text
Date Partition 1
Date Partition 2
Date Partition 3
...
```

### Task Parallelism

Independent transformations execute simultaneously.

### Shuffle Optimization

Reduce expensive shuffles by:

- Broadcast joins
    
- Bucketing
    
- Repartitioning on join keys
    
- Data co-location
    

Example:

```python
broadcast(customer_dimension)
```

instead of large distributed joins.

---

## Resource Allocation

Assume Spark on Kubernetes.

Example sizing:

```text
200 Workers
16 vCPU each
64 GB RAM each
```

Total:

```text
3200 vCPU
12.8 TB RAM
```

Use:

- Dynamic Allocation
    
- Autoscaling
    
- Spot instances for non-critical jobs
    

Separate pools:

```text
ETL Pool
Adhoc Pool
ML Pool
```

to prevent resource contention.

---

## Failure Recovery

At 50 TB scale, failures are guaranteed.

### Checkpointing

Persist intermediate state.

```text
Raw -> Checkpoint -> Curated
```

### Idempotent Processing

Re-running a job should not create duplicates.

Use:

```sql
MERGE
UPSERT
```

instead of append-only writes.

### Retry Strategy

- Retry transient failures
    
- Exponential backoff
    

### Partition-Level Recovery

Instead of:

```text
Reprocess 50 TB
```

only reprocess:

```text
sale_date=2026-06-04
region=APAC
```

that failed.

### Data Quality Gates

Validate:

- Row counts
    
- Null thresholds
    
- Duplicate checks
    
- Referential integrity
    

before publishing results.

---

## Monitoring

I would implement monitoring at three levels.

### Infrastructure Monitoring

Metrics:

- CPU
    
- Memory
    
- Disk
    
- Network
    
- Executor utilization
    

Tools:

- Prometheus
    
- Grafana
    

---

### Pipeline Monitoring

Metrics:

- Records processed
    
- Throughput
    
- Partition completion %
    
- Stage execution time
    
- Shuffle size
    

Tools:

- Spark UI
    
- Airflow
    
- Datadog
    

---

### Data Quality Monitoring

Metrics:

- Freshness
    
- Completeness
    
- Volume anomalies
    
- Duplicate rates
    

Tools:

- Great Expectations
    
- Soda
    

---

## Meeting the 4-Hour SLA

Key techniques:

|Area|Optimization|
|---|---|
|Storage|Partitioned Iceberg/Delta tables|
|Compute|Large Spark cluster|
|Processing|Incremental CDC|
|Joins|Broadcast joins, bucketing|
|Files|256 MB–1 GB files|
|Recovery|Partition-level restart|
|Monitoring|End-to-end observability|

---

# Follow-up: What would you do if the Job Suddenly Takes 7 Hours?

I would troubleshoot systematically.

### Step 1: Identify the Bottleneck

Check:

- Data volume increase?
    
- Cluster resource reduction?
    
- Increased shuffle?
    
- Data skew?
    
- Small-file explosion?
    
- Expensive joins?
    

---

### Step 2: Compare Historical Runs

Look at:

```text
Yesterday: 4 hours
Today: 7 hours
```

Compare:

- Input size
    
- Number of files
    
- Shuffle volume
    
- Executor utilization
    
- Failed/retried tasks
    

---

### Common Root Causes

#### Data Skew

Example:

```text
90% of sales belong to one region
```

One executor becomes overloaded.

Fix:

- Salting
    
- Repartitioning
    
- Skew-aware joins
    

---

#### Small File Problem

Instead of:

```text
50,000 files
```

now:

```text
5,000,000 files
```

Spark spends time listing and opening files.

Fix:

```text
Compaction
OPTIMIZE
VACUUM
```

---

#### Shuffle Explosion

Join cardinality unexpectedly increases.

Fix:

- Broadcast joins
    
- Better partition keys
    
- Pre-aggregation
    

---

#### Resource Contention

Other workloads consuming cluster resources.

Fix:

- Dedicated queues
    
- Resource reservations
    
- Autoscaling
    

---

### Step 3: Immediate SLA Recovery

To restore SLA quickly:

1. Scale cluster horizontally.
    
2. Increase executor count.
    
3. Process only critical partitions first.
    
4. Enable autoscaling.
    
5. Skip non-essential downstream aggregations.
    

---

### Step 4: Long-Term Prevention

Implement:

- SLA monitoring
    
- Throughput alerts
    
- Data growth forecasting
    
- Capacity planning
    
- Automatic skew detection
    

This turns the discussion from simply "running Spark jobs" into demonstrating that you understand large-scale batch processing, operational reliability, and production-grade data platform design.