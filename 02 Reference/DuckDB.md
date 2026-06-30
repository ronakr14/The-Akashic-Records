---
domain: Data Engineering
domain_suggested: null
category: Reference
category_suggested: null
source_type: obsidian
status: review
tags: [duckdb, analytics, embedded, olap, dataengineering]
---






```table-of-contents
```

## What DuckDB Actually Is

DuckDB is:

- Embedded OLAP database
- Columnar storage engine
- Vectorized query execution engine
- Single-node analytics engine
- Zero-server architecture

The analogy:

SQLite → OLTP
DuckDB → OLAP

Just like SQLite embedded transactional databases into applications, DuckDB embeds analytical databases into applications.

No server. No cluster. No coordinator. No worker nodes.

```python
import duckdb

duckdb.sql("""
SELECT *
FROM patients
WHERE age > 60
""")
```

---

## Architectural Philosophy

Traditional analytics architecture:

```text
Application
     |
     v
Warehouse
(Snowflake)
     |
     v
Storage
(S3)
```

DuckDB philosophy:

```text
Application
     |
     v
DuckDB Engine
     |
     +---- CSV
     +---- Parquet
     +---- Iceberg
     +---- Local Files
     +---- S3
```

Move computation closer to data. Avoid moving data into databases whenever possible.

---

## Why DuckDB Became Popular

Historically:

```text
CSV
  |
Pandas
  |
Out Of Memory
```

or

```text
CSV
  |
Spark
  |
Cluster
  |
Overkill
```

DuckDB fills the gap.

```text
CSV
  |
DuckDB
  |
Done
```

Example: 100 GB Parquet — DuckDB can query it directly:

```sql
SELECT *
FROM 'patients.parquet'
```

without importing.

---

## Internal Architecture

```text
               SQL Parser
                    |
                    v
             Logical Planner
                    |
                    v
             Optimizer
                    |
                    v
             Physical Plan
                    |
                    v
           Vectorized Engine
                    |
                    v
             Storage Layer
```

Same pipeline as enterprise warehouses, embedded in a single process.

---

## Vectorized Execution

Instead of row-at-a-time processing:

```text
Row 1
Row 2
Row 3
```

DuckDB processes data in vectors:

```text
Vector
2048 rows
```

Example:

```sql
SELECT SUM(amount)
FROM claims
```

Traditional:

```text
read row
read row
read row
```

DuckDB:

```text
read 2048 rows
calculate
read next 2048 rows
```

Benefits:

- CPU cache friendly
- SIMD optimization
- Very fast aggregation

Same concept used by [[Snowflake]], [[Databricks]], [[ClickHouse]], [[SingleStore]].

---

## Columnar Storage

DuckDB stores data by column:

```text
PatientID
---------
1
2
3

Age
----
45
60
90
```

instead of by row:

```text
1,45
2,60
3,90
```

Benefits:

- Compression
- Scan efficiency
- Analytics speed

For:

```sql
SELECT AVG(age)
```

only the `age` column is read. Huge difference vs row-store.

---

## DuckDB vs PostgreSQL

|Area|PostgreSQL|DuckDB|
|---|---|---|
|OLTP|Excellent|Poor|
|OLAP|Moderate|Excellent|
|ACID|Excellent|Good|
|Concurrent Writes|Excellent|Limited|
|Dashboard Queries|Moderate|Excellent|
|Aggregations|Moderate|Excellent|
|Transactions|Excellent|Limited|
|ETL Analytics|Moderate|Excellent|

Rule:

```text
Postgres = System of Record
DuckDB = Analytics Engine
```

Not a replacement. Complement.

---

## DuckDB and Data Lakes

Modern data lake:

```text
S3
  |
 Parquet
  |
 Iceberg
```

DuckDB can query directly:

```sql
SELECT *
FROM read_parquet(...)
```

or

```sql
SELECT *
FROM iceberg_scan(...)
```

No warehouse required.

Architecture:

```text
Parquet
     |
DuckDB
     |
BI Tool
```

---

## DuckDB and Medallion Architecture

Medallion Architecture layers:

```text
Bronze
Raw FHIR
Raw HL7
Raw Claims

Silver
Cleaned Data

Gold
Business Metrics
```

DuckDB fits naturally in:

```text
Bronze -> Silver
Silver -> Gold
```

transformations.

---

## DuckDB + Python

One of the strongest integrations.

```text
DuckDB
  |
Pandas
Polars
PyArrow
```

Example:

```python
df = duckdb.sql("""
SELECT *
FROM patient_claims
""").df()
```

No ETL. No JDBC. No Spark session.

---

## DuckDB + Polars

This combination is becoming a serious alternative to [[Spark]] for many workloads.

```text
Polars
   |
DuckDB
   |
Parquet
```

Typical pattern:

```text
Polars = transformations
DuckDB = SQL analytics
```

For datasets under a few hundred GB, many data engineers now use DuckDB + Polars instead of Spark.

---

## DuckDB vs Spark

|Area|DuckDB|Spark|
|---|---|---|
|Setup|Simple|Complex|
|Cluster|No|Yes|
|Scale|Single Node|Distributed|
|Cost|Low|High|
|100 GB|Excellent|Good|
|10 TB|Struggles|Excellent|
|100 TB|Impossible|Excellent|

Rule:

```text
If it fits on one machine
DuckDB wins
```

DuckDB often beats Spark at 10–500 GB scale. Spark wins at 20+ TB.

---

## DuckDB in a Modern Data Platform

A pattern increasingly recommended in practice:

```text
PostgreSQL
      |
      v
 Debezium
      |
      v
 Kafka
      |
      v
 S3 Data Lake
      |
      v
 Iceberg
      |
      +--------+
      |        |
      v        v
  DuckDB    Spark
      |
      v
 Analytics
```

DuckDB becomes:

- Developer analytics layer
- Local analytics engine
- Ad-hoc SQL engine
- Lightweight marts

---

## When to Use DuckDB

Use DuckDB for:

- Clinical KPI calculations
- Data quality checks
- Local analyst sandboxes
- Semantic layer prototyping
- Gold-layer aggregations
- Regulatory reports
- Data validation pipelines

Avoid DuckDB for:

- Patient-facing OLTP APIs
- High-concurrency workloads
- Thousands of simultaneous users
- Transaction processing

---

## The Future — Architectural Trends

```text
Data Warehouse Era
2005-2020
Everything goes into warehouse
```

↓

```text
Lakehouse Era
2020-2030
Compute comes to data
```

DuckDB is one of the strongest representatives of this shift.

Current architecture direction:

```text
Small-Medium Analytics
DuckDB + Iceberg + Polars
```

is becoming the new:

```text
Spark + Hive + Hadoop
```

for many organizations.

---

## See Also

- [[Data Modelling]]
- [[Data Warehousing]]
- [[Apache Spark]]
- [[Apache Iceberg]]
- [[Polars]]
- [[PostgreSQL]]
- [[Medallion Architecture]]
- [[Debezium]]
