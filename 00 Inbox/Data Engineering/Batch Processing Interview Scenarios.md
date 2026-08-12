---
domain: data-engineering
subdomain: interview
note_type: interview
source_type: self
status: evergreen
level: advanced
tags:
  - system-design
---
# AI Summary
Collection of advanced batch processing interview scenarios covering production-scale architecture, performance optimization, failure recovery, incident response, and platform design. Topics include handling unexpected data volume spikes, reducing SLA from three hours to one hour, managing incorrect batch outputs through structured incident response, and designing a complete batch processing framework with scheduling, retries, metadata, data quality, observability, cost optimization, and multi-tenancy. The note emphasizes architectural reasoning, operational trade-offs, and production best practices expected in senior data engineering interviews.

---
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
- [[Failure Recovery in Batch Data Pipelines]] — failure recovery strategies
- [[Idempotency in Data Pipelines]] — idempotency patterns
- [[Data Quality in Batch Pipelines]] — data quality in pipelines

## What is a data contract and how does it apply to batch pipelines?
A data contract is an agreement between producer and consumer on schema, semantics, SLAs, and ownership — written, versioned, enforced at the ingest boundary (not after the fact).
* **Schema** — column names, types, nullability, allowed values.
* **Semantics** — definition of `revenue`, granularity of `order_id`, partition semantics.
* **SLA** — max lag, max volume, max null rate. Producer owns; consumer can break the contract by changing query semantics.
* **Ownership** — named team accountable for changes.
* **Enforcement** — schema registry (Protobuf/Avro) + automated validation in the ingest job. Breaking changes require versioned migration.
* **Why it matters for batch** — eliminates the "silent schema drift at 3am" class of incidents. Turns tribal knowledge into a CI-enforced artifact.
* **Tools** — DataHub, Great Expectations, Protobuf Schema Registry, Open Data Contract Standard (ODCS).

## How would you attribute batch pipeline cost to teams, products, or business units?
FinOps for data. Every pipeline run emits cost metadata, rolled up by ownership tag.
* **Tag at submission** — `team`, `product`, `cost_center`, `pipeline_owner`, `env`. Tags flow through orchestrator → cluster → warehouse query history.
* **Compute cost** — `cluster_seconds × instance_price × utilization` for Spark/Flink; `credits_used × credit_price` for Snowflake/BigQuery; `DPU-seconds` for Databricks.
* **Storage cost** — bytes stored per layer (raw/curated/sandbox), tagged by producer team.
* **Roll-up dashboard** — daily/weekly spend per team; anomaly alerts on >X% deviation.
* **Chargeback / showback** — bill owners; budget enforcement at pipeline level (kill if team exceeds monthly budget).
* **Per-row cost** — `cost / rows_written` = unit economics; identify pipelines that are expensive per record (likely candidates for optimization or deletion).
* **Tooling** — CloudZero, Vantage, Apptio for cloud FinOps; DataHub + dbt for lineage-driven cost attribution.

## What testing strategies are essential for batch pipelines?
* **Unit tests** — transformation logic on fixture data; mocked sources.
* **Schema tests** — every output table has expected schema; dbt's `not_null`, `unique`, `accepted_values`.
* **Data tests** — value distributions, referential integrity, freshness, volume. Great Expectations, Soda Core, dbt tests.
* **Contract tests** — producer schema matches consumer expectations (DataHub, Schema Registry).
* **Data diff tests** — compare today's output vs yesterday's, on key metrics (count, sum, hash of sample). Catches silent regressions even when tests pass.
* **Replay tests** — re-run pipeline against historical inputs; assert output matches a frozen golden dataset.
* **SLA tests** — pipeline completes within time budget on a representative input.
* **Failure tests** — inject failures (bad rows, missing partitions, slow sources); assert pipeline fails gracefully, doesn't corrupt downstream.
* **End-to-end** — small synthetic dataset traverses the entire pipeline; verify final output.
* **CI/CD** — tests run on PR; a SQL change that breaks a test blocks merge.

Refer: [[Data Quality in Batch Pipelines]]

## How would you handle PII and sensitive data in a batch pipeline?
* **Classify at ingest** — tag columns as `public | internal | confidential | restricted | pii | phi` using automated scanners (BigQuery DLP, AWS Macie, Presidio).
* **Mask early** — apply masking/tokenization in the staging layer, not the curated layer. Once PII lands in curated tables, auditability gets hard.
* **Tokenization** — replace PII with a token; store real values in a separate, access-controlled vault. Joins still work.
* **Deterministic hashing** — for join keys, use HMAC with a rotating salt. Reversible only by the vault service.
* **Row/column-level security** — engine-native (BigQuery row access policies, Snowflake row access policies, Iceberg hidden partitions) so downstream consumers never see unauthorized rows.
* **Access logging** — every PII column read goes to an audit log; alert on bulk reads.
* **Retention** — auto-delete raw PII after N days; keep aggregates longer.
* **Compliance** — GDPR right-to-erasure requires pipeline to reprocess affected partition; design partitions to be rewritable per-subject.
* **Interview framing** — show you understand that "security" isn't just encryption at rest; it's classification → masking → access control → audit.

## Explain data lineage and how you'd implement it for a batch platform.
Lineage = graph of where data came from, what transformed it, and where it went.
* **Two kinds:**
  * **Technical lineage** — table-to-table, column-level. Parsed from query logs, dbt manifests, Spark plans.
  * **Business lineage** — dataset → dashboard → business decision. Owned by data steward.
* **Capture at execution time**, not declaratively — actual lineage reflects what ran, not what was intended.
* **OpenLineage + Marquez** — open standard; Spark/Dbt/Airflow emit events; Marquez stores the graph. Avoid vendor lock-in.
* **Use cases:**
  * Impact analysis — "what breaks if I change this column?"
  * Root cause — "which upstream source caused the bad number?"
  * Compliance — "where did this PII flow?"
  * Cost attribution — "which downstream dashboards depend on this expensive pipeline?"
* **Failure modes** — declared lineage that drifts from reality; missing column-level granularity; lineage for legacy jobs you can't instrument.
Refer: 

## Compare modern orchestrators: Airflow vs Dagster vs Prefect vs Spark declarative.
| Dimension | Airflow | Dagster | Prefect | Spark Declarative |
|---|---|---|---|---|
| Model | DAG of tasks | Asset/data-centric | Task-centric, dynamic | Pipeline-of-pipelines (DLT) |
| Sweet spot | Mature, ops-heavy teams | Data + ML teams | Python-first, quick start | ETL on Databricks |
| Lineage | Plugin (OpenLineage) | First-class asset graph | Limited | First-class |
| Testing | Workable, slow | First-class (asset checks) | First-class | Built-in expectations |
| Backfills | Manual or plugin | First-class partition backfills | First-class | First-class |
| Dynamic | Limited | Strong (sensor assets) | Strong (subflows) | Limited |
| Footprint | Heavy (scheduler + workers) | Lighter | Lightest | Spark-bound |
| Interview angle | "Mature, but lineage/backfills need work" | "Asset model matches how data teams think" | "Fastest to ship" | "Best if you're already on Databricks" |

Choice depends on team maturity and whether you think in tasks or assets.

## What FinOps levers are unique to batch workloads?
* **Right-sizing executors** — pick executor count from telemetry, not over-provisioning.
* **Spot/preemptible for non-urgent** — ETL workloads can tolerate preemption; ML training usually can't.
* **Auto-suspend / auto-terminate** — dev clusters off at night; warehouses auto-suspend after 5min idle.
* **Tiered storage** — hot data on standard, warm on infrequent access, cold on Glacier/Archive. Most lakehouses are 80% cold.
* **Photonic / Photon accelerators** — engine-level speedup = direct cost cut for the same workload.
* **Result caching** — repeated queries hit cache. BigQuery/Snowflake handle this; Spark needs manual broadcast caching.
* **Cluster sharing** — pool multiple small jobs on one long-lived cluster instead of cold-starting per job.
* **Schedule shift** — move batch to off-peak for spot discount or region with cheaper compute.
* **Delete unused** — tables no one queried in 90 days → archive or drop. Most orgs find 30–50% of storage is orphaned.
* **Tag everything** — untagged cost is untrackable cost.

## How do you design a batch pipeline to support safe rollbacks?
* **Versioned writes** — every output to `/table/dt=YYYY-MM-DD/v=run_id/`. Old versions remain queryable.
* **View/table swap, not overwrite** — atomically point a view at the latest version; never overwrite the active partition in place.
* **Code + config versioning** — every run records the git SHA of pipeline code and config; roll back means re-running with old code.
* **Data diff at promotion** — promote a new version only after automated comparison vs current.
* **Read-side compatibility** — consumers query a versioned view, never the raw path; they tolerate version flips.
* **Rollback playbook** — documented: detect → freeze downstream → swap to last-good version → notify → root-cause.
* **Blue/green for big releases** — write new version in parallel; switch view only after validation.
* **Why most teams fail** — they overwrite partitions in place; once bad data is in, rollback = rerun everything.

## See Also
- [[Batch Processing]] — batch processing overview
- [[Stream Processing]] — when streaming beats batch
- [[Idempotency in Data Pipelines]] — making pipelines retry-safe
- [[Incremental Data Loading Strategies]] — incremental loading patterns
- [[Data Modelling]] — data modelling principles