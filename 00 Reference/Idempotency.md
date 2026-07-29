# AI Summary
Idempotency. A job is **idempotent** if running it multiple times produces the same final state

```table-of-contents
```

# Idempotency

## What Is Idempotency?

A job is **idempotent** if running it multiple times produces the same final state.

Example:

```text
Run #1 → 1,000 rows loaded
Run #2 → still 1,000 rows loaded
Run #3 → still 1,000 rows loaded
```

Not:

```text
Run #1 → 1,000 rows
Run #2 → 2,000 rows
Run #3 → 3,000 rows
```

Mathematically: `f(f(x)) = f(x)`. Applying the function twice is the same as applying it once. In data pipelines, this means the operation is safe to retry without side effects.

---

## Delivery Semantics

Idempotency is closely related to delivery guarantees. Understand the distinction:

| Semantic | Definition | Requires Idempotency? |
|---|---|---|
| **At-most-once** | Data is processed zero or more times. May lose records. | No |
| **At-least-once** | Data is processed one or more times. May duplicate. | Yes — to absorb duplicates |
| **Exactly-once** | Data is processed exactly once. No loss, no duplicates. | Yes — plus dedup or txn |

→ **Risk:** Assuming exactly-once when your pipeline only guarantees at-least-once leads to silent data corruption. Most distributed systems are at-least-once — idempotency is your responsibility.

---

## Failure Modes

Jobs fail. Understand what happens at each failure point.

### Scenario 1: Crash After Write, Before Commit

```text
Write 1,000 rows to target
Crash before transaction commits
```

**Without idempotency:** Partial data visible. Retry writes another 1,000 rows on top of partials.

**With idempotent write (overwrite/MERGE):** Retry produces clean state.

### Scenario 2: Crash After Commit, Before Watermark Update

```text
Write succeeds
Transaction committed
Crash before advancing watermark
```

**Without idempotency:** Next run re-reads same data → duplicates.

**With idempotency:** MERGE handles duplicates, or partition overwrite replaces same data.

### Scenario 3: Crash During Write

```text
Write row 1-500
Crash
Write never completes
```

**With atomic writes:** Transaction rolls back. No partial data visible.

**Without atomic writes:** 500 rows visible. Readers see incomplete state.

→ **Risk:** Not understanding failure modes means your "idempotent" pipeline isn't idempotent under the failures that actually happen.

---

## Common Techniques

### 1. Partition Overwrite (Most Common)

Instead of appending data:

```sql
INSERT INTO sales
SELECT * FROM staging_sales;
```

Use:

```sql
INSERT OVERWRITE sales
PARTITION(dt='2026-06-01')
SELECT * FROM staging_sales;
```

Process:

```text
Delete partition
↓
Rebuild partition
↓
Publish
```

Re-running produces identical results.

**Good for:** Daily batch loads, data lake pipelines, Hive/Spark/Iceberg/Delta workloads

### 2. MERGE / UPSERT

Load records based on business keys.

```sql
MERGE INTO orders t
USING staging_orders s
ON t.order_id = s.order_id
WHEN MATCHED THEN
 UPDATE SET ...
WHEN NOT MATCHED THEN
 INSERT ...
```

If the job runs again:

```text
Existing rows updated
New rows inserted
No duplicates
```

**Good for:** CDC, incremental pipelines, dimension tables

### 3. Deduplication Using Natural Keys

Suppose `order_id` is unique. Before writing:

```sql
SELECT DISTINCT *
FROM incoming_orders;
```

or

```sql
ROW_NUMBER()
OVER (
  PARTITION BY order_id
  ORDER BY updated_at DESC
)
```

Keep only the latest record.

### 4. Maintain Watermarks Carefully

Track:

```text
Last processed timestamp
Last processed ID
```

Example:

```sql
WHERE updated_at > watermark
```

After successful completion:

```text
Update watermark
```

**Common mistake:**

```text
Read data
↓
Advance watermark
↓
Job crashes
```

Records are lost forever.

**Correct:**

```text
Read data
↓
Write target
↓
Validate
↓
Commit watermark
```

### 5. Atomic Writes

Avoid partially written data.

**Bad:**

```text
Write file1
Write file2
Crash
```

Readers see incomplete data.

**Good:**

```text
Write temp files
Validate
Atomic rename/swap
Publish
```

Used heavily by Apache Iceberg, Delta Lake, and Apache Hudi.

### 6. Batch Run IDs

Track processed batches. Audit table:

```sql
batch_id
status
processed_at
```

Before processing:

```sql
SELECT *
FROM audit_table
WHERE batch_id='2026-06-01'
```

If already completed:

```text
Skip execution
```

### 7. Deterministic Transformations

Avoid:

```sql
SELECT CURRENT_TIMESTAMP;
```

or

```sql
SELECT RANDOM();
```

during transformations. These produce different results every rerun.

Prefer:

```sql
SELECT source_timestamp;
```

from the source data.

### 8. Staging → Validation → Publish Pattern

A robust design:

```text
Raw Data
    ↓
Staging
    ↓
Validation
    ↓
Publish
```

Never write directly to production tables. This prevents partial results from becoming visible.

---

## Distributed System Patterns

When idempotency spans multiple services or steps:

### Two-Phase Commit (2PC)

```text
Phase 1: Prepare all participants
Phase 2: Commit all (or rollback if any failed)
```

Guarantees atomicity across distributed systems. Used in databases but expensive for data pipelines.

### Saga Pattern

```text
Step A → Step B → Step C
```

If Step C fails, run compensating transactions:

```text
Undo B → Undo A
```

Each step must be idempotent so retries are safe.

### Idempotent Consumers

When consuming from Kafka or event streams:

- Use `offset` as watermark
- Deduplicate by event ID
- Commit offset only after successful processing

→ **Risk:** At-least-once consumers without dedup produce duplicates. This is the most common data quality bug in streaming pipelines.

---

## Testing Idempotency

### How to Verify

1. **Run twice, compare:** Execute the pipeline twice. Row counts and checksums should match.
2. **Inject failures:** Kill the job at 25%, 50%, 75% completion. Verify final state is correct.
3. **Duplicate input:** Feed the same data twice. Verify no duplicates in output.
4. **Out-of-order input:** Feed data in different order. Verify final state is identical.

### Checklist

- [ ] Pipeline produces same row count on rerun
- [ ] No duplicate primary keys after rerun
- [ ] Aggregates (sum, count) match after rerun
- [ ] Partial failures leave no incomplete data
- [ ] Watermarks only advance on success
- [ ] Non-deterministic functions are avoided or seeded

---

## Real Example

Daily orders pipeline:

```text
Process dt=2026-06-01
```

**Bad:**

```sql
INSERT INTO fact_orders
SELECT *
FROM staging_orders;
```

Retry: Duplicates created.

**Good:**

```sql
DELETE FROM fact_orders
WHERE dt='2026-06-01';
INSERT INTO fact_orders
SELECT *
FROM staging_orders
WHERE dt='2026-06-01';
```

or `INSERT OVERWRITE`. Retry: Same final result.

---

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|---|---|---|
| Append-only pipelines | Duplicates on retry | Use overwrite or MERGE |
| Watermark before write | Lost records on crash | Commit watermark after write + validate |
| Non-deterministic transforms | Different results per run | Use source timestamps, fixed seeds |
| No atomic writes | Partial data visible | Write to temp, then atomic rename |
| No dedup on at-least-once | Duplicate rows | Add MERGE or ROW_NUMBER dedup |
| Assuming exactly-once | Silent data corruption | Design for at-least-once + idempotency |
| No audit trail | Can't tell what was processed | Track batch IDs and status |
