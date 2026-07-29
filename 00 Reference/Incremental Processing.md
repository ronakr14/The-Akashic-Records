# AI Summary
None. Expected discussion: `Watermarks, High-water marks, CDC, Timestamp-based extraction, Idempotency`

```table-of-contents
```
## You have a 100 TB table. A full reload takes 15 hours. How would you implement incremental loading?
Expected discussion: `Watermarks, High-water marks, CDC, Timestamp-based extraction, Idempotency`

For a 100 TB table, a full reload every run is impractical — it wastes compute, misses SLAs, and overloads the source. The goal is to read only the changed data, reducing 100 TB to perhaps a few hundred GB.

I would evaluate three approaches, chosen based on source capabilities:

### Approach 1 — Timestamp-Based Extraction (most common)

If the source table has an `updated_at` column, I maintain a **watermark** — a metadata table storing the last successful load timestamp. Each run extracts only rows where `updated_at > watermark`, then merges them into the target.

A **high-water mark** is the highest value seen so far; a **watermark** is the progress tracker for ingestion. In practice they're often the same value, but conceptually: the high-water mark is "what's the max," the watermark is "what have I processed."

**Limitation:** This misses deletes (row gone, no timestamp to find) and in-place updates that don't touch `updated_at`.

### Approach 2 — Incrementing Primary Key

For append-only tables with a sequential PK (e.g., `order_id`), track the last processed ID and extract `WHERE order_id > last_id`. Simpler but cannot handle updates or deletes.

### Approach 3 — Change Data Capture (CDC) — best if available

Instead of querying the table, capture the database transaction log (MySQL Binlog, PostgreSQL WAL, SQL Server CDC). This produces events for inserts, updates, and deletes — solving the delete problem that timestamp-based extraction has.

Tools: Debezium + Kafka. Events flow through a landing zone into staging, then merge into the target.

### Merge Strategy

Data lands in a staging layer, then merges into the target using **MERGE/UPSERT on business key**:

```sql
MERGE INTO sales tgt
USING sales_increment src
ON tgt.order_id = src.order_id
WHEN MATCHED THEN UPDATE SET amount = src.amount
WHEN NOT MATCHED THEN INSERT (...);
```

This prevents duplicates when the same row appears in multiple runs.

### Idempotency

If the job fails halfway, re-running must produce the same final state. I ensure this by:

- MERGE on business key (not raw INSERT) — safe to replay
- Watermark advancement as an **atomic step** with the batch commit — if the batch fails, the watermark doesn't move
- Tracking batch IDs in a metadata table for replay detection and audit
- Designing every step to be re-runnable without side effects

### Failure Modes at 100 TB Scale

- **Late-arriving data** — a record committed before the watermark but with `updated_at` after (backfill, repair). Mitigation: lookback window of 1–2x normal lag, plus dedup on business key during merge.
- **Deletes invisible to timestamp** — solved by CDC, or by adding a soft-delete flag to the source and filtering on it during merge.
- **Clock drift** — source DB and pipeline host clocks diverge. Mitigation: use DB-side commit timestamps rather than host clock; alert on skew.
- **Bulk backdated updates** — same-timestamp bulk changes slip through. Mitigation: periodic full partition scan (weekly) as a safety net.

### Operational Considerations

At 100 TB, incremental loading interacts with partitioning: partition by date or region so only relevant partitions are scanned. The incremental job touches only the current partition plus a lookback. Parallelism comes from partition-level concurrency — e.g., 4 partitions at a time.

**Assumption:** An initial full load has already completed. After that, daily incremental takes over. If a full backfill is ever needed (e.g., new column, corruption), I'd run it on isolated infrastructure with throttling, then swap into production atomically.

---

Refer: [[Incremental Load Strategy]]

---
## What can go wrong with timestamp-based incremental loads?
Look for:
* Clock drift
* Late arriving records
* Timezone issues
* Duplicate processing
* Missing records

Common failure modes and mitigations:
* **Clock drift** — source DB and pipeline host clocks diverge, so a record committed at `T+1s` may be missed. Mitigation: use a DB-side timestamp (`SYS_CHANGE_VERSION`, LSN, commit timestamp) instead of host clock; reconcile with NTP and alert on >N seconds skew.
* **Late arriving records** — record committed before watermark but with `updated_at` after watermark (backfill, repair). Mitigation: lookback window (1–2x normal lag) and dedup on business key during merge.
* **Timezone issues** — source stored UTC, ingest layer interprets as local, watermark misaligns. Mitigation: store everything in UTC end-to-end; never convert at the ingest boundary; assert timezone in schema tests.
* **Duplicate processing** — same row updated twice in source window, or job rerun overlaps. Mitigation: idempotent merge on business key, batch_id tagging, and dedup window (keep latest by source ts).
* **Missing records** — deletes are invisible to timestamp CDC; same-timestamp bulk updates. Mitigation: add soft-delete flag check, or layer CDC/log-based capture on top; for bulk updates, scan the affected partition once per day.
* **Backwards clock adjustments** (DST, VM migration) can produce negative-lag windows. Mitigation: clamp watermark to monotonic clock and force checkpoint replay if anomaly detected.

Refer: [[Incremental Load Strategy]]

---
## Explain how you would backfill one year of historical data without impacting production batch jobs.

Approach: isolate, slice, throttle.

* **Isolate the pipeline** — run on a separate cluster/pool, separate warehouse, separate scheduler. Never share executors or a metastore lock with prod. Tag every run as `backfill=true` so it cannot be promoted to prod by accident.
* **Slice the window** — process year in chunks (week or month), parallelize by partition. Year = 12 monthly runs or 52 weekly runs in parallel up to cluster capacity. Each slice is independent and rerunnable.
* **Throttle resource use** — cap concurrency (e.g. 4 slices at a time), set lower priority/preemptible, schedule off-peak (weekends). Use a separate queue with strict quotas.
* **Write to a separate target** — `table_backfill_yyyy`, then atomic swap or view rewrite to prod table once validated. Avoid hot-partition writes during business hours.
* **Pause or divert prod** — if data is large enough, pause downstream consumers (or switch them to a frozen snapshot) for the duration. Use feature flags on dashboards.
* **Validate before cutover** — row counts, reconciliation vs source, DQ gates, parity check on a sample of aggregates. Only swap the view when parity holds.
* **Cleanup** — drop backfill table or move to cold storage; record lineage so future readers know the data was backfilled, not native.
* **Coordinate with stakeholders** — announce window, define rollback plan, have a kill switch (terminate the backfill pool).

## See Also
- [[Incremental Load Strategy]] — incremental loading patterns
- [[Idempotency]] — making incremental loads safe
- [[Batch Processing]] — batch processing overview
- [[ETL vs ELT]] — choosing the right approach
