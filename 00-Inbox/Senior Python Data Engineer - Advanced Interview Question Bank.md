# AI Summary
This interview should assess a **Senior Data Engineer / Data Platform Engineer with strong Python skills**, not a Python backend developer. The core evaluation areas are **enterprise data architecture, scalable ETL pipelines, advanced SQL, Python/Pandas, Airflow, Azure, Data Lake/Warehouse design, data quality, observability, and production reliability**.

At senior level, focus less on syntax and tool trivia and more on **architecture decisions, trade-offs, scalability, failure recovery, idempotency, performance, security, and end-to-end ownership**. Scenario-based and system-design questions should carry more weight than isolated technical questions.

---

# Senior Python Data Engineer — Advanced Interview Question Bank

> [!abstract] Interview Focus  
> This role is fundamentally a **Senior Data Engineering / Data Platform Engineering** position with strong Python skills. The interview should prioritize architecture, data pipelines, reliability, scalability, Azure, SQL, Airflow, and end-to-end ownership rather than treating Python as a backend-development role.

## Role Profile

**Primary focus:** Data Engineering (~80%)

**Core capabilities:**

- Enterprise Data Platform architecture
    
- End-to-end data pipelines
    
- Python-based ETL and data engineering
    
- Advanced SQL
    
- Pandas
    
- Apache Airflow
    
- Azure
    
- Data Lakes
    
- Data Warehouses
    
- Analytics / Power BI
    
- Structured and unstructured data
    
- Data quality and observability
    
- API-based ingestion
    
- Production operations and reliability
    

---

# 1. Enterprise Data Platform Architecture

## Q1. Design an enterprise data platform from scratch

> You have 50+ source systems consisting of relational databases, REST APIs, SaaS applications, CSV/Excel files, and unstructured documents. Data ultimately needs to support Power BI reporting.
> 
> Design the end-to-end architecture.

### Look for

- Source systems
    
- Ingestion layer
    
- Landing/raw zone
    
- Transformation layer
    
- Curated layer
    
- Data warehouse / serving layer
    
- Semantic layer
    
- Power BI
    
- Batch vs streaming decisions
    
- Data quality
    
- Metadata/catalog
    
- Schema evolution
    
- Security
    
- Lineage
    
- Orchestration
    
- Monitoring
    
- Reprocessing
    
- Disaster recovery
    
- Cost management
    

### Follow-ups

- Why Data Lake + Data Warehouse instead of only a Data Warehouse?
    
- Where would transformations happen?
    
- Where would data quality be enforced?
    
- How would you handle schema evolution?
    
- How would you make the platform reusable for 100+ pipelines?
    
- How would you support backfills?
    
- How would you handle source-system failures?
    

> [!tip] Interviewer signal  
> This is arguably the **most important question** for the role. The candidate should think in terms of a platform, not individual pipelines.

---

# 2. Enterprise Pipeline Standardization

## Q2. Standardizing 300 pipelines

> Your platform has 300 pipelines. Every team is creating pipelines differently. How would you standardize the platform?

### Look for

- Reusable pipeline framework
    
- Configuration-driven pipelines
    
- Metadata-driven ingestion
    
- Standard DAG patterns
    
- Common Python libraries
    
- Naming conventions
    
- Data contracts
    
- CI/CD
    
- Observability
    
- Standard retry/error handling
    
- Idempotency
    
- Common security patterns
    

### Follow-up

> How would you prevent individual teams from reinventing ingestion, validation, logging, and error handling?

### Red flag

> "We create reusable Python functions."

That is implementation-level thinking rather than platform-level thinking.

---

# 3. Metadata-Driven Ingestion

## Q3. Design a metadata-driven ingestion framework

> Design a framework capable of ingesting hundreds of tables from different source systems using configuration rather than custom code for every source.

Possible metadata:

```text
source_system
source_type
source_connection
source_table
target_path
load_type
watermark_column
primary_key
partition_column
schedule
schema
data_quality_rules
```

### Follow-ups

- How would the framework dynamically generate pipelines?
    
- Where would metadata be stored?
    
- How would you support full vs incremental loads?
    
- How would you handle CDC?
    
- How would you handle schema evolution?
    
- How would you handle source-specific exceptions?
    
- How would you version configuration?
    

### Strong candidate may discuss

- Control tables
    
- Dynamic DAG generation
    
- Dynamic task mapping
    
- Watermarks
    
- CDC
    
- Data contracts
    
- Schema registry
    
- Configuration management
    

---

# 4. Advanced Python for Data Engineering

## Q4. Processing 100 GB with Pandas

> A Python pipeline processes 100 GB of data using Pandas and crashes due to memory exhaustion. How would you redesign it?

### Look for

- Chunking
    
- Streaming
    
- Predicate pushdown
    
- Column pruning
    
- Parquet
    
- PyArrow
    
- Memory profiling
    
- Avoiding unnecessary materialization
    
- Spark when scale demands it
    
- Polars / DuckDB where appropriate
    

### Follow-up

> When would you still choose Pandas?

Strong answer:

> Pandas is appropriate when the working dataset fits comfortably in memory and its ecosystem provides value. It should not automatically become the default processing engine for large-scale data.

---

# 5. Python Concurrency

## Q5. Multiprocessing vs threading vs asyncio

> Explain the difference between multiprocessing, multithreading, and asyncio in Python. Which would you use for a high-volume API ingestion pipeline?

### Expected reasoning

|Workload|Likely approach|
|---|---|
|CPU-bound|Multiprocessing|
|I/O-bound synchronous|Threads|
|High-concurrency I/O|Asyncio|
|Distributed processing|Spark / distributed engine|

### Follow-ups

- The API allows only 100 requests/minute. How would you enforce that?
    
- What happens if individual requests have highly variable latency?
    
- How would you handle retries without overwhelming the API?
    
- How would you preserve ordering if ordering matters?
    

---

# 6. Idempotency

## Q6. Duplicate records after retries

> A Python ETL process occasionally produces duplicate records after retries. How would you make the pipeline idempotent?

### Look for

- Business/natural keys
    
- Batch IDs
    
- Source offsets
    
- Watermarks
    
- Upserts
    
- `MERGE`
    
- Deduplication
    
- Transaction boundaries
    
- Effectively-once processing
    

### Critical follow-up

> Can you guarantee exactly-once processing across an external REST API, Python, and a database?

A strong candidate should distinguish:

- At-most-once
    
- At-least-once
    
- Exactly-once
    
- Idempotency
    
- Transactional guarantees
    
- Deduplication
    

---

# 7. Production Python Repository Design

## Q7. Structure a production-grade Python data engineering repository

> How would you structure a Python repository containing ingestion, transformation, validation, orchestration, and tests?

Possible structure:

```text
src/
    ingestion/
    transformation/
    validation/
    storage/
    orchestration/
    utils/

tests/
    unit/
    integration/
    fixtures/

configs/
dags/
scripts/

pyproject.toml
```

### Follow-ups

- Where should business logic live?
    
- How do you prevent Airflow DAGs from becoming giant Python scripts?
    
- How would you test transformations independently of Airflow?
    
- How would you manage configuration?
    
- How would you package reusable components?
    

---

# 8. Advanced Pandas

## Q8. Optimizing a large Pandas transformation

> A 20-million-row DataFrame takes 40 minutes to process. How would you investigate and optimize it?

### Look for

- Vectorization
    
- Avoiding `.apply()`
    
- Data types
    
- Categoricals
    
- Groupby optimization
    
- Merge strategy
    
- Memory usage
    
- Copying
    
- Profiling
    
- Chunking
    
- Alternative processing engines
    

### Follow-up

> What would make you abandon Pandas entirely?

---

## Q9. Why is this problematic?

```python
df["result"] = df.apply(
    lambda row: expensive_function(row),
    axis=1
)
```

### Follow-up

> How would you redesign it?

Look for:

- Vectorized operations
    
- Mapping
    
- Joins
    
- Precomputation
    
- Batch operations
    
- Alternative processing engines
    

---

# 9. Advanced SQL

## Q10. Optimizing a 5-billion-row query

> You have a 5-billion-row fact table joined with a 10-million-row dimension. The query takes 45 minutes. How would you investigate?

### Look for

- Execution plan
    
- Join strategy
    
- Partition pruning
    
- Predicate pushdown
    
- Statistics
    
- Data skew
    
- Clustering
    
- Indexing where applicable
    
- Data types
    
- Materialization
    
- Pre-aggregation
    
- Join order
    
- Broadcast strategies where applicable
    

### Follow-up

> How would you determine whether the problem is the SQL itself or the underlying data layout?

---

# 10. Incremental SQL Loads

## Q11. Designing an incremental load

> How would you implement an incremental load using SQL?

Then introduce complications:

- What if records arrive late?
    
- What if existing records are updated?
    
- What if records are deleted from the source?
    
- What if the pipeline fails halfway through?
    
- What if the watermark itself is incorrect?
    
- What if two pipeline executions overlap?
    

### Strong candidate should discuss

- Watermarks
    
- CDC
    
- `MERGE`
    
- Change tracking
    
- Soft deletes
    
- Audit/control tables
    
- Idempotency
    
- Transaction boundaries
    
- Reprocessing
    

---

# 11. Slowly Changing Dimensions

## Q12. Implement SCD Type 2

Design a dimension:

```text
customer_id
name
address
effective_from
effective_to
is_current
```

### Follow-ups

- Customer changes address three times in one day. What happens?
    
- Yesterday's record arrives again. What happens?
    
- How do you handle late-arriving changes?
    
- What happens if the source has no reliable update timestamp?
    
- How do you reconcile historical corrections?
    

---

# 12. Data Lake Architecture

## Q13. Design storage for a multi-petabyte Data Lake

### Discuss

- Parquet
    
- Partitioning
    
- File sizing
    
- Small-file problem
    
- Compaction
    
- Schema evolution
    
- ACID table formats
    
- Retention
    
- Lifecycle policies
    
- Metadata
    
- Catalog
    
- Access control
    
- Encryption
    

### Follow-up

> What would you partition by?

Do not accept simply:

> "Date."

The candidate should discuss:

- Query patterns
    
- Cardinality
    
- Partition size
    
- Data distribution
    
- Write patterns
    
- Partition pruning
    
- Risk of over-partitioning
    

---

# 13. Small Files Problem

## Q14. 20 million small Parquet files

> You have 20 million Parquet files, most only 2–5 MB. What problems does this create and how would you fix it?

### Look for

- Metadata overhead
    
- Object-store request overhead
    
- Query planning overhead
    
- Poor scan efficiency
    
- Excessive file listing
    
- Compaction
    
- Appropriate target file size
    
- Write parallelism
    

---

# 14. Data Lake vs Data Warehouse

## Q15. When should data live in a Lake, Warehouse, or both?

Ask:

> When would you put data in the Data Lake?

> When would you put it in the Warehouse?

> Why would you deliberately store the same logical data in both?

> What responsibilities belong to each layer?

> When does a Data Lake become a Data Swamp?

### Red flag

> "Lake is raw and Warehouse is structured."

That answer is too simplistic for a Senior Data Engineer.

---

# 15. Advanced Airflow

## Q16. Optimizing a 200-task Airflow DAG

> An Airflow DAG contains 200 tasks and takes 8 hours. How would you optimize it?

### Look for

- Task granularity
    
- Parallelism
    
- Pools
    
- Executor
    
- Queues
    
- Scheduler configuration
    
- Dynamic task mapping
    
- Deferrable operators
    
- Sensor behavior
    
- Dependency design
    
- XCom misuse
    
- DAG parsing overhead
    

---

# 16. Airflow XCom

## Q17. What belongs in XCom?

> What should and shouldn't be stored in Airflow XCom?

### Good candidates

- Small metadata
    
- IDs
    
- File paths
    
- Status
    
- Configuration references
    

### Bad candidates

- DataFrames
    
- Large datasets
    
- Files
    
- Millions of records
    

### Follow-up

> Where should large intermediate data live?

---

# 17. Airflow Failure Recovery

## Q18. Partial pipeline failure

> An Airflow task writes 80% of its output and then fails. Airflow retries the task. What happens?

### Look for

- Idempotency
    
- Atomic writes
    
- Temporary locations
    
- Transactional writes
    
- `MERGE`
    
- Partition overwrite
    
- Checkpointing
    
- Cleanup
    
- Exactly-once/effectively-once semantics
    

---

# 18. Airflow vs Transformation Engine

## Q19. Should Airflow perform transformations?

> Airflow is being used as the transformation engine. Is this a good design?

Expected reasoning:

> Airflow is primarily an orchestrator, not the data-processing engine.

Then ask:

> What should actually perform the transformation?

Possible answers depend on architecture:

- SQL engine
    
- Spark
    
- Databricks
    
- Warehouse
    
- Pandas for genuinely small workloads
    
- Specialized processing engines
    

---

# 19. Azure Architecture

## Q20. Design the platform on Azure

> Take the enterprise data platform you designed earlier and map it onto Azure services.

Potential services:

- ADLS Gen2
    
- Azure Data Factory
    
- Azure Databricks
    
- Azure Functions
    
- Azure SQL
    
- Synapse
    
- Key Vault
    
- Azure Monitor
    
- Microsoft Entra ID
    
- Event Hubs
    
- Microsoft Purview
    
- Azure DevOps / GitHub
    

### Critical follow-up

> Why did you choose this service instead of the alternatives?

The goal is not to test Azure service memorization. Test **architectural reasoning**.

---

# 20. ADF vs Airflow

## Q21. When would you use ADF vs Airflow?

> Your organization has both Azure Data Factory and Airflow. What would you put in each?

Possible discussion:

### Airflow

- Cross-platform orchestration
    
- Complex DAGs
    
- Python-driven workflows
    
- Dependency management
    
- External-system orchestration
    

### ADF

- Azure-native ingestion
    
- Data movement
    
- Azure integration
    
- Low-code orchestration
    
- Azure-native transformations where appropriate
    

### Follow-up

> Would you ever use both in the same pipeline?

Look for nuanced reasoning rather than a rigid answer.

---

# 21. Azure Security

## Q22. Secure pipeline access

> Your pipeline needs access to ADLS, Key Vault, and Azure SQL. How would you authenticate it?

### Look for

- Managed Identity
    
- Microsoft Entra ID
    
- RBAC
    
- Key Vault
    
- Service principals where required
    
- Least privilege
    
- Secret rotation
    
- Network controls
    

### Red flag

> Store the connection string in Airflow Variables.

---

# 22. REST API Ingestion

## Q23. Design a production API ingestion pipeline

> You're ingesting data from a REST API that supports pagination, rate limiting, and incremental timestamps. Design the ingestion pipeline.

### Look for

- Pagination
    
- Authentication
    
- Rate limiting
    
- Retry
    
- Exponential backoff
    
- Incremental watermark
    
- Duplicate handling
    
- API failure recovery
    
- Schema changes
    
- Raw payload preservation
    
- Audit metadata
    
- Observability
    

### Follow-up

> Page 7 fails after pages 1–6 have already been written. What happens?

---

# 23. Data Quality

## Q24. Designing data quality into an enterprise platform

### Discuss

- Schema validation
    
- Null checks
    
- Uniqueness
    
- Referential integrity
    
- Range checks
    
- Business rules
    
- Freshness
    
- Volume anomalies
    
- Distribution anomalies
    
- Quarantine
    
- Data contracts
    
- Validation framework
    

### Critical follow-up

> Should a pipeline always fail when data quality fails?

A strong candidate should distinguish between:

- Critical failures
    
- Warnings
    
- Quarantine
    
- Partial acceptance
    
- Downstream flagging
    

---

# 24. Observability

## Q25. Power BI shows incorrect numbers

> A business user says:
> 
> "Yesterday's Power BI dashboard is showing incorrect numbers."
> 
> Walk me through how you would investigate it.

Expected reasoning:

```text
Power BI
   ↓
Semantic Model
   ↓
Warehouse
   ↓
Curated Data
   ↓
Transformation
   ↓
Pipeline
   ↓
Raw Data
   ↓
Source
```

### Look for

- Lineage
    
- Pipeline runs
    
- Data freshness
    
- Row counts
    
- Reconciliation
    
- Data quality
    
- Schema changes
    
- Recent deployments
    
- Source-system changes
    
- Transformation changes
    

This is an excellent test of operational maturity.

---

# 25. Failure and Recovery

## Q26. 2 TB pipeline fails at 90%

> Your daily pipeline processes 2 TB and fails after 90% completion. How would you restart it without processing everything again?

### Look for

- Checkpoints
    
- Partition-level processing
    
- Watermarks
    
- Idempotency
    
- Atomic writes
    
- Control tables
    
- Incremental processing
    
- Recovery metadata
    

---

# 26. Exactly-Once Semantics

## Q27. What does exactly-once mean?

Ask:

> What is the difference between at-most-once, at-least-once, and exactly-once processing?

Then:

> Can you guarantee exactly-once semantics in a distributed pipeline?

Strong candidates should recognize that "exactly once" is often achieved through combinations of:

- Transactional systems
    
- Idempotent writes
    
- Deduplication
    
- Checkpointing
    
- Atomic commits
    
- Source/target guarantees
    

---

# 27. Schema Evolution

## Q28. Source schema changes

> Your source suddenly adds a column. What should happen?

Then progressively introduce:

1. A column is removed.
    
2. A datatype changes.
    
3. A column is renamed.
    
4. A nested JSON structure changes.
    
5. A source starts sending malformed records.
    

### Look for

- Schema contracts
    
- Compatibility rules
    
- Versioning
    
- Validation
    
- Quarantine
    
- Alerting
    
- Backward compatibility
    
- Migration strategy
    

---

# 28. Unstructured Data

## Q29. Structured + unstructured platform

> Your platform receives PDFs, JSON documents, images, and CSV files. How would you design ingestion and downstream processing?

### Look for

- Raw preservation
    
- Object storage
    
- Metadata
    
- Content hashes
    
- Versioning
    
- Document extraction
    
- OCR where appropriate
    
- Processing status
    
- Cataloging
    
- Search/indexing
    
- Security
    

---

# 29. Batch vs Streaming

## Q30. When should you use streaming?

> When would you choose batch over streaming?

Follow-up:

> When does streaming become unnecessary complexity?

Good answer:

> Don't introduce streaming simply because Kafka/Event Hubs exists. The business latency requirement should justify the operational complexity.

---

# 30. Performance and Cost

## Q31. Azure costs increased 4×

> Your platform works correctly but Azure costs have increased fourfold over six months. How would you investigate?

### Look for

- Compute utilization
    
- Storage growth
    
- Query patterns
    
- Pipeline frequency
    
- Cluster sizing
    
- Idle resources
    
- Data duplication
    
- Small files
    
- Full reloads
    
- Poor partitioning
    
- Warehouse workloads
    
- Retention policies
    
- Data egress
    
- Inefficient transformations
    

---

# 31. CI/CD

## Q32. CI/CD for a Data Platform

> How would you implement CI/CD for a production data platform?

Expected flow:

```text
Git
 ↓
Pull Request
 ↓
Lint / Type Checking
 ↓
Unit Tests
 ↓
Integration Tests
 ↓
Schema / Data Contract Tests
 ↓
Build
 ↓
Deploy
 ↓
Environment Validation
 ↓
Production
```

### Follow-ups

- How do you test data pipelines?
    
- How do you manage environment-specific configuration?
    
- How do you prevent production credentials from entering source control?
    
- How do you handle database migrations?
    
- How do you roll back a broken pipeline?
    

---

# 32. Testing Data Pipelines

## Q33. How would you test a Python ETL pipeline?

### Unit tests

- Transformation logic
    
- Functions
    
- Edge cases
    

### Integration tests

- Databases
    
- APIs
    
- Storage
    

### Data quality tests

- Schema
    
- Counts
    
- Nulls
    
- Uniqueness
    
- Business rules
    

### End-to-end tests

```text
Source
  ↓
Pipeline
  ↓
Target
```

### Follow-up

> Which parts would you mock and which would you test against real infrastructure?

---

# 33. Production Debugging

## Q34. Pipeline suddenly becomes 8× slower

> Pipeline duration increased from 30 minutes to 4 hours over the last month. There were no code changes. What do you investigate?

Possible causes:

- Data volume increased
    
- Data skew
    
- Query plan changed
    
- Statistics changed
    
- Partition pruning stopped working
    
- Small-file growth
    
- API latency
    
- Source-system performance
    
- Azure resource contention
    
- Airflow scheduling delay
    
- Network issues
    
- Downstream bottleneck
    

---

# 34. CV Deep Dive — Detecting Fake Seniority

## Q35. Largest pipeline personally designed

> Tell me about the largest data pipeline you've personally designed.

Then drill into:

- How much data?
    
- How many sources?
    
- What was the SLA?
    
- What was the architecture?
    
- What was your personal contribution?
    
- How was it monitored?
    
- How did it fail?
    
- What was the biggest production incident?
    
- How did you recover?
    
- What architectural decisions did you make?
    
- What would you change today?
    

The candidate should be able to get **extremely specific**.

---

# 35. Production Incident

## Q36. Tell me about a pipeline failure in production

Follow up:

- What caused it?
    
- How did you detect it?
    
- What was the blast radius?
    
- How did you recover?
    
- How long was the outage?
    
- What did you change afterward?
    
- Did you add monitoring?
    
- Did you change the architecture?
    
- How did you prevent recurrence?
    

> [!warning] Red Flag  
> "We didn't really have production issues."

Production data systems have issues. Seniority is often revealed by how someone understands and responds to them.

---

# 36. Architecture Stress Test

## Q37. Enterprise Platform Whiteboard Exercise

> Your company has:
> 
> - 100+ relational databases
>     
> - 20 REST APIs
>     
> - CSV/Excel uploads
>     
> - JSON event data
>     
> - 5 TB/day ingestion
>     
> - Power BI consumers
>     
> - Azure as the cloud platform
>     
> - Airflow as the orchestration standard
>     
> 
> Data must be available for reporting within 2 hours.
> 
> Design the platform.

Candidate should cover:

```text
Sources
   ↓
Ingestion
   ↓
Raw / Landing
   ↓
Transformation
   ↓
Curated
   ↓
Warehouse
   ↓
Semantic Layer
   ↓
Power BI
```

Also require:

- Security
    
- Data quality
    
- Monitoring
    
- Lineage
    
- Disaster recovery
    
- Cost optimization
    
- Schema evolution
    
- Backfills
    
- Incremental processing
    
- CI/CD
    

---

# 37. Architecture Change Scenarios

After the candidate presents the architecture, introduce changes.

## Change 1 — Volume

> One source suddenly produces 10× more data.

Ask:

> What changes in your architecture?

---

## Change 2 — Latency

> Business now requires near-real-time reporting.

Ask:

> What architectural components change?

---

## Change 3 — Schema

> A critical source changes its schema unexpectedly.

Ask:

> How does the platform react?

---

## Change 4 — Corruption

> Yesterday's data was corrupted.

Ask:

> How do you recover?

---

## Change 5 — Performance

> Power BI users complain about slow dashboards.

Ask:

> Where do you investigate first?

---

## Change 6 — Cost

> Azure costs have doubled.

Ask:

> How do you identify the cause and optimize the platform?

---

# 38. Interview Scoring Framework

|Area|Weight|
|---|--:|
|Data Engineering Architecture|**25%**|
|Python|**15%**|
|Advanced SQL|**15%**|
|Azure|**15%**|
|Airflow / Orchestration|**10%**|
|Data Lake / Warehouse|**10%**|
|Data Quality / Observability|**5%**|
|API / Integration|**5%**|
|**Total**|**100%**|

---

# 39. Seniority Calibration

## Tier 1 — Excellent Senior

Can take:

> "We need an enterprise data platform."

and turn it into:

- Architecture
    
- Standards
    
- Implementation strategy
    
- Operational model
    
- Security model
    
- Reliability strategy
    
- Cost model
    
- Delivery roadmap
    

They can also explain **why** they made each decision.

---

## Tier 2 — Good Senior

Can:

- Build complex pipelines
    
- Design moderately complex architectures
    
- Debug production issues
    
- Work independently
    
- Understand platform trade-offs
    

May still require architectural direction for the largest enterprise decisions.

---

## Tier 3 — Mid-Level

Can:

- Write Python
    
- Write SQL
    
- Build Airflow DAGs
    
- Implement ETL
    
- Work with Azure services
    

But struggles with:

- Platform-wide decisions
    
- Failure modes
    
- Scalability
    
- Data contracts
    
- Governance
    
- Cost
    
- Architecture trade-offs
    

---

## Tier 4 — Backend Engineer Wearing a Data Engineer Hat

Strong in:

- Python
    
- FastAPI
    
- REST APIs
    
- Microservices
    
- OOP
    
- Backend architecture
    

But weak in:

- Data modeling
    
- Incremental processing
    
- Data Lake architecture
    
- Data Warehouse architecture
    
- ETL
    
- Data quality
    
- Orchestration
    
- Analytical workloads
    
- Data lifecycle
    
- Data platform architecture
    

> [!danger] Hiring Risk  
> For this JD, strong Python/API knowledge should **not compensate for weak Data Engineering fundamentals**.

---

# 40. Interviewer Philosophy

The most useful senior-level questions are rarely:

> "What is X?"

Instead ask:

> **Why did you choose X?**

> **What happens when X fails?**

> **How does X scale?**

> **How would you monitor X?**

> **How would you recover X?**

> **What are the trade-offs?**

> **What would make you change the design?**

> **What would you do differently today?**

These questions reveal whether the candidate has actually **owned production systems** or has simply worked with the technologies listed on their resume.

---

# Recommended Interview Flow

## Round 1 — Technical Screening

**45–60 minutes**

Focus on:

- Python
    
- SQL
    
- ETL
    
- Pandas
    
- Airflow
    
- Azure fundamentals
    

## Round 2 — Senior Data Engineering

**60 minutes**

Focus on:

- Architecture
    
- Data Lake
    
- Data Warehouse
    
- Incremental processing
    
- Data quality
    
- Performance
    
- Failure recovery
    

## Round 3 — Architecture / System Design

**60 minutes**

Use the:

> **5 TB/day Enterprise Data Platform**

whiteboard exercise.

## Round 4 — Practical Deep Dive

**45–60 minutes**

Take one project directly from the candidate's CV and interrogate it deeply.

> "You designed this. Walk me through it."

Then drill into every major architectural component.

---

# Core Principle

For this role:

> **Python is the implementation language. Data Engineering is the discipline. Architecture is the seniority test.**

The interview should therefore spend **more time asking "why?" and "what happens when it fails?" than asking Python syntax questions**.

A candidate who can write beautiful Python but cannot explain incremental loading, partitioning, idempotency, data quality, orchestration, failure recovery, Azure architecture, and analytical workloads is **not a strong fit for this particular Senior role**.