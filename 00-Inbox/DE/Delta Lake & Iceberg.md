---
domain: data-engineering
subdomain: lakehouse-table-formats
note_type: technology
source_type: self
status: evergreen
level: advanced
tags:
  - delta-lake
  - lakehouse
  - table-formats
---
# AI Summary
```
  Comprehensive guide to modern lakehouse table formats, explaining why Delta Lake, Apache Iceberg, and Hudi exist beyond Parquet-based data lakes. Covers the reliability problems they solve, internal architectures, ACID transactions, metadata management, time travel, multi-engine support, catalog integration, operational maintenance, decision criteria, and industry trends to help engineers choose the right table format for different workloads. :contentReference[oaicite:2]{index=2}
```
---
> Yes. This is one of the most important topics in modern data engineering.
>
> Before we discuss them, challenge one common assumption:
>
> Many engineers think:
>
> ```
> Data Lake + Parquet = Lakehouse
> ```
>
> Not true.

A plain data lake with Parquet files still lacks:

- ACID transactions
- Concurrent writes
- Schema evolution
- Time travel
- Rollbacks
- Metadata management

That's why table formats like **Delta Lake**, **Iceberg**, and **Hudi** were created.

---

## The Problem They Solve

Imagine a data lake:

```text
s3://sales/

part-001.parquet
part-002.parquet
part-003.parquet
```

Now a Spark job starts writing:

```text
part-004.parquet
part-005.parquet
```

Halfway through writing:

```text
Job crashes
```

Questions:

- Which files are valid?
- Which are incomplete?
- Can readers continue safely?
- Can we rollback?

Traditional data lakes cannot answer these questions.

This is called the **data lake reliability problem**.

→ **Risk:** Without a table format, concurrent writes produce corrupt or inconsistent data. Recovery is manual and error-prone.

---

## What Table Formats Actually Are

They are **table formats**, not storage systems.

```text
Storage Layer
-------------
S3
ADLS
GCS
HDFS

        ↑

Table Format
-------------
Delta Lake
Iceberg
Hudi
```

Think of them as:

```text
Git for Data
```

They track:

- Versions
- Commits
- Metadata
- Schema changes

---

## Delta Lake

Originally created by Databricks.

### Architecture

```text
sales_table/

_data/
  part-001.parquet
  part-002.parquet

_delta_log/
  000000.json
  000001.json
  000002.json
```

The secret sauce is `_delta_log` — every change is recorded as a transaction log.

### Example: Time Travel

Version 1:

```text
customer
---------
1
2
3
```

Insert:

```sql
INSERT INTO customer
VALUES (4)
```

Creates Version 2. Now you can query:

```sql
SELECT *
FROM customer VERSION AS OF 1
```

This is called **Time Travel**.

### Strengths

- **Excellent Spark Integration** — Delta was built around Spark. `Spark + Delta` is still the most mature combination.
- **MERGE Support** — `MERGE INTO customer` works extremely well. This is why Delta dominates CDC workloads.

    ```text
    SQL Server CDC
          ↓
    Databricks
          ↓
    Delta Lake
    ```

- **Mature Ecosystem** — Works seamlessly with Databricks, Spark, and Structured Streaming.

### Weaknesses

- **Historically Databricks-Centric** — Although Delta has become more open, many advanced features arrived first in Databricks. Some organizations worried about vendor lock-in.

---

## Iceberg

Originally created at Netflix.

Netflix had a huge problem:

```text
Petabytes of data
Millions of partitions
```

Hive metadata became a bottleneck. Iceberg was designed to solve that.

### Architecture

Instead of transaction logs, Iceberg uses a metadata hierarchy:

```text
Metadata File
       ↓
Manifest Files
       ↓
Parquet Files
```

This allows Iceberg to scale extremely well — metadata is never a single point of contention.

### Strengths

- **Engine Independence** — Works with almost everything:

    - Spark
    - Flink
    - Trino
    - Presto
    - Snowflake
    - Athena
    - DuckDB
    - Dremio

    This is Iceberg's biggest advantage.

- **Better Multi-Engine Story** — Suppose:

    ```text
    Spark writes
    Trino reads
    Flink streams
    DuckDB explores
    ```

    Iceberg handles this naturally.

- **Better Metadata Scaling** — For huge datasets (10 PB+, billions of files), Iceberg often scales more elegantly.

- **Partition Evolution** — You can change partitioning without rewriting the entire dataset. Delta's support is more limited here.

### Weaknesses

- **MERGE operations** were historically weaker than Delta. The gap has narrowed significantly.
- **Streaming integration** lagged Delta. Again, the gap is closing.

---

## Hudi

Originally created at Uber. The third major table format — often overlooked but important.

### When Hudi Fits

- **Streaming-first workloads** — Hudi was built for real-time ingestion from the start.
- **Record-level upserts/deletes** — Hudi handles these efficiently without rewriting entire files.
- **Incremental processing** — Hudi's change streams allow efficient downstream consumption.

### Hudi vs Delta vs Iceberg

| Dimension | Delta | Iceberg | Hudi |
|---|---|---|---|
| Creator | Databricks | Netflix | Uber |
| Primary strength | Spark + MERGE | Multi-engine | Streaming ingestion |
| Streaming | Good | Good | Excellent |
| Upsert performance | Excellent | Good | Excellent |
| Engine support | Spark-centric | Universal | Spark/Flink-centric |
| Maturity | High | High | Growing |

→ **Risk:** Choosing a table format without evaluating all three can lead to painful migrations. The "best" format depends on your engine mix and workload pattern.

---

## Comparison

| Feature | Delta | Iceberg | Hudi |
|---|---|---|---|
| Creator | Databricks | Netflix | Uber |
| Metadata | Transaction Log | Metadata + Manifest | Timeline (commits) |
| Spark Support | Excellent | Excellent | Excellent |
| Databricks Support | Native | Good | Good |
| Trino Support | Good | Excellent | Good |
| Flink Support | Good | Excellent | Excellent |
| Snowflake Support | Growing | Excellent | Limited |
| Athena Support | Good | Excellent | Limited |
| Time Travel | Yes | Yes | Yes |
| ACID | Yes | Yes | Yes |
| Schema Evolution | Yes | Yes | Yes |
| Partition Evolution | Limited | Better | Limited |
| Multi-Engine | Good | Excellent | Good |
| Upsert/MERGE | Excellent | Good | Excellent |

---

## When to Choose What

### Choose Delta Lake when:

- You are a Databricks shop
- Your primary engine is Spark
- You need strong MERGE/CDC support
- You want the most mature ecosystem

### Choose Iceberg when:

- You use multiple engines (Spark + Trino + Flink + DuckDB)
- You want vendor-neutral table format
- You need partition evolution at scale
- You have petabytes of data and billions of partitions

### Choose Hudi when:

- Your workload is streaming-first
- You need record-level upserts/deletes at high frequency
- You want efficient incremental processing downstream
- You are building a real-time data lake

### The Pragmatic Answer

Most companies end up supporting more than one. The industry trend:

- **Databricks-centric** → Delta Lake
- **Open Lakehouse** → Iceberg
- **Real-time ingestion** → Hudi (or Iceberg with Flink)

The momentum in the broader ecosystem is currently behind **Apache Iceberg** because vendors want a common table format that nobody controls. Today you'll see support from Snowflake, AWS, Google, Netflix, Apple, and LinkedIn — all investing heavily in Iceberg.

---

## Catalog Layer

Table formats need a **catalog** to track which tables exist and where their metadata lives.

| Catalog | Ecosystem | Notes |
|---|---|---|
| Hive Metastore | Legacy | Still widely used; single point of failure at scale |
| Unity Catalog | Databricks | Unified governance across Databricks assets |
| Nessie | Iceberg-native | Git-like branching for table metadata |
| AWS Glue | AWS | Managed catalog; integrates with Athena, Redshift Spectrum |

→ **Risk:** Picking the wrong catalog creates the same metadata bottleneck you were trying to escape. Match your catalog to your table format and engine mix.

---

## Operational Concerns

Table formats are not "set and forget." They require ongoing maintenance.

### Compaction

Small files hurt query performance. All three formats support compaction:

- **Delta:** `OPTIMIZE` command
- **Iceberg:** `rewrite_data_files` action
- **Hudi:** Built-in compaction for MOR (Merge-on-Read) tables

### Snapshot Expiration / Vacuum

Old snapshots consume storage and slow metadata operations:

- **Delta:** `VACUUM` (default retains 7 days of history)
- **Iceberg:** `expire_snapshots` procedure
- **Hudi:** `clean` command

### Monitoring

Watch for:

- Snapshot count growth (unbounded = metadata bloat)
- File count per partition (too many small files)
- Time since last compaction/clean
- Long-running write transactions blocking readers

---

## Where the Industry Is Moving

```text
Delta Lake  = Best Databricks Experience
Iceberg     = Open Lakehouse Standard
Hudi        = Real-Time Ingestion Specialist
```

For a Senior Data Engineer → Data Architect learning path:

1. Parquet internals
2. Data Lake fundamentals
3. Delta Lake internals
4. CDC with Delta MERGE
5. Iceberg internals
6. Catalogs (Hive, Nessie, Unity Catalog)
7. Open Lakehouse architecture
8. Multi-engine architecture (Spark + Flink + Trino + DuckDB)
9. Table format internals (ACID, snapshots, manifests, partition evolution)

The architect-level discussion: *"How Delta/Iceberg/Hudi actually implement ACID transactions, snapshots, manifests, partition evolution, and metadata trees under the hood."* That's where most engineers stop, and where architects start.