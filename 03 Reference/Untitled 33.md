How would you validate a batch load before publishing it?
Possible checks:
* Row counts
* Null checks
* Referential integrity
* Distribution checks
* Freshness checks
This is a very common production-oriented question. The interviewer is testing whether you understand that **a successful ETL job does not necessarily mean correct data**.

A mature pipeline should have a **data validation gate** between processing and publishing.

```text
Raw → Transform → Validation → Publish
```

If validation fails:

```text
Raw → Transform → Validation FAILED
                    ↓
                Quarantine
                    ↓
                 Alert
```

The data should **not** be published to downstream consumers.

---

# Validation Framework

I typically organize checks into five categories:

1. Completeness (row counts)
    
2. Validity (nulls and formats)
    
3. Integrity (relationships)
    
4. Consistency (distribution checks)
    
5. Freshness (timeliness)
    

---

# 1. Row Count Validation

The first and simplest check.

## Why?

Detect:

- Partial loads
    
- Missing files
    
- Truncated extracts
    
- Pipeline failures
    

---

### Example

Source:

```text
Orders: 10,000,000 rows
```

Target:

```text
Orders: 2,000,000 rows
```

Immediately suspicious.

---

### SQL Example

```sql
SELECT COUNT(*)
FROM source_orders;
```

vs

```sql
SELECT COUNT(*)
FROM target_orders;
```

---

### Tolerance-Based Validation

Sometimes transformations legitimately filter records.

Example:

```text
Source: 10,000,000

Expected:
9,950,000–10,050,000
```

Use configurable thresholds.

---

# 2. Null Checks

Critical fields should never be null.

---

## Example

```text
order_id
customer_id
transaction_date
```

must always exist.

---

### SQL Example

```sql
SELECT COUNT(*)
FROM orders
WHERE order_id IS NULL;
```

Expected:

```text
0
```

---

### Common Checks

|Column|Rule|
|---|---|
|order_id|NOT NULL|
|customer_id|NOT NULL|
|amount|NOT NULL|
|email|Valid format|

---

# 3. Referential Integrity Checks

Ensure relationships remain valid.

---

## Example

Orders table:

```text
customer_id
```

should exist in:

```text
customers
```

---

### SQL Example

```sql
SELECT COUNT(*)
FROM orders o
LEFT JOIN customers c
ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL;
```

Expected:

```text
0
```

---

### Detects

- Missing dimension records
    
- Broken joins
    
- Incomplete loads
    

---

# 4. Duplicate Checks

Frequently overlooked.

---

### Example

Primary key:

```text
order_id
```

should be unique.

---

### SQL

```sql
SELECT
order_id,
COUNT(*)
FROM orders
GROUP BY order_id
HAVING COUNT(*) > 1;
```

Expected:

```text
No rows
```

---

### Detects

- Retry failures
    
- Non-idempotent loads
    
- Duplicate ingestion
    

---

# 5. Distribution Checks

Row counts can pass while data is still wrong.

This is where distribution validation helps.

---

## Example

Yesterday:

```text
US Sales = 40%
EU Sales = 35%
APAC Sales = 25%
```

Today:

```text
US Sales = 98%
EU Sales = 1%
APAC Sales = 1%
```

Likely an issue.

---

### Validate Histograms

Compare:

```text
Country Distribution
Product Distribution
Order Status Distribution
Revenue Distribution
```

against historical baselines.

---

### Example Query

```sql
SELECT
country,
COUNT(*)
FROM orders
GROUP BY country;
```

Compare to prior runs.

---

### Detects

- Missing partitions
    
- Corrupt source files
    
- Bad transformations
    

---

# 6. Aggregate Reconciliation

Very common in financial systems.

---

### Example

Source

```text
Revenue = $52,314,123
```

Target

```text
Revenue = $49,201,554
```

Problem.

---

### Validate

```sql
SELECT SUM(amount)
FROM orders;
```

---

Common metrics:

```text
COUNT(*)
SUM(revenue)
SUM(quantity)
AVG(order_value)
```

---

# 7. Freshness Checks

Ensures current data was actually loaded.

---

### Example

Expected:

```text
Data available by 2 AM
```

Latest record:

```text
11 PM yesterday
```

Load may have failed.

---

### SQL

```sql
SELECT MAX(updated_at)
FROM orders;
```

Expected:

```text
Within SLA
```

---

### Detects

- Stuck pipelines
    
- Source extraction failures
    
- Delayed feeds
    

---

# 8. Schema Validation

Check schema consistency before publishing.

---

### Example

Expected:

```text
customer_id BIGINT
```

Received:

```text
customer_id STRING
```

Potential downstream breakage.

---

Validate:

- Column names
    
- Data types
    
- Required fields
    

---

# 9. Partition Validation

For partitioned datasets.

---

Example:

```text
sales/
  sale_date=2026-06-04
```

Verify:

- Partition exists
    
- Files exist
    
- Record count > 0
    

---

Detects:

- Missing partitions
    
- Failed writes
    

---

# 10. Business Rule Validation

The most valuable checks.

These are domain-specific.

---

Examples:

```text
Revenue >= 0
```

```text
Order Amount > 0
```

```text
Inventory >= 0
```

```text
Order Date <= Current Date
```

---

These often catch issues that technical checks miss.

---

# Publish Strategy

Never write directly to production tables.

Instead:

```text
Stage Table
     ↓
Validation
     ↓
PASS
     ↓
Publish
```

or

```text
Stage Table
     ↓
Validation
     ↓
FAIL
     ↓
Quarantine + Alert
```

---

# Automation

Common tools:

- Great Expectations
    
- Soda
    
- dbt tests
    

---

# Interview Answer (2-Minute Version)

> Before publishing a batch load, I would implement a validation gate. First, I'd perform row count reconciliation to ensure expected volumes were loaded. Next, I'd run null checks and uniqueness checks on critical business keys. I'd validate referential integrity between fact and dimension tables to detect broken relationships. Then I'd compare key distributions and aggregate metrics, such as revenue totals and record counts, against historical baselines to catch anomalies. I'd also perform freshness checks to ensure the latest data meets SLA requirements and validate schema compatibility. Only after all validations pass would the data be promoted from staging to production. If any check fails, the batch would be quarantined and alerts triggered, preventing bad data from reaching downstream consumers.