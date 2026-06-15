How would you design automated data quality gates in a batch pipeline?

This is a classic **Senior Data Engineer** interview question because it tests whether you think beyond "pipeline succeeded" and focus on **data correctness**.

---

# Design Goal

Prevent bad data from reaching downstream systems by automatically validating data at key stages.

```text
Source
   ↓
Ingestion
   ↓
Data Quality Gate #1
   ↓
Transformation
   ↓
Data Quality Gate #2
   ↓
Curated Layer
   ↓
Data Quality Gate #3
   ↓
Consumers
```

If a quality check fails:

```text
Fail pipeline
OR
Quarantine data
OR
Raise alert
```

depending on severity.

---

# Layer 1: Ingestion Quality Checks

Validate raw source data immediately after ingestion.

## Row Count Validation

Example:

```text
Yesterday: 10M rows
Today: 12 rows
```

Clearly suspicious.

Rule:

```python
today_count >= yesterday_count * 0.8
```

Alert if violated.

---

## File Arrival Validation

Expected:

```text
sales_20260601.csv
sales_20260602.csv
sales_20260603.csv
```

Check:

- File exists
    
- Correct naming convention
    
- File size not zero
    

---

## Schema Validation

Expected:

```text
order_id BIGINT
customer_id BIGINT
amount DECIMAL
```

Received:

```text
amount STRING
```

Fail immediately.

Tools:

- Great Expectations
    
- Deequ
    
- Pandera
    
- dbt tests
    

---

# Layer 2: Transformation Quality Checks

After transformations verify business logic.

---

## Null Checks

Critical columns:

```sql
order_id
customer_id
transaction_date
```

Rule:

```sql
SELECT COUNT(*)
FROM orders
WHERE order_id IS NULL
```

Expected:

```text
0
```

---

## Uniqueness Checks

Example:

```sql
order_id
```

must be unique.

```sql
SELECT order_id
FROM orders
GROUP BY order_id
HAVING COUNT(*) > 1
```

Failure indicates duplicate processing.

---

## Referential Integrity

Check:

```text
orders.customer_id
```

exists in:

```text
customers.customer_id
```

Example:

```sql
LEFT JOIN customers
```

Any unmatched records indicate data quality issues.

---

# Layer 3: Business Rule Validation

The most valuable checks.

---

## Revenue Validation

Yesterday:

```text
Revenue = $1.2M
```

Today:

```text
Revenue = $4
```

Pipeline succeeded.

Data is wrong.

Rule:

```text
Revenue deviation < 20%
```

Alert if exceeded.

---

## Domain Checks

Example:

```sql
age >= 0
age <= 120
```

or

```sql
amount >= 0
```

Reject invalid records.

---

## Allowed Values

Example:

```text
status IN
(
  'NEW',
  'PROCESSING',
  'COMPLETED',
  'FAILED'
)
```

Anything else is invalid.

---

# Layer 4: Incremental Load Validation

Common production issue.

---

## Missing Records

Suppose:

```text
Last watermark = 2026-06-01 23:59:59
```

Need to verify:

```text
No records skipped
```

Checks:

```sql
MIN(timestamp)
MAX(timestamp)
```

within expected range.

---

## Duplicate Processing

Check:

```sql
COUNT(*)
```

vs

```sql
COUNT(DISTINCT business_key)
```

Large differences indicate reprocessing.

---

# Layer 5: Freshness Checks

Data can be correct but stale.

Example:

```sql
MAX(created_at)
```

Expected:

```text
Within last 24 hours
```

Alert if:

```text
48+ hours old
```

---

# Quarantine Strategy

Not every failure should stop production.

Instead:

```text
Good Records → Main Table
Bad Records → Quarantine Table
```

Example:

```text
customer_id missing
invalid amount
bad date format
```

Store rejected records for investigation.

---

# Monitoring and Alerting

Send alerts through:

- Slack
    
- Teams
    
- Email
    
- PagerDuty
    

Include:

```text
Pipeline Name
Check Failed
Expected Value
Actual Value
Sample Records
```

Avoid:

```text
"Pipeline failed"
```

without context.

---

# Metadata-Driven Framework (Senior-Level Design)

Instead of hardcoding checks:

Create configuration table.

|Table|Check Type|Threshold|
|---|---|---|
|orders|Null Check|0|
|orders|Duplicate Check|0|
|orders|Row Count Variance|20%|
|sales|Freshness|24h|

Pipeline engine reads rules dynamically.

Benefits:

- Reusable
    
- Scalable
    
- Self-service
    
- Easier governance
    

---

# Modern Stack Example

- Ingestion: Airflow / Dagster
    
- Storage: S3 / ADLS
    
- Processing: Spark / DuckDB
    
- Quality Framework: Great Expectations, Deequ, dbt tests
    
- Monitoring: Prometheus + Grafana
    
- Alerting: Slack/PagerDuty
    

---

# Interview Answer (2-Minute Version)

> I would implement automated quality gates at ingestion, transformation, and curated layers. Checks would include schema validation, row count reconciliation, null checks, uniqueness checks, referential integrity, freshness validation, and business-rule validations such as revenue anomalies. Critical failures would stop the pipeline, while record-level issues would be quarantined. All checks would be metadata-driven so new datasets can onboard without code changes. Finally, I'd integrate monitoring and alerting to provide immediate visibility into quality failures before bad data reaches consumers.