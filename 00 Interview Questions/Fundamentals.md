---
domain: Data Engineering
domain_suggested: null
category: Learning
category_suggested: null
source_type: obsidian
status: review
tags: [fundamentals, interview, data-engineering]
---




```table-of-contents
```
## If you could collect only 10 metrics from every batch job, which would you choose and why?

Pick for: cost signal, SLA signal, DQ signal, debuggability, anomaly detection. Order by leverage:

1. `job_id`, `run_id`, `code_sha`, `job_status` — identity + traceability.
2. `input_bytes`, `input_row_count`, `input_file_count` — volume signal; regression detector.
3. `output_bytes`, `output_row_count` — output volume + write success.
4. `partitions_scanned` (count, list) — pruning effectiveness.
5. `runtime_seconds` (per stage) — SLA tracking + anomaly.
6. `shuffle_bytes` — cost driver; skew/cost signal.
7. `cluster_seconds` (or `credits_used`) — cost.
8. `error_count`, `retry_count` — reliability.
9. `max_event_ts` (input freshness) — data lag.
10. `data_quality_check_results` (pass/fail summary) — DQ signal.

Why these: they cover the 4 dimensions interviewers care about — *did it run, did it cost, did it deliver correct data, will it scale.* Anything else (GC, spill, task counts) is debug-only and derivable from logs.

## How would you build an AI system that recommends batch optimizations automatically?
treat it as a **closed-loop optimization platform** rather than a simple recommendation engine.
The goal is:

> Observe → Diagnose → Recommend → Validate → Learn

High level

* **Observe** — collect plan features + runtime metadata for every run (Q37 metrics + plan fingerprint from Q27).
* **Diagnose** — for each run, classify into known anti-patterns: small files, broadcast-exceeded, join-before-filter, skew, missing partition pruning, full scan.
* **Recommend** — for each anti-pattern, generate a fix. Each fix has: estimated savings (cost, runtime), risk score, and a verification plan.
* **Validate** — apply in a sandbox cluster or shadow run. Compare to baseline. Promote only if improvement > threshold and no regressions.
* **Learn** — feed actual outcomes back into the model. Recommendations that didn't help get down-weighted.

Architecture:
* **Detection layer** — rule-based (anti-pattern matchers) + ML (anomaly detection, plan similarity).
* **Recommendation store** — catalog of fixes; each fix is a parameterized template (e.g. "set broadcast threshold to 50MB" parameterized by table size).
* **Sandbox execution** — clone the pipeline, apply fix, run on a sample input, compare.
* **Decision engine** — combines recommendation confidence + risk + estimated savings; decides auto-apply, suggest, or skip.
* **Feedback loop** — actual outcome (did the fix help?) → labeled training data → better models.

Hardest part: trust. Auto-apply only reversible, safe changes. For risky ones, generate a PR and require human review.

## How would you estimate the cost of a batch workload before execution?

Cost estimation, layered by accuracy:

* **Static estimation** — read the pipeline code/SQL; estimate bytes scanned from table stats; estimate compute from past runs of similar jobs. Output: predicted cost with ±30% confidence interval.
* **From plan** — `EXPLAIN` to get `scan_bytes`, `join_count`, `shuffle_bytes`. Compute cost = `f(scan_bytes, shuffle_bytes, runtime_estimate)` calibrated from past runs.
* **Dry-run** — execute on a 1% sample of input; extrapolate cost and runtime. Most accurate; takes time and a small amount of compute.
* **Warehouse pricing models** — Snowflake `QUERY_HISTORY` estimates; BigQuery `bytes_processed` from dry-run queries; Databricks `cost_per_DBU`.
* **Cost formula example (Spark on cloud):**
  `cost = cluster_seconds × instance_price × utilization + storage_gb × storage_price + shuffle_egress_gb × network_price`
* **Pre-flight check** — combine estimate + budget check; abort if predicted cost > X.
* **Anchored to history** — cost model trained on (input_bytes, joins, shuffle) → cost from past runs. New runs predicted by feature similarity.

What this enables: cost-aware scheduling (run cheap jobs at expensive times, expensive jobs at cheap times), budget enforcement, chargeback.

## How would you predict batch job runtime using historical telemetry?
Inputs might include:
```json
{
  "rows_scanned": 500000000,
  "join_count": 4,
  "shuffle_gb": 120,
  "partition_count": 250
}
```

Approaches:

* **Linear / GBM model** — features: `input_bytes`, `output_bytes`, `join_count`, `shuffle_bytes`, `partition_count`, `cluster_size`, code SHA embedding. Target: `runtime_seconds`. Train on last 90 days of runs.
* **Per-job model** — simple ARIMA or Prophet on `runtime` time series for each job. Captures drift, code-change effects.
* **Cluster-based** — group jobs by feature fingerprint; for new job, predict based on peers.
* **Calibrated simulation** — Spark has cost models per operator; calibrate from real runs to predict accurately.

Features that matter most (rule of thumb):
1. `input_bytes` (huge — biggest lever)
2. `shuffle_bytes` (proxy for join/agg work)
3. `join_count` × `join_type` (broadcast is fast, SMJ is expensive)
4. `partition_count` and `partition_size_distribution` (skew detection)
5. `cluster_size` (more executors → faster, with diminishing returns)
6. Code SHA / query template (different SQL = different cost)

Pitfalls:
* Cold start (new job). Use similarity to nearest neighbor.
* Cluster config drift. Normalize to a baseline cluster size before training.
* Code changes break historical patterns. Re-train when SHA changes.
* Input distribution shift. Include input_bytes + skew as features.

Accuracy target: ±20% on p50, ±40% on p95. Use it for SLA risk scoring and capacity planning, not as a guarantee.

## Design a self-tuning batch platform that automatically:
* Detects slow jobs
* Recommends optimizations
* Applies safe optimizations
* Measures improvement

Loop:

* **Detect** — nightly scan of metadata store. Compare each job's recent runs (last 7 vs prior 30). Flag if p50 runtime or cost > X% worse, or if new anti-pattern emerges. Output: ranked list of candidate jobs.
* **Diagnose** — for each candidate, dig into plan, stage metrics, config. Identify the bottleneck (skew, shuffle, small files, broadcast, etc.).
* **Recommend** — match bottleneck to fix template. Each fix: code/config change, expected savings, risk score.
* **Auto-apply (low-risk only)** — for fixes that are reversible and safe (broadcast threshold, partition count, file compaction), apply to a clone of the pipeline, run on a sample input, compare cost/runtime. If improvement > threshold and no regression, promote.
* **Suggest (higher-risk)** — open a PR with the proposed change; require human review; auto-test in CI; merge when approved.
* **Measure** — re-run with new config in production; record new metadata; compare to baseline. Update the model.
* **Learn** — what worked, what didn't? Tune the recommendation confidence thresholds.
* **UX** — weekly digest email; in-IDE warnings; Slack alerts on big wins.

Critical principle: **never auto-apply an irreversible or behavior-changing optimization**. Compaction is safe (atomic, reversible). Schema changes are not. Broadcasting different tables than the planner chose is not.

Refer: [[Idempotency]]

## See Also
- [[Idempotency]] — idempotency deep-dive
- [[Batch Processing]] — batch processing overview
- [[ETL vs ELT]] — ETL vs ELT decision framework
- [[Data Engineering Playbook]] — 15 core truths of data engineering
- [[Incremental Load Strategy]] — incremental loading