---
domain: Data Engineering
domain_suggested: null
category: Snippet
category_suggested: null
source_type: obsidian
status: review
tags: [query-plan, intelligence, optimization]
---




```table-of-contents
```
# Objective
Build an AI-driven optimization engine capable of:
- Analyzing query plans
- Detecting performance bottlenecks
- Recommending optimizations
- Predicting runtime and cost
- Eventually applying safe optimizations automatically
The query execution plan is the primary source of optimization intelligence.
---
# Architecture Overview
```
SQL Query
    ↓
Query Planner
    ↓
Logical Plan
    ↓
Physical Plan
    ↓
Feature Extraction Layer
    ↓
Optimization Knowledge Graph
    ↓
AI Recommendation Engine
    ↓
Optimization Suggestions
```
---
# Query Plan Information to Extract
## 1. Query Shape Features
Purpose:  
Understand query complexity and workload patterns.
### Attributes
```
{
  "query_type": "SELECT",
  "table_count": 2,
  "join_count": 1,
  "join_types": ["HASH_JOIN"],
  "aggregation_count": 1,
  "window_function_count": 0,
  "cte_count": 1,
  "subquery_count": 2,
  "query_type": "SELECT"
}
```
### Why It Matters
Signals:
- Query complexity
- Resource consumption likelihood
- Runtime prediction
- Cost estimation
---
## 2. Scan-Level Metadata
Purpose:  
Measure data access efficiency.
### Attributes
```
{
  "table_name": "sales",
  "scan_type": "PARQUET_SCAN",
  "estimated_rows": 1000000000,
  "actual_rows": 950000000,
  "bytes_scanned": 1200000000000,
  "files_scanned": 4000,
  "partitions_scanned": 365,
  "partitions_total": 365
}
```
### Derived Signals
#### Partition Pruning Effectiveness
```
partitions_scanned / partitions_total
```
#### Scan Efficiency
```
rows_returned / rows_scanned
```
Optimization opportunities:
- Better partitioning
- File compaction
- Predicate pushdown
---
## 3. Join Intelligence
Purpose:  
Identify expensive data movement and join strategies.
### Attributes
```
{
  "join_type": "HASH_JOIN",
  "left_rows": 1000000000,
  "right_rows": 10000,
  "output_rows": 50000000,
  "join_keys": ["customer_id"]
}
```
### Derived Features
#### Broadcast Join Candidate
```
right_rows < broadcast_threshold
```
#### Join Selectivity
```
output_rows / max(left_rows,right_rows)
```
#### Cartesian Join Detection
```
join condition missing
```
Optimization opportunities:
- Broadcast joins
- Join reordering
- Predicate pushdown
- Join elimination
---
## 4. Shuffle Analysis
Purpose:  
Measure distributed execution cost.
### Attributes
```
{
  "shuffle_read_gb": 850,
  "shuffle_write_gb": 920,
  "shuffle_partitions": 200
}
```
### Derived Metrics
#### Shuffle Amplification
```
shuffle_bytes / scan_bytes
```
#### Partition Balance
```
largest_partition / average_partition
```
Optimization opportunities:
- Repartitioning
- Adaptive Query Execution
- Better partition keys
---
## 5. Data Skew Detection
Purpose:  
Identify uneven workload distribution.
### Attributes
```
{
  "largest_partition_mb": 15000,
  "average_partition_mb": 100
}
```
### Skew Ratio
```
largest_partition / average_partition
```
Example:
```
15000 / 100 = 150x
```
Classification:
```
1-5      Normal
5-20     Moderate
20+      Severe
100+     Critical
```
Optimization opportunities:
- Salting
- Repartitioning
- AQE skew handling
---
## 6. Cardinality Estimation Accuracy
Purpose:  
Measure optimizer statistics quality.
### Attributes
```
{
  "estimated_rows": 10000,
  "actual_rows": 5000000
}
```
### Error Ratio
```
actual_rows / estimated_rows
```
Example:
```
500x estimation error
```
Optimization opportunities:
- Refresh statistics
- Analyze tables
- Histograms
---
## 7. Operator Cost Breakdown
Purpose:  
Find execution hotspots.
### Attributes
```
{
  "operator": "HASH_AGGREGATE",
  "cpu_ms": 50000,
  "memory_mb": 12000,
  "rows_in": 500000000,
  "rows_out": 1000
}
```
### Top Operators
Track:
- Hash Join
- Sort
- Aggregate
- Window
- Scan
- Exchange
Output:
```
Top Costly Operators
Cost Contribution %
```
---
## 8. Spill Detection
Purpose:  
Detect memory pressure.
### Attributes
```
{
  "memory_spill_gb": 80,
  "disk_spill_gb": 120
}
```
Optimization opportunities:
- Increase memory
- Reduce partition size
- Fix skew
- Tune shuffle partitions
---
## 9. Filter Effectiveness
Purpose:  
Measure filtering efficiency.
### Attributes
```
{
  "rows_before_filter": 1000000000,
  "rows_after_filter": 5000
}
```
### Filter Reduction Ratio
```
rows_after / rows_before
```
Optimization opportunities:
- Earlier filtering
- Predicate pushdown
- Materialized views
---
## 10. Aggregation Efficiency
Purpose:  
Measure data reduction.
### Attributes
```
{
  "input_rows": 1000000000,
  "output_rows": 100
}
```
### Aggregation Compression
```
input_rows / output_rows
```
Optimization opportunities:
- Partial aggregation
- Pre-aggregation
- Materialized aggregates
---
## 11. Data Movement Metrics
Purpose:  
Understand network bottlenecks.
### Attributes
```
{
  "network_transfer_gb": 450,
  "remote_reads_gb": 300,
  "local_reads_gb": 20
}
```
Optimization opportunities:
- Data locality
- Better partition placement
- Reduced shuffle
---
## 12. Runtime Telemetry Correlation
Purpose:  
Combine plan and execution metrics.
### Attributes
```
{
  "cpu_pct": 90,
  "memory_pct": 40,
  "network_pct": 15,
  "disk_pct": 5
}
```
### Bottleneck Classification
```
CPU Bound
Memory Bound
Network Bound
Disk Bound
Mixed
```
---
# Core AI Features
## Feature Vector
Recommended model input:
```
{
  "scan_gb": 1200,
  "shuffle_gb": 900,
  "spill_gb": 80,
  "join_count": 5,
  "aggregation_count": 2,
  "skew_ratio": 150,
  "partition_pruning": false,
  "predicate_pushdown": false,
  "broadcast_candidate": true,
  "cardinality_error": 500
}
```
---
# Recommendation Engine
## Rule-Based Layer
Examples:
### Partition Pruning
```
IF
partitions_scanned > 80%
THEN
recommend partitioning strategy review
```
### Broadcast Join
```
IF
small_table_size < threshold
THEN
recommend broadcast join
```
### Statistics
```
IF
cardinality_error > 10x
THEN
recommend ANALYZE TABLE
```
### Skew
```
IF
skew_ratio > 20
THEN
recommend salting
```
---
# ML Models
Potential prediction targets:
### Runtime Prediction
```
Predicted Runtime (seconds)
```
### Cost Prediction
```
Predicted Compute Cost
```
### Failure Prediction
```
Probability of Failure
```
### SLA Prediction
```
Probability of Missing SLA
```
---
# Recommended Metadata Schema
```
{
  "query_id": "",
  "query_hash": "",
  "query_type": "",
  "tables": [],
  "joins": [],
  "operators": [],
  "scan_bytes": 0,
  "shuffle_bytes": 0,
  "network_bytes": 0,
  "spill_bytes": 0,
  "estimated_rows": 0,
  "actual_rows": 0,
  "skew_ratio": 0,
  "partition_pruning": false,
  "predicate_pushdown": false,
  "broadcast_candidate": false,
  "runtime_sec": 0,
  "cost_score": 0
}
```
---
# Top 10 Features to Prioritize First
1. Bytes Scanned
2. Shuffle Volume
3. Data Skew Ratio
4. Join Strategy
5. Spill Volume
6. Partition Pruning Effectiveness
7. Predicate Pushdown Effectiveness
8. Estimated vs Actual Rows
9. Operator Cost Distribution
10. Runtime Telemetry Correlation
These features typically explain the majority of performance issues across Spark, Databricks, Snowflake, Trino, DuckDB, BigQuery, and modern lakehouse architectures.
---
This document can serve as the foundation for the next implementation phase: designing the normalized query-plan feature extraction layer and the metadata catalog schema that feeds your AI optimization engine.