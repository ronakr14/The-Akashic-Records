A batch job completes successfully but produces incorrect numbers.
How would you detect and prevent this?

This is a classic **data quality and observability** problem. The hardest failures in data engineering are not jobs that fail—they're jobs that succeed and silently produce bad data.

## How to Detect Incorrect Numbers

### 1. Row Count Validation

Compare source and target counts.

```sql
-- Source
SELECT COUNT(*) FROM orders_source;

-- Target
SELECT COUNT(*) FROM orders_target;
```

Alert if variance exceeds a threshold.

Example:

|Expected|Actual|
|---|---|
|10,000,000|9,200,000|

Something is clearly wrong.

---

### 2. Aggregate Reconciliation

Validate business metrics.

```sql
SELECT
    COUNT(*) AS orders,
    SUM(order_amount) AS revenue
FROM orders;
```

Compare with:

- Previous day
    
- Source system
    
- Finance reports
    

Example:

|Metric|Yesterday|Today|
|---|---|---|
|Revenue|$1.2M|$120K|

Likely a pipeline issue.

---

### 3. Freshness Checks

Verify data arrived.

```sql
SELECT MAX(created_at)
FROM orders;
```

If the latest timestamp is hours behind expectations:

```text
Expected: 2026-06-04 23:59
Actual:   2026-06-04 06:00
```

The load may have stopped midway.

---

### 4. Null Checks

Critical columns should never suddenly become null.

```sql
SELECT COUNT(*)
FROM orders
WHERE customer_id IS NULL;
```

Unexpected spikes indicate transformation problems.

---

### 5. Uniqueness Checks

Detect duplicates.

```sql
SELECT order_id, COUNT(*)
FROM orders
GROUP BY order_id
HAVING COUNT(*) > 1;
```

Important for incremental loads.

---

### 6. Referential Integrity Checks

Verify joins still work.

```sql
SELECT COUNT(*)
FROM orders o
LEFT JOIN customers c
ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL;
```

Large counts may indicate dimension load failures.

---

### 7. Distribution Anomaly Detection

Compare statistical patterns.

Example:

|Metric|Historical|Today|
|---|---|---|
|Avg order value|85|84|
|Median|80|79|
|Max|5000|5100|

Looks healthy.

But:

|Metric|Historical|Today|
|---|---|---|
|Avg order value|85|8|

Something broke.

---

### 8. Schema Drift Detection

Check for:

- New columns
    
- Missing columns
    
- Type changes
    

Example:

```text
price DECIMAL
```

becomes:

```text
price STRING
```

and downstream aggregations silently fail.

---

## How to Prevent Incorrect Numbers

### 1. Data Quality Gates

Do not publish data unless validations pass.

Pipeline:

```text
Extract
   ↓
Transform
   ↓
Validate
   ↓
Publish
```

If validation fails:

```text
STOP PIPELINE
```

instead of exposing bad data.

---

### 2. Automated Expectations

Use tools such as:

- Great Expectations
    
- Soda
    
- dbt tests
    

Example:

```yaml
expect_column_values_to_not_be_null
expect_table_row_count_to_be_between
expect_column_values_to_be_unique
```

---

### 3. Reconciliation Framework

For every load:

```text
Source count
Target count

Source revenue
Target revenue

Source customers
Target customers
```

Store results in audit tables.

---

### 4. Idempotent Processing

Ensure reruns don't create duplicates.

Example:

```sql
MERGE INTO target
```

instead of:

```sql
INSERT INTO target
```

---

### 5. Monitoring and Alerting

Alert on:

- Row count drops
    
- Revenue changes
    
- Freshness issues
    
- Null spikes
    
- Duplicate spikes
    

Don't wait for business users to discover problems.

---

### 6. Canary / Sample Validation

Before loading billions of rows:

- Validate a subset
    
- Compare results
    
- Then publish
    

Common in large-scale pipelines.

---

### 7. End-to-End Data Contracts

Define expectations between producers and consumers.

Example:

```text
customer_id: NOT NULL
order_amount: DECIMAL
created_at: UTC timestamp
```

Breaking changes are detected before deployment.

---

## Interview Answer

> A successful batch job does not guarantee correct data. I would implement automated data quality checks including row-count reconciliation, aggregate validation, freshness checks, null and uniqueness tests, referential integrity checks, and anomaly detection. To prevent bad data from reaching consumers, I would place quality gates in the pipeline so data is only published when validations pass. I would also maintain audit tables, monitoring, alerting, and idempotent processing to ensure both correctness and recoverability.