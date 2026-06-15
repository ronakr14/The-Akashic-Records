For DuckDB, some of these fields are straightforward, some are difficult, and a few are impossible to obtain generically without profiling the data.

Assuming you want to populate `metadata.column_profile` for **all tables and columns** in a catalog, here's how each field maps:

|Column|How to get it|
|---|---|
|schema_name|`information_schema.columns`|
|table_name|`information_schema.columns`|
|column_name|`information_schema.columns`|
|data_type|`information_schema.columns`|
|cardinality|`COUNT(DISTINCT column)`|
|null_pct|`COUNT(*) FILTER (WHERE column IS NULL) / COUNT(*) * 100`|
|min_val|`MIN(column)`|
|max_val|`MAX(column)`|
|has_index|DuckDB index metadata|
|avg_size|Estimated via `AVG(length(CAST(col AS VARCHAR)))`|

---

## Get Column Metadata

```sql
SELECT
    table_schema,
    table_name,
    column_name,
    data_type
FROM information_schema.columns
WHERE table_schema NOT IN ('information_schema','pg_catalog');
```

---

## Profile One Column Dynamically

Example for column `customer_id`:

```sql
SELECT
    COUNT(DISTINCT customer_id) AS cardinality,

    100.0 *
    SUM(CASE WHEN customer_id IS NULL THEN 1 ELSE 0 END)
    / COUNT(*) AS null_pct,

    MIN(customer_id)::VARCHAR AS min_val,
    MAX(customer_id)::VARCHAR AS max_val,

    AVG(LENGTH(CAST(customer_id AS VARCHAR))) AS avg_size
FROM sales.orders;
```

---

## Detect Indexes

DuckDB stores indexes in system catalog:

```sql
SELECT *
FROM duckdb_indexes();
```

Example:

```sql
SELECT
    table_name,
    index_name,
    sql
FROM duckdb_indexes();
```

You'll need to parse the indexed columns and mark `has_index`.

---

## Generate Profiling Queries Automatically

```sql
SELECT
    table_schema,
    table_name,
    column_name,
    data_type
FROM information_schema.columns
WHERE table_schema='main';
```

Then in Python:

```python
for row in columns:

    query = f"""
    INSERT INTO metadata.column_profile
    SELECT
        '{row.table_name}',
        '{row.schema_name}',
        '{row.column_name}',
        '{row.data_type}',

        COUNT(DISTINCT "{row.column_name}"),

        100.0 *
        SUM(CASE WHEN "{row.column_name}" IS NULL THEN 1 ELSE 0 END)
        / COUNT(*),

        MIN("{row.column_name}")::VARCHAR,
        MAX("{row.column_name}")::VARCHAR,

        FALSE,

        AVG(LENGTH(CAST("{row.column_name}" AS VARCHAR)))

    FROM "{row.schema_name}"."{row.table_name}";
    """
```

---

## Performance Issue

For a lakehouse optimizer, running:

```sql
COUNT(DISTINCT col)
MIN(col)
MAX(col)
```

for **every column of every table** can become extremely expensive.

A better architecture is:

### Fast Profile

Collect:

- row count
    
- null %
    
- min/max
    
- avg size
    

using a single scan per table.

### Deep Profile

Collect:

- cardinality
    
- histograms
    
- quantiles
    
- skew metrics
    

only for:

- partition columns
    
- join columns
    
- filter columns
    
- columns referenced in query history
    

This is how systems such as Snowflake, Databricks, and Microsoft Fabric typically approach statistics collection at scale.

For your lakehouse optimization project, I'd strongly recommend separating **lightweight metadata collection** from **expensive column profiling**, otherwise metadata collection itself can become one of the largest workloads in the platform.