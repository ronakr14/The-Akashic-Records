import { useState } from "react";

const JD_SUMMARY = {
  role: "Senior Python Data Engineer",
  focus: "Python · Azure · PySpark · SQL tuning · CI/CD",
  fit: "ETL pipelines · Azure ADF · SQL · distributed systems",
  overask: "Python internals · PySpark optimisation · Pytest/CI-CD · Azure-native design · Distributed theory",
};

const TABS = [
  { id: "py", label: "Python depth", risk: "HIGH" },
  { id: "spark", label: "PySpark", risk: "HIGH" },
  { id: "azure", label: "Azure", risk: "MED" },
  { id: "sql", label: "SQL & DB design", risk: "MED" },
  { id: "test", label: "Testing & CI/CD", risk: "HIGH" },
  { id: "dist", label: "Distributed systems", risk: "MED" },
];

const DATA = {
  py: {
    intro:
      "This is the JD's #1 requirement — 'expert-level Python for data engineering.' Your resume shows Python usage but not Python engineering depth. Expect questions on memory management, concurrency, and design patterns that go beyond scripting.",
    questions: [
      {
        diff: "Hard",
        tag: "JD: Expert Python",
        q: "How do you handle memory-efficient processing of large datasets in Python when the data doesn't fit in memory?",
        a: `The core principle is avoiding materialising the full dataset in memory — you process in streams or chunks.

For file-based data, I use Python generators. Instead of pd.read_csv() which materialises the full DataFrame, I use the chunksize parameter — pd.read_csv(path, chunksize=50_000) — which returns an iterator of DataFrames. Each chunk is processed and the result is written before the next chunk loads. Peak memory stays bounded to one chunk.

For more complex transformations, I write custom generator pipelines:

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

This is lazy evaluation — nothing materialises until the terminal load() function pulls from the chain.

For Pandas-heavy workloads, I downcast dtypes aggressively — int64 to int32/int16 where value range allows, float64 to float32. For low-cardinality columns, pd.Categorical can reduce memory 10–50x.

When even chunking isn't enough, the right answer is to push processing into the database or into Spark — Python shouldn't be the processing layer for truly large-scale data.`,
        tip: "The generator pipeline code is the centrepiece — practice writing it fluently. Then close with the escalation principle: Python for medium scale, push to Spark for large scale.",
      },
      {
        diff: "Hard",
        tag: "JD: Expert Python",
        q: "What's the difference between multiprocessing, multithreading, and asyncio in Python? When would you use each in a data pipeline?",
        a: `The distinction comes down to the GIL and the nature of the bottleneck.

Threading uses OS threads but the GIL means only one thread executes Python bytecode at a time. This makes threading useful for I/O-bound tasks — waiting on network responses, database queries, file reads — where threads spend most of their time waiting. In a data pipeline I'd use threading for parallel HTTP calls to an API or parallel reads from multiple S3 files.

Multiprocessing spawns separate processes, each with its own GIL and memory space. This is the right tool for CPU-bound work — data transformation, serialisation, heavy computation. Each process runs Python truly in parallel. I use multiprocessing.Pool for parallelising CPU-heavy per-partition transformations.

Asyncio is single-threaded cooperative concurrency — coroutines yield control voluntarily using await. It's most efficient for very high concurrency I/O workloads where you'd need thousands of threads with the threading model. In data engineering I use asyncio for pipeline stages making many concurrent API calls — enriching 500k records by calling an identity API, with 500 in-flight requests at once from a single thread.

In practice on my healthcare ETL: asyncio for concurrent NDC code validation against an external drug reference API. Multiprocessing for the CPU-heavy DEID tokenisation step processing 500k patient records. Plain threading for parallel S3 file uploads at pipeline close. Each tool matched to its bottleneck type.`,
        tip: "Closing with real examples from your pipeline converts a textbook answer into an experienced engineer's answer.",
      },
      {
        diff: "Medium",
        tag: "JD: Expert Python",
        q: "How do you design Python data pipeline code for testability? What patterns do you use?",
        a: `Testability starts with separating concerns — I/O, transformation, and orchestration should be distinct layers.

The core principle: transformation logic should be pure functions — they take data in, return data out, no side effects. A function that reads from S3, transforms, and writes to Snowflake in one block is untestable without mocking the entire infrastructure. Splitting into read(), transform(), and write() lets me unit test transform() with a local DataFrame and no cloud dependencies.

def transform_pharmacy_records(df: pd.DataFrame) -> pd.DataFrame:
    """Pure function — no I/O, deterministic, unit testable."""
    df = df.copy()
    df["ndc_code"] = df["ndc_code"].str.strip().str.upper()
    df["sales_amount"] = pd.to_numeric(df["sales_amount"], errors="coerce")
    df = df.dropna(subset=["patient_id", "ndc_code"])
    return df

For I/O layers, I use dependency injection — readers and writers are passed as protocol interfaces so tests inject fakes:

class DataReader(Protocol):
    def read(self, path: str) -> pd.DataFrame: ...

def run_pipeline(reader: DataReader, writer: DataWriter, path: str):
    df = reader.read(path)
    df = transform_pharmacy_records(df)
    writer.write(df)

In tests I pass a FakeReader returning a hardcoded DataFrame — pipeline logic runs without any cloud connection.

The test pyramid I follow: 70% unit tests on pure transform functions, 20% integration tests with local Spark or SQLite, 10% end-to-end tests against a dev environment. The heavy unit test base keeps CI fast — typically under 3 minutes.`,
        tip: "The Protocol-based dependency injection pattern is a strong signal of Python engineering maturity. Many data engineers know testing in principle but haven't applied structural patterns like this.",
      },
      {
        diff: "Medium",
        tag: "JD: Expert Python",
        q: "What Python performance profiling tools do you use, and how have you diagnosed and fixed a real performance bottleneck?",
        a: `My profiling stack depends on the problem type.

For CPU-bound bottlenecks: cProfile for a full call graph, then line_profiler for line-by-line timing on the hot function.

python -m cProfile -o profile.out pipeline.py
snakeviz profile.out  # visual flame chart

A real example: our DEID tokenisation step was taking 8 minutes for 500k records. cProfile showed 90% of time in the hash function. line_profiler showed we were calling hashlib.sha256().hexdigest() per record in a Python loop. The fix was vectorising — computing the hash in a Pandas apply with a batched approach and pre-compiling the HMAC key outside the loop. Runtime dropped to 40 seconds.

For memory bottlenecks: memory_profiler and tracemalloc. memory_profiler decorates functions with @profile and prints per-line memory delta. I used this to find our schema validation step was keeping three copies of the full DataFrame in memory simultaneously during a merge — original, copy for validation, merged result. Restructuring to validate in-place and release intermediate frames cut peak memory by 60%.

For I/O bottlenecks: usually time.perf_counter() around I/O calls is enough to isolate — if 80% of runtime is in one database read, the fix is at the query or connection level, not in Python.

The principle: don't optimise without measuring. I've seen engineers rewrite perfectly fast code in NumPy because it "felt slow" while the real bottleneck was a missing index on the source database. Profile first, optimise the actual bottleneck, measure the improvement.`,
        tip: "The 'profile first, don't guess' closing principle is a senior-level signal. Interviewers respect engineers who resist premature optimisation.",
      },
    ],
  },
  spark: {
    intro:
      "PySpark is listed as a core requirement. Your resume mentions it but doesn't showcase depth. Expect internals questions — not just 'have you used it' but 'how does it actually work and what did you tune.'",
    questions: [
      {
        diff: "Hard",
        tag: "JD: PySpark",
        q: "Explain the Spark execution model — what is a job, stage, and task? How does understanding this help you optimise pipelines?",
        a: `Spark's execution model has three levels: jobs, stages, and tasks.

A job is triggered by an action — collect(), write(), count(). Everything before the action is a lazy transformation DAG. When the action fires, Spark compiles the DAG into a job.

A stage is a unit of work that can execute without a shuffle. Spark breaks the job DAG into stages at shuffle boundaries — points where data needs to move between partitions (joins, groupBys, repartitions). Within a stage, operations are pipelined together on each partition without network I/O.

A task is the smallest unit — one task processes one partition in one stage. If a stage has 200 partitions, it spawns 200 tasks distributed across executors.

Why this matters for optimisation:

Shuffle is expensive. Every stage boundary involves writing shuffle files to disk and reading them across the network. Minimising shuffles is the highest-leverage optimisation. Broadcast joins eliminate shuffle entirely for small table joins:

spark.conf.set("spark.sql.autoBroadcastJoinThreshold", 50 * 1024 * 1024)

Partition count affects parallelism. Too few = underutilised executors. Too many = excessive task scheduling overhead. Target 2–4 tasks per CPU core. Check with df.rdd.getNumPartitions() and adjust with repartition() or coalesce().

Data skew is the hardest problem. I detect it from the Spark UI — one stage task taking 10 minutes while others take 30 seconds. The fix is salting: adding a random prefix to the skewed join key.

In my healthcare ETL, the pharmacy transaction table had severe skew by pharmacy_id — a handful of large chains accounted for 40% of records. Salting that join reduced the long-tail stage time from 25 minutes to 4 minutes.`,
        tip: "The pharmacy skew example grounds the theory. Always close Spark internals answers with a real production impact number.",
      },
      {
        diff: "Hard",
        tag: "JD: PySpark",
        q: "What's the difference between narrow and wide transformations? Why does it matter?",
        a: `Narrow transformations operate on a single partition — the output depends only on one input partition. No data moves between executors. Examples: map(), filter(), select(), withColumn(). These are cheap and pipelined within a stage.

Wide transformations require data from multiple input partitions — a shuffle is required. Examples: groupBy(), join(), repartition(), distinct(), orderBy(). These create stage boundaries and involve disk writes and network I/O.

Why it matters in practice:

Pipeline optimisation: push filters and selects before wide transformations. If you filter 80% of records before a groupBy, you move far less data across the network. Spark's Catalyst optimiser does some of this automatically via predicate pushdown, but I always verify with df.explain(extended=True).

Caching strategy: cache the output of an expensive wide transformation if consumed multiple times downstream. df.cache() before the second use avoids re-executing the shuffle. Always unpersist() when done — Spark's memory management isn't aggressive about eviction.

In one pipeline, we had three successive wide transformations on a 500M-row table with no caching. Adding a checkpoint after the first two — df.checkpoint() writes to S3 and breaks the DAG lineage — reduced recovery time on failures from recomputing 3 shuffles to recomputing 1.`,
        tip: "Mentioning df.explain() and Spark UI shows you actually debug Spark, not just write it. That's the separator between 'used PySpark' and 'owns PySpark.'",
      },
      {
        diff: "Medium",
        tag: "JD: PySpark",
        q: "When would you use Pandas UDFs over regular PySpark transformations, and what are the performance implications?",
        a: `Pandas UDFs are the right tool when you need Python/Pandas logic that can't be expressed in native Spark SQL functions — custom statistical models, complex string processing, or calling a Python library with no Spark equivalent.

There are three types. SCALAR UDFs operate on a Pandas Series and return a Series — one-to-one row transformation. GROUPED_MAP takes a partition as a Pandas DataFrame and returns a DataFrame — useful for per-group operations like per-pharmacy seasonality adjustments. GROUPED_AGG takes grouped data and returns a scalar — for custom aggregations.

Performance trade-off vs native Spark functions: native Spark SQL functions execute in the JVM using Catalyst-optimised code generation. Pandas UDFs require serialising data from JVM to Python via Apache Arrow, executing in Python, then serialising back. Arrow-based serialisation is much faster than old row-by-row pickle serialisation, but there's still overhead.

Rule of thumb: if a native Spark function can do it, use it. date_format(), regexp_replace(), when()/otherwise() — all JVM-side. Reach for Pandas UDFs only when you genuinely need Python logic.

In practice: I used a Pandas GROUPED_MAP UDF for our NER-based PHI detection step. Each partition of clinical notes was processed as a Pandas DataFrame through the spaCy NER model. The vectorised UDF processed 10k records per Arrow batch vs 1 at a time — roughly 8x faster.

One important gotcha: Pandas UDFs require explicit return schema declarations. If the schema is wrong, Spark fails at runtime, not compile time. I always test UDFs on a small sample before running on the full dataset.`,
        tip: "The NER processing use case shows you reached for Pandas UDFs for the right reason (Python library dependency), not because you didn't know the native API.",
      },
    ],
  },
  azure: {
    intro:
      "Azure is listed as mandatory. Your resume shows ADF usage but the JD wants Azure-native architecture thinking — Data Lake design, Delta Lake, and cloud-native pipeline patterns across the full stack.",
    questions: [
      {
        diff: "Hard",
        tag: "JD: Azure mandatory",
        q: "Design an Azure-native data platform for ingesting, processing, and serving large-scale structured and semi-structured data.",
        a: `I'd structure this around three zones — ingestion, processing, and serving — with governance running throughout as a vertical, not a layer.

Ingestion: Azure Event Hubs for real-time streaming sources (CDC events, clickstream) feeding into ADLS Gen2. For batch sources — databases, SaaS APIs, file drops — Azure Data Factory handles orchestration with its native connectors. ADLS Gen2 is the raw landing zone, partitioned by source and date. Key design decision: raw zone is immutable — append-only, never modified after landing.

Processing: Azure Databricks with PySpark for heavy transformation. Databricks sits on top of ADLS Gen2 and writes to Delta Lake tables. Delta gives us ACID transactions on the data lake — critical for late-arriving data and backfill scenarios. The medallion architecture maps naturally: raw ADLS → bronze Delta → silver Delta → gold Delta. ADF orchestrates Databricks jobs for scheduling, dependencies, and retry logic.

Serving: Azure Synapse Dedicated SQL Pool for structured analytical workloads needing high-concurrency BI access. Synapse Serverless for ad-hoc exploration without provisioning. For ML feature serving, direct Delta table access from Databricks.

Governance throughout: Azure Purview for cataloguing and lineage, Key Vault for secrets management, Azure Active Directory for identity-based access control, Azure Monitor + Log Analytics for pipeline observability.

The Databricks vs Synapse split: Databricks for complex PySpark transformation and ML workloads, Synapse for SQL-centric serving and BI integration. They interoperate well through shared ADLS storage — this isn't an either/or choice.`,
        tip: "The 'governance is a vertical, not a layer' framing lands well with senior interviewers. The Databricks + Synapse coexistence answer shows Azure ecosystem maturity.",
      },
      {
        diff: "Medium",
        tag: "JD: Azure mandatory",
        q: "How does ADLS Gen2 differ from Blob Storage, and how does that affect your data lake design?",
        a: `ADLS Gen2 is built on Blob Storage but adds a hierarchical namespace — a true directory structure with atomic rename and delete at the directory level. This is a critical difference for data lake workloads.

With flat Blob Storage, a "directory" is just a naming convention. Renaming or deleting a "directory" requires listing all objects with that prefix and operating on each individually. On a partition with 50,000 files, a rename is 50,000 API calls — slow and non-atomic. If it fails midway, you have a partial rename that can corrupt downstream reads.

ADLS Gen2's hierarchical namespace makes directory rename atomic and O(1) — the metadata operation completes in one step regardless of how many files are in the directory. This is what makes Databricks Delta Lake commit operations performant on Azure — Delta's transaction protocol does atomic directory renames to swap in new data.

For data lake design: partition by the dimensions you query on — typically date, source, and entity type. Use the atomic rename guarantee for staging patterns — write to a temp directory, validate, then rename to production atomically. This gives idempotent loads without complex file-level bookkeeping.

ADLS Gen2 also adds POSIX-style ACLs at the directory and file level, which Blob Storage doesn't support natively. This is what enables fine-grained access control — giving the analytics team read access to /gold/ without exposing /raw/ — critical for HIPAA-adjacent workloads.

The practical implication: always use ADLS Gen2, never plain Blob Storage, for a data lake. The hierarchical namespace and ACL support are non-optional for production workloads.`,
        tip: "Most candidates know ADLS Gen2 is 'better' but can't explain why. The atomic rename tied to Delta Lake commits is a concrete differentiator.",
      },
    ],
  },
  sql: {
    intro:
      "The JD calls out advanced SQL and database performance tuning explicitly. Your resume shows strong SQL but expect indexing strategy, query plan analysis, and data modelling questions that go deeper than what you've covered so far.",
    questions: [
      {
        diff: "Hard",
        tag: "JD: SQL tuning",
        q: "How do you approach indexing strategy for a heavily queried PostgreSQL table?",
        a: `Indexing strategy starts with understanding query patterns — specifically the WHERE, JOIN, and ORDER BY columns in the most frequent and most expensive queries. I get this from pg_stat_statements which tracks query frequency and total execution time.

B-tree indexes are the default and cover equality and range conditions — patient_id = X, transaction_date BETWEEN x AND y. For a primary lookup key I always have a B-tree. The question is which additional columns to index.

Composite indexes: when queries consistently filter on (pharmacy_id, transaction_date), a composite index on those two columns is far more efficient than two separate indexes. Order matters — leading column for equality predicates, trailing column for range predicates. An index on (pharmacy_id, transaction_date) supports WHERE pharmacy_id = X AND transaction_date > Y but won't help a query filtering only on transaction_date.

Partial indexes: when queries consistently filter on a subset of rows — WHERE status = 'ACTIVE' — a partial index covers only those rows:

CREATE INDEX idx_active_transactions
ON pharmacy_transactions(patient_id)
WHERE status = 'ACTIVE';

This is smaller, faster to maintain, and fits in cache better than a full-table index.

What I watch for: over-indexing. Every index has a write cost — INSERT, UPDATE, DELETE must update all indexes on the table. I regularly check pg_stat_user_indexes for indexes with zero or near-zero idx_scan counts and drop them.

EXPLAIN ANALYZE is always my first tool before adding an index — I want to confirm the query plan is doing a sequential scan where I expect an index scan, and that adding the index actually changes the plan.`,
        tip: "The pg_stat_statements starting point and the over-indexing warning both signal production experience, not textbook knowledge.",
      },
      {
        diff: "Medium",
        tag: "JD: DB design",
        q: "When would you choose MongoDB over a relational database, and what data modelling patterns does that require?",
        a: `The decision comes down to three factors: schema flexibility, access pattern, and scale requirements.

MongoDB makes sense when data has genuinely variable or evolving structure. In a healthcare context, clinical event records are a good fit: a lab result, a medication order, and a procedure note all have different attributes. Forcing them into a relational schema requires either a wide sparse table or an EAV pattern — both operationally painful. A document store lets each event type carry its own schema.

The other driver is access pattern. MongoDB is optimised for retrieving a complete entity in one read — the entire patient record with all embedded events. If your primary query is "give me everything about patient X," embedding related data in a single document avoids the multi-join query a relational model requires.

The modelling shift: relational thinking normalises to minimise redundancy and optimises for flexible querying. MongoDB modelling denormalises to optimise for the primary access pattern. The key question is always "how will this data be queried?" If the answer is "always by patient_id for the full record," embed. If the answer is "sometimes by patient, sometimes by drug, sometimes by date range across all patients," relational with indexes serves better.

The failure mode I've seen: treating MongoDB as a "schema-free" database and storing whatever arrives without thinking about access patterns. You end up with deeply nested inconsistent documents that require $unwind aggregation pipelines — slow and hard to maintain. Document databases still require disciplined modelling; the discipline is just different.

In my current work, MongoDB was used for the audit log of pipeline events — high write volume, variable event payload structure, and the primary query was "all events for job X in the last hour." A document per event with job metadata embedded was the natural fit.`,
        tip: "The 'failure mode of treating MongoDB as schema-free' is the most memorable part. It shows production judgment, not just knowing when MongoDB is theoretically appropriate.",
      },
    ],
  },
  test: {
    intro:
      "Testing and CI/CD are explicit JD requirements — Pytest, Git, CI/CD pipelines. Your resume mentions regression validation but not testing architecture. This is a gap that will be probed directly.",
    questions: [
      {
        diff: "Hard",
        tag: "JD: Pytest · CI/CD",
        q: "How do you structure Pytest for a data pipeline codebase? Walk me through your test organisation and fixtures strategy.",
        a: `I organise tests to mirror the pipeline structure, with separate directories for unit, integration, and end-to-end tests:

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

Fixtures are the most important design decision. I use conftest.py at each level with scoped fixtures:

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

The parametrize decorator is my main tool for edge case coverage:

@pytest.mark.parametrize("ndc,expected_valid", [
    ("12345-678-90", True),
    ("INVALID",      False),
    (None,           False),
    ("",             False),
])
def test_ndc_validation(ndc, expected_valid):
    assert validate_ndc(ndc) == expected_valid

CI configuration: unit tests on every PR, integration tests on merge to main, e2e on deploy to dev. PR feedback stays under 2 minutes for the unit suite.`,
        tip: "The session-scoped SparkSession fixture is a practical detail that shows real Pytest experience — function-scoped Spark is a common performance mistake that experienced engineers know to avoid.",
      },
      {
        diff: "Medium",
        tag: "JD: CI/CD",
        q: "How do you implement CI/CD for a data pipeline? What does each stage validate?",
        a: `My CI/CD setup has four stages, each with a clear gate function.

Stage 1 — Code quality (fast, every PR): ruff for linting and import sorting, mypy for type checking, black --check for formatting. Runs in under 30 seconds. I enforce type hints on all public functions — they're the cheapest form of documentation and catch data contract bugs at development time.

Stage 2 — Unit tests (2–3 minutes, every PR): pytest tests/unit/ with coverage reporting. I gate PRs at 80% coverage minimum on the transforms module — not the I/O layer, which is covered by integration tests. Coverage reports go to a PR comment via pytest-cov.

Stage 3 — Integration tests (5–10 minutes, merge to main): pytest tests/integration/ with docker-compose spinning up PostgreSQL and a local Spark environment. This validates that transformation logic works correctly against real database connectors and real Spark execution, not mocked interfaces.

Stage 4 — Deployment validation (on deploy to dev/staging): runs a subset of the e2e test suite against the dev environment, including a smoke test that runs a small sample of the full pipeline end-to-end and validates output row counts and schema against expected values.

For Azure DevOps — which is what I've used — this maps to a YAML pipeline with four jobs in a dependsOn chain so a failed unit test blocks integration tests from running, saving CI minutes.

One addition specific to data pipelines: a data contract check in CI. Using dbt test suite or a schema registry to validate that any changes to transformation output schemas are intentional — not accidental column drops or type changes that would break downstream consumers.`,
        tip: "Mentioning Azure DevOps specifically maps to the JD. The data contract check in CI bridges your data engineering expertise into the CI/CD context.",
      },
    ],
  },
  dist: {
    intro:
      "The JD mentions 'troubleshoot and optimise distributed data systems' — this is the overask territory. These questions separate senior from lead. Expect theory + practical failure mode questions.",
    questions: [
      {
        diff: "Hard",
        tag: "JD: Distributed systems",
        q: "How do you handle exactly-once processing guarantees in a distributed data pipeline?",
        a: `True exactly-once is one of the hardest guarantees in distributed systems and it's worth being precise about what it actually means in practice.

There are three delivery guarantees: at-most-once (messages may be dropped, no duplicates), at-least-once (no messages dropped, duplicates possible), and exactly-once (no drops, no duplicates). Most production systems achieve exactly-once semantics through idempotent processing rather than true exactly-once delivery.

The practical pattern: at-least-once delivery + idempotent writes = exactly-once effect.

For idempotent writes, the key is making the write operation safe to repeat. For database inserts, I use upsert logic with a deduplication key:

INSERT INTO pharmacy_transactions (...)
VALUES (...)
ON CONFLICT (source_system, source_record_id)
DO UPDATE SET processed_at = EXCLUDED.processed_at,
              amount = EXCLUDED.amount;

The source_record_id is a natural key from the source — if the same record is delivered twice, the second write is a no-op or idempotent update.

For file-based loads into a data lake: write to a staging partition, validate, then atomically rename to the production partition. On failure and retry, the re-run overwrites the staging partition (idempotent) and re-renames.

For Kafka-based streaming: Kafka's transactions API provides exactly-once for Kafka-to-Kafka flows. For Kafka-to-database, track the Kafka offset in the same transaction as the database write, so you resume from the last committed offset without reprocessing.

The tradeoff: exactly-once semantics add latency and complexity. At-least-once with idempotent writes is almost always the right engineering decision — simpler to implement, easier to reason about under failure, lower latency than two-phase commit approaches.`,
        tip: "The 'at-least-once + idempotent writes = exactly-once effect' framing is the key insight. It shows you understand the practical engineering solution, not just the theoretical problem.",
      },
      {
        diff: "Hard",
        tag: "JD: Distributed systems",
        q: "What is CAP theorem and how does it affect your database and pipeline design decisions?",
        a: `CAP theorem states that a distributed system can only guarantee two of three properties simultaneously: Consistency (every read returns the most recent write), Availability (every request receives a response), and Partition tolerance (the system continues operating when network partitions occur).

Since network partitions are a reality in distributed systems, the practical choice is between CP (Consistency + Partition tolerance) and AP (Availability + Partition tolerance).

How this maps to database choices:

PostgreSQL is CP. Under a network partition, PostgreSQL prioritises consistency — a replica won't serve reads if it might be behind the primary. This is the right choice for healthcare data where stale reads would cause clinical errors — medication dosing decisions can't be based on data that might be 30 seconds stale.

Cassandra is AP. Under a partition, Cassandra continues serving reads and writes from available nodes, accepting some nodes may have stale data, reconciling via eventual consistency. Appropriate for high-throughput audit logging or event streams where availability matters more than strict consistency.

DynamoDB is configurable — strongly consistent reads vs eventually consistent reads per request. I use strongly consistent reads for lookups gating a business decision, eventually consistent for analytics aggregations where seconds of staleness is acceptable.

How it affects pipeline design: when reading from an AP system during a partition event, I design downstream validation to catch consistency anomalies — duplicate records, missing records, out-of-order events — rather than assuming the source is always consistent. The data quality framework in my current pipeline was partly designed around this.

In practice, most data engineering decisions sit in the CP vs AP framing — the math behind CAP is less useful than understanding the failure modes of your specific databases under network stress.`,
        tip: "Closing with 'the math is less useful than understanding failure modes' is a mature practitioner framing. It shows you've moved past using CAP as a theoretical talking point.",
      },
      {
        diff: "Medium",
        tag: "JD: Distributed systems",
        q: "How do you handle late-arriving data in a distributed pipeline?",
        a: `Late-arriving data is one of the most operationally painful problems and it manifests differently in batch vs streaming contexts.

In batch pipelines, late data typically arrives in a subsequent day's extract — a pharmacy system submits Monday's transactions on Tuesday due to a batch delay. The naive approach — partition by load date — misattributes these records to Tuesday and breaks Monday reporting. The correct approach is to partition by event date (transaction date) rather than load date, and design the pipeline to accept inserts into historical partitions.

In my healthcare ETL: we kept a 7-day reprocessing window. Any day's pipeline could receive late records for up to 7 days back. Delta Lake's merge operation handled this gracefully:

MERGE INTO target USING new_records
ON target.id = new_records.id
WHEN MATCHED THEN UPDATE SET ...
WHEN NOT MATCHED THEN INSERT ...

The reconciliation report ran on T+1 and T+7 — once for immediate detection, once for final close. If T+7 still showed discrepancies, that triggered manual investigation.

In streaming pipelines, late data is handled through watermarking. In Spark Structured Streaming, a watermark defines how long to wait for late records before closing a time window:

df.withWatermark("event_time", "2 hours")
  .groupBy(window("event_time", "1 hour"))
  .agg(sum("amount"))

Records arriving more than 2 hours after the window end are dropped. The watermark-vs-completeness tradeoff is a business decision — 2 hours of latency tolerance vs real-time completeness. I always make this explicit in the pipeline contract so downstream consumers know the completeness guarantee.

The hardest case: late data affecting an already-delivered client extract. Our mitigation was a structured correction extract process — updated records with a version number, allowing the client to apply corrections to their own systems.`,
        tip: "The correction extract process at the end shows you've thought through the full business lifecycle of late data, not just the technical handling.",
      },
    ],
  },
};

const riskColor = (risk) => {
  if (risk === "HIGH") return { bg: "#3d1a1a", color: "#f87171", border: "#7f2d2d" };
  return { bg: "#3d2e1a", color: "#fbbf24", border: "#7f5e2d" };
};

const diffStyle = (diff) => {
  if (diff === "Hard") return { bg: "#3d1a1a", color: "#f87171" };
  if (diff === "Medium") return { bg: "#3d2e1a", color: "#fbbf24" };
  return { bg: "#1a3d2a", color: "#4ade80" };
};

export default function InterviewPrep() {
  const [activeTab, setActiveTab] = useState("py");
  const [openQ, setOpenQ] = useState({});

  const toggleQ = (id) => setOpenQ((prev) => ({ ...prev, [id]: !prev[id] }));

  const section = DATA[activeTab];

  return (
    <div style={{ fontFamily: "'Georgia', serif", background: "#0f0f0f", minHeight: "100vh", padding: "1.5rem 1rem", color: "#e5e5e5" }}>
      {/* Header band */}
      <div style={{ background: "#1a1a1a", border: "0.5px solid #2a2a2a", borderRadius: 10, padding: "12px 16px", marginBottom: 20, display: "flex", flexWrap: "wrap", gap: 12 }}>
        {Object.entries({ Role: JD_SUMMARY.role, Focus: JD_SUMMARY.focus, "Your fit": JD_SUMMARY.fit, "Overask areas": JD_SUMMARY.overask }).map(([k, v]) => (
          <div key={k} style={{ fontSize: 12, color: "#888" }}>
            <span style={{ color: "#ccc", fontWeight: 600 }}>{k}:</span> {v}
          </div>
        ))}
      </div>

      {/* Tabs */}
      <div style={{ display: "flex", flexWrap: "wrap", gap: 6, marginBottom: 20 }}>
        {TABS.map((t) => {
          const rc = riskColor(t.risk);
          const active = activeTab === t.id;
          return (
            <button
              key={t.id}
              onClick={() => { setActiveTab(t.id); setOpenQ({}); }}
              style={{
                padding: "6px 12px", fontSize: 13, borderRadius: 8, cursor: "pointer",
                background: active ? "#1e1e1e" : "transparent",
                border: active ? "0.5px solid #444" : "0.5px solid #2a2a2a",
                color: active ? "#e5e5e5" : "#888",
                display: "flex", alignItems: "center", gap: 6,
                fontFamily: "inherit",
              }}
            >
              {t.label}
              <span style={{ fontSize: 10, padding: "1px 6px", borderRadius: 10, background: rc.bg, color: rc.color, border: `0.5px solid ${rc.border}`, fontFamily: "system-ui" }}>
                {t.risk}
              </span>
            </button>
          );
        })}
      </div>

      {/* Intro */}
      <div style={{ background: "#161616", border: "0.5px solid #2a2a2a", borderRadius: 8, padding: "10px 14px", marginBottom: 16, fontSize: 13, color: "#999", lineHeight: 1.6 }}>
        {section.intro}
      </div>

      {/* Questions */}
      {section.questions.map((item, i) => {
        const qid = `${activeTab}-${i}`;
        const isOpen = !!openQ[qid];
        const ds = diffStyle(item.diff);
        return (
          <div key={qid} style={{ border: "0.5px solid #2a2a2a", borderRadius: 10, marginBottom: 14, overflow: "hidden" }}>
            <div
              onClick={() => toggleQ(qid)}
              style={{ padding: "14px 16px", cursor: "pointer", background: isOpen ? "#1a1a1a" : "#141414", display: "flex", justifyContent: "space-between", alignItems: "flex-start", gap: 12 }}
            >
              <div>
                <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 6, flexWrap: "wrap" }}>
                  <span style={{ fontSize: 11, padding: "2px 8px", borderRadius: 20, background: ds.bg, color: ds.color, fontFamily: "system-ui", fontWeight: 600 }}>{item.diff}</span>
                  <span style={{ fontSize: 11, padding: "2px 8px", borderRadius: 20, background: "#1a2a3d", color: "#60a5fa", fontFamily: "system-ui" }}>{item.tag}</span>
                </div>
                <div style={{ fontSize: 14, fontWeight: 600, color: "#ddd", lineHeight: 1.5 }}>{item.q}</div>
              </div>
              <span style={{ fontSize: 18, color: "#555", flexShrink: 0, marginTop: 2, transform: isOpen ? "rotate(180deg)" : "none", transition: "transform 0.2s" }}>▾</span>
            </div>

            {isOpen && (
              <div style={{ borderTop: "0.5px solid #2a2a2a", padding: "16px" }}>
                <div style={{ fontSize: 11, fontWeight: 600, color: "#555", textTransform: "uppercase", letterSpacing: "0.07em", marginBottom: 10, fontFamily: "system-ui" }}>Sample answer</div>
                <pre style={{ fontSize: 13, color: "#ccc", lineHeight: 1.8, whiteSpace: "pre-wrap", fontFamily: "'Georgia', serif", margin: 0 }}>{item.a}</pre>
                <div style={{ marginTop: 14, padding: "10px 14px", borderLeft: "2px solid #333", fontSize: 12, color: "#777", lineHeight: 1.6, fontFamily: "system-ui" }}>
                  <span style={{ fontWeight: 600, color: "#aaa" }}>Coaching note: </span>{item.tip}
                </div>
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}
