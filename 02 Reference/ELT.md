---
type: concept
---

# ELT

```table-of-contents
```

> **ELT:** Store the data first, then clean it.

---

## The Pattern

```text
Source Systems
      ↓
   Extract
      ↓
     Load
      ↓
 Data Warehouse
      ↓
  Transform
      ↓
Analytics Tables
```

**Extract → Load → Transform**

Move everything to the new house first. Organize and clean it inside the new house.

---

## Real Example

Suppose you run an ecommerce company. Data comes from:

- Website
- Mobile App
- Payment Gateway
- CRM
- Marketing Platform

### Raw Data

Website:

| user_id | country |
| ------- | ------- |
| 1       | India   |
| 2       | USA     |

Orders:

| user_id | amount |
| ------- | ------ |
| 1       | 1000   |
| 2       | 2000   |

### ELT in Action

Load everything first. Warehouse contains:

```text
raw.website
raw.orders
raw.crm
raw.payments
```

Then transformations happen inside the warehouse using SQL:

```sql
SELECT
    w.user_id,
    w.country,
    o.amount
FROM raw.website w
JOIN raw.orders o
ON w.user_id = o.user_id;
```

Result becomes:

```text
analytics.customer_orders
```

---

## Why ELT Became Popular

Cloud changed everything. Modern warehouses became extremely powerful:

- Snowflake
- Databricks
- Google BigQuery
- Amazon Redshift

Now warehouses can process terabytes or petabytes directly. So:

```text
Why transform outside?
Just load first and transform inside.
```

This created ELT.

---

## ETL vs ELT

| Dimension | ETL | ELT |
|---|---|---|
| Order | Extract → Transform → Load | Extract → Load → Transform |
| Transform location | Middleware / ETL server | Warehouse / lakehouse |
| Raw data preserved | Usually discarded after transform | Kept in raw layer |
| Flexibility | Fixed schema-on-write | Schema-on-read, re-transform later |
| Best for | Legacy warehouses, small compute | Cloud warehouses, elastic compute |
| Latency | Transform happens before load | Load is instant, transform is async |
| Tooling | Informatica, Talend, SSIS | dbt, Airflow, Dataform |

→ **Risk:** Choosing ETL for a cloud warehouse wastes compute. Choosing ELT for a legacy warehouse overwhelms it.

---

## Medallion Architecture (Bronze / Silver / Gold)

The standard ELT pattern in modern lakehouses:

```text
Bronze (Raw)
    ↓
Silver (Cleaned)
    ↓
Gold (Business)
```

### Bronze — Raw Ingestion

- Exact copy of source data
- No transformations, no filtering
- Schema-on-read
- Append-only or snapshot
- Purpose: data lineage, reprocessing

### Silver — Cleaned & Enriched

- Schema applied
- Nulls handled
- Deduplication
- Basic joins (e.g., enrich orders with customer data)
- PII masking applied
- Purpose: single source of truth for analysts

### Gold — Business Logic

- Aggregations
- Business rules (revenue recognition, cohorting)
- Feature engineering for ML
- Star schema / dimensional models
- Purpose: dashboards, ML, ad-hoc queries

→ **Risk:** Skipping silver and going bronze → gold creates inconsistent definitions across teams. Everyone interprets raw data differently.

---

## ELT Advantages

### Fast Ingestion

Load first. Transform later. Source systems are not bottlenecked by complex transformations.

### Keep Raw Data

Huge benefit. If requirements change:

```text
Re-run transformation
```

No need to pull data again. Raw data is always there.

### Better for AI and Analytics

Data scientists often need raw data. ELT preserves it.

### Scales Easily

Warehouse compute handles transformations. Elastic scaling — pay for what you use.

### Flexibility

Same raw data can serve multiple transformation pipelines for different teams.

---

## ELT Disadvantages

### Higher Storage Cost

Raw + transformed data coexist. Storage is cheap but not free.

### Governance Required

Bad data enters the warehouse. Need:

- Data quality checks
- Monitoring
- Lineage tracking

### Security Challenges

Sensitive data may already be stored. Must control access carefully — raw tables often contain PII.

### Transform Complexity

Without discipline, transforms become tangled. "Transform later" can become "transform never" without proper orchestration.

---

## Modern ELT Tooling

### Ingestion (Extract + Load)

| Tool | Type | Best For |
|---|---|---|
| Fivetran | Managed | SaaS sources, low engineering overhead |
| Airbyte | Open-source / Managed | Custom sources, cost-sensitive |
| Stitch | Managed | Simple pipelines, small teams |
| Custom (Spark, Python) | DIY | Complex sources, high volume |

### Transformation

| Tool | Type | Best For |
|---|---|---|
| dbt | SQL-first | Analytics engineers, version-controlled SQL |
| Dataform | SQL-first | GCP-native teams |
| Custom SQL | DIY | Simple transformations |

### Orchestration

| Tool | Type | Best For |
|---|---|---|
| Airflow | Open-source | Complex DAGs, multi-step pipelines |
| Dagster | Open-source | Data-aware orchestration, testing |
| Prefect | Open-source | Python-native, simple setup |
| Managed (MWAA, Cloud Composer) | Managed | Teams wanting no infra overhead |

→ **Risk:** Tool sprawl. Picking a different tool for each layer creates integration debt. Prefer a unified ecosystem (e.g., Airbyte + dbt + Airflow).

---

## Data Quality in ELT

ELT means bad data lands in your warehouse. Quality must be built in.

### Where to Test

| Layer | What to Test |
|---|---|
| Bronze → Silver | Schema conformance, null rates, freshness |
| Silver → Gold | Business rule validation, referential integrity, uniqueness |
| Gold (output) | Aggregate consistency, cross-table reconciliation |

### Tools

- **dbt tests** — built-in (unique, not_null, relationships, accepted_values)
- **Great Expectations** — comprehensive validation framework
- **Soda** — data quality checks as code
- **Monte Carlo / Anomalo** — automated anomaly detection

### Key Principles

- Test at every layer boundary
- Fail the pipeline on critical violations
- Log warnings on non-critical violations
- Track quality metrics over time

→ **Risk:** No quality gates = silent data corruption. Downstream consumers lose trust, and nobody knows why.

---

## When to Choose ETL vs ELT

### Choose ETL when:

- Source warehouse has limited compute
- Data must be anonymized before landing (GDPR, HIPAA)
- You need only a narrow subset of source data
- Legacy systems with fixed schemas
- Latency requirements are sub-second

### Choose ELT when:

- Using a cloud warehouse (Snowflake, BigQuery, Databricks)
- You want to preserve raw data for future use
- Multiple teams need different views of the same data
- Requirements are evolving
- You have strong orchestration and testing practices

### Hybrid Approach

Many real-world pipelines use both:

```text
ETL (light) → Load → ELT (heavy)
```

- ETL: filter sensitive fields, basic validation
- Load: land in warehouse
- ELT: business logic, aggregations, modeling

---

## Monitoring & Observability

### What to Track

| Metric | Why It Matters |
|---|---|
| Pipeline success/failure rate | Basic health |
| Freshness (time since last load) | SLA compliance |
| Row count anomalies | Detect silent data loss |
| Schema changes | Catch breaking changes early |
| Transform duration | Performance degradation |
| Quality test failures | Data reliability |
| Lineage | Impact analysis when things break |

### Alerting Strategy

- **Critical:** Pipeline down, quality test failure on gold layer → page on-call
- **Warning:** Freshness SLA at risk, quality test failure on silver → Slack alert
- **Info:** Schema change detected, transform duration increased 2× → dashboard

---

## Common Anti-Patterns

| Anti-Pattern | Problem | Fix |
|---|---|---|
| No raw layer | Can't reprocess when logic changes | Always keep bronze |
| Gold-only transforms | Inconsistent definitions across teams | Enforce silver as single source of truth |
| No tests | Silent data corruption | Add quality gates at every boundary |
| Monolithic transform | Hard to debug, slow to run | Break into layered, idempotent steps |
| "Transform later" forever | Raw data accumulates, nobody trusts it | Schedule regular transform jobs |
| PII in raw layer | Compliance violation | Mask or filter at ingestion boundary |
