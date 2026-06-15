## Design a batch system that supports:
* Reprocessing historical data
* Backfills
* Auditability
* Data lineage
How would you organize:
* Raw layer
* Curated layer
* Metadata layer
This question is really testing whether you understand **data lake architecture beyond simple ETL**. The keywords—**reprocessing, backfills, auditability, and lineage**—all point toward designing for **reproducibility** and **governance**.

---

# High-Level Architecture

```text
                Source Systems
                       |
                Batch Ingestion
                       |
                ┌─────────────┐
                │  Raw Layer  │
                └─────────────┘
                       |
                Data Validation
                       |
                ┌─────────────┐
                │ Curated     │
                │ Layer       │
                └─────────────┘
                       |
                Business Views
                       |
                BI / ML / Data Products

                       ↑
                ┌─────────────┐
                │ Metadata    │
                │ Layer       │
                └─────────────┘
```

---

# Design Principles

To support:

|Requirement|Design Principle|
|---|---|
|Reprocessing|Immutable raw data|
|Backfills|Partition-based reruns|
|Auditability|Versioned datasets + load history|
|Lineage|Metadata-driven tracking|

---

# 1. Raw Layer (Bronze)

The raw layer is the most important component.

### Purpose

Store source data exactly as received.

Never:

- Update
    
- Delete
    
- Transform
    

Only append.

---

## Folder Structure

```text
raw/

  crm/
      load_date=2026-06-01/
      load_date=2026-06-02/

  erp/
      load_date=2026-06-01/
      load_date=2026-06-02/

  mobile/
      load_date=2026-06-01/
```

Every ingestion creates a new batch.

---

## Add Batch Metadata

Every record receives:

```sql
source_system
batch_id
load_timestamp
file_name
record_hash
```

Example:

|customer_id|source|batch_id|load_ts|
|---|---|---|---|
|101|CRM|B20260601|01-Jun|

---

## Why?

Suppose Finance says:

> Revenue for March changed.

We can reload:

```text
raw/sales/load_date=2026-03-15
```

without requesting data again.

---

## Retention

Keep raw data indefinitely.

Storage is usually cheaper than re-ingesting.

---

# 2. Curated Layer (Silver / Gold)

The curated layer contains trusted business datasets.

---

## Silver Layer

Responsibilities:

- Standardization
    
- Deduplication
    
- Validation
    
- Data quality enforcement
    

Example:

```text
customer_master
product_master
sales_transactions
```

---

## Gold Layer

Business-ready datasets.

Examples:

```text
daily_sales
monthly_revenue
customer_360
inventory_kpis
```

---

# Versioning Strategy

Use:

- Apache Iceberg
    
- Delta Lake
    

Benefits:

- Snapshots
    
- Time travel
    
- Version history
    

Example:

```sql
SELECT *
FROM sales VERSION AS OF 157
```

This is critical for audits.

---

# Reprocessing Historical Data

A common interview topic.

---

## Scenario

Bug discovered:

```text
Tax calculation incorrect
```

for:

```text
Jan 2025 → Mar 2025
```

---

## Approach

Re-run only affected partitions.

```text
sales/
    sale_date=2025-01
    sale_date=2025-02
    sale_date=2025-03
```

Pipeline:

```text
Raw
 ↓
Silver
 ↓
Gold
```

for those partitions only.

Avoid full lake rebuilds.

---

# Backfill Strategy

Backfills happen when:

- New business logic introduced
    
- Historical data received late
    
- Missing ingestion fixed
    

---

## Example

Marketing starts providing:

```text
campaign_id
```

today.

Business wants:

```text
Last 3 years attribution
```

---

## Solution

Backfill workflow:

```text
Historical Raw Data
        ↓
Apply New Logic
        ↓
Write New Version
        ↓
Validate
        ↓
Publish
```

Use separate environments:

```text
backfill_run_001
backfill_run_002
```

before promoting results.

---

# Auditability

Interviewers love this section.

---

## Questions We Should Answer

Who loaded the data?

When?

From which file?

Using which code version?

How many records?

Were records rejected?

---

## Audit Tables

### Ingestion Audit

|batch_id|source|rows|load_time|
|---|---|---|---|
|B1001|CRM|5M|01:00|

---

### Transformation Audit

|run_id|job|source_version|target_version|
|---|---|---|---|
|R2001|Sales ETL|102|210|

---

### Data Quality Audit

|run_id|check|result|
|---|---|---|
|R2001|Null Check|PASS|

---

## Result

Every dataset becomes traceable.

---

# Data Lineage

Lineage answers:

> Where did this data come from?

and

> What breaks if I change this table?

---

## Column-Level Example

```text
monthly_revenue
      |
      +---- sales_fact.amount
      |
      +---- currency_rate.rate
```

---

## Dataset-Level Example

```text
CRM
ERP
Mobile
      ↓
sales_fact
      ↓
customer_360
      ↓
executive_dashboard
```

---

## Metadata Captured

For every pipeline:

```text
source tables
target tables
columns used
transformation logic
run_id
timestamp
owner
```

---

## Lineage Tools

Examples:

- OpenMetadata
    
- DataHub
    
- Apache Atlas
    

---

# 3. Metadata Layer

This is the control plane of the entire platform.

Many candidates forget this layer.

---

## Metadata Categories

### Technical Metadata

```text
table_name
columns
datatypes
partition_keys
file_count
storage_location
```

---

### Operational Metadata

```text
job_id
runtime
status
retry_count
SLA
```

---

### Lineage Metadata

```text
source_dataset
target_dataset
transformation
```

---

### Data Quality Metadata

```text
row_count
duplicate_count
null_count
freshness
```

---

### Audit Metadata

```text
batch_id
loaded_by
load_timestamp
source_file
```

---

## Example Metadata Tables

```sql
metadata.datasets

metadata.pipeline_runs

metadata.data_quality_results

metadata.lineage

metadata.audit_log
```

---

# Recommended Organization

```text
Data Lake
│
├── raw/
│     ├── crm/
│     ├── erp/
│     ├── mobile/
│     └── api/
│
├── curated/
│     ├── silver/
│     └── gold/
│
└── metadata/
      ├── dataset_catalog
      ├── lineage
      ├── audit_log
      ├── pipeline_runs
      └── dq_results
```

---

# Interview Summary

> I would organize the platform into three layers. The Raw layer would store immutable, append-only source data partitioned by ingestion date and enriched with batch metadata to enable replay, reprocessing, and backfills. The Curated layer would contain validated and business-ready datasets managed through Iceberg or Delta Lake to support versioning, time travel, and partition-level reprocessing. The Metadata layer would act as the governance control plane, storing dataset catalogs, lineage information, audit logs, pipeline execution history, and data quality results. This architecture enables historical reprocessing, controlled backfills, full auditability, and end-to-end lineage while keeping the system reproducible and operationally manageable.