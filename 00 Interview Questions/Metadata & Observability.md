---
type: question
---

```table-of-contents
```
## What metadata would you collect from every batch job?
Possible answer:
```json
{
  "job_id": "",
  "runtime_sec": 0,
  "records_read": 0,
  "records_written": 0,
  "partitions_scanned": [],
  "bytes_processed": 0,
  "error_count": 0
}
```
---
## How would you identify inefficient batch jobs automatically?

Detector design — run nightly over the metadata store:
* **Compare each job to itself** — last 30 days runtime trend. Flag jobs whose p50 runtime increased >X% week-over-week, or whose variance grew.
* **Compare each job to its peers** — same engine, similar data volume, similar join count. Flag the worst-performer.
* **Cost-per-output** — `cost / rows_written`. Outliers are candidates.
* **Scanned-to-written ratio** — high ratio means over-scan; investigate pruning, pushdown.
* **Shuffle-per-input ratio** — high shuffle = suboptimal joins or pre-aggregation missing.
* **Retry rate** — jobs that retry >N times are likely inefficient or fragile.
* **Memory-per-byte** — high executor memory, low throughput = memory pressure or skew.
* **Files-per-partition** — small-file problem, drives planning time up.
* **Schedule drift** — runtime creeping toward SLA; flag before breach.
* **Use ML** — anomaly detection on (job_id, runtime, bytes_processed, cost) over time.

Output: ranked list of "top 10 inefficient jobs this week" with suggested levers. Pair with auto-remediation playbook (repartition, broadcast, file compaction) where safe.

---
## What telemetry signals would help predict SLA violations before they happen?

Predict before breach (lead time matters):
* **Input volume vs historical** — if today's input bytes are 1.5x the 30-day p95 at the halfway mark of the job, runtime will likely exceed SLA. Compute ETA = `(runtime_so_far / input_so_far) × expected_total_input`.
* **Task progress vs schedule** — Spark stage completion rate. If after 30 minutes we're at 10% (vs expected 40%), SLA breach likely.
* **Skew signals** — p95 task time > 5x median, or single task stage taking >70% of stage wall time.
* **Shuffle spill** — early signs of memory pressure; failure likely mid-run.
* **GC time growing** — heap pressure; OOM may follow.
* **Cluster utilization** — autoscaler lagging behind required executors; queue depth growing.
* **Source freshness** — if upstream SLA is already missed, downstream will miss too. Cascade forecast.
* **External dependencies** — database lock waits, API rate-limit responses, queue backlog.
* **Resource contention** — neighboring jobs on the same cluster taking capacity.

Emit a **SLA risk score** every 5 minutes during the run; if score > threshold, alert ops *during* the run, not after it finishes. Enable intervention: scale up, kill and restart with bigger cluster, drop partition.

---
## Design a metadata-driven batch optimization platform.
This is a Staff-level question.

Goal: turn every batch run into structured metadata, then drive optimization recommendations automatically.

Architecture:
* **Ingestion** — every job emits run metadata: inputs (bytes, rows, files, partitions), code SHA, cluster config, runtime per stage, shuffle bytes, GC, spill, cost, error counts. Standardize on OpenLineage events.
* **Storage** — time-series metadata store (for trends) + columnar warehouse (for ad-hoc analysis). Marquez + a parquet layer or BigQuery.
* **Catalog** — joins metadata with the data catalog (table → owner → criticality) and code repo (job → git SHA → author).
* **Anomaly & trend detection** — for each job, statistical model of expected runtime, bytes, cost. Flag deviations.
* **Pattern recognition** — cluster jobs by features (join count, shuffle ratio, file count). Identify which jobs look like a known anti-pattern (e.g. "small files," "broadcast exceeded," "high skew").
* **Recommendation engine** — for each detected anti-pattern, generate a fix: repartition, broadcast hint, increase parallelism, compact files, change file format. Each recommendation has a confidence score and an estimated savings.
* **Auto-remediation** — for safe, reversible changes (e.g. file compaction, broadcast threshold), apply automatically in a sandbox, measure, promote.
* **Closed loop** — re-run with change; compare new metadata; learn which recommendations actually improved cost/runtime. ML feedback loop.
* **UX** — weekly digest, in-IDE warnings, PR comments ("this PR will increase runtime by ~12%").

Why it's a Staff question: requires combining metadata, ML, catalog, and runtime control — the full data platform surface.