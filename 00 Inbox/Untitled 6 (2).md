This is actually a stronger hackathon problem than it looks.

Most teams will build:

> Chatbot + SQL metadata + LLM summary

and call it "AI Optimization."

Judges specifically warned against that.

The winning projects will look more like:

> Autonomous FinOps + Query Intelligence + Optimization Agent

rather than a chatbot.

---

# What I would build

## Project Name

**LakeMind**

### AI-Powered Self-Optimizing Lakehouse

Tagline:

> Observe → Analyze → Reason → Recommend → Simulate

The important part is:

**Optimization recommendations must be generated from evidence, not from generic LLM advice.**

---

# Core Idea

Instead of analyzing a single query:

Build an agent that continuously learns from:

- Query history
    
- Query plans
    
- Table metadata
    
- Partition layouts
    
- Cluster metrics
    
- Storage statistics
    
- ETL execution history
    

and produces:

- Root-cause analysis
    
- Optimization recommendations
    
- Cost savings estimates
    
- Auto-generated optimization scripts
    

---

# Architecture

```text
                    +----------------+
                    | Streamlit UI   |
                    +-------+--------+
                            |
                            v

+------------------------------------------------+
|             Optimization Agent                 |
|------------------------------------------------|
| Query Agent                                    |
| Storage Agent                                  |
| Cost Agent                                     |
| ETL Agent                                      |
| Partition Agent                                |
+------------------------------------------------+
                 |
                 v

+------------------------------------------------+
|      Optimization Knowledge Graph              |
+------------------------------------------------+

                 |
                 v

+------------------------------------------------+
|      Lakehouse Telemetry Layer                 |
|------------------------------------------------|
| Query Logs                                     |
| Spark History                                  |
| Delta Metadata                                 |
| Cluster Metrics                                |
| Storage Statistics                             |
+------------------------------------------------+

                 |
                 v

      DuckDB + Delta Lake
```

---

# Why This Is Different

Instead of:

```text
User:
Why is query slow?

LLM:
Maybe missing partitioning.
```

You do:

```text
Agent:
Query scanned 1.2 TB.

Partition pruning not used.

Filter column:
country

Table partition:
ingestion_date

Estimated wasted scan:
92%

Recommendation:
Repartition by country + ingestion_date

Expected cost reduction:
38%
```

Now it becomes engineering intelligence.

---

# Feature 1

## Query DNA Analyzer

This alone can be a hackathon winner.

Every query becomes:

```json
{
  "tables": [...],
  "joins": [...],
  "filters": [...],
  "scan_size": "...",
  "duration": "...",
  "user": "...",
  "warehouse": "..."
}
```

Then cluster similar queries.

Example:

```text
1000 daily queries

400 belong to:
Sales Dashboard

300 belong to:
Customer Analytics

300 belong to:
Adhoc Users
```

Now discover:

```text
Top expensive query families
```

rather than individual queries.

This is much more enterprise-like.

---

# Feature 2

## Partition Advisor

Input:

```text
Query history
```

Agent computes:

```text
Filter frequency
Cardinality
Skew
Scan percentage
```

Example:

```text
Table:
sales

Queries:

WHERE region
70%

WHERE order_date
20%

WHERE customer_id
10%
```

Agent recommends:

```text
Partition:
region

ZORDER:
order_date
```

with reasoning.

---

# Feature 3

## Join Intelligence Engine

This is very visual.

Analyze:

```text
Join type
Broadcast usage
Shuffle size
Skew
```

Example:

```text
orders
2 GB

customers
10 MB
```

Current:

```sql
SELECT *
FROM orders o
JOIN customers c
```

Agent:

```text
Broadcast join possible.

Current shuffle:
2.1 GB

Expected shuffle:
10 MB
```

Estimated runtime reduction:

```text
45%
```

Judges will love this.

---

# Feature 4

## Dataset Graveyard Detector

Enterprise pain.

Find:

```text
Tables never queried
```

for:

```text
30 days
60 days
90 days
```

Output:

```text
Unused datasets:
132

Storage:
15 TB

Potential savings:
$420/month
```

Very practical.

---

# Feature 5

## Cost Attribution Engine

Connect:

```text
Query
→ User
→ Team
→ Cluster
→ Cost
```

Example:

```text
Marketing Team

Cost:
$1200/month

Top driver:
dashboard_refresh.sql

42% of spend
```

Classic FinOps.

---

# Feature 6

## Cluster Rightsizing Agent

Analyze:

```text
CPU
Memory
Concurrency
Idle Time
```

Example:

```text
Current cluster:
16 workers

Average utilization:
18%
```

Recommendation:

```text
8 workers

Projected savings:
48%
```

This feels very enterprise.

---

# Feature 7

## Optimization Script Generator

This is where AI becomes visible.

Agent generates:

```sql
OPTIMIZE sales;

VACUUM sales RETAIN 168 HOURS;
```

or

```sql
ALTER TABLE sales
PARTITIONED BY (region);
```

or

```sql
CREATE MATERIALIZED VIEW mv_sales;
```

Judges will see actual actionability.

---

# Feature 8

## What-If Simulator

This could be your differentiator.

User asks:

> What happens if I partition sales by region?

Agent simulates:

```text
Current scan:
1.2 TB

Expected scan:
180 GB

Expected runtime:
-55%

Expected cost:
-42%
```

Now you're not merely recommending.

You're forecasting.

That's very strong.

---

# Feature 9

## Optimization Knowledge Graph

Most teams won't do this.

Nodes:

```text
Query
Table
User
Pipeline
Cluster
Dataset
```

Relationships:

```text
USES
SCANS
JOINS
WRITES
RUNS_ON
```

Now the agent can reason.

Example:

```text
Query A

depends on

Pipeline B

which creates

Table C

which causes skew
```

Suddenly root-cause analysis becomes much more powerful.

---

# Feature 10

## Self-Healing Agent

This aligns with your earlier self-healing ETL interests.

Example:

```text
Daily ETL suddenly
3x slower
```

Agent discovers:

```text
File count explosion

10,000 small files
```

Recommendation:

```sql
OPTIMIZE TABLE
```

or

```text
Compact files
```

Potentially auto-generate remediation.

This is hackathon gold because it moves from analytics to autonomous action.

---

# If I Had Only 10 Days

I would NOT build all 10 features.

I'd build 4 exceptionally well:

### 1. Query DNA Analyzer

### 2. Partition Advisor

### 3. Join Intelligence Engine

### 4. What-If Simulator

Then add:

### Optimization Script Generator

as the AI showcase.

---

# Minimal Demo Flow

Upload:

```text
query_history.csv
table_metadata.csv
cluster_metrics.csv
```

Agent pipeline:

```text
Analyze
↓
Detect inefficiencies
↓
Reason
↓
Estimate savings
↓
Generate scripts
↓
Show dashboard
```

Demo question:

> Why is sales dashboard slow?

Agent:

```text
Root Causes

1. Missing partition pruning
2. Large shuffle join
3. Small file fragmentation

Potential savings

Compute:
37%

Storage:
18%

Runtime:
52%

Generated Fixes:
[SQL scripts]
```

That demonstrates:

- AI reasoning
    
- Lakehouse knowledge
    
- FinOps
    
- Cost optimization
    
- Autonomous recommendations
    

which aligns almost perfectly with the judging criteria.

The key design decision I'd make is to treat the LLM as the **reasoning layer**, not the analytics layer. All metrics, skew detection, partition analysis, join analysis, cost estimation, and workload mining should come from deterministic engines. The LLM's job is to explain, prioritize, simulate, and generate remediation plans from those facts. That's the difference between a chatbot and a credible lakehouse optimization platform.



Good choice. If you build the Query DNA Analyzer properly, it becomes the foundation for almost every other feature (partition advisor, join intelligence, cost attribution, workload clustering, optimization recommendations).

## What is Query DNA?

Think of it as converting a raw SQL query and its execution metadata into a structured fingerprint.

Instead of storing:

```sql
SELECT *
FROM sales s
JOIN customers c ON s.customer_id = c.id
WHERE region = 'APAC'
```

you store:

```json
{
  "query_id": "q123",
  "tables": ["sales", "customers"],
  "join_count": 1,
  "join_type": ["inner"],
  "filter_columns": ["region"],
  "group_by_columns": [],
  "order_by_columns": [],
  "estimated_scan_gb": 120,
  "execution_time_sec": 45,
  "cluster": "warehouse_a",
  "user": "marketing_team",
  "query_family": "sales_customer_lookup"
}
```

Now thousands of queries become analyzable.

---

# What raw data do you need?

There are 4 levels.

## Level 1 (Minimum Viable)

Only query history.

Example:

|query_id|sql_text|execution_time|
|---|---|---|
|q1|SELECT ...|45|
|q2|SELECT ...|32|

Can be:

- Spark history logs
    
- Databricks query history
    
- Snowflake query history
    
- Trino query logs
    
- Athena query logs
    

This is enough for:

- table extraction
    
- join extraction
    
- filter extraction
    
- query clustering
    

---

## Level 2 (Good)

Add execution statistics.

Example:

|query_id|duration|bytes_scanned|rows_scanned|
|---|---|---|---|
|q1|45 sec|1.2 TB|800M|

Now you can identify:

```text
Slow because:
- huge scan
- large joins
- excessive aggregation
```

---

## Level 3 (Strong)

Add query execution plans.

Example:

```json
{
  "operator": "HashJoin",
  "shuffle_bytes": "1.8GB",
  "broadcast": false
}
```

Spark EXPLAIN output.

Databricks query profile.

Snowflake query profile.

Now you can detect:

- shuffle-heavy joins
    
- skew
    
- full scans
    
- broadcast opportunities
    

---

## Level 4 (Winning)

Add workload metadata.

Example:

```json
{
  "user":"finance",
  "cluster":"warehouse_x",
  "dashboard":"sales_dashboard",
  "schedule":"hourly"
}
```

Now you can answer:

```text
Which dashboards cost the most?
Which team consumes most compute?
```

---

# Query DNA Schema

I'd design something like:

```python
class QueryDNA:

    query_id: str

    tables: list

    joins: list

    filters: list

    group_bys: list

    order_bys: list

    aggregations: list

    scan_bytes: int

    execution_time: float

    rows_scanned: int

    rows_returned: int

    cluster_name: str

    user_name: str

    timestamp: datetime
```

Store in:

```text
DuckDB
or
Delta Table
```

---

# Extraction Pipeline

## Step 1

Parse SQL

Use:

```python
sqlglot
```

This is probably the best choice.

Extract:

```text
Tables
Columns
Joins
Filters
CTEs
Subqueries
```

Example:

```python
import sqlglot
```

---

## Step 2

Build DNA

Input:

```sql
SELECT *
FROM orders o
JOIN customers c
ON o.customer_id = c.id
WHERE region='APAC'
```

Output:

```json
{
  "tables": [
    "orders",
    "customers"
  ],

  "joins": [
    "customer_id=id"
  ],

  "filters": [
    "region"
  ]
}
```

---

# What insights can be generated?

This is where value appears.

---

## Insight 1

### Most Expensive Query Families

Cluster similar queries.

Example:

```sql
SELECT ...
FROM sales
WHERE region='US'

SELECT ...
FROM sales
WHERE region='APAC'
```

Same structure.

Different parameters.

Same family.

Result:

```text
Sales Dashboard Queries

Count:
15,000/day

Cost:
42% of warehouse spend
```

---

## Insight 2

### Repeated Scans

```text
sales table

scanned:
1200 times/day

total:
95 TB/day
```

Recommendation:

```text
Create materialized view
```

---

## Insight 3

### Inefficient Filters

```sql
WHERE customer_name='John'
```

Table not partitioned.

Full scan.

Recommendation:

```text
Partition pruning unavailable.
```

---

## Insight 4

### Join Hotspots

Example:

```text
orders JOIN customers

executed:
4000 times/day
```

Potential:

```text
Cache dimension table
Broadcast join
```

---

## Insight 5

### Dashboard Detection

Many queries look similar.

Example:

```text
sales_dashboard
```

runs:

```text
every 5 min
```

Consumes:

```text
30% warehouse resources
```

Very valuable for enterprises.

---

# AI Layer

This is where most teams start.

You should start much later.

The deterministic engine should first produce:

```json
{
  "query":"Q123",

  "issues":[
    "Large scan",
    "Missing partition pruning",
    "High shuffle"
  ],

  "evidence":{
      "scan_tb":1.8,
      "shuffle_gb":3.2
  }
}
```

Then send this to the LLM.

Prompt:

```text
Act as a Lakehouse Optimization Engineer.

Explain:

1. Root cause
2. Business impact
3. Recommendation
4. Estimated savings
```

Now AI is reasoning on facts.

---

# Demo Dataset (Hackathon Friendly)

Even without real Databricks telemetry, you can generate:

### query_history.csv

```text
query_id
sql_text
user
duration
scan_bytes
```

### execution_plan.json

```text
query_id
shuffle_bytes
join_type
broadcast
```

### table_metadata.csv

```text
table
size_gb
partition_column
file_count
```

That is enough to create a convincing Query DNA Analyzer.

---

My recommendation is to structure the project around a central **Query DNA table**. Every optimization feature later should consume that table. If you do that, Partition Advisor, Join Intelligence, Cost Attribution, Workload Clustering, and What-If Simulation all become downstream modules rather than separate systems. That will make the architecture look much more mature during judging.


Exactly. This is where many hackathon projects become unrealistic.

If your Query DNA Analyzer is analyzing **historical executions**, then `scan_gb`, `execution_time_sec`, `shuffle_bytes`, etc. come from telemetry/history.

But if you're trying to analyze a **new query before execution**, then those values must be estimated from current metadata and statistics.

These are actually two different modes:

## Mode 1: Post-Execution Analysis

Input:

```sql
SELECT *
FROM sales
WHERE region='APAC'
```

Plus actual execution record:

```json
{
  "bytes_scanned": 120GB,
  "execution_time": 45s,
  "shuffle_bytes": 10GB
}
```

You simply consume telemetry.

This is how Databricks, Snowflake, BigQuery, etc. work.

---

## Mode 2: Pre-Execution Optimization Advisor

Input:

```sql
SELECT *
FROM sales
WHERE region='APAC'
```

No execution history available.

Now you must estimate.

This is much more interesting from an AI perspective.

---

# What metadata do you need?

For each table:

```json
{
  "table":"sales",
  "total_size_gb":1000,
  "row_count":1000000000,

  "partitions":{
      "region":5,
      "year":3
  },

  "column_stats":{
      "region":{
          "cardinality":5
      },

      "customer_id":{
          "cardinality":100000000
      }
  }
}
```

This exists in:

- Delta Lake statistics
    
- Hive Metastore
    
- Iceberg metadata
    
- Spark catalog
    
- Snowflake INFORMATION_SCHEMA
    

---

# Estimating Scan Size

Suppose:

```text
sales table
1 TB
```

Query:

```sql
SELECT *
FROM sales
WHERE region='APAC'
```

Partitioned by:

```text
region
```

5 values.

Estimate:

```text
1TB / 5

≈ 200GB
```

Scan estimate:

```json
{
  "estimated_scan_gb": 200
}
```

---

## No Partition Available

Table:

```text
1 TB
```

Query:

```sql
WHERE customer_name='John'
```

No partition.

Estimate:

```text
Full table scan

≈ 1000 GB
```

---

# Estimating Selectivity

Suppose:

```text
100M rows
```

Column:

```text
country
```

Distinct values:

```text
10
```

Query:

```sql
WHERE country='India'
```

Estimated rows:

```text
100M / 10

≈ 10M rows
```

Very simple cardinality-based estimation.

Database optimizers do exactly this.

---

# Estimating Join Cost

Suppose:

```text
orders      500 GB
customers    2 GB
```

Join:

```sql
orders.customer_id =
customers.customer_id
```

Estimate:

```text
Scan:
502 GB
```

Then determine:

```text
Can broadcast?
```

Threshold:

```text
customers < 10GB
```

Answer:

```text
YES
```

Potential join strategy:

```text
Broadcast Hash Join
```

---

# Estimating Shuffle

For Spark-style systems:

Rule of thumb:

```text
Shuffle ≈ Data participating
in GROUP BY or JOIN
```

Example:

```sql
SELECT customer_id,
SUM(amount)
FROM sales
GROUP BY customer_id
```

If:

```text
sales = 500GB
```

Then:

```text
shuffle ≈ 300-500GB
```

depending on cardinality.

Not exact.

But good enough for recommendations.

---

# What Would Impress Judges More?

I would actually store both.

```json
{
  "estimated_scan_gb": 180,
  "actual_scan_gb": 220,

  "estimated_runtime_sec": 35,
  "actual_runtime_sec": 42
}
```

Then your system becomes:

> AI Cost & Performance Prediction Engine

Now you can demonstrate:

```text
Prediction Accuracy:
87%
```

which sounds much more sophisticated.

---

# A Better Query DNA Design

I would split it into three layers.

### Query Structure

```json
{
  "tables":["sales","customers"],
  "joins":[...],
  "filters":[...],
  "aggregations":[...]
}
```

Derived from SQL parser.

---

### Metadata Context

```json
{
  "table_size_gb":1000,
  "row_count":1000000000,
  "partition_columns":["region"],
  "file_count":25000
}
```

Derived from catalog.

---

### Optimization Intelligence

```json
{
  "estimated_scan_gb":200,
  "estimated_shuffle_gb":80,
  "partition_pruning":true,
  "broadcast_possible":true,
  "optimization_score":62
}
```

Derived by your engine.

---

This separation is important because it lets you answer two different questions:

1. **Why was this query slow?** (actual telemetry analysis)
    
2. **Will this query be slow?** (predictive optimization)
    

For a hackathon, the second one is rarer and often more impressive. A system that can look at a SQL statement plus current table metadata and say:

> "This query will likely scan 1.1 TB, trigger a 300 GB shuffle, miss partition pruning, and cost approximately ₹X to run. Rewriting it this way reduces cost by 45%."

feels much closer to a self-optimizing lakehouse than simply analyzing historical logs.



For a hackathon, you don't need _real enterprise telemetry_. You need telemetry that is:

1. Realistic
    
2. Explainable
    
3. Consistent
    
4. Rich enough to drive recommendations
    

There are several approaches, ranked from strongest to weakest.

---

# Option 1: Generate Real Spark Telemetry (Best)

This is what I'd do.

## Setup

Create a local Spark or Databricks Community Edition environment.

Generate:

```text
customers      10M rows
orders         100M rows
sales          500M rows
products       1M rows
```

Store as:

```text
Parquet
Delta Lake
```

Run deliberately good and bad queries.

Examples:

### Bad Query

```sql
SELECT *
FROM sales
WHERE customer_name = 'John'
```

No partition.

Full scan.

---

### Bad Join

```sql
SELECT *
FROM sales s
JOIN customers c
ON s.customer_id = c.customer_id
```

No broadcast hint.

---

### Bad Aggregation

```sql
SELECT customer_id,
SUM(amount)
FROM sales
GROUP BY customer_id
```

Huge shuffle.

---

Then collect:

```python
spark.sql(query)
```

and extract:

```python
queryExecution.executedPlan
```

or Spark event logs.

Now your telemetry is genuinely produced.

Judges love this.

---

# Option 2: Use Spark Event Logs

Spark automatically emits:

```json
SparkListenerSQLExecutionStart
SparkListenerTaskEnd
SparkListenerJobEnd
```

containing:

```text
Duration
Shuffle Read
Shuffle Write
Executor Time
Input Size
Output Size
```

You can build your entire Query DNA from this.

---

# Option 3: Use EXPLAIN FORMATTED

Very hackathon-friendly.

Example:

```sql
EXPLAIN FORMATTED
SELECT ...
```

Spark outputs:

```text
Scan parquet sales

ReadSchema:
...

PartitionFilters:
...

PushedFilters:
...
```

and

```text
BroadcastHashJoin
SortMergeJoin
HashAggregate
Exchange
```

You can parse this.

No actual execution required.

---

# Option 4: Use TPC-DS Dataset

This is what database vendors use for benchmarking.

Tables:

```text
store_sales
catalog_sales
customer
item
store
date_dim
```

Huge schema.

Lots of joins.

Lots of realistic queries.

Perfect for optimization demos.

You can generate:

```text
1 GB
10 GB
100 GB
```

scale factors.

---

# Option 5: Synthetic Telemetry Generator (Most Practical)

Honestly, for a 10-day hackathon, this is probably enough.

Create:

```python
query_history.csv
```

Example:

|query_id|scan_gb|shuffle_gb|runtime|
|---|---|---|---|
|q1|500|200|120|
|q2|1000|400|300|

Then generate realistic relationships.

For example:

```python
runtime =
0.2 * scan_gb
+
0.5 * shuffle_gb
+
random_noise
```

Now:

```text
More scan
→ more runtime

More shuffle
→ more runtime
```

which looks realistic.

---

# What Would I Do?

If I were building this hackathon project:

## Dataset

Use:

```text
TPC-DS
```

or

```text
Fake ecommerce data
```

---

## Telemetry

Run:

```text
50-100 queries
```

through:

```text
DuckDB
or
Spark
```

Collect:

```text
execution_time
rows_scanned
tables_used
joins
```

---

## Then Enrich

Generate:

```text
shuffle_bytes
cluster_name
compute_cost
```

synthetically.

Example:

```python
compute_cost =
scan_gb * 0.05
+
runtime_min * 0.1
```

Nobody will question this during a hackathon if you clearly label it as an estimated cost model.

---

# The Shortcut I'd Recommend

Build a telemetry schema like:

```json
{
  "query_id": "Q123",
  "sql": "...",

  "execution_time_sec": 125,

  "scan_gb": 520,

  "shuffle_gb": 210,

  "rows_scanned": 100000000,

  "join_type": "SortMergeJoin",

  "partition_pruning": false,

  "broadcast_possible": true,

  "cluster": "large-warehouse",

  "estimated_cost": 18.5
}
```

Generate 1000 records.

Then your Query DNA Analyzer has enough signal to discover:

- expensive query families
    
- bad joins
    
- missing partitions
    
- overused tables
    
- workload patterns
    

without spending days building infrastructure.

For judging, a compelling story is often:

> "We executed representative workloads on a Spark/Delta dataset, collected actual execution metrics, and augmented them with a cost model to simulate enterprise-scale telemetry."

That sounds far stronger than "we made a CSV with random numbers."


# LakeMind – Query DNA Analyzer

## Handoff & Design Summary

### Project Context

Hackathon Theme:  
**AI-Powered Query & Cost Optimization for Lakehouse**

Overall Vision:  
Build a Self-Optimizing Lakehouse platform that proactively analyzes workloads, identifies inefficiencies, predicts cost/performance impact, and recommends optimizations.

The Query DNA Analyzer is the foundational component upon which all downstream optimization modules depend.

---

# Why Query DNA?

Raw SQL is difficult to analyze at scale.

The Query DNA Analyzer converts SQL queries into structured metadata and optimization features that can be used for:

- Query clustering
    
- Cost attribution
    
- Partition recommendations
    
- Join optimization
    
- Workload intelligence
    
- Performance prediction
    
- Optimization script generation
    

Think of Query DNA as the equivalent of telemetry fingerprints for SQL workloads.

---

# Core Architecture

```text
SQL Query
    |
    v
SQL Parser (SQLGlot)
    |
    v
Query Structure Extraction
    |
    v
Metadata Enrichment
    |
    v
Optimization Intelligence Engine
    |
    v
Query DNA Record
```

---

# Query DNA Model

The model should be separated into three logical layers.

## 1. Query Structure Layer

Derived directly from SQL parsing.

Example:

{  
"query_id": "Q123",  
"tables": ["sales", "customers"],  
"joins": ["sales.customer_id = customers.customer_id"],  
"filter_columns": ["region"],  
"group_by_columns": [],  
"order_by_columns": [],  
"aggregations": []  
}

Extract using:

- SQLGlot
    
- SQL Parser
    
- AST Traversal
    

---

## 2. Metadata Context Layer

Derived from current lakehouse metadata.

Example:

{  
"table_size_gb": 1000,  
"row_count": 1000000000,  
"partition_columns": ["region"],  
"file_count": 25000,  
"column_stats": {  
"region": {  
"cardinality": 5  
}  
}  
}

Potential sources:

- Delta Lake metadata
    
- Iceberg metadata
    
- Hive Metastore
    
- DuckDB catalog
    
- INFORMATION_SCHEMA
    

---

## 3. Optimization Intelligence Layer

Derived by custom heuristics and analysis.

Example:

{  
"estimated_scan_gb": 200,  
"estimated_shuffle_gb": 80,  
"partition_pruning": true,  
"broadcast_possible": true,  
"optimization_score": 62  
}

This layer powers recommendations.

---

# Important Design Decision

Two different operating modes exist.

## Mode A: Post-Execution Analysis

Purpose:

Analyze completed queries using actual telemetry.

Inputs:

- Query history
    
- Runtime metrics
    
- Query profiles
    
- Spark event logs
    

Outputs:

- Root cause analysis
    
- Cost attribution
    
- Historical optimization recommendations
    

Example:

{  
"actual_scan_gb": 220,  
"actual_runtime_sec": 42  
}

---

## Mode B: Pre-Execution Optimization Advisor

Purpose:

Predict performance before query execution.

Inputs:

- SQL text
    
- Current table metadata
    
- Current statistics
    

Outputs:

- Estimated scan size
    
- Estimated runtime
    
- Potential bottlenecks
    
- Optimization recommendations
    

Example:

{  
"estimated_scan_gb": 180,  
"estimated_runtime_sec": 35  
}

This mode is more innovative and aligns strongly with the Self-Optimizing Lakehouse vision.

---

# Scan Estimation Strategy

The scan estimate should not rely on historical telemetry.

Instead, derive it from current metadata.

Example:

Table:

sales

Size:

1 TB

Partition:

region

Cardinality:

5

Query:

SELECT *  
FROM sales  
WHERE region='APAC'

Estimated Scan:

1 TB / 5

= 200 GB

---

If no partition pruning exists:

Query:

WHERE customer_name='John'

Estimated Scan:

Full Table Scan

= 1 TB

---

# Join Cost Estimation

Example:

orders 500 GB  
customers 2 GB

Join:

orders.customer_id =  
customers.customer_id

Estimated Scan:

502 GB

Broadcast Eligibility:

customers < threshold

Recommendation:

Broadcast Hash Join

---

# Shuffle Estimation

For joins and aggregations:

GROUP BY  
DISTINCT  
JOIN

Approximate shuffle size based on:

- participating data size
    
- grouping cardinality
    
- join cardinality
    

Output:

{  
"estimated_shuffle_gb": 300  
}

---

# Query DNA Use Cases

## Query Clustering

Group structurally similar queries into families.

Example:

Sales Dashboard Queries

Count:  
15,000/day

Cost:  
42% of warehouse spend

---

## Join Hotspot Detection

Identify repeatedly executed expensive joins.

Recommendation:

- Broadcast joins
    
- Materialized views
    
- Caching
    

---

## Repeated Scan Detection

Identify tables scanned excessively.

Recommendation:

- Materialized views
    
- Aggregated tables
    
- Semantic caching
    

---

## Cost Attribution

Map:

Query  
→ User  
→ Team  
→ Cluster  
→ Cost

---

## Partition Advisor

Analyze:

- Filter frequency
    
- Cardinality
    
- Scan patterns
    

Recommend:

- Partition columns
    
- Clustering keys
    
- Z-order columns
    

---

# Telemetry Strategy for Hackathon

Recommended approach:

Use a hybrid model.

## Actual Data

Generate datasets:

- customers
    
- orders
    
- sales
    
- products
    

Store in:

- DuckDB
    
- Delta Lake
    
- Parquet
    

Run representative workloads.

Collect:

- execution time
    
- rows scanned
    
- tables used
    
- joins
    

---

## Synthetic Enrichment

Augment telemetry with:

- shuffle bytes
    
- cluster metadata
    
- estimated compute cost
    
- warehouse utilization
    

Example:

{  
"scan_gb": 500,  
"shuffle_gb": 200,  
"runtime_sec": 120,  
"estimated_cost": 18.5  
}

This enables realistic enterprise scenarios without requiring large infrastructure.

---

# Recommended MVP Scope

Build exceptionally well:

1. Query DNA Analyzer
    
2. Query Clustering
    
3. Scan Estimation
    
4. Join Intelligence
    
5. Partition Advisor
    

Stretch Goal:

Optimization Script Generator

Example Output:

- OPTIMIZE TABLE
    
- VACUUM
    
- CREATE MATERIALIZED VIEW
    
- Partition recommendations
    

---

# Key Message For Judges

The platform does not rely on generic LLM suggestions.

Deterministic engines first derive:

- scan estimates
    
- join costs
    
- partition effectiveness
    
- workload patterns
    

The AI layer then:

- explains findings
    
- prioritizes recommendations
    
- estimates business impact
    
- generates remediation actions
    

This transforms the solution from a chatbot into a genuine Lakehouse Optimization Intelligence Platform.