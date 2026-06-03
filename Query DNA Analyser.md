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

```
1000 daily queries

400 belong to:
Sales Dashboard

300 belong to:
Customer Analytics

300 belong to:
Adhoc Users
```

Now discover:

```
Top expensive query families
```

rather than individual queries.

What is Query DNA? : converting a raw SQL query and its execution metadata into a structured fingerprint.

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

Insight
### Most Expensive Query Families
### Repeated Scans
### Inefficient Filters
### Join Hotspots
### Dashboard Detection

engine produces:
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

prompt:
Act as a Lakehouse Optimization Engineer.

Explain:

1. Root cause
2. Business impact
3. Recommendation
4. Estimated savings

metadata before execution

post execution:
{
  "bytes_scanned": 120GB,
  "execution_time": 45s,
  "shuffle_bytes": 10GB
}

pre execution
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

# Estimating Scan Size
## No Partition Available
# Estimating Selectivity
# Estimating Join Cost
# Estimating Shuffle

{
  "estimated_scan_gb": 180,
  "actual_scan_gb": 220,

  "estimated_runtime_sec": 35,
  "actual_runtime_sec": 42
}

AI Cost & Performance Prediction Engine
Prediction Accuracy:
87%

### Query Structure

```
{  "tables":["sales","customers"],  "joins":[...],  "filters":[...],  "aggregations":[...]}
```

Derived from SQL parser.

---

### Metadata Context

```
{  "table_size_gb":1000,  "row_count":1000000000,  "partition_columns":["region"],  "file_count":25000}
```

Derived from catalog.

---

### Optimization Intelligence

```
{  "estimated_scan_gb":200,  "estimated_shuffle_gb":80,  "partition_pruning":true,  "broadcast_possible":true,  "optimization_score":62}
```

Derived by your engine.

**Why was this query slow?** (actual telemetry analysis)
**Will this query be slow?** (predictive optimization)

This query will likely scan 1.1 TB, trigger a 300 GB shuffle, miss partition pruning, and cost approximately ₹X to run. Rewriting it this way reduces cost by 45%."