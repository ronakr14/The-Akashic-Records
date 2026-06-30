---
domain: Data Engineering
domain_suggested: null
category: Learning
category_suggested: null
source_type: obsidian
status: review
tags: [python, interview, data-engineering, senior]
---




## Python depth (HIGH)

JD's #1 requirement — "expert-level Python for data engineering." Resume shows Python usage but not Python engineering depth. Expect questions on memory management, concurrency, and design patterns beyond scripting.

### Q1 — Hard · JD: Expert Python

**How do you handle memory-efficient processing of large datasets in Python when the data doesn't fit in memory?**

Core principle: avoid materialising full dataset in memory — process in streams or chunks.

- File-based: generators. Use `pd.read_csv(path, chunksize=50_000)` — iterator of DataFrames. Process one chunk, write result, load next. Peak memory bounded to one chunk.
- Custom generator pipelines: lazy evaluation — nothing materialises until terminal `load()` pulls from chain.

```python
def extract_records(filepath):
    with open(filepath) as f:
        for line in f:
            yield json.loads(line)

def transform(records):
    for rec in records:
        if rec.get("status") == "active":
            yield {"id": rec["id"], "value": rec["amount"] * 1.1}

def load(records, conn):
    batch = []
    for rec in records:
        batch.append(rec)
        if len(batch) >= 1000:
            conn.executemany(INSERT_SQL, batch)
            batch.clear()
    if batch:
        conn.executemany(INSERT_SQL, batch)
```

- Pandas: downcast dtypes aggressively — `int64 → int32/int16`, `float64 → float32`. Low-cardinality columns → `pd.Categorical` (10–50x memory reduction).
- When chunking isn't enough: push processing into DB or Spark. Python shouldn't be the processing layer for truly large-scale data.

**Coaching note:** Generator pipeline code is the centrepiece — practice writing fluently. Close with escalation principle: Python for medium scale, push to Spark for large scale.

---

### Q2 — Hard · JD: Expert Python

**What's the difference between multiprocessing, multithreading, and asyncio in Python? When would you use each in a data pipeline?**

Distinction comes down to the GIL and the nature of the bottleneck.

- **Threading** — OS threads, GIL allows one thread to execute Python bytecode at a time. Useful for I/O-bound tasks (network, DB, file). Use for parallel HTTP calls, parallel S3 reads.
- **Multiprocessing** — separate processes, own GIL + memory space. Right tool for CPU-bound work (transformation, serialisation). Use `multiprocessing.Pool` for parallelising per-partition transforms.
- **Asyncio** — single-threaded cooperative concurrency, coroutines yield via `await`. Most efficient for very high concurrency I/O (thousands of in-flight requests). Use for many concurrent API calls (e.g., enriching 500k records, 500 in-flight from one thread).

**Real example — healthcare ETL:**
- `asyncio` → concurrent NDC code validation against external drug reference API.
- Multiprocessing → CPU-heavy DEID tokenisation, 500k patient records.
- Plain threading → parallel S3 file uploads at pipeline close.

Each tool matched to its bottleneck type.

**Coaching note:** Closing with real examples converts textbook answer into experienced engineer's answer.

---

### Q3 — Medium · JD: Expert Python

**How do you design Python data pipeline code for testability? What patterns do you use?**

Testability starts with separating concerns — I/O, transformation, orchestration as distinct layers.

Core principle: transformation logic = pure functions (data in, data out, no side effects). Reading S3 + transforming + writing Snowflake in one block is untestable without mocking infrastructure. Split into `read()`, `transform()`, `write()` → unit-test `transform()` on local DataFrame with no cloud dependencies.

```python
def transform_pharmacy_records(df: pd.DataFrame) -> pd.DataFrame:
    """Pure function — no I/O, deterministic, unit testable."""
    df = df.copy()
    df["ndc_code"] = df["ndc_code"].str.strip().str.upper()
    df["sales_amount"] = pd.to_numeric(df["sales_amount"], errors="coerce")
    df = df.dropna(subset=["patient_id", "ndc_code"])
    return df
```

I/O layers: dependency injection via `Protocol` interfaces. Tests inject fakes.

```python
class DataReader(Protocol):
    def read(self, path: str) -> pd.DataFrame: ...

def run_pipeline(reader: DataReader, writer: DataWriter, path: str):
    df = reader.read(path)
    df = transform_pharmacy_records(df)
    writer.write(df)
```

Test pyramid: 70% unit (pure transforms), 20% integration (local Spark / SQLite), 10% e2e (dev env). Heavy unit base keeps CI fast — typically under 3 min.

**Coaching note:** Protocol-based DI signals Python engineering maturity. Many data engineers know testing in principle but haven't applied structural patterns like this.

---

### Q4 — Medium · JD: Expert Python

**What Python performance profiling tools do you use, and how have you diagnosed and fixed a real performance bottleneck?**

Profiling stack by problem type:

- **CPU-bound:** `cProfile` for full call graph → `line_profiler` for line-by-line on hot function.

```bash
python -m cProfile -o profile.out pipeline.py
snakeviz profile.out  # visual flame chart
```

Real example: DEID tokenisation taking 8 min for 500k records. cProfile → 90% time in hash function. `line_profiler` → `hashlib.sha256().hexdigest()` called per record in Python loop. Fix: vectorise via Pandas apply, batched approach, pre-compile HMAC key outside loop. Runtime dropped to 40 s.

- **Memory:** `memory_profiler`, `tracemalloc`. Decorate with `@profile` for per-line memory delta. Found schema validation keeping 3 copies of full DataFrame simultaneously during merge (original + validation copy + merged result). Restructured to validate in-place, release intermediates → peak memory cut by 60%.

- **I/O:** `time.perf_counter()` around I/O calls. If 80% runtime in one DB read, fix is at query/connection level, not Python.

Principle: don't optimise without measuring. Profile first, optimise actual bottleneck, measure improvement.

**Coaching note:** "Profile first, don't guess" closing principle is senior-level signal. Interviewers respect engineers who resist premature optimisation.

---

## PySpark (HIGH)

JD lists PySpark as core requirement. Resume mentions but doesn't showcase depth. Expect internals questions — not just "have you used it" but "how does it work and what did you tune."

### Q1 — Hard · JD: PySpark

**Explain the Spark execution model — what is a job, stage, task? How does understanding this help optimise pipelines?**

Three levels: jobs, stages, tasks.

- **Job** — triggered by action (`collect()`, `write()`, `count()`). Everything before action is lazy transformation DAG. Action compiles DAG into a job.
- **Stage** — unit of work that can execute without shuffle. Job DAG broken at shuffle boundaries (joins, `groupBy`, `repartition`). Within stage, operations pipelined on each partition, no network I/O.
- **Task** — smallest unit, one task = one partition in one stage. Stage with 200 partitions → 200 tasks across executors.

**Optimisation leverage:**

- **Shuffle is expensive.** Every stage boundary writes shuffle files to disk + reads across network. Minimising shuffles = highest leverage. Broadcast joins eliminate shuffle for small tables:

```python
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", 50 * 1024 * 1024)
```

- **Partition count affects parallelism.** Too few = underutilised executors. Too many = scheduling overhead. Target 2–4 tasks per CPU core. Check `df.rdd.getNumPartitions()`, adjust with `repartition()` / `coalesce()`.

- **Data skew is the hardest problem.** Detect from Spark UI — one stage task taking 10 min while others take 30 s. Fix: salting — random prefix on skewed join key.

**Healthcare ETL example:** Pharmacy transaction table had severe skew by `pharmacy_id` — handful of large chains = 40% of records. Salting that join reduced long-tail stage time from 25 min → 4 min.

**Coaching note:** Pharmacy skew example grounds theory. Always close Spark internals answers with real production impact number.

---

### Q2 — Hard · JD: PySpark

**What's the difference between narrow and wide transformations? Why does it matter?**

- **Narrow** — operate on single partition, output depends only on one input partition. No data moves between executors. Examples: `map()`, `filter()`, `select()`, `withColumn()`. Cheap, pipelined within stage.
- **Wide** — require data from multiple input partitions, shuffle required. Examples: `groupBy()`, `join()`, `repartition()`, `distinct()`, `orderBy()`. Create stage boundaries, disk + network I/O.

**Practice implications:**

- **Pipeline optimisation:** push filters + selects before wide transformations. Filter 80% before `groupBy` = move far less data. Catalyst does some predicate pushdown automatically, but verify with `df.explain(extended=True)`.
- **Caching strategy:** cache output of expensive wide transformation if consumed multiple times. `df.cache()` before second use avoids re-executing shuffle. Always `unpersist()` when done — Spark memory management isn't aggressive about eviction.

**Healthcare example:** Three successive wide transformations on 500M-row table, no caching. Added `df.checkpoint()` after first two (writes to S3, breaks DAG lineage). Recovery time on failures dropped from recomputing 3 shuffles → 1.

**Coaching note:** Mentioning `df.explain()` and Spark UI shows you actually debug Spark. Separator between "used PySpark" and "owns PySpark."

---

### Q3 — Medium · JD: PySpark

**When would you use Pandas UDFs over regular PySpark transformations, and what are the performance implications?**

Pandas UDFs are right tool when you need Python/Pandas logic not expressible in native Spark SQL — custom statistical models, complex string processing, Python libraries without Spark equivalent.

**Three types:**
- **SCALAR** — Pandas Series in, Series out. One-to-one row transformation.
- **GROUPED_MAP** — partition as DataFrame in, DataFrame out. Per-group ops (per-pharmacy seasonality adjustments).
- **GROUPED_AGG** — grouped data in, scalar out. Custom aggregations.

**Performance trade-off vs native:** native Spark SQL functions execute in JVM using Catalyst-optimised codegen. Pandas UDFs require serialising data JVM → Python via Apache Arrow, execute in Python, serialise back. Arrow-based much faster than row-by-row pickle, but overhead remains.

**Rule of thumb:** if native Spark can do it, use it. `date_format()`, `regexp_replace()`, `when()/otherwise()` — all JVM-side. Reach for Pandas UDFs only when you genuinely need Python logic.

**Real example:** Pandas GROUPED_MAP UDF for NER-based PHI detection. Each partition of clinical notes processed as DataFrame through spaCy NER model. Vectorised UDF processed 10k records per Arrow batch vs 1 at a time — ~8x faster.

**Gotcha:** Pandas UDFs require explicit return schema declarations. Wrong schema → runtime failure (not compile time). Always test on small sample before full dataset.

**Coaching note:** NER processing use case shows you reached for Pandas UDFs for right reason (Python library dependency), not because you didn't know native API.

---

## Azure (MED)

JD lists Azure as mandatory. Resume shows ADF usage but JD wants Azure-native architecture thinking — Data Lake design, Delta Lake, cloud-native pipeline patterns across full stack.

### Q1 — Hard · JD: Azure mandatory

**Design an Azure-native data platform for ingesting, processing, and serving large-scale structured and semi-structured data.**

Structure around three zones (ingestion, processing, serving) with governance as vertical, not layer.

**Ingestion:**
- Azure Event Hubs → real-time streaming sources (CDC, clickstream) feeding ADLS Gen2.
- Azure Data Factory → batch sources (databases, SaaS APIs, file drops), orchestration + native connectors.
- ADLS Gen2 = raw landing zone, partitioned by source + date. Raw zone immutable — append-only, never modified after landing.

**Processing:**
- Azure Databricks with PySpark for heavy transformation. Sits on ADLS Gen2, writes Delta Lake tables.
- Delta gives ACID transactions on data lake — critical for late-arriving data + backfill.
- Medallion architecture: raw ADLS → bronze Delta → silver Delta → gold Delta.
- ADF orchestrates Databricks jobs for scheduling, dependencies, retries.

**Serving:**
- Azure Synapse Dedicated SQL Pool — structured analytical, high-concurrency BI.
- Synapse Serverless — ad-hoc exploration without provisioning.
- ML feature serving → direct Delta table access from Databricks.

**Governance (vertical):**
- Azure Purview — catalogue + lineage.
- Key Vault — secrets.
- Azure AD — identity-based access control.
- Azure Monitor + Log Analytics — pipeline observability.

**Databricks vs Synapse split:** Databricks for complex PySpark + ML; Synapse for SQL-centric serving + BI integration. They interoperate via shared ADLS storage — not either/or.

**Coaching note:** "Governance is a vertical, not a layer" lands well with senior interviewers. Databricks + Synapse coexistence shows Azure ecosystem maturity.

---

### Q2 — Medium · JD: Azure mandatory

**How does ADLS Gen2 differ from Blob Storage, and how does that affect your data lake design?**

ADLS Gen2 built on Blob Storage but adds hierarchical namespace — true directory structure with atomic rename + delete at directory level. Critical difference for data lake workloads.

- **Flat Blob Storage:** "directory" = naming convention. Renaming/deleting = list all objects with prefix + operate on each. Partition with 50k files → rename = 50k API calls, slow + non-atomic. Partial failure = corrupted downstream reads.
- **ADLS Gen2 hierarchical namespace:** directory rename atomic + O(1) — metadata operation completes in one step regardless of file count. This is what makes Databricks Delta Lake commits performant on Azure — Delta's transaction protocol does atomic directory renames to swap in new data.

**Data lake design implications:**
- Partition by query dimensions — typically date, source, entity type.
- Use atomic rename guarantee for staging patterns — write to temp dir, validate, rename to production atomically. Gives idempotent loads without complex file-level bookkeeping.
- ADLS Gen2 also adds POSIX-style ACLs at directory + file level (Blob Storage doesn't natively). Enables fine-grained access control — analytics team read `/gold/`, no access to `/raw/`. Critical for HIPAA-adjacent workloads.

**Practical rule:** always use ADLS Gen2, never plain Blob Storage, for a data lake. Hierarchical namespace + ACL support non-optional for production workloads.

**Coaching note:** Most candidates know ADLS Gen2 is "better" but can't explain why. Atomic rename tied to Delta Lake commits is concrete differentiator.

---

## SQL & DB design (MED)

JD calls out advanced SQL + database performance tuning explicitly. Resume shows strong SQL but expect indexing strategy, query plan analysis, data modelling beyond what's been covered.

### Q1 — Hard · JD: SQL tuning

**How do you approach indexing strategy for a heavily queried PostgreSQL table?**

Indexing strategy starts with understanding query patterns — `WHERE`, `JOIN`, `ORDER BY` columns in most frequent + expensive queries. Source: `pg_stat_statements` (query frequency + total execution time).

- **B-tree indexes** — default, cover equality + range (`patient_id = X`, `transaction_date BETWEEN x AND y`). Primary lookup key always has B-tree. Question: which additional columns to index.
- **Composite indexes** — queries consistently filtering on `(pharmacy_id, transaction_date)` → composite index far more efficient than two separate. Order matters — leading column for equality, trailing for range. Index on `(pharmacy_id, transaction_date)` supports `WHERE pharmacy_id = X AND transaction_date > Y` but won't help query filtering only on `transaction_date`.
- **Partial indexes** — queries consistently filter subset (`WHERE status = 'ACTIVE'`) → partial index covers only those rows:

```sql
CREATE INDEX idx_active_transactions
ON pharmacy_transactions(patient_id)
WHERE status = 'ACTIVE';
```

Smaller, faster to maintain, fits in cache better than full-table index.

**Watch for over-indexing.** Every index has write cost — INSERT/UPDATE/DELETE must update all indexes. Check `pg_stat_user_indexes` for indexes with zero/near-zero `idx_scan` counts and drop them.

**Always first tool:** `EXPLAIN ANALYZE` before adding index — confirm query plan doing sequential scan where index scan expected, confirm adding index actually changes plan.

**Coaching note:** `pg_stat_statements` starting point + over-indexing warning both signal production experience, not textbook knowledge.

---

### Q2 — Medium · JD: DB design

**When would you choose MongoDB over a relational database, and what data modelling patterns does that require?**

Decision: three factors — schema flexibility, access pattern, scale.

- **Schema flexibility** — MongoDB makes sense when data has genuinely variable/evolving structure. Healthcare: clinical event records (lab result, medication order, procedure note) have different attributes. Forcing into relational = wide sparse table or EAV pattern (both operationally painful). Document store lets each event type carry own schema.
- **Access pattern** — MongoDB optimised for retrieving complete entity in one read (entire patient record with embedded events). If primary query is "everything about patient X," embedding avoids multi-join relational query.

**Modelling shift:** relational normalises to minimise redundancy + optimise flexible querying. MongoDB denormalises to optimise primary access pattern. Key question: "how will data be queried?"
- "Always by patient_id for full record" → embed.
- "Sometimes by patient, sometimes by drug, sometimes by date range across patients" → relational + indexes serves better.

**Failure mode:** treating MongoDB as "schema-free," storing whatever arrives without thinking about access patterns. End up with deeply nested inconsistent documents requiring `$unwind` aggregation pipelines — slow, hard to maintain. Document databases still require disciplined modelling; discipline is just different.

**Real example:** MongoDB used for audit log of pipeline events — high write volume, variable event payload structure, primary query "all events for job X in last hour." Document per event with job metadata embedded was natural fit.

**Coaching note:** "Failure mode of treating MongoDB as schema-free" is most memorable part. Shows production judgment, not just theoretical knowledge.

---

## Testing & CI/CD (HIGH)

Testing + CI/CD explicit JD requirements — Pytest, Git, CI/CD pipelines. Resume mentions regression validation but not testing architecture. Gap will be probed directly.

### Q1 — Hard · JD: Pytest · CI/CD

**How do you structure Pytest for a data pipeline codebase? Walk me through your test organisation and fixtures strategy.**

Tests mirror pipeline structure, separate dirs for unit / integration / e2e:

```
tests/
  unit/
    test_transforms.py      # pure function tests, no I/O
    test_validators.py
    test_schema_contracts.py
  integration/
    test_pipeline_stages.py # local Spark or SQLite
    test_db_readers.py      # local PG container
  e2e/
    test_full_pipeline.py   # dev environment only
```

**Fixtures = most important design decision.** Use `conftest.py` at each level with scoped fixtures:

```python
# tests/conftest.py
@pytest.fixture(scope="session")
def spark():
    """Session-scoped — one SparkSession for all tests. Startup cost is ~5s."""
    spark = SparkSession.builder.master("local[2]").appName("test").getOrCreate()
    yield spark
    spark.stop()

@pytest.fixture
def sample_pharmacy_df(spark):
    """Function-scoped — fresh DataFrame per test."""
    data = [
        ("P001", "12345-678-90", "2024-01-15", 150.0, "ACTIVE"),
        ("P002", None,           "2024-01-15", 200.0, "ACTIVE"),  # null NDC
        ("P003", "12345-678-91", "2024-01-15", -50.0, "ACTIVE"),  # negative amount
    ]
    return spark.createDataFrame(data, ["patient_id","ndc_code","date","amount","status"])
```

`parametrize` for edge case coverage:

```python
@pytest.mark.parametrize("ndc,expected_valid", [
    ("12345-678-90", True),
    ("INVALID",      False),
    (None,           False),
    ("",             False),
])
def test_ndc_validation(ndc, expected_valid):
    assert validate_ndc(ndc) == expected_valid
```

**CI config:** unit tests every PR, integration tests on merge to main, e2e on deploy to dev. PR feedback under 2 min for unit suite.

**Coaching note:** Session-scoped SparkSession fixture is practical detail showing real Pytest experience — function-scoped Spark is common performance mistake experienced engineers avoid.

---

### Q2 — Medium · JD: CI/CD

**How do you implement CI/CD for a data pipeline? What does each stage validate?**

Four stages, each with clear gate function.

**Stage 1 — Code quality (fast, every PR):** ruff (linting + import sorting), mypy (type checking), `black --check` (formatting). Runs under 30 s. Enforce type hints on all public functions — cheapest documentation, catches data contract bugs at dev time.

**Stage 2 — Unit tests (2–3 min, every PR):** `pytest tests/unit/` with coverage reporting. Gate PRs at 80% coverage minimum on transforms module (not I/O layer — covered by integration). Coverage reports to PR comment via `pytest-cov`.

**Stage 3 — Integration tests (5–10 min, merge to main):** `pytest tests/integration/` with docker-compose spinning up PostgreSQL + local Spark. Validates transformation logic works against real DB connectors + real Spark execution, not mocked interfaces.

**Stage 4 — Deployment validation (on deploy to dev/staging):** subset of e2e suite against dev environment, including smoke test running small sample of full pipeline end-to-end + validating output row counts + schema against expected values.

**Azure DevOps mapping:** YAML pipeline with four jobs in `dependsOn` chain — failed unit test blocks integration tests, saving CI minutes.

**Data-pipeline-specific addition:** data contract check in CI. dbt test suite or schema registry to validate changes to transformation output schemas are intentional — not accidental column drops or type changes breaking downstream consumers.

**Coaching note:** Mentioning Azure DevOps specifically maps to JD. Data contract check in CI bridges data engineering expertise into CI/CD context.

---

## Distributed systems (MED)

JD mentions "troubleshoot and optimise distributed data systems" — overask territory. These questions separate senior from lead. Expect theory + practical failure mode questions.

### Q1 — Hard · JD: Distributed systems

**How do you handle exactly-once processing guarantees in a distributed data pipeline?**

True exactly-once is one of the hardest guarantees in distributed systems — worth being precise about what it actually means in practice.

**Three delivery guarantees:**
- At-most-once — messages may be dropped, no duplicates.
- At-least-once — no messages dropped, duplicates possible.
- Exactly-once — no drops, no duplicates.

Most production systems achieve exactly-once semantics through **idempotent processing**, not true exactly-once delivery.

**Practical pattern:** at-least-once delivery + idempotent writes = exactly-once effect.

**Idempotent writes — make write operation safe to repeat:**
- DB inserts: upsert with deduplication key:

```sql
INSERT INTO pharmacy_transactions (...)
VALUES (...)
ON CONFLICT (source_system, source_record_id)
DO UPDATE SET processed_at = EXCLUDED.processed_at,
              amount = EXCLUDED.amount;
```

`source_record_id` = natural key from source. Same record delivered twice → second write is no-op or idempotent update.

- File-based loads → data lake: write to staging partition, validate, atomically rename to production partition. On failure + retry, re-run overwrites staging (idempotent) and re-renames.
- Kafka streaming: transactions API provides exactly-once for Kafka-to-Kafka flows. For Kafka-to-DB, track Kafka offset in same transaction as DB write — resume from last committed offset without reprocessing.

**Trade-off:** exactly-once adds latency + complexity. At-least-once with idempotent writes almost always the right engineering decision — simpler, easier to reason about under failure, lower latency than two-phase commit.

**Coaching note:** "At-least-once + idempotent writes = exactly-once effect" framing is key insight. Shows you understand practical engineering solution, not just theoretical problem.

---

### Q2 — Hard · JD: Distributed systems

**What is CAP theorem and how does it affect your database and pipeline design decisions?**

CAP: distributed system can only guarantee two of three simultaneously:
- **Consistency** — every read returns most recent write.
- **Availability** — every request receives response.
- **Partition tolerance** — system continues operating when network partitions occur.

Since network partitions are reality, practical choice is **CP** (Consistency + Partition tolerance) vs **AP** (Availability + Partition tolerance).

**Database mapping:**
- **PostgreSQL = CP.** Under partition, prioritises consistency — replica won't serve reads if might be behind primary. Right choice for healthcare data where stale reads cause clinical errors — medication dosing decisions can't be based on data potentially 30 s stale.
- **Cassandra = AP.** Under partition, continues serving reads + writes from available nodes, accepts some nodes may have stale data, reconciles via eventual consistency. Appropriate for high-throughput audit logging or event streams where availability > strict consistency.
- **DynamoDB = configurable.** Strongly consistent reads vs eventually consistent per request. Strongly consistent for lookups gating business decision; eventually consistent for analytics aggregations where seconds of staleness acceptable.

**Pipeline design impact:** reading from AP system during partition event, design downstream validation to catch consistency anomalies (duplicate records, missing records, out-of-order events) rather than assuming source always consistent. Data quality framework in current pipeline partly designed around this.

In practice, most data engineering decisions sit in CP vs AP framing — math behind CAP less useful than understanding failure modes of specific databases under network stress.

**Coaching note:** Closing with "math less useful than understanding failure modes" is mature practitioner framing. Shows you've moved past CAP as theoretical talking point.

---

### Q3 — Medium · JD: Distributed systems

**How do you handle late-arriving data in a distributed pipeline?**

Late-arriving data is one of most operationally painful problems — manifests differently in batch vs streaming.

**Batch pipelines:** late data typically arrives in subsequent day's extract — pharmacy submits Monday transactions on Tuesday due to batch delay. Naive (partition by load date) misattributes records to Tuesday, breaks Monday reporting. Correct: **partition by event date** (transaction date) rather than load date, design pipeline to accept inserts into historical partitions.

**Healthcare ETL:** 7-day reprocessing window. Any day's pipeline could receive late records up to 7 days back. Delta Lake merge handled gracefully:

```sql
MERGE INTO target USING new_records
ON target.id = new_records.id
WHEN MATCHED THEN UPDATE SET ...
WHEN NOT MATCHED THEN INSERT ...
```

Reconciliation report ran on T+1 and T+7 — immediate detection + final close. T+7 still showing discrepancies → manual investigation.

**Streaming pipelines:** late data handled via **watermarking**. Spark Structured Streaming: watermark defines how long to wait for late records before closing time window:

```python
df.withWatermark("event_time", "2 hours")
  .groupBy(window("event_time", "1 hour"))
  .agg(sum("amount"))
```

Records arriving > 2 hours after window end = dropped. Watermark-vs-completeness trade-off = business decision (latency tolerance vs real-time completeness). Make explicit in pipeline contract so downstream consumers know completeness guarantee.

**Hardest case:** late data affecting already-delivered client extract. Mitigation = structured correction extract process — updated records with version number, allowing client to apply corrections to their own systems.

**Coaching note:** Correction extract process at end shows you've thought through full business lifecycle of late data, not just technical handling.

---

## See Also
- [[System Design]]
- [[Partitioning]]
- [[Fundamentals]]
- [[Data Modelling]]
- [[Reliability Engineering]]
- [[Orchestration]]
- [[python]] — Python fundamentals
- [[Distributed System]] — distributed systems foundations
- [[Idempotency]] — idempotency patterns
- [[Data Engineering Playbook]] — 15 core truths