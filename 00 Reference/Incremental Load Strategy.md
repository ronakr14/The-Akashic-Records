# AI Summary
None. Source Table Size: 100 TB

```table-of-contents
```

## Problem Statement

```text
Source Table Size: 100 TB
Full Reload Time: 15 Hours
Business SLA: Daily (or more frequent)
```

A full reload is no longer practical because:

- Expensive
- Misses SLA
- Wastes compute
- Increases source system load

The solution is **incremental loading**.

---

## High-Level Strategy

Instead of:

```text
Read 100 TB
```

every day:

```text
Read only records that changed
since last successful load
```

Example:

```text
Total Table: 100 TB
Daily Changes: 500 GB
Process:
500 GB instead of 100 TB
```

That's a 200x reduction.

---

## Approach 1 — Timestamp-Based Extraction

Most common solution.

Assume source table:

```sql
customer_orders
(
    order_id,
    customer_id,
    amount,
    created_at,
    updated_at
)
```

### Maintain a Watermark

Metadata table:

```sql
etl_watermark
(
    table_name,
    last_successful_timestamp
)
```

Example:

|table_name|last_successful_timestamp|
|---|---|
|customer_orders|2026-06-03 23:59:59|

### Extraction Query

```sql
SELECT *
FROM customer_orders
WHERE updated_at >
      '2026-06-03 23:59:59';
```

Only changed rows are extracted.

### Update Watermark

After successful completion:

```text
2026-06-04 23:59:59
```

becomes the new watermark.

---

## Watermark vs High-Water Mark

Interviewers often use these interchangeably.

### Watermark

Tracks progress of ingestion.

```text
Last Processed Timestamp
```

### High-Water Mark

Highest successfully processed value.

```text
updated_at = 2026-06-04 22:30:15
```

or

```text
order_id = 99999999
```

Both serve the same purpose:

```text
Don't reread old data
```

---

## Approach 2 — Incrementing Primary Key

Useful when timestamps don't exist.

Example:

```sql
orders
(
    order_id,
    ...
)
```

Maintain:

```text
Last Processed Order ID
```

Query:

```sql
SELECT *
FROM orders
WHERE order_id > 99999999;
```

### Limitation

Misses:

```text
Updates
Deletes
```

Works best for append-only tables.

---

## Approach 3 — Change Data Capture (CDC)

Best enterprise solution.

Instead of querying tables directly: capture database transaction logs.

Examples:

- MySQL Binlog
- PostgreSQL WAL
- SQL Server CDC

Tools: [[Debezium]], [[Apache Kafka]]

### CDC Events

Insert:

```json
{
  "op":"INSERT",
  "id":1001
}
```

Update:

```json
{
  "op":"UPDATE",
  "id":1001
}
```

Delete:

```json
{
  "op":"DELETE",
  "id":1001
}
```

### Benefits

- Captures inserts, updates, and deletes
- Near real-time
- No full table scans

---

## Incremental Pipeline Architecture

```text
Source Database
        |
        |
   CDC / Watermark
        |
        v
Landing Zone
        |
        v
Staging Layer
        |
        v
Merge Into Target
        |
        v
Analytics Table
```

---

## Handling Updates

Suppose:

```text
order_id=100
amount=500
```

changes to:

```text
amount=700
```

Appending would create duplicates. Instead:

```sql
MERGE INTO sales tgt
USING sales_increment src
ON tgt.order_id = src.order_id
WHEN MATCHED THEN
UPDATE SET amount = src.amount
WHEN NOT MATCHED THEN
INSERT (...);
```

---

## Handling Deletes

Without CDC, deletes are difficult:

```text
Row removed from source
```

Target never knows.

### CDC Solution

CDC emits a DELETE event. Target executes:

```sql
DELETE
FROM sales
WHERE order_id = 100;
```

---

## Idempotency

A very common follow-up interview question:

> What happens if the job fails halfway?

[[Idempotency]] ensures re-running the same job produces the same result. Key techniques:

- Use watermarks to avoid reprocessing
- Use MERGE instead of INSERT
- Track job status in metadata tables
- Design jobs to be re-runnable without side effects

---

## Production Design — 100 TB Table Checklist

1. Initial full load once.
2. Store watermarks in metadata tables.
3. Extract incrementally using `updated_at`.
4. Prefer CDC if available.
5. Use MERGE/UPSERT for updates.
6. Handle deletes through CDC events.
7. Implement idempotent batch processing.
8. Use checkpoints and retries.
9. Use a small lookback window for late-arriving records.

---

## See Also

- [[ETL vs ELT]]
- [[Debezium]]
- [[Data Engineering]]
- [[Apache Kafka]]
- [[00 Reference/DuckDB]]
