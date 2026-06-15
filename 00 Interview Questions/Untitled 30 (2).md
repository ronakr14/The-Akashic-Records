## 5. What can go wrong with timestamp-based incremental loads?
Look for:
* Clock drift
* Late arriving records
* Timezone issues
* Duplicate processing
* Missing records
This is one of those questions where many candidates answer:

> "Use `updated_at > last_watermark`"

and stop there.

The interviewer is usually looking for whether you understand the **edge cases that can silently corrupt data**.

---

# Basic Incremental Load

Most people start with:

```sql
SELECT *
FROM orders
WHERE updated_at > :last_watermark
```

Example:

```text
Last Watermark:
2026-06-04 10:00:00
```

Load records newer than that timestamp.

Looks simple.

Unfortunately, many things can go wrong.

---

# 1. Late Arriving Records

## Scenario

```text
Order Created:
10:05

Network Delay:
20 minutes

Arrives:
10:25
```

But watermark has already advanced to:

```text
10:20
```

Next extraction:

```sql
WHERE updated_at > '10:20'
```

The 10:05 record is permanently missed.

---

## Solution

Use a lookback window:

```sql
WHERE updated_at >
      watermark - INTERVAL '1 HOUR'
```

Example:

```text
Watermark = 10:20

Query from:
09:20 onwards
```

Then deduplicate during merge.

This is one of the most common production fixes.

---

# 2. Clock Drift

Distributed systems rarely have perfectly synchronized clocks.

---

## Scenario

Application Server A:

```text
10:00:00
```

Database Server:

```text
09:59:30
```

Difference:

```text
30 seconds
```

A record may appear "older" than the stored watermark.

---

## Result

```text
Record skipped
```

even though it is new.

---

## Solution

Use:

- Database-generated timestamps
    
- CDC log positions
    
- Transaction IDs
    

instead of application timestamps.

CDC is usually safer because log sequence numbers are ordered.

---

# 3. Timezone Issues

Extremely common.

---

## Scenario

Source:

```text
UTC
```

Pipeline:

```text
IST
```

Target:

```text
UTC
```

Watermark:

```text
2026-06-04 10:00:00
```

Question:

```text
10:00 in which timezone?
```

If that isn't explicit, you'll either:

- miss data
    
- duplicate data
    

---

## Daylight Saving Problems

Example:

```text
01:30 AM
```

can occur twice during DST transitions.

Now:

```sql
updated_at > '01:30'
```

becomes ambiguous.

---

## Solution

Store everything in:

```text
UTC
```

and use timezone-aware timestamps.

---

# 4. Duplicate Processing

A very common side effect of lookback windows.

---

## Example

Run 1:

```text
Load:
10:00 → 11:00
```

Run 2:

```text
Load:
10:50 → 12:00
```

Records between:

```text
10:50 → 11:00
```

appear twice.

---

## Solution

Use idempotent loading.

Example:

```sql
MERGE INTO target
USING staging
```

instead of:

```sql
INSERT INTO target
```

Use:

- Primary keys
    
- Business keys
    
- Deduplication logic
    

---

# 5. Missing Records Due to Boundary Conditions

One of the nastiest bugs.

---

## Scenario

Watermark:

```text
10:00:00
```

Record timestamp:

```text
10:00:00
```

Query:

```sql
WHERE updated_at > '10:00:00'
```

Record never loads.

---

## Alternative

```sql
WHERE updated_at >= '10:00:00'
```

Now you may get duplicates.

---

## Solution

Use composite watermarks.

Example:

```text
(updated_at, order_id)
```

instead of timestamp alone.

---

# 6. Timestamp Precision Differences

Source system:

```text
2026-06-04 10:00:00.123456
```

Target metadata:

```text
2026-06-04 10:00:00
```

Milliseconds are lost.

---

## Result

Records may:

- be skipped
    
- be duplicated
    

depending on comparison logic.

---

## Solution

Store full precision.

Never truncate watermark values.

---

# 7. Source Updates Without Timestamp Updates

A surprisingly common application bug.

---

## Scenario

Developer updates:

```text
customer_name
```

but forgets to update:

```text
updated_at
```

Incremental extraction never sees the change.

---

## Result

Target data becomes stale.

---

## Solution

Prefer:

- CDC
    
- Database triggers
    
- Change tracking features
    

over relying solely on application-maintained timestamps.

---

# 8. Deleted Records

Timestamp extraction only sees rows that exist.

---

## Scenario

```text
Order 100 deleted
```

Source table:

```text
Row disappears
```

Incremental query:

```sql
WHERE updated_at > watermark
```

cannot detect the deletion.

---

## Result

Target still contains the record.

---

## Solution

Use CDC.

CDC emits:

```text
DELETE event
```

which can be propagated downstream.

---

# 9. Watermark Updated Too Early

Classic operational bug.

---

## Scenario

```text
Read Data
Update Watermark
Job Fails
```

Now:

```text
Data not loaded
Watermark advanced
```

Next run skips those records forever.

---

## Solution

Advance watermark only after:

```text
Extraction Complete
Validation Passed
Load Successful
Commit Successful
```

---

# 10. Out-of-Order Events

Especially common with distributed systems.

---

## Scenario

Records arrive:

```text
10:05
10:10
10:03
```

because of retries or queue delays.

Simple timestamp logic assumes ordered arrival.

---

## Result

Older events may be skipped.

---

## Solution

- Lookback windows
    
- Event-time processing
    
- CDC sequence numbers
    
- Transaction log offsets
    

---

# What Senior Engineers Usually Prefer

For large-scale production systems:

### Good

```text
updated_at watermark
```

### Better

```text
(updated_at + business key)
```

### Best

```text
CDC
(Log Sequence Number / WAL Offset / Binlog Position)
```

Because CDC naturally handles:

- Inserts
    
- Updates
    
- Deletes
    
- Ordering
    
- Recovery
    
- Idempotency
    

---

# Interview Summary Answer

> Timestamp-based incremental loads are simple but can fail in several ways. Common issues include late-arriving records that fall behind the watermark, clock drift between systems, timezone and daylight-saving inconsistencies, duplicate processing caused by lookback windows, and missing records due to boundary conditions or timestamp precision loss. Additional risks include source systems not updating the timestamp correctly, inability to detect deletes, premature watermark advancement, and out-of-order event arrival. To mitigate these issues, I would store timestamps in UTC, use lookback windows with idempotent MERGE operations, maintain composite high-water marks when necessary, update watermarks only after successful commits, and prefer CDC-based extraction for mission-critical pipelines because it provides ordered, reliable change tracking for inserts, updates, and deletes.