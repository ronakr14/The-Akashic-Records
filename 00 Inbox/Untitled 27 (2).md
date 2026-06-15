## Design a batch architecture for a data lake where data arrives from:
* CRM
* ERP
* Mobile apps
* Third-party APIs
Requirements:
* Daily refresh
* Historical retention
* Data quality validation
* Schema evolution support
For a data engineering system design interview, I'd structure the answer around **ingestion → storage → processing → governance → operations**.

---

# Batch Data Lake Architecture

### Requirements

Sources:

- CRM (Salesforce, HubSpot, etc.)
    
- ERP (SAP, Oracle ERP)
    
- Mobile applications
    
- Third-party APIs
    

Requirements:

- Daily refresh
    
- Historical retention
    
- Data quality validation
    
- Schema evolution
    

---

# High-Level Architecture

```text
                    +-------------+
                    | CRM Systems |
                    +-------------+
                           |
                    +-------------+
                    | ERP Systems |
                    +-------------+
                           |
                    +-------------+
                    | Mobile Apps |
                    +-------------+
                           |
                    +-------------+
                    | Third Party |
                    |    APIs     |
                    +-------------+
                           |
                    [Batch Ingestion]
                           |
                    +-------------+
                    | Raw Zone    |
                    | (Bronze)    |
                    +-------------+
                           |
                 Data Validation Layer
                           |
                    +-------------+
                    | Cleansed    |
                    | (Silver)    |
                    +-------------+
                           |
                 Business Transformations
                           |
                    +-------------+
                    | Curated     |
                    | (Gold)      |
                    +-------------+
                           |
                BI / ML / Analytics
```

---

# 1. Ingestion Layer

Since the requirement is **daily refresh**, batch ingestion is sufficient.

### CRM

Typical methods:

- Salesforce Bulk API
    
- CRM exports
    
- Incremental extraction using `LastModifiedDate`
    

Example:

```sql
WHERE LastModifiedDate > last_successful_run
```

---

### ERP

Common approaches:

- Database extracts
    
- CDC snapshots
    
- Scheduled exports
    

Example:

```text
SAP → CSV/Parquet → Data Lake
```

---

### Mobile Apps

Usually:

```text
App Events
    ↓
Operational DB
    ↓
Daily Export
    ↓
Data Lake
```

---

### Third-Party APIs

Use scheduled extraction jobs:

```text
Airflow
  ↓
REST API
  ↓
JSON Files
  ↓
Data Lake
```

Store raw responses for auditing.

---

# 2. Storage Layer

Use cloud object storage:

- Amazon S3
    
- Azure Data Lake Storage
    
- Google Cloud Storage
    

---

## Lakehouse Format

Use:

- Apache Iceberg  
    or
    
- Delta Lake
    

Reasons:

- ACID transactions
    
- Time travel
    
- Schema evolution
    
- Partition pruning
    

---

# 3. Multi-Zone Architecture

## Bronze Layer (Raw)

Purpose:

Store source data exactly as received.

Example:

```text
bronze/
   crm/
      load_dt=2026-06-04/
   erp/
      load_dt=2026-06-04/
```

Characteristics:

- Immutable
    
- No transformations
    
- Full auditability
    

Retention:

```text
Forever
```

This enables replay and recovery.

---

## Silver Layer (Validated & Standardized)

Activities:

- Deduplication
    
- Data type normalization
    
- Reference data enrichment
    
- Quality checks
    

Example:

```text
customer_id
customer_name
country_code
```

instead of inconsistent source formats.

---

## Gold Layer (Business Ready)

Examples:

```text
daily_sales
customer_360
inventory_snapshot
```

Optimized for:

- BI dashboards
    
- Reporting
    
- ML feature generation
    

---

# 4. Historical Retention Strategy

One of the most important interview topics.

---

## Raw Retention

Keep every ingestion batch.

```text
bronze/crm/load_dt=YYYY-MM-DD
```

Never overwrite.

---

## Slowly Changing Dimensions

For customer/product master data:

Use:

### Type 2 History

```text
customer_id
customer_name
effective_from
effective_to
is_current
```

Example:

|Customer|City|Effective From|Effective To|
|---|---|---|---|
|101|Pune|Jan 1|Mar 31|
|101|Mumbai|Apr 1|Current|

Historical analysis remains accurate.

---

## Snapshot Tables

For ERP inventory:

```text
inventory_snapshot_dt
```

Store daily snapshots.

---

# 5. Data Quality Validation

Data quality should occur before data reaches Silver.

---

## Validation Categories

### Completeness

```text
customer_id NOT NULL
```

---

### Uniqueness

```text
order_id unique
```

---

### Referential Integrity

```text
order.customer_id
exists in customer table
```

---

### Freshness

```text
data arrival within SLA
```

---

### Volume Checks

Example:

```text
Yesterday: 10M records
Today: 500K records
```

Alert immediately.

---

## Data Quality Frameworks

Common tools:

- Great Expectations
    
- Soda
    

Failed records go to:

```text
quarantine zone
```

instead of stopping the entire pipeline.

---

# 6. Schema Evolution Support

Real-world systems constantly change schemas.

Example:

CRM adds:

```text
customer_tier
```

next month.

---

## Challenges

Without schema evolution:

```text
Pipeline Failure
```

---

## Solution

Use Iceberg/Delta features.

Supported changes:

### Add Columns

```sql
ALTER TABLE customer
ADD COLUMN customer_tier STRING;
```

---

### Optional Fields

Allow nullable columns.

```text
NULL
```

for historical records.

---

### Schema Registry

Maintain metadata:

```text
source
column
datatype
version
effective_date
```

---

### Compatibility Rules

Allow:

```text
Additive changes
```

Disallow:

```text
Breaking datatype changes
```

without review.

---

# 7. Orchestration

Use:

- Apache Airflow
    
- Dagster
    

Daily workflow:

```text
Extract
   ↓
Load Bronze
   ↓
Quality Validation
   ↓
Transform Silver
   ↓
Build Gold
   ↓
Publish
```

---

# 8. Monitoring

Track:

### Pipeline Metrics

- Runtime
    
- Success rate
    
- Throughput
    

### Data Metrics

- Row counts
    
- Freshness
    
- Null percentages
    

### Cost Metrics

- Storage growth
    
- Compute consumption
    

---

# Interview Summary Answer

> I would build a layered lakehouse architecture using object storage and Iceberg/Delta tables. Data from CRM, ERP, mobile applications, and third-party APIs would be ingested daily into a Bronze layer in its raw form. A Silver layer would perform standardization, deduplication, and data quality validation, while a Gold layer would expose business-ready datasets. Historical retention would be achieved through immutable raw storage, snapshot tables, and SCD Type 2 dimensions. Data quality would be enforced through completeness, uniqueness, freshness, and referential integrity checks. Schema evolution would be handled using Iceberg/Delta capabilities, metadata management, and compatibility rules to support non-breaking changes without pipeline downtime. This design provides scalability, auditability, historical tracking, and operational reliability.