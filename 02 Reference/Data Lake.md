---
domain: Data Engineering
domain_suggested: null
category: Curated
category_suggested: null
source_type: obsidian
status: review
tags: [data-lake, architecture, storage, tags, data-engineering]
---




```table-of-contents
```


A **data lake** is a centralized storage repository that holds **large amounts of raw data** in its original format until it is needed.

Unlike a traditional database or data warehouse, a data lake can store:

- Structured data (tables, spreadsheets)
- Semi-structured data (JSON, XML, logs)
- Unstructured data (images, videos, emails, documents)

---

# Analogy

Think of a data lake as a **natural lake** where water from many sources flows in and is stored as-is.

- **Data Lake** = Store everything first, organize later.
- **Data Warehouse** = Clean and organize data before storing it.

---

# Architecture

A modern data lake has more layers than the classic 3-box diagram:

```text
Data Sources
│  (Applications, Sensors, Databases, Logs, APIs, Streaming)
▼
Ingestion Layer
│  (Batch: Airflow, Spark | Streaming: Kafka, Kinesis)
▼
Raw Storage (Object Store: S3 / ADLS / GCS / HDFS)
│
├── Bronze Layer       ← raw ingestion, no transforms
│   (immutable, append-only)
│
├── Silver Layer       ← cleaned, deduped, validated
│   (schema enforced, basic quality)
│
└── Gold Layer         ← business-ready, aggregated
    (feature stores, dimensional models)
│
▼
Catalog & Metadata
   (Unity Catalog, AWS Glue, Hive Metastore, Apache Atlas)
│
▼
Consumption
   (Spark, Presto/Trino, Databricks, dbt, BI tools, ML platforms)
```

Key insight: the **medallion architecture** (bronze/silver/gold) is the dominant design pattern in modern data lakes. It provides a clear data quality progression from raw to production-ready.

---

# Why Use a Data Lake?

## Benefits

- Stores massive volumes of data at low cost (object storage is cheap)
- Supports big data analytics and AI/ML workloads
- Flexible — no need to define a schema upfront (schema-on-read)
- Can integrate data from many sources in one place
- Decouples storage from compute (scale independently)
- Ideal for batch and streaming workloads

## Challenges

- Data can become disorganized ("data swamp") if not governed properly
- Security and access control can be complex at scale
- Data quality management requires explicit tooling
- Query performance can be poor without proper file organization
- Metadata and cataloging are critical but often neglected
- Schema evolution can break downstream consumers

---

# The Lakehouse Paradigm

The industry has largely shifted from "raw data lake" to **Lakehouse** architecture.

A Lakehouse combines data lake flexibility with data warehouse capabilities:

|Capability|Traditional Data Lake|Lakehouse|
|---|---|---|
|Storage|Object store (S3, ADLS, GCS)|Same object store|
|ACID Transactions|No (eventual consistency)|Yes (Delta Lake, Iceberg, Hudi)|
|Schema Enforcement|No (read-only)|Yes (write-time validation)|
|Data Versioning|No|Yes (time travel)|
|Upserts / Deletes|Rewrite entire partitions|Row-level operations|
|Metadata Catalog|External (Glue, Hive)|Built-in (Unity Catalog, etc.)|
|Query Engines|Spark, Presto|Spark, Trino, DuckDB, Python|
|ML / AI|Direct file access|Feature stores + SQL analytics|

The key innovation: **open table formats** (Delta Lake, Apache Iceberg, Apache Hudi) add transactional guarantees on top of cheap object storage.

See: [[Delta Lake & Iceberg]] for format comparison.

---

# Data Lake vs Data Warehouse

|Feature|Data Lake|Data Warehouse|Lakehouse|
|---|---|---|---|
|Data Type|Any format|Structured|Any format|
|Schema|Applied when read|Applied when written|Applied when written (enforced)|
|Cost|Lower (object storage)|Higher (proprietary)|Lower (object storage)|
|Users|Data engineers, data scientists|Data engineers, analysts, scientists|All|
|Use Cases|AI, ML, big data, streaming|Reporting, dashboards|Both|
|Query Latency|Seconds to minutes|Milliseconds to seconds|Milliseconds to minutes|
|Concurrency|Dozens of queries|Hundreds concurrent|Dozens to hundreds|
|Data Freshness|Near real-time possible|Batch ETL (hours)|Streaming + batch|
|Governance|Manual / external catalog|Built-in|Built-in catalog + lineage|
|ACID Compliance|No (traditionally)|Yes|Yes|

---

# ACID on Data Lakes — How It Works

Traditional data lakes lacked transactions. Three open-source formats solved this:

## Delta Lake
- Default format for Databricks
- Transaction log (`_delta_log/`) records every operation
- Supports time travel, schema evolution, MERGE/UPSERT

## Apache Iceberg
- Originated at Netflix
- Hidden partitioning (no partition columns required in queries)
- Wide ecosystem support (Snowflake, Trino, Spark, Dremio)

## Apache Hudi
- Originated at Uber
- Built for streaming ingestion
- Record-level indexes for fast upserts

All three provide:
- Snapshot isolation
- Time travel (query historical versions)
- Schema evolution without rewriting data
- Compaction and Z-ordering for performance

---

# Governance & Cataloging

A data lake without governance becomes a data swamp. Key components:

| Tool | Purpose |
|---|---|
| Databricks Unity Catalog | Unified governance, lineage, access control |
| AWS Glue Catalog | Metadata management for S3-based lakes |
| Apache Hive Metastore | Traditional SQL metadata catalog |
| Apache Atlas | Data governance and lineage tracking |
| Apache Ranger / AWS IAM | Fine-grained access control |
| dbt | Data transformations, testing, documentation |

Best practice: enforce **schema validation at write time**, maintain a **centralized catalog**, and track **column-level lineage** so consumers understand where data came from.

---

# When to Use What

| Scenario | Recommendation |
|---|---|
| Exploratory analytics, ML training on raw data | Data Lake |
| Executive dashboards, financial reporting | Data Warehouse |
| Need both flexibility + ACID + SQL analytics | Lakehouse |
| Small team, simple analytics, <1 TB | Data Warehouse (skip the lake) |
| Real-time streaming + historical batch | Lakehouse (streaming table support) |
| Regulatory compliance (audit, lineage) | Lakehouse or Warehouse |

Rule of thumb: if you're starting fresh in 2026, default to **Lakehouse** on object storage. It subsumes both traditional data lakes and warehouses for most workloads.

---

# Popular Technologies

## Storage
- [Amazon S3](https://aws.amazon.com/s3/)
- [Azure Data Lake Storage](https://azure.microsoft.com/en-us/products/storage/data-lake-storage/)
- [Google Cloud Storage](https://cloud.google.com/storage)
- [Apache Hadoop HDFS](https://hadoop.apache.org/)

## Table Formats
- [Delta Lake](https://delta.io/)
- [Apache Iceberg](https://iceberg.apache.org/)
- [Apache Hudi](https://hudi.apache.org/)

## Platforms
- [Databricks Lakehouse Platform](https://www.databricks.com/)
- [Snowflake](https://www.snowflake.com/) (hybrid warehouse/lakehouse)
- [Apache Spark](https://spark.apache.org/) (processing engine)
- [Trino / Presto](https://trino.io/) (query engine)

## Orchestration & Transformation
- [Apache Airflow](https://airflow.apache.org/)
- [dbt](https://www.getdbt.com/)

---

# Example

A retail company might store sales records, website clickstreams, customer reviews, and product images in a data lake:

- **Bronze**: raw Kafka events + CSV exports from POS systems
- **Silver**: deduplicated, validated, schema-enriched sales data
- **Gold**: customer 360 view, product recommendations, daily revenue aggregates

Data scientists use the silver/gold layers for ML models. Analysts query gold via SQL. Raw data remains in bronze for reprocessing if business logic changes.

---

# See Also

- [[Delta Lake & Iceberg]] — table format comparison
- [[Data Mesh]] — decentralized data architecture alternative
- [[02 Reference/Partitioning]] — file organization within a lake
- [[Parquet]] — columnar format used in lake storage
- [[Distributed System]] — horizontal scaling fundamentals
- [[Data Modelling]] — dimensional and analytical modeling patterns
