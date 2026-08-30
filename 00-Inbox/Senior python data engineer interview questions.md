# AI Summary
Comprehensive senior Python Data Engineer interview question bank for an Enterprise Data Platform role. Prioritizes Data Engineering over backend engineering and covers advanced Python, Pandas, ETL/ELT architecture, Airflow, SQL, data lakes and warehouses, Azure, API design, system design, and senior ownership. Includes production-focused scenarios around idempotency, schema evolution, failures, observability, security, cost, Power BI, and architectural tradeoffs, plus red flags for distinguishing genuine senior experience from superficial tool familiarity.

---

# Senior Python Data Engineer — Interview Question Bank

_Enterprise Data Platform role | Azure + Airflow + ETL focus, with Backend/API depth included_

No time limit assumed — this is the full loop. Suggested weighting if you need to prioritize:

- Python/Pandas (advanced) — 15%
- ETL & Pipeline Architecture — 20%
- Airflow/Orchestration — 15%
- Advanced SQL — 15%
- Data Lake/Warehouse/Analytics — 15%
- Azure — 10%
- Backend Engineering / API — 10%

Note: the JD explicitly frames this as Data Engineering-first, not Backend Engineering-first — so treat Section 7 as a secondary but real signal (candidate should be _strong_, not necessarily _expert_, on pure backend concerns), and keep Sections 1–6 as the primary bar.

---

## 1. Python for Data Engineering (Advanced, not general SWE)

1. **Pandas at scale**: Pandas loads everything into memory. Walk me through how you'd process a 40GB CSV on a machine with 16GB RAM using Pandas-adjacent tooling — what are your options (chunking, `dtype` optimization, categoricals, Dask, Polars, PyArrow), and how do you decide between them?
    
    - _Listen for_: chunked reads (`chunksize`), dtype downcasting, categorical encoding, awareness that Pandas is single-threaded/single-node, and knowing when to escalate to Spark/Dask instead of forcing Pandas.
2. **Vectorization vs. iteration**: Show me (verbally or on a whiteboard) how you'd rewrite a `df.apply(lambda row: ..., axis=1)` operation using vectorized operations. Why does this matter at enterprise scale?
    
3. **Memory management**: How do you profile memory usage in a long-running Python ETL job? Have you dealt with memory leaks in pipelines that run for hours? What tools (`memory_profiler`, `tracemalloc`, `objgraph`) have you used?
    
4. **Idempotency**: Design a Python ETL function that's safe to re-run if it fails halfway through (e.g., after loading 60% of files into a Data Lake). What patterns do you use — checkpointing, upserts, watermarking, transactional writes?
    
5. **Schema drift / evolution**: A source system silently adds a new column or changes a data type. How do you design your Python ingestion layer to detect this and either adapt or fail loudly rather than corrupting downstream data?
    
6. **Concurrency**: When would you use `asyncio` vs. `multiprocessing` vs. `threading` in a data pipeline context (e.g., pulling from 20 REST APIs vs. transforming 20 large files)? What's the GIL's practical impact on each?
    
7. **Data quality as code**: How do you implement automated data validation in Python (e.g., Great Expectations, Pandera, custom assertions) as a first-class pipeline step rather than an afterthought?
    
8. **Error handling philosophy**: In a multi-stage pipeline (extract → validate → transform → load), where do you put retry logic vs. dead-letter handling vs. hard failure? How do partial failures get communicated to downstream consumers/Power BI?
    

---

## 2. ETL / ELT Architecture

9. **ETL vs. ELT**: Given this role touches Data Lake + Data Warehouse + Power BI, when would you push transformation logic upstream (ETL, in Python) vs. downstream (ELT, in the warehouse via SQL/dbt-style)? What drove that decision in a system you've built?
    
10. **End-to-end ownership**: This role explicitly wants someone who owns "architecture and design through to implementation." Walk me through a pipeline you designed from source system → Data Lake → Data Warehouse → reporting layer. What were the architectural decision points, and what would you do differently now?
    
11. **Structured vs. unstructured**: The JD calls out working across both. How does your ingestion pattern differ for a relational source (SQL Server/Postgres CDC) vs. unstructured data (logs, PDFs, JSON blobs, emails)? Do they land in the same lake zone?
    
12. **Medallion / layered architecture**: Do you design your Data Lake with Bronze/Silver/Gold (or landing/staging/curated) zones? Justify the boundaries — what logic lives in each layer and why?
    
13. **Late-arriving / out-of-order data**: A source system backfills data three days late. How does your pipeline handle this without duplicating or silently dropping records downstream in the warehouse?
    
14. **Slowly Changing Dimensions**: How have you implemented SCD Type 2 in a pipeline feeding a Data Warehouse consumed by Power BI? Did you do it in Python, SQL, or via a framework?
    
15. **Batch vs. near-real-time**: The JD doesn't mention streaming explicitly — how do you probe whether "data availability for reporting" implies daily batch, micro-batch, or near-real-time needs, and how would your architecture change across those?
    

---

## 3. Airflow / Orchestration

16. **DAG design philosophy**: What makes a "good" DAG in your view — task granularity, idempotency, use of `XCom`, sensors vs. polling? Have you had a DAG that became unmaintainable, and what did you refactor?
    
17. **Dynamic DAGs**: How would you design a DAG that needs to process an unknown/variable number of source tables (e.g., 5 today, 50 next quarter) without hand-writing a task per table? (Dynamic task mapping, `TaskGroup`, config-driven DAG generation.)
    
18. **Failure & alerting strategy**: A downstream Power BI report is stale because an upstream Airflow task silently failed at 2 AM. How do you design SLAs, alerting (email/Slack/Teams), and retries so this doesn't happen — or is caught immediately?
    
19. **Dependency management across teams**: How do you handle cross-DAG dependencies (e.g., DAG B shouldn't run until DAG A's Gold layer is validated)? `ExternalTaskSensor`, sensors vs. datasets/Airflow 2.4+ data-aware scheduling, or an orchestration-of-orchestrators pattern?
    
20. **Compute separation**: Do you run heavy transformation logic inside the Airflow worker, or does Airflow just orchestrate (triggering Azure Data Factory, Databricks jobs, or Azure Functions) while compute happens elsewhere? Why?
    
21. **Airflow on Azure**: Have you run Airflow via Azure-managed options (e.g., self-hosted on AKS, or via Astronomer) vs. using native Azure Data Factory instead/alongside? Trade-offs?
    

---

## 4. Advanced SQL

22. **Window functions**: Write a query to find, per customer, their most recent order and the % change in order value vs. their previous order. (Tests `LAG`/`LEAD`, `PARTITION BY`, `ROW_NUMBER`.)
    
23. **Query performance**: You have a query joining a 500M-row fact table with three dimension tables that's timing out in the warehouse. Walk through your diagnostic process — execution plan reading, indexing, partitioning/clustering keys, statistics, materialized views.
    
24. **Incremental loading logic**: Write the SQL/logic pattern you'd use for an incremental MERGE/UPSERT into a warehouse table based on a watermark column, handling both inserts and updates safely.
    
25. **Deduplication at scale**: Given a staging table with duplicate records from multiple pipeline retries, write a query to identify and retain only the "correct" version (e.g., latest by timestamp) without a full table rewrite.
    
26. **Data modeling**: For Power BI consumption, do you favor a star schema, snowflake, or a wide denormalized table? Justify based on query patterns, DAX performance, and maintainability.
    
27. **CTEs vs. temp tables vs. subqueries**: When does query readability trade off against performance in your warehouse of choice, and how do you decide?
    

---

## 5. Data Lake / Data Warehouse / Analytics Platform

28. **File formats**: Why choose Parquet/Delta/ORC over CSV/JSON in a Data Lake? Talk about columnar storage, compression, schema enforcement, and how this affects downstream query cost in the warehouse.
    
29. **Partitioning strategy**: How do you decide partition keys for lake storage (e.g., by date, by source system, by region)? What's gone wrong when partitioning was designed poorly (small-file problem, partition skew)?
    
30. **Lakehouse concepts**: Are you familiar with Delta Lake / Apache Iceberg-style table formats (ACID on top of a lake)? Have you used them, and what problem did they solve for you versus a plain lake?
    
31. **Data governance & lineage**: How do you track lineage from source system to Power BI report so that when a number looks wrong, you can trace it back? Have you used Azure Purview or an equivalent catalog?
    
32. **Cost control**: Enterprise data platforms can balloon in cloud cost. What levers have you pulled to control storage + compute cost (lifecycle policies, compression, right-sizing warehouse compute, query optimization, caching for Power BI)?
    
33. **Data contracts**: How do you formalize expectations with upstream source-system owners so that schema/semantic changes don't silently break your pipeline?
    

---

## 6. Azure (Mandatory)

34. **Service selection**: Given this platform (Data Lake → Warehouse → Power BI), how would you architect it on Azure — which services (ADLS Gen2, Azure Data Factory, Synapse Analytics / Fabric, Azure Databricks, Azure SQL/Managed Instance) and why those over alternatives?
    
35. **Azure Data Factory vs. Airflow**: The JD asks specifically for Airflow experience, but Azure's native tool is ADF. Have you used both? When would you choose Airflow-orchestrating-Azure-services over going all-in on native ADF pipelines?
    
36. **Security & access**: How do you handle secrets/credentials in an Azure pipeline (Key Vault, Managed Identity) rather than hardcoding connection strings? How do you scope access to ADLS at the folder/container level for different consumer teams?
    
37. **Power BI integration specifics**: What's your experience optimizing a Data Warehouse/lakehouse layer specifically for Power BI performance — import vs. DirectQuery vs. composite models, aggregation tables, incremental refresh?
    
38. **Cost/monitoring**: How do you monitor pipeline health and cost in Azure — Azure Monitor, Log Analytics, cost alerts? Give an example of catching a runaway cost or failure before it became a problem.
    

---

## 7. Backend Engineering / API Design (Extended)

Since the role considers Python + Data Engineering + Backend jointly, and there's no time constraint, use this section to fully probe backend depth. Frame these around the platform's actual use case — APIs that feed ingestion/integration and expose curated data — rather than a generic microservices interview, so you can also judge _judgment about scope_, not just raw backend skill.

39. **API purpose in this platform**: Where would APIs sit in this architecture — pulling data in from SaaS sources, exposing curated Gold-layer data to other systems, or both? Design the contract for one of those APIs (endpoints, payload shape, auth).
    
40. **Framework choice**: FastAPI vs. Flask vs. Django REST Framework for a service that (a) triggers/monitors pipeline runs, or (b) exposes processed data. Justify your choice — async support, validation (Pydantic), performance, team velocity.
    
41. **Sync vs. async design**: When building a FastAPI service that calls a slow downstream (e.g., triggering an ADF pipeline and polling for completion), how do you design the endpoint — sync blocking call, background task, webhook callback, or a job-status polling pattern? Trade-offs of each.
    
42. **Authentication & authorization**: Design auth for an internal API that lets other teams pull curated data — API keys, OAuth2 client credentials flow, Azure AD/Entra ID integration, or mutual TLS? How do you scope permissions per consuming team/dataset?
    
43. **Pagination & large payloads**: An API endpoint exposes a dataset that can be millions of rows. How do you design pagination (offset vs. cursor-based), and how does this differ from how you'd hand the same data off via the Data Lake instead?
    
44. **Rate limiting & backpressure**: How do you protect an API (and the pipeline/database behind it) from being overwhelmed by a consuming system polling too aggressively? Where does throttling logic live?
    
45. **Idempotency in APIs**: Design a `POST /pipeline-runs` endpoint that triggers a data load. How do you prevent a network retry from triggering duplicate pipeline runs (idempotency keys, request deduplication)?
    
46. **Versioning strategy**: A consuming team depends on `/api/v1/customers`. You need to change the schema. How do you version the API and manage the deprecation of v1 without breaking downstream consumers — many of whom may be feeding Power BI or other systems?
    
47. **Testing strategy**: What's your approach to testing an API layer — unit tests for business logic, integration tests against a test database, contract testing (e.g., Pact) if multiple teams depend on the API, and how does this differ from testing a data pipeline? _(Good opportunity to probe SDET background here.)_
    
48. **Database design for OLTP vs. OLAP**: If this backend service needs its own operational database (e.g., tracking pipeline run metadata, job status, audit logs) separate from the analytical warehouse, how do you design that schema differently — normalization, indexing, transaction isolation levels?
    
49. **Observability**: How do you instrument an API for production — structured logging, correlation/trace IDs across a request that spans API → pipeline trigger → data lake write, metrics (latency, error rate), and how do you tie an API error back to a specific pipeline failure?
    
50. **Security fundamentals**: How do you protect an API surface against SQL injection, over-fetching sensitive data, and secrets leaking into logs? Where do Key Vault/Managed Identity fit into a FastAPI/Flask app running on Azure?
    
51. **Deployment & scaling**: How would you deploy and scale this API layer on Azure — App Service, Azure Functions (consumption vs. premium), AKS/containers? What drives that choice given this is a supporting service, not the core product?
    
52. **Monolith vs. service boundary**: Should the "pipeline trigger/status API" and the "data exposure API" be the same service or separate? How do you reason about service boundaries in a platform that's data-engineering-first, so you don't over-engineer a microservices architecture the team doesn't need?
    
53. **CI/CD for backend code vs. pipeline code**: Do you use the same CI/CD pattern (testing, deployment gates, environments) for the API layer as for your Airflow DAGs/ETL code, or do they diverge? Walk through your pipeline for shipping a backend change safely.
    

---

## 8. System Design / Scenario (Senior-level, whiteboard style)

54. **Full architecture prompt**: _"You're joining to build this Enterprise Data Platform from the ground up. You have five source systems: an on-prem SQL Server ERP, a SaaS CRM with a REST API, a folder of unstructured PDF invoices, a Postgres app database, and a third-party vendor dropping daily CSVs to SFTP. You also need to expose a subset of curated data via API to two internal consuming teams. Design the end-to-end architecture from ingestion to Power BI and API exposure, on Azure, orchestrated with Airflow."_

- _Evaluate_: ingestion pattern per source type, lake zoning, orchestration and dependency handling, error/alerting strategy, warehouse modeling for BI, where the API layer sits and how it's secured, and how they sequence delivery (MVP vs. full platform) — this directly probes "own delivery from architecture through implementation" plus backend judgment.

55. **Failure scenario**: "It's Monday 9 AM, executives are looking at a Power BI dashboard, and the numbers are wrong. Separately, a partner team says your API has been returning 500s since Friday. Walk me through how you triage both, and whether they're related." Tests lineage discipline, logging/observability across both pipeline and API surfaces, and calm methodical troubleshooting under pressure.
    
56. **Trade-off defense**: "A stakeholder wants real-time data in Power BI, and a partner team wants a real-time webhook instead of polling your API. Your current architecture is nightly batch with a simple REST API. How do you evaluate whether to rebuild for streaming/event-driven, or push back — and how do you communicate that trade-off to a non-technical stakeholder?" Tests architectural judgment and business communication expected at senior level.
    

---

## 9. Seniority / Ownership Signals (Behavioral, but role-specific)

57. Tell me about a time you inherited or built a data platform with no existing standards. What conventions (naming, layering, testing, CI/CD for pipelines and APIs) did you establish, and how did you get team buy-in?
58. Describe a time your architectural recommendation was overruled. How did you handle it, and were you right in hindsight?
59. How do you mentor or review the work of less senior data engineers on pipeline design — what do you look for in a code/design review that a junior wouldn't catch?
60. Tell me about a time you had to decide whether something belonged in the data pipeline layer or the backend/API layer. How did you make that call, and did it hold up?

---

## Suggested Red Flags to Watch For

- Talks about Pandas/APIs as the _primary_ skill rather than the data platform as a whole (misaligned with "Data Engineering first, not Backend Engineering").
- No mention of idempotency, schema drift, or failure handling unprompted — suggests pipelines built for demos, not production/enterprise scale.
- Can name Airflow concepts but has only orchestrated toy DAGs, not multi-team dependency chains.
- No Azure-native service knowledge beyond "I used Blob Storage" — thin on ADF/Synapse/Databricks/Key Vault specifics.
- Treats the warehouse/BI layer as someone else's problem — doesn't think about Power BI performance implications of their modeling choices.
- On backend questions: reaches for a full microservices/Kubernetes answer for what should be a small supporting API — over-engineering signal, and a mismatch with "should not be positioned as a Backend Developer role."
- Can't distinguish when logic belongs in the API vs. the pipeline vs. the warehouse — suggests weak system boundaries thinking, which matters more at senior level than raw coding speed.