# Objective
Design a system capable of predicting batch job runtime before execution using historical telemetry, workload characteristics, and infrastructure metrics.
The predicted runtime can be used for:
- SLA forecasting
- Resource planning
- Cost estimation
- Capacity management
- Automated optimization recommendations
- Intelligent scheduling
---
# Problem Statement
Batch workloads often experience runtime variability due to:
- Data growth
- Data skew
- Small file problems
- Cluster contention
- Code changes
- Infrastructure changes
Traditional approaches such as using average runtime are inaccurate and do not scale.
The goal is to build a telemetry-driven prediction engine that learns from historical executions and continuously improves.

---
# Data Collection Requirements
## Job Metadata
Collect:

|Field|Description|
|---|---|
|job_id|Unique job identifier|
|pipeline_id|Parent pipeline|
|workflow_id|DAG/workflow identifier|
|environment|Dev/Test/Prod|
|code_version|Git commit/version|
|schedule_type|Daily/Hourly/etc|

---
## Runtime Metrics

| Field              | Description              |
| ------------------ | ------------------------ |
| start_time         | Job start                |
| end_time           | Job end                  |
| runtime_seconds    | Total execution duration |
| queue_wait_seconds | Scheduler wait           |
|retry_count|Number of retries|

---
## Data Characteristics
|   |   |
|---|---|
|Field|Description|
|input_rows|Rows processed|
|input_bytes|Bytes scanned|
|output_rows|Rows written|
|output_bytes|Bytes written|
|partition_count|Number of partitions|
|file_count|Files processed|

---
## Execution Metrics
|   |   |
|---|---|
|Field|Description|
|cpu_utilization|CPU usage|
|memory_utilization|Memory usage|
|shuffle_bytes|Shuffle volume|
|spill_bytes|Spill volume|
|network_bytes|Network transfer|
|disk_io_bytes|Disk activity|

---
## Cluster Metrics
|   |   |
|---|---|
|Field|Description|
|executor_count|Executors used|
|executor_cores|Total cores|
|executor_memory|Allocated memory|
|concurrent_jobs|Cluster contention|
|cluster_load|Utilization level|

---
# Runtime Drivers
The strongest predictors of runtime are usually:
```
Runtime ≈f(Input Size,Rows,Partitions,Shuffle Size,File Count,Concurrency,Cluster Size)
```
Typical runtime influencers:
### Data Volume
Higher scan volume generally increases runtime.
### Shuffle Volume
Often the strongest predictor for Spark workloads.
### Small File Count
Large numbers of small files increase metadata and scheduling overhead.
### Data Skew
Uneven partitions significantly increase execution time.
### Cluster Contention
Concurrent workloads reduce available resources.

---
# Feature Engineering
## Raw Features
- input_bytes
- input_rows
- output_rows
- shuffle_bytes
- file_count
- executor_count
- cpu_hours
- memory_gb_hours
- day_of_week
- hour_of_day
---
## Derived Features
### Shuffle Ratio
shuffle_ratio = shuffle_bytes / input_bytes
Measures network-intensive workloads.

---
### Data Skew Ratio
skew_ratio =  
largest_partition /  
average_partition
Detects workload imbalance.

---
### Small File Ratio
small_file_ratio =  
small_files /  
total_files
Identifies metadata bottlenecks.

---
### Resource Density
resource_density =  
cores /  
input_tb
Measures compute allocation efficiency.


---
# Modeling Strategy
## Phase 1: Baseline
Linear Regression
Advantages:
- Fast
- Explainable
- Easy to validate
Typical accuracy:
70–80%

---
## Phase 2: Production Model
Recommended:
- XGBoost
- LightGBM
- Random Forest
Benefits:
- Handles non-linear relationships
- Captures thresholds
- Works well with telemetry data
Expected accuracy:
85–95%
depending on telemetry quality.

---
# Job-Specific Models
Global models often underperform.
Recommended:
### Option 1
One model per job.
Example:
Customer ETL Model
Sales ETL Model
Inventory ETL Model

---
### Option 2
One model per workload category.
Examples:
- Dimension Loads
- Fact Loads
- Aggregation Jobs
- Machine Learning Pipelines
- Reporting Workloads
---
# Runtime Prediction Flow
## Input
Upcoming Job
Example:
Input Size = 8 TB
Files = 500,000
Expected Shuffle = 12 TB
Executors = 100

---
## Model Output
Runtime Prediction:
78 minutes
Confidence Interval:
78 ± 8 minutes

---
# SLA Risk Prediction
Build an additional classification model.
Target:
Will SLA be violated?
Output:
Probability Score
Example:
92% SLA Breach Risk
Benefits:
- Easier business interpretation
- Better alerting
- Better scheduling decisions
---
# Online Runtime Prediction
Static predictions are insufficient.
During execution:
Collect:
- Actual scan rate
- Actual shuffle rate
- Spill metrics
- Skew metrics
Recompute prediction.
Example:
Initial Estimate:  
60 min
After 20% Completion:  
95 min
After Skew Detection:  
140 min
This enables proactive intervention.

---
# Recommended Metadata Schema
## Job Run Table
job_run_metrics
Contains:
- job_id
- run_id
- runtime_seconds
- input_bytes
- output_bytes
- shuffle_bytes
- spill_bytes
- cpu_hours
- memory_gb_hours
- executor_count
- cluster_load
---
## Feature Store Table
runtime_features
Contains engineered features used by training pipelines.

---
## Prediction Table
runtime_predictions
Contains:
- prediction_id
- job_id
- predicted_runtime
- actual_runtime
- confidence_score
- model_version
- prediction_timestamp
---
# Future Enhancements
## Cost Prediction
Predict:
- Cloud spend
- Compute hours
- Storage costs
---
## Resource Recommendation
Recommend:
- Executors
- Memory
- Partitions
- Cluster size
---
## Optimization Recommendation
Predict and recommend:
- File compaction
- Join optimization
- Partition tuning
- Shuffle reduction
- Broadcast join opportunities
---
## Autonomous Optimization
Future state:
1. Predict runtime
2. Detect bottlenecks
3. Recommend optimization
4. Apply safe optimization
5. Measure improvement
6. Learn from results
---
# Target Architecture
Historical Runs  
↓  
Telemetry Collection  
↓  
Feature Store  
↓  
Feature Engineering  
↓  
ML Runtime Model  
↓  
Runtime Prediction  
↓  
SLA Prediction  
↓  
Cost Prediction  
↓  
Optimization Recommendation Engine

---
# Key Takeaways
1. Runtime prediction is primarily a telemetry and feature-engineering problem.
2. Shuffle volume, skew, and data size are typically the strongest predictors.
3. Tree-based models outperform simple averages and regression models.
4. Job-specific models provide significantly better accuracy.
5. Online prediction during execution improves reliability.
6. Runtime prediction becomes the foundation for SLA management, cost forecasting, and autonomous workload optimization.
This document can serve as the design baseline for a future **AI-driven Lakehouse Optimizer** where runtime prediction, cost prediction, bottleneck detection, and optimization recommendations are integrated into a single decision engine.
!