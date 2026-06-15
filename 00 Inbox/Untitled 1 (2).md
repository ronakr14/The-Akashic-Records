Looking at the metadata you currently collect, there are two categories:

1. **Can be calculated today from existing metadata**
    
2. **Cannot be calculated accurately without additional instrumentation**
    

## 1. query_stats (Mostly achievable)

This table is an aggregation of `query_history`.

```sql
INSERT OR REPLACE INTO metadata.query_stats
SELECT
    query_hash,

    CAST(
        quantile_cont(duration_ms, 0.50)
        AS BIGINT
    ) AS p50_exec_ms,

    CAST(
        quantile_cont(duration_ms, 0.95)
        AS BIGINT
    ) AS p95_exec_ms,

    NULL AS avg_bytes_scanned, -- not available

    COUNT(*) AS total_runs,

    NULL AS total_cost_usd, -- requires pricing model

    MAX(executed_at) AS last_seen

FROM metadata.query_history
WHERE status = 'SUCCESS'
GROUP BY query_hash;
```

### If warehouse pricing exists

Example:

```sql
CASE warehouse_size
    WHEN 'SMALL' THEN duration_ms/1000.0 * 0.0001
    WHEN 'MEDIUM' THEN duration_ms/1000.0 * 0.0002
    WHEN 'LARGE' THEN duration_ms/1000.0 * 0.0004
END
```

Then:

```sql
SUM(cost_usd) AS total_cost_usd
```

---

# 2. query_profile

This is where things get tricky.

Current metadata:

### Available

From query_history

```text
duration_ms
rows_returned
status
engine
memory delta
cpu delta
```

From query_feature

```text
join_count
group by
order by
window functions
cte count
subqueries
```

---

## Can Calculate

### exec_time_ms

```sql
duration_ms
```

### rows_returned

```sql
rows_returned
```

### query_type

Can infer from SQL text.

```sql
CASE
    WHEN upper(trim(sql_text)) LIKE 'SELECT%' THEN 'SELECT'
    WHEN upper(trim(sql_text)) LIKE 'INSERT%' THEN 'INSERT'
    WHEN upper(trim(sql_text)) LIKE 'UPDATE%' THEN 'UPDATE'
    WHEN upper(trim(sql_text)) LIKE 'DELETE%' THEN 'DELETE'
    WHEN upper(trim(sql_text)) LIKE 'MERGE%' THEN 'MERGE'
    WHEN upper(trim(sql_text)) LIKE 'CREATE%' THEN 'DDL'
    ELSE 'UNKNOWN'
END
```

### has_full_scan

Heuristic only.

Example:

```sql
CASE
    WHEN has_where = FALSE
     AND tables_referenced IS NOT NULL
    THEN TRUE
    ELSE FALSE
END
```

Not reliable.

### partition_pruning_applied

Heuristic.

```sql
CASE
    WHEN has_where
     AND filter_predicates LIKE '%partition%'
    THEN 'YES'
    ELSE 'UNKNOWN'
END
```

Again, not reliable.

---

# Cannot Calculate Reliably

These require execution plan or engine telemetry.

## bytes_scanned

Need:

```text
DuckDB EXPLAIN ANALYZE
Parquet scan metrics
Storage layer metrics
```

Cannot infer from duration.

---

## bytes_written

Need:

```text
INSERT
COPY
CTAS
MERGE output metrics
```

Not available.

---

## partitions_scanned

Need:

```text
partition pruning statistics
```

Not available.

---

## partitions_total

Need catalog metadata.

Not available from current tables.

---

## spill_bytes

Need runtime execution metrics.

Example:

```text
DuckDB profiling
Spark task metrics
Snowflake query profile
```

Not available.

---

## cache_hit

Need engine cache statistics.

Not available.

---

## compilation_time

Need planner/optimizer metrics.

Not available.

---

# Recommended Query Profile Population

Given current metadata:

```sql
INSERT OR REPLACE INTO metadata.query_profile
SELECT
    h.query_id,

    CAST(h.duration_ms AS BIGINT) AS exec_time_ms,

    NULL AS bytes_scanned,

    NULL AS bytes_written,

    h.rows_returned,

    NULL AS partitions_scanned,

    NULL AS partitions_total,

    NULL AS spill_bytes,

    CASE
        WHEN f.has_where = FALSE
        THEN TRUE
        ELSE FALSE
    END AS has_full_scan,

    CASE
        WHEN upper(trim(h.sql_text)) LIKE 'SELECT%' THEN 'SELECT'
        WHEN upper(trim(h.sql_text)) LIKE 'INSERT%' THEN 'INSERT'
        WHEN upper(trim(h.sql_text)) LIKE 'UPDATE%' THEN 'UPDATE'
        WHEN upper(trim(h.sql_text)) LIKE 'DELETE%' THEN 'DELETE'
        WHEN upper(trim(h.sql_text)) LIKE 'MERGE%' THEN 'MERGE'
        ELSE 'OTHER'
    END AS query_type,

    CASE
        WHEN f.has_where THEN 'POSSIBLE'
        ELSE 'NO'
    END AS partition_pruning_applied,

    NULL AS cache_hit,

    NULL AS compilation_time

FROM metadata.query_history h
LEFT JOIN metadata.query_feature f
    ON h.query_id = f.query_id;
```

---

# If your goal is an AI query optimization engine

I would strongly recommend adding a third metadata source:

```sql
metadata.query_plan
```

```sql
query_id
operator_id
operator_type
rows_in
rows_out
bytes_in
bytes_out
cpu_time_ms
memory_mb
spill_bytes
estimated_rows
actual_rows
```

captured from:

```sql
EXPLAIN ANALYZE
PRAGMA enable_profiling
PRAGMA profiling_output
```

in DuckDB.

Once you have operator-level telemetry, you can accurately derive:

- bytes scanned
    
- bytes written
    
- full table scans
    
- partition pruning effectiveness
    
- join strategy
    
- skew indicators
    
- spill detection
    
- optimizer recommendations
    

Without execution-plan telemetry, `query_profile` will mostly be a heuristic layer rather than a true performance profile. For a lakehouse optimization platform, execution plans are usually the most valuable dataset after query history.



In DuckDB, **bytes scanned** and **bytes written** measure two completely different parts of query execution.

|Metric|Meaning|Example|
|---|---|---|
|**Bytes Scanned**|Amount of data read from storage|Reading 100 GB of Parquet files|
|**Bytes Written**|Amount of data produced and persisted|Writing 5 GB to a table or Parquet file|

---

## Bytes Scanned

This is the volume of data DuckDB must **read** to execute a query.

Example:

```sql
SELECT *
FROM sales
WHERE country = 'US';
```

Suppose:

```text
sales table = 1 TB
country filter prunes 90%
```

DuckDB may only scan:

```text
100 GB
```

So:

```text
bytes_scanned = 100 GB
```

not:

```text
1 TB
```

### Includes

- Parquet file reads
    
- CSV reads
    
- Table reads
    
- Index reads
    
- Temporary spill reads
    

### Important

A query can return 10 rows while scanning terabytes.

Example:

```sql
SELECT *
FROM events
WHERE event_id = 123;
```

Result:

```text
rows_returned = 1
bytes_scanned = 5 TB
```

This is usually an optimization problem.

---

## Bytes Written

This is data DuckDB persists during execution.

Example:

```sql
CREATE TABLE sales_copy AS
SELECT *
FROM sales;
```

Suppose:

```text
sales = 100 GB
```

Then:

```text
bytes_written ≈ 100 GB
```

because a new table is created.

---

### Common Write Operations

#### INSERT

```sql
INSERT INTO sales_archive
SELECT *
FROM sales;
```

Data copied:

```text
bytes_written = size of inserted rows
```

---

#### COPY

```sql
COPY sales TO 'sales.parquet';
```

Output file:

```text
sales.parquet = 15 GB
```

Then:

```text
bytes_written = 15 GB
```

---

#### CREATE TABLE AS

```sql
CREATE TABLE result AS
SELECT ...
```

Writes new storage blocks.

---

#### UPDATE / DELETE

These may rewrite storage segments internally.

Example:

```sql
UPDATE sales
SET amount = amount * 1.1;
```

DuckDB may rewrite chunks of the table.

---

## Example Scenarios

### Scenario 1

```sql
SELECT COUNT(*)
FROM events;
```

Table:

```text
500 GB
```

Metrics:

```text
bytes_scanned = 500 GB
bytes_written = 0
rows_returned = 1
```

---

### Scenario 2

```sql
CREATE TABLE us_events AS
SELECT *
FROM events
WHERE country='US';
```

Table:

```text
500 GB
```

US rows:

```text
50 GB
```

Metrics:

```text
bytes_scanned = 500 GB
bytes_written = 50 GB
```

---

### Scenario 3

```sql
COPY (
    SELECT *
    FROM events
    WHERE country='US'
)
TO 'us_events.parquet';
```

Metrics:

```text
bytes_scanned = 500 GB
bytes_written = 50 GB
```

---

## Why Both Matter

Consider two queries:

### Query A

```sql
SELECT *
FROM huge_table;
```

```text
bytes_scanned = 10 TB
bytes_written = 0
```

Problem:

```text
Expensive read
```

---

### Query B

```sql
CREATE TABLE result AS
SELECT *
FROM huge_table;
```

```text
bytes_scanned = 10 TB
bytes_written = 10 TB
```

Problem:

```text
Expensive read
Expensive write
Storage growth
```

---

## In DuckDB Profiling

If you're building a query optimization platform, you'd ideally capture:

```text
bytes_scanned
bytes_written
rows_read
rows_output
operator timings
spill bytes
memory peak
```

from:

```sql
PRAGMA enable_profiling;
EXPLAIN ANALYZE ...
```

or the profiling JSON output.

One caveat: DuckDB does **not currently expose a single built-in `bytes_scanned` metric** like Snowflake or BigQuery. You'll typically derive it from:

- Parquet file metadata
    
- Table sizes
    
- Scan operators in `EXPLAIN ANALYZE`
    
- Profiling JSON
    

Similarly, **bytes_written** often has to be inferred from:

- Output table size
    
- Generated file size
    
- Storage growth before/after execution
    

rather than a direct system metric. This is why many DuckDB observability systems maintain their own scan/write estimators alongside query profiling.

If you're using **Pandas**, there are several ways to get distinct values from a column.

### Distinct values

```python
distinct_values = df["column_name"].unique()
```

Returns a NumPy array:

```python
array(['A', 'B', 'C'])
```

---

### Distinct values as a Python list

```python
distinct_values = df["column_name"].dropna().unique().tolist()
```

Output:

```python
['A', 'B', 'C']
```

---

### Count of distinct values

```python
num_distinct = df["column_name"].nunique()
```

Output:

```python
3
```

---

### Distinct values sorted

```python
distinct_values = sorted(df["column_name"].dropna().unique())
```

Output:

```python
['A', 'B', 'C']
```

---

### Frequency of each distinct value

```python
value_counts = df["column_name"].value_counts()
```

Output:

```python
A    10
B     5
C     2
```

---

### For all columns

```python
for col in df.columns:
    print(col, df[col].dropna().unique())
```

Or:

```python
distinct_map = {
    col: df[col].dropna().unique().tolist()
    for col in df.columns
}
```

This creates:

```python
{
    'country': ['US', 'UK', 'IN'],
    'status': ['ACTIVE', 'INACTIVE']
}
```

If you're working with a **DuckDB query result DataFrame** and want distinct values for every column to populate your `column_profile.cardinality`, there are more efficient approaches than calling `unique()` on every column.


Use Python's `any()` with a generator expression:

```python
values = [100, 500, 4000, 200]

has_value_gt_3000 = any(v > 3000 for v in values)

print(has_value_gt_3000)
```

Output:

```python
True
```

### Example in an `if` statement

```python
if any(v > 3000 for v in values):
    print("At least one value exceeds 3000")
```

### If the list may contain `None`

```python
if any(v is not None and v > 3000 for v in values):
    print("At least one value exceeds 3000")
```

### For a DataFrame column

```python
if any(df["duration_ms"] > 3000):
    print("Some queries took longer than 3 seconds")
```

A more Pandas-native approach is:

```python
if (df["duration_ms"] > 3000).any():
    print("Some queries took longer than 3 seconds")
```

The Pandas version is generally preferred for DataFrame columns because it operates directly on the boolean Series.


The error tells you exactly what's wrong:

```python
large = tables_meta["max_rows"].dropna().unique().tolist()
```

but:

```python
TypeError: list indices must be integers or slices, not str
```

means `tables_meta` is a **Python list**, not a Pandas DataFrame.

You're doing:

```python
tables_meta["max_rows"]
```

which only works on a DataFrame or dict.

---

### Verify the type

Add:

```python
print(type(tables_meta))
print(tables_meta)
```

You'll likely see something like:

```python
<class 'list'>
```

---

### Scenario 1: List of dictionaries

If `tables_meta` looks like:

```python
[
    {"table_name": "orders", "max_rows": 5000},
    {"table_name": "customers", "max_rows": 1000}
]
```

then use:

```python
large = [row["max_rows"] for row in tables_meta if row["max_rows"] is not None]
```

or

```python
large_table_exists = any(
    row["max_rows"] > 3000
    for row in tables_meta
    if row["max_rows"] is not None
)
```

---

### Scenario 2: DuckDB fetchall()

If you did:

```python
tables_meta = conn.execute(sql).fetchall()
```

then you'll get:

```python
[
    ("orders", 5000),
    ("customers", 1000)
]
```

You must access by position:

```python
large = [row[1] for row in tables_meta]
```

or

```python
large_table_exists = any(row[1] > 3000 for row in tables_meta)
```

---

### Scenario 3: You intended a DataFrame

Instead of:

```python
fetchall()
```

use:

```python
tables_meta = conn.execute(sql).df()
```

Then your original code works:

```python
large = tables_meta["max_rows"].dropna().unique().tolist()

large_table_exists = any(v > 3000 for v in large)
```

---

For your lakehouse optimizer project, I'd recommend printing:

```python
print(type(tables_meta))
print(tables_meta[:5])
```

right before line 19. That will immediately reveal whether you're dealing with:

- `DataFrame`
    
- `list[dict]`
    
- `list[tuple]`
    

and the fix becomes obvious.


The error means that at least one value in `_large` is a **Pandas Series**, not a scalar number.

For example, your data may look like:

```python
_large = [
    1000,
    2000,
    pd.Series([5000]),
]
```

Then:

```python
v > 3000
```

returns:

```python
0    True
dtype: bool
```

and `any()` tries to evaluate that Series as a boolean, which raises:

```python
ValueError: The truth value of a Series is ambiguous
```

### First thing to check

Add:

```python
print(type(_large))
print(_large)

for v in _large:
    print(type(v), v)
```

I suspect you'll see something like:

```python
<class 'pandas.core.series.Series'>
```

or

```python
[
    Series(...),
    Series(...)
]
```

---

### Common root cause

Your comprehension:

```python
_large = [row["max_rows"] for row in tables_meta if row["max_rows"] is not None]
```

suggests `row` is probably a DataFrame row or dict-like object where `row["max_rows"]` is itself a Series.

If `tables_meta` is actually a DataFrame, don't iterate rows this way.

Instead do:

```python
large = (tables_meta["max_rows"] > 3000).any()
```

This is the clean Pandas solution.

---

### If `tables_meta` is a list of dicts

Then do:

```python
_large = [
    row["max_rows"]
    for row in tables_meta
    if row["max_rows"] is not None
]

large = any(float(v) > 3000 for v in _large)
```

---

### If `tables_meta` comes from `to_dict("records")`

Example:

```python
tables_meta = df.to_dict("records")
```

Then your code should work:

```python
large = any(
    row["max_rows"] > 3000
    for row in tables_meta
    if row["max_rows"] is not None
)
```

No intermediate list needed.

---

### Most likely issue in your code

You're probably doing something like:

```python
for row in tables_meta:
    row["max_rows"]
```

where `row` is actually a DataFrame column (or Series), not a record.

Print:

```python
print(type(tables_meta))
print(type(tables_meta[0]) if len(tables_meta) else None)
```

or paste the output of:

```python
print(type(tables_meta))
print(tables_meta)
```

and I can pinpoint the exact fix in a few seconds.


This error is different from the previous one.

```text
Analysis error: 'QueryFeatures' object has no attribute 'to_dict'
```

means you're calling:

```python
features.to_dict()
```

but `features` is an instance of your custom class:

```python
class QueryFeatures:
    ...
```

and that class doesn't implement a `to_dict()` method.

### Check what `features` actually is

```python
print(type(features))
```

You'll likely see:

```python
<class 'QueryFeatures'>
```

---

### Option 1: Access attributes directly

If your class looks like:

```python
class QueryFeatures:
    def __init__(self):
        self.join_count = 5
        self.has_where = True
```

Then use:

```python
features.join_count
features.has_where
```

instead of:

```python
features.to_dict()["join_count"]
```

---

### Option 2: Convert with `__dict__`

Python objects expose their attributes via:

```python
feature_dict = features.__dict__
```

Example:

```python
print(features.__dict__)
```

Output:

```python
{
    'join_count': 5,
    'has_where': True,
    ...
}
```

---

### Option 3: Add a `to_dict()` method

If this is your own class:

```python
class QueryFeatures:
    ...
```

Add:

```python
class QueryFeatures:
    ...

    def to_dict(self):
        return self.__dict__
```

Then:

```python
features.to_dict()
```

works.

---

### Option 4: If using a dataclass (recommended)

```python
from dataclasses import dataclass, asdict

@dataclass
class QueryFeatures:
    join_count: int
    has_where: bool
```

Convert via:

```python
feature_dict = asdict(features)
```

---

For your lakehouse optimizer, if `QueryFeatures` is a model object returned by your SQL parser, I'd recommend making it a `@dataclass` and using:

```python
from dataclasses import asdict

feature_dict = asdict(features)
```

It's cleaner than manually maintaining a `to_dict()` method as the class grows.

# Lakehouse Optimizer – Query Profiling & Analysis Engine Handoff

## Objective

Build a metadata-driven query optimization platform using DuckDB query telemetry.

Current metadata sources:

### metadata.query_history

Captures:

- query_id
    
- query_hash
    
- sql_text
    
- execution timestamps
    
- duration_ms
    
- rows_returned
    
- warehouse metadata
    
- status/error
    
- memory metrics
    
- CPU metrics
    
- execution engine
    

### metadata.query_feature

Captures parsed SQL features:

- tables_referenced
    
- columns_referenced
    
- join_count
    
- join_types
    
- filter_predicates
    
- group_by_cols
    
- order_by_cols
    
- window_functions
    
- aggregations
    
- cte_count
    
- subquery_count
    
- complexity_score
    
- has_where/group/order/limit/having
    
- cross_join
    

---

# Query Profile Design

Target table:

```sql
metadata.query_profile
```

Fields:

- exec_time_ms
    
- bytes_scanned
    
- bytes_written
    
- rows_returned
    
- partitions_scanned
    
- partitions_total
    
- spill_bytes
    
- has_full_scan
    
- query_type
    
- partition_pruning_applied
    
- cache_hit
    
- compilation_time
    

## Findings

### Can be derived immediately

|Field|Source|
|---|---|
|exec_time_ms|duration_ms|
|rows_returned|query_history|
|query_type|sql_text|
|has_full_scan|heuristic using has_where|
|partition_pruning_applied|heuristic using filters|

### Cannot be accurately derived today

Requires execution-plan telemetry:

- bytes_scanned
    
- bytes_written
    
- partitions_scanned
    
- partitions_total
    
- spill_bytes
    
- cache_hit
    
- compilation_time
    

Recommendation:

Introduce:

```sql
metadata.query_plan
```

to store operator-level telemetry.

Potential fields:

- operator_type
    
- rows_in
    
- rows_out
    
- bytes_in
    
- bytes_out
    
- cpu_time_ms
    
- memory_mb
    
- spill_bytes
    
- estimated_rows
    
- actual_rows
    

Source:

```sql
EXPLAIN ANALYZE
PRAGMA enable_profiling
```

---

# Query Stats Design

Target table:

```sql
metadata.query_stats
```

Fields:

- p50_exec_ms
    
- p95_exec_ms
    
- avg_bytes_scanned
    
- total_runs
    
- total_cost_usd
    
- last_seen
    

## Computation Strategy

Derived from:

```sql
metadata.query_history
```

Metrics:

### p50

```sql
quantile_cont(duration_ms, 0.50)
```

### p95

```sql
quantile_cont(duration_ms, 0.95)
```

### total_runs

```sql
COUNT(*)
```

### last_seen

```sql
MAX(executed_at)
```

### total_cost_usd

Requires warehouse pricing model.

---

# Bytes Scanned vs Bytes Written

## Bytes Scanned

Amount of data read.

Examples:

- Parquet scans
    
- Table scans
    
- Index reads
    

Example:

```sql
SELECT * FROM sales WHERE country='US'
```

Table = 1 TB

Actual scan = 100 GB

Result:

```text
bytes_scanned = 100 GB
```

## Bytes Written

Amount of data persisted.

Examples:

```sql
INSERT
COPY
CREATE TABLE AS
MERGE
```

Example:

```sql
CREATE TABLE us_sales AS
SELECT *
FROM sales
```

Output size = 50 GB

Result:

```text
bytes_written = 50 GB
```

## Important Observation

DuckDB does not expose a single built-in bytes_scanned metric similar to Snowflake or BigQuery.

Must estimate using:

- Parquet metadata
    
- Query profiling
    
- Scan operators
    
- File statistics
    

---

# Python Debugging Notes

## Issue 1

Error:

```python
TypeError: list indices must be integers or slices, not str
```

Code:

```python
tables_meta["max_rows"]
```

Root Cause:

```python
tables_meta
```

was a list, not a DataFrame.

Fix:

If list of dicts:

```python
[row["max_rows"] for row in tables_meta]
```

If DataFrame:

```python
tables_meta["max_rows"]
```

---

## Issue 2

Goal:

Determine if any table exceeds threshold.

Correct pattern:

```python
large = any(
    row["max_rows"] > 3000
    for row in tables_meta
    if row["max_rows"] is not None
)
```

For DataFrame:

```python
large = (tables_meta["max_rows"] > 3000).any()
```

---

## Issue 3

Error:

```python
ValueError:
The truth value of a Series is ambiguous
```

Root Cause:

At least one element being evaluated inside:

```python
any(v > 3000 for v in values)
```

was a Pandas Series rather than a scalar.

Debug strategy:

```python
for v in values:
    print(type(v))
```

Preferred DataFrame solution:

```python
(df["max_rows"] > 3000).any()
```

---

## Issue 4

Error:

```python
'QueryFeatures' object has no attribute 'to_dict'
```

Root Cause:

Custom Python object.

Not a DataFrame.

Not a dictionary.

Fix Options:

### Access attributes directly

```python
features.join_count
```

### Convert via

```python
features.__dict__
```

### Add method

```python
def to_dict(self):
    return self.__dict__
```

### Preferred

Use dataclass:

```python
from dataclasses import dataclass, asdict
```

Convert:

```python
asdict(features)
```

---

# Recommended Next Steps

1. Add query_plan telemetry collection.
    
2. Capture DuckDB profiling JSON.
    
3. Build operator-level metadata tables.
    
4. Derive true bytes scanned/written metrics.
    
5. Implement query health score using:
    
    - execution time
        
    - join count
        
    - complexity score
        
    - large table participation
        
    - full scan detection
        
    - cross joins
        
6. Aggregate query history into query_stats for trend analysis.
    
7. Add optimization recommendation engine using query_profile + query_plan.