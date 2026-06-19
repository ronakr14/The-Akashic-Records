```table-of-contents
```
# What is Idempotency?
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
---
# Common Techniques
## 1. Partition Overwrite (Most Common)
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
### Good for
- Daily batch loads
- Data lake pipelines
- Hive/Spark/Iceberg/Delta workloads
---
## 2. MERGE / UPSERT
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
### Good for
- CDC
- Incremental pipelines
- Dimension tables
---
## 3. Deduplication Using Natural Keys
Suppose:
```text
order_id
```
is unique.
Before writing:
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

---
## 4. Maintain Watermarks Carefully
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
Never update the watermark before the load succeeds.
### Common mistake
```text
Read data
↓
Advance watermark
↓
Job crashes
```
Records are lost forever.
Correct:
```text
Read data
↓
Write target
↓
Validate
↓
Commit watermark
```
---
## 5. Atomic Writes
Avoid partially written data.
Bad:
```text
Write file1
Write file2
Crash
```
Readers see incomplete data.
Good:
```text
Write temp files
Validate
Atomic rename/swap
Publish
```
Used heavily by:
- Apache Iceberg
- Delta Lake
- Apache Hudi
---
## 6. Batch Run IDs
Track processed batches.
Audit table:
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
---
## 7. Deterministic Transformations
Avoid:
```sql
SELECT CURRENT_TIMESTAMP;
```
or
```sql
SELECT RANDOM();
```
during transformations.
These produce different results every rerun.
Prefer:
```sql
SELECT source_timestamp;
```
from the source data.

---
## 8. Staging → Validation → Publish Pattern
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
Never write directly to production tables.
This prevents partial results from becoming visible.

---
# Real Example
Daily orders pipeline:
```text
Process dt=2026-06-01
```
Bad:
```sql
INSERT INTO fact_orders
SELECT *
FROM staging_orders;
```
Retry:
```text
Duplicates created
```
Good:
```sql
DELETE FROM fact_orders
WHERE dt='2026-06-01';
INSERT INTO fact_orders
SELECT *
FROM staging_orders
WHERE dt='2026-06-01';
```
or
```sql
INSERT OVERWRITE
```
Retry:
```text
Same final result
```
---