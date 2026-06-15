Design a metadata-driven batch optimization platform.

This is a **Staff/Principal Data Engineer** level design question because you're essentially building an internal version of parts of:

- Databricks Optimizer
    
- Snowflake Query Insights
    
- Google Cloud Recommender
    
- Amazon Web Services Cost Optimization Hub
    

The key idea:

> Use metadata and telemetry to continuously identify inefficient batch jobs and automatically generate optimization recommendations.

---

# 1. Problem Statement

Large enterprises run:

```text
1000+ pipelines
100+ TB/day
Millions of dollars/year in compute
```

Most inefficiencies remain hidden:

- Full table scans
    
- Poor partitioning
    
- Data skew
    
- Small files
    
- Wrong join strategies
    
- Overprovisioned clusters
    
- Repeated transformations
    

The platform should:

```text
Observe
Analyze
Recommend
Learn
```

without modifying business logic.

---

# 2. High-Level Architecture

```text
                ┌────────────────────┐
                │ Batch Pipelines    │
                │ Spark/DuckDB/dbt   │
                └─────────┬──────────┘
                          │
                          ▼
              ┌─────────────────────┐
              │ Metadata Collectors │
              └─────────┬───────────┘
                        │
                        ▼
             ┌──────────────────────┐
             │ Metadata Lakehouse   │
             └─────────┬────────────┘
                       │
        ┌──────────────┼───────────────┐
        ▼              ▼               ▼

 Rule Engine   Pattern Engine   ML Engine

        ▼              ▼               ▼

             Recommendation Engine

                       ▼

             Dashboards / APIs
```

---

# 3. Metadata Collection Layer

The most important layer.

Without metadata, optimization is impossible.

---

## A. Query Metadata

Capture:

```json
{
  "query_id": "q123",
  "job_id": "daily_sales",
  "query_text": "...",
  "tables": ["sales","customer"],
  "join_count": 2,
  "group_by_count": 1,
  "order_by_count": 0
}
```

Extraction methods:

- SQL parser
    
- Logical plan parser
    
- Query fingerprinting
    

---

## B. Execution Telemetry

Capture:

```json
{
  "runtime_sec": 320,
  "cpu_time_sec": 290,
  "memory_peak_gb": 64,
  "spill_gb": 12,
  "shuffle_gb": 800
}
```

Sources:

- Spark event logs
    
- DuckDB profiling
    
- Airflow metadata
    
- Warehouse telemetry
    

---

## C. Data Layout Metadata

Capture:

```json
{
  "table":"sales",
  "partition_columns":["sale_date"],
  "file_count":50000,
  "avg_file_mb":3,
  "format":"parquet"
}
```

Used for:

- Small file detection
    
- Partition recommendations
    

---

## D. Historical Metadata

Store:

```text
Runtime history
Data growth history
Cost history
SLA history
```

This enables trend analysis.

---

# 4. Metadata Repository

Store everything centrally.

Example schema:

### Job Fact

```sql
job_fact
---------
job_id
run_id
runtime_sec
status
input_gb
output_gb
cost_usd
```

---

### Query Fact

```sql
query_fact
-----------
query_id
job_id
join_count
groupby_count
filter_count
```

---

### Storage Fact

```sql
storage_fact
-------------
table_name
partition_count
file_count
avg_file_size
```

---

### Recommendation Fact

```sql
recommendation_fact
-------------------
recommendation_id
job_id
severity
recommendation
estimated_savings
```

---

# 5. Optimization Rule Engine

First version should be deterministic.

Rules are easy to explain.

---

## Rule 1: Scan Waste

```python
if scan_bytes / output_bytes > 100:
    emit("Excessive scanning")
```

Example:

```text
30 TB scanned
40 GB output
```

Recommendation:

```text
Enable partition pruning
```

---

## Rule 2: Small Files

```python
if avg_file_size < 32MB:
    emit("Small file problem")
```

Recommendation:

```text
Run compaction
```

---

## Rule 3: Data Skew

```python
if max_task_time / median_task_time > 10:
    emit("Potential skew")
```

Recommendation:

```text
Investigate join keys
```

---

## Rule 4: Excessive Shuffle

```python
if shuffle_bytes > input_bytes * 3:
    emit("Shuffle heavy workload")
```

---

## Rule 5: Runtime Regression

```python
if runtime > p95_runtime:
    emit("Performance regression")
```

---

# 6. Query Pattern Engine

Detect recurring anti-patterns.

Example:

```sql
SELECT *
FROM sales
WHERE DATE(order_ts)='2026-06-01'
```

Problem:

```text
Function on filter column
```

Recommendation:

```sql
WHERE order_date='2026-06-01'
```

---

Another example:

```sql
SELECT *
```

from:

```text
200-column table
```

Recommendation:

```text
Column pruning opportunity
```

---

# 7. Data Layout Advisor

Analyzes:

```text
Access patterns
Filter columns
Join columns
Aggregation columns
```

Generates:

### Partition Recommendation

Current:

```text
Partition: region
```

Observed workload:

```text
95% queries filter sale_date
```

Recommendation:

```text
Partition by sale_date
```

---

### Clustering Recommendation

Observed:

```text
Frequent filters on customer_id
```

Recommend:

```text
Sort / Cluster by customer_id
```

---

# 8. Resource Optimization Engine

Analyze cluster utilization.

Example:

```text
Executors = 100
CPU Utilization = 15%
```

Recommendation:

```text
Reduce executors to 40
```

Potential savings:

```text
60%
```

---

# 9. ML/AI Layer

Once enough metadata exists.

Features:

```text
Runtime
Input Size
Shuffle
Spill
Partition Count
File Count
CPU
Memory
```

Models:

### Anomaly Detection

Detect:

```text
Job normally runs 20 min
Today 90 min
```

---

### Recommendation Ranking

Estimate:

```text
Optimization effort
vs
Expected savings
```

Prioritize highest ROI.

---

# 10. Recommendation Engine

Convert findings into actions.

Example output:

```json
{
  "job":"daily_sales",
  "severity":"HIGH",
  "issue":"Partition pruning ineffective",
  "evidence":"3650 partitions scanned",
  "recommendation":"Partition on sale_date",
  "estimated_runtime_reduction":"70%"
}
```

---

# 11. API Layer

Provide:

```text
GET /jobs
GET /recommendations
GET /hotspots
GET /cost-savings
```

Used by:

- Dashboards
    
- Copilots
    
- AI agents
    

---

# 12. Dashboard

Key views:

### Optimization Hotspots

|Job|Waste Score|
|---|---|
|sales_batch|92|
|orders_batch|87|

---

### Savings Opportunity

|Job|Estimated Savings|
|---|---|
|sales_batch|$50K/year|
|orders_batch|$20K/year|

---

### SLA Risk

|Job|Risk|
|---|---|
|customer_batch|High|

---

# Advanced Version (What I'd Build for Your AI Lakehouse Project)

Given your DuckDB-based optimization platform, I'd add:

```text
Metadata Collection
        ↓
Telemetry Graph
        ↓
Optimization Knowledge Base
        ↓
LLM Reasoning Layer
        ↓
Recommendation Generation
```

Where the LLM receives:

```json
{
  "query_features": {...},
  "telemetry": {...},
  "storage_metadata": {...},
  "historical_runs": {...}
}
```

and generates:

```text
Root Cause:
Partition pruning not applied

Evidence:
3650 partitions scanned

Recommendation:
Partition by event_date

Estimated Savings:
72%
```

This evolves the platform from a **rule engine** into an **AI-powered optimization advisor** that explains _why_ a job is inefficient, not just _that_ it is inefficient.