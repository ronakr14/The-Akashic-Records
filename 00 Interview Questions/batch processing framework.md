Design a batch processing framework from scratch.
Requirements:
* Scheduling
* Dependency management
* Retries
* Metadata collection
* Data quality
* Observability
* Cost optimization
Designing a batch processing framework from scratch is essentially designing a mini version of systems like Apache Airflow, Dagster, AWS Glue, and Databricks Workflows combined into a single platform.

The key principle:

> Separate orchestration, execution, metadata, and observability into independent services.

---

# High-Level Architecture

```text
                 +-------------------+
                 |  UI / API Layer   |
                 +---------+---------+
                           |
                           v
                 +-------------------+
                 | Metadata Catalog  |
                 +---------+---------+
                           |
         +-----------------+----------------+
         |                                  |
         v                                  v

+----------------+              +------------------+
| Scheduler      |              | Monitoring       |
| Service        |              | Service          |
+-------+--------+              +--------+---------+
        |                                |
        v                                v

+-----------------------------------------------+
| DAG Orchestrator                              |
+----------------+------------------------------+
                 |
                 v

+-----------------------------------------------+
| Execution Engine                              |
| Spark / Flink / SQL / Python / Containers     |
+----------------+------------------------------+
                 |
                 v

+-----------------------------------------------+
| Storage Layer                                 |
| Lakehouse / Warehouse / Object Storage        |
+-----------------------------------------------+
```

---

# 1. Scheduling Layer

## Responsibilities

- Trigger jobs
    
- Support cron schedules
    
- Event-based execution
    
- Backfill processing
    

### Metadata

```sql
job_schedule
-------------
job_id
cron_expression
timezone
enabled
next_run_time
last_run_time
```

Example:

```text
daily_sales_load
0 2 * * *
```

Runs every day at 2 AM.

---

## Scheduler Workflow

Every minute:

```python
for job in schedules:
    if current_time >= next_run:
        create_run(job)
```

Creates:

```sql
job_run
------------
run_id
job_id
start_time
status
```

---

# 2. Dependency Management

Represent jobs as DAGs.

Example:

```text
raw_orders
      |
      v
stg_orders
      |
      v
fact_orders
      |
      v
sales_dashboard
```

Store DAG metadata:

```sql
job_dependencies
-----------------
parent_job
child_job
```

---

## DAG Validation

Detect:

- Cycles
    
- Missing jobs
    
- Invalid dependencies
    

Example:

```text
A -> B -> C -> A
```

Reject deployment.

Use topological sorting.

Complexity:

```text
O(V + E)
```

---

# 3. Execution Framework

Each task runs independently.

Task definition:

```yaml
task:
  name: customer_load
  engine: spark
  retries: 3
  timeout: 2h
```

Supported engines:

|Engine|Use Case|
|---|---|
|SQL|ELT|
|Spark|Large data|
|Python|Transformations|
|Container|Custom workloads|

Executor API:

```python
execute(task_id)
```

Returns:

```json
{
  "status":"SUCCESS",
  "duration":120
}
```

---

# 4. Retry Framework

Failures happen.

Need automatic recovery.

---

## Retry Metadata

```sql
task_runs
-----------
task_run_id
attempt_number
status
error_message
```

---

## Retry Logic

```python
max_retries = 3

while retries < max_retries:
    execute()
```

Backoff:

```text
Retry 1 → 1 min
Retry 2 → 5 min
Retry 3 → 15 min
```

Avoids cascading failures.

---

## Retry Categories

### Retry

Transient failures:

```text
Network timeout
Temporary cluster issue
Storage unavailable
```

### No Retry

Permanent failures:

```text
Syntax error
Schema mismatch
Missing column
```

Classification reduces waste.

---

# 5. Metadata Collection Framework

This becomes the brain of the platform.

Every execution generates metadata.

---

## Job Metadata

```sql
job_run
---------
run_id
job_id
status
start_time
end_time
duration
```

---

## Task Metadata

```sql
task_run
---------
task_id
rows_read
rows_written
bytes_read
bytes_written
cpu_seconds
memory_peak
shuffle_bytes
```

---

## Dataset Metadata

```sql
dataset_metadata
------------------
dataset_name
row_count
file_count
size_bytes
partition_count
```

---

## Query Metadata

Capture:

```text
Query text
Execution plan
Scan volume
Join count
Aggregation count
Runtime
```

This later powers AI optimization.

---

# 6. Data Quality Framework

Never publish bad data.

---

## Validation Pipeline

```text
Extract
   |
Validate
   |
Publish
```

Not:

```text
Extract
   |
Publish
```

---

## Quality Rules

### Row Count

```sql
current_count >= yesterday_count * 0.9
```

---

### Null Check

```sql
customer_id IS NOT NULL
```

---

### Uniqueness

```sql
order_id unique
```

---

### Referential Integrity

```sql
fact.customer_id
exists in dim_customer
```

---

### Freshness

```text
data age < 2 hours
```

---

## Quality Metadata

```sql
dq_results
------------
rule_name
dataset
status
failed_rows
```

Failed quality checks:

```text
Do not publish
Raise incident
```

---

# 7. Observability Platform

Three pillars:

---

## Metrics

Store:

```text
Runtime
Rows processed
Cost
CPU
Memory
Failures
Retries
```

Example:

```text
fact_orders
runtime=15m
rows=1.2B
```

---

## Logs

Centralized logs:

```text
Task started
Task completed
Task failed
```

Searchable by:

```text
run_id
job_id
task_id
```

---

## Traces

Track execution path:

```text
Pipeline
 ├── Task A
 ├── Task B
 └── Task C
```

Useful for bottleneck analysis.

---

# 8. SLA Management

Store:

```sql
sla_definition
---------------
job_id
expected_duration
deadline
```

Example:

```text
Must finish before 7 AM
```

---

Monitor:

```python
predicted_finish > SLA
```

Alert early.

---

# 9. Cost Optimization Framework

This is where many platforms stop.

A modern framework should optimize automatically.

---

## Collect Cost Signals

Per job:

```text
CPU hours
Memory hours
Storage IO
Network IO
Cluster size
```

---

## Detect Waste

### Small Files

```text
10,000 files
20 KB each
```

Recommend:

```text
Compaction
```

---

### Over-Partitioning

```text
3650 partitions
5 MB each
```

Recommend:

```text
Partition redesign
```

---

### Excessive Scans

```text
10 TB scanned
100 rows returned
```

Recommend:

```text
Partition pruning
Z-ordering
Indexing
```

---

### Skew

```text
One task = 90%
Others = 10%
```

Recommend:

```text
Salting
Repartitioning
```

---

### Bad Join Strategy

```text
Shuffle join
small dimension table
```

Recommend:

```text
Broadcast join
```

---

# 10. Incident Management

When a job fails:

```text
Failure
   |
Root Cause Detection
   |
Auto Retry
   |
Escalation
   |
Ticket Creation
```

Incident metadata:

```sql
incidents
-----------
incident_id
job_id
root_cause
severity
resolution
```

---

# 11. Metadata-Driven Architecture

The most scalable design is:

```text
Code = Generic
Behavior = Metadata
```

Example:

Instead of:

```python
run_customer_pipeline()
run_sales_pipeline()
run_marketing_pipeline()
```

Use:

```sql
pipeline_definition
-------------------
pipeline_name
source
target
rules
schedule
```

Generic engine:

```python
execute(metadata)
```

Now adding a pipeline requires:

```text
Insert metadata
No code deployment
```

---

# Future Evolution (AI-Native Batch Platform)

Once metadata is collected, build an optimization engine that learns from executions:

```text
Historical Runs
      |
      v
Metadata Lake
      |
      v
Feature Extraction
      |
      v
ML/LLM Optimizer
```

Capabilities:

- Predict SLA violations before execution
    
- Recommend partition strategies
    
- Detect skew automatically
    
- Estimate runtime before execution
    
- Recommend cluster sizing
    
- Generate query optimizations
    
- Auto-remediate common failures
    

The architecture becomes:

```text
Scheduler
     |
Orchestrator
     |
Execution Engine
     |
Metadata Layer
     |
AI Optimization Layer
```

In mature data organizations, the metadata layer is often more valuable than the execution engine itself because it enables reliability, governance, observability, and continuous optimization across every batch workload.