---
domain: Data Engineering
domain_suggested: null
category: Learning
category_suggested: null
source_type: obsidian
status: review
tags: [batch-processing, interview, data-engineering]
---




```table-of-contents
```
## A batch pipeline that normally processes 500 GB suddenly receives 20 TB.
What happens?
How would you prevent failures?

What happens (without protection):
* Compute explodes — 40x data, but executor count fixed → tasks per executor balloon, OOM and shuffle spill.
* Shuffle bytes grow proportionally — disk pressure, GC pauses.
* Wall clock blows past SLA.
* Downstream consumers may break (BI tools hitting a 20TB table for the first time, dashboards timeout).
* Cost spike — autoscaler keeps adding executors trying to keep up.

Prevention:
* **Backpressure at ingest** — reject or quarantine inputs above N GB/day; alert on volume anomaly before processing starts.
* **Schema/data contracts** — producer declares expected max volume; consumer rejects anomalies at the boundary.
* **Adaptive sizing** — observe input bytes at step 1, scale executor pool dynamically (Airflow sensors + Kubernetes HPA, or Databricks autoscaling with min/max bounds).
* **Partition-aware parallelism** — set parallelism to `2–3x partition count`, not fixed `200`. 40x data = 40x partitions = need to scale executors accordingly.
* **Pre-flight check** — fast probe (count rows/files/bytes) before launching heavy step; abort or scale if anomalous.
* **Streaming fallback** — if a daily job keeps overflowing, switch that source to micro-batch/streaming (Kafka, Auto Loader) so load is smoothed.
* **Circuit breakers** — if estimated runtime exceeds SLA by 2x, fail fast and notify instead of running 8 hours and missing SLA anyway.
* **Capacity tests** — load-test the pipeline quarterly at 10x expected volume; if it breaks, that's a P0, not a surprise.
* **Cost guardrails** — hard cap on cluster spend per run; kill switch that aborts if $X exceeded.

---
## Your nightly batch SLA is 3 hours.
Business now requires 1 hour.
What architectural changes would you consider?

Layered approach — address each bottleneck independently:

* **Compute scaling**
  * Right-size cluster: from "shared dev cluster" to dedicated, scaled to peak input.
  * Use Photon/Photon-class accelerators on supported engines.
  * Increase parallelism: parallelism = `2–3× partition_count`, not a fixed number.

* **Algorithm / query changes**
  * Rewrite the slowest joins as broadcast joins (if small dim).
  * Pre-aggregate hub tables; reduce downstream fan-out.
  * Salting for known skewed keys.
  * Replace UDFs with built-in functions.

* **Data layout**
  * Z-order/cluster on hot filter columns (data skipping).
  * Compact small files.
  * Partition by frequently filtered date column.
  * Materialize intermediate tables so steps don't recompute each run.

* **Ingest / upstream changes**
  * Switch from full-refresh to incremental / CDC (cut input 10x).
  * Pre-clean at ingest so curated layer is faster.

* **Streaming hybrid**
  * If daily SLA can't be met, move to micro-batch / streaming (latency <1 min, not 1 hr).

* **Caching**
  * Cache hot dimension tables (broadcast).
  * Cache intermediate query results.

* **Parallelism refactor**
  * Split the pipeline into parallel branches by entity (e.g. orders and customers run concurrently).

* **Operational**
  * Pre-warm clusters (avoid cold start).
  * Spot/preemptible for cost; on-demand for speed.
  * SLA risk monitor that triggers scale-up mid-run.

* **Measure, don't guess** — profile first, then invest in the biggest win. Usually: incremental ingest + layout + parallelism = 3x improvement.

---
## You discover that yesterday's batch produced incorrect results.
Downstream dashboards have already consumed the data.
Walk me through your incident response process.

Incident response — five phases:

1. **Detect & declare incident**
   * Whoever noticed (on-call, dashboard user, automated alert) opens an incident.
   * Severity: data correctness typically SEV1 (downstream impact), SEV2 if scoped.
   * Incident commander + comms lead assigned.

2. **Stop the bleed**
   * If today's batch would propagate the bad logic, pause or kill it.
   * If downstream has auto-refresh from bad tables, disable refresh on critical dashboards.
   * Roll back the active version to last-known-good (versioned writes make this possible).
   * Snapshot the bad output for forensics.

3. **Diagnose**
   * Look at run metadata: code SHA, input bytes, configs, recent deploys.
   * Compare bad output to last good output (data diff): which rows are wrong, by how much.
   * Identify root cause: schema drift, bug, bad input, infra.
   * Timeline: when did the bad run happen? When did consumers read it?

4. **Notify & communicate**
   * Status page: "data for [date] is incorrect, reprocess underway."
   * Stakeholder list: dashboard owners, downstream ML teams, execs.
   * ETA for fix.
   * Compliance/legal if PII / financial impact.

5. **Fix & verify**
   * Patch the root cause (code, config, or upstream source).
   * Re-run the affected window.
   * Validate via DQ gates + reconciliation vs source.
   * Promote the corrected version.
   * Re-enable downstream refresh.

6. **Post-mortem**
   * Blameless writeup within 5 business days.
   * Why did DQ gates not catch it? Why did consumers not notice sooner?
   * Action items: add check, add alert, add test, fix root cause upstream.
   * Track to completion.

---
## Design a batch processing framework from scratch.
Requirements:
* Scheduling
* Dependency management
* Retries
* Metadata collection
* Data quality
* Observability
* Cost optimization

Core components:
* **Scheduler** — DAG-based with cron triggers, sensors, event triggers. Time-zone aware. Backfill-aware.
* **Dependency manager** — declare upstream/downstream; topological sort; parallel execution of independent tasks.
* **Retry & recovery** — per-task retry policy (max attempts, exponential backoff); pipeline-level resume from last successful task.
* **Idempotency layer** — every task accepts a `run_id`; writes are versioned; reruns produce the same result.
* **Metadata collector** — emits: job_id, run_id, code SHA, input/output bytes, rows, partitions, runtime per stage, shuffle bytes, GC, spill, cost. Standard format (OpenLineage).
* **DQ framework** — schema, null rate, distribution, freshness, reconciliation checks. Blocking vs warning severity. Quarantine path.
* **Observability** — structured logs, metrics (Prometheus/CloudWatch), traces (OpenTelemetry), lineage (OpenLineage/Marquez).
* **Alerting** — runtime anomalies, SLA risk score, DQ failures, cost anomalies. Pager for production SLA breaches.
* **Cost controls** — per-run budget, kill switch, auto-suspend idle clusters, executor right-sizing, tiered storage policies.
* **UI** — DAG visualization, run history, lineage view, DQ dashboard, cost attribution per team.
* **CLI / SDK** — define pipelines as code (Python/SQL), versioned in git, reviewed via PR.
* **Pluggable compute** — abstracted execution backend (Spark, Flink, Snowflake, BigQuery). One pipeline can mix.
* **Multi-tenancy** — namespace isolation, per-team quotas, RBAC.

Build-vs-buy: most teams should *not* build this from scratch. Buy Airflow/Dagster/Prefect + Great Expectations/Soda + OpenLineage/Marquez + a FinOps tool. Build only the integration glue and your own DQ contracts library.

## See Also
- [[Batch Processing]] — batch processing overview
- [[Failure Recovery]] — failure recovery strategies
- [[Idempotency]] — idempotency patterns
- [[Data Quality]] — data quality in pipelines