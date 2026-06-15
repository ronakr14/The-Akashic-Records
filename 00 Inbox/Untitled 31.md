6. Explain how you would backfill one year of historical data without impacting production batch jobs.
This question is less about ETL mechanics and more about **capacity planning, workload isolation, and operational safety**.

The interviewer wants to know:

> "Can you run a massive backfill without breaking today's production pipelines?"

A poor answer is:

```text
Run the backfill job.
```

A good answer focuses on **isolation, prioritization, throttling, and validation**.

---

# Scenario

```text
Historical Data Needed: 1 Year
Production Pipeline: Daily
Production SLA: Must Not Break
```

Assume:

```text
Daily Volume = 500 GB
Backfill Volume = 180 TB
```

Running both workloads on the same resources could:

- Miss SLAs
    
- Starve production jobs
    
- Cause cluster contention
    
- Increase costs unexpectedly
    

---

# Design Principles

1. Production first
    
2. Isolate workloads
    
3. Backfill incrementally
    
4. Validate before publishing
    
5. Make backfill restartable
    

---

# Architecture

```text
                    Production Queue
                           |
                    Daily Pipeline
                           |
                    Gold Tables
                           |
                           |
            -------------------------------
                           |
                    Backfill Queue
                           |
                 Historical Processing
                           |
                    Validation Layer
                           |
                    Controlled Publish
```

The key idea:

```text
Separate compute
Shared storage
```

---

# 1. Create a Dedicated Backfill Environment

Never run large backfills on the same cluster as production.

Example:

```text
Cluster A
Production ETL

Cluster B
Backfill ETL
```

or

```text
Kubernetes Namespace
   production

Kubernetes Namespace
   backfill
```

Benefits:

- Production SLAs protected
    
- Resource contention reduced
    
- Easier rollback
    

---

# 2. Process in Partitions

Never backfill:

```text
Jan 2025 → Dec 2025
```

in a single run.

Instead:

```text
Month-by-Month

2025-01
2025-02
2025-03
...
```

or

```text
Day-by-Day
```

Benefits:

- Easier retries
    
- Better monitoring
    
- Smaller failure domains
    

---

# Example

```text
sales/
   sale_date=2025-01-01
   sale_date=2025-01-02
```

Process each partition independently.

---

# 3. Throttle Resource Usage

Even with separate clusters, storage systems can become bottlenecks.

Control:

```text
Max Concurrent Jobs
Max Executors
Max Throughput
```

Example:

```text
Production:
70% capacity

Backfill:
30% capacity
```

Production always gets priority.

---

# 4. Use Historical Snapshots

A common mistake is reading current source systems.

Bad:

```text
Backfill → Query Production Database
```

for 1 year of history.

This can overload source systems.

---

# Better

Read from:

```text
Raw Data Lake
Archive Storage
Snapshots
CDC Logs
```

Example:

```text
Bronze Layer
```

becomes the source for backfill.

---

# 5. Write to Temporary Tables

Never overwrite production tables directly.

Bad:

```text
Backfill
    ↓
Production Table
```

If logic is wrong:

```text
Dashboard Corruption
```

---

# Better

```text
Backfill
    ↓
Validation Table
    ↓
Quality Checks
    ↓
Publish
```

Example:

```text
sales_gold_backfill
```

then:

```sql
SWAP TABLE
```

or

```sql
MERGE
```

after validation.

---

# 6. Make Backfill Restartable

Suppose:

```text
Month 1 Complete
Month 2 Complete
Month 3 Failed
```

You don't want:

```text
Restart Year-Long Job
```

Store progress:

|Partition|Status|
|---|---|
|Jan|Complete|
|Feb|Complete|
|Mar|Failed|

Resume from:

```text
March
```

only.

---

# 7. Data Validation

Before publishing:

## Volume Validation

```text
Source: 100M
Target: 100M
```

---

## Aggregation Validation

```sql
SUM(revenue)
COUNT(order_id)
```

must match expected values.

---

## Data Quality Checks

- Nulls
    
- Duplicates
    
- Referential integrity
    

---

# 8. Publish Strategy

### Option A: MERGE

```sql
MERGE INTO sales_gold
USING sales_backfill
```

Good for partial corrections.

---

### Option B: Partition Swap

For partitioned tables:

```text
2025-01
2025-02
```

Replace only affected partitions.

Much safer than full table replacement.

---

# Monitoring

Track:

### Progress

```text
Processed Months
Remaining Months
```

---

### Resource Metrics

```text
CPU
Memory
Shuffle
Storage I/O
```

---

### SLA Metrics

```text
Production Runtime
Backfill Runtime
```

Alert if production starts slowing down.

---

# What If Resources Are Limited?

If only one cluster exists:

1. Run production jobs first.
    
2. Schedule backfill during off-peak hours.
    
3. Limit executor count.
    
4. Process fewer partitions per day.
    

Example:

```text
Daily Production: 1 AM – 4 AM
Backfill: 5 AM – 10 AM
```

---

# Interview Summary Answer

> To backfill one year of historical data without impacting production, I would isolate the workload from production using a dedicated compute cluster, queue, or resource pool. I would process historical data in partitions (daily or monthly) rather than as a single job, making the backfill restartable and easier to monitor. The backfill would read from immutable raw storage or archived snapshots instead of querying operational systems. Results would be written to temporary tables and validated through row-count, aggregate, and data-quality checks before being merged into production datasets. Resource throttling and workload prioritization would ensure production retains guaranteed capacity, and progress metadata would allow the backfill to resume from the last successful partition rather than restarting the entire year. This approach minimizes operational risk while maintaining production SLAs.