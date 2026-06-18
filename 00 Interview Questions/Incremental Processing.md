```table-of-contents
```
## You have a 100 TB table.
A full reload takes 15 hours. How would you implement incremental loading?
Expected discussion: `Watermarks, High-water marks, CDC, Timestamp-based extraction, Idempotency`

For a 100 TB table, I would avoid full reloads and implement incremental loading. My preferred approach would be timestamp-based extraction using an `updated_at` column and a metadata table storing the last successful watermark or high-water mark. Each run would extract only records modified since the previous successful load. If the source system supports CDC, I would use transaction log-based capture to detect inserts, updates, and deletes efficiently. Data would be loaded into a staging area and merged into the target using UPSERT/MERGE operations. To ensure idempotency, I would track batch IDs, maintain checkpoints, and design the pipeline so that rerunning the same batch produces the same final state without duplicates. For late-arriving data, I would use a small lookback window and deduplication logic during the merge process. This reduces processing from 100 TB to only the changed data while maintaining correctness and recoverability.

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