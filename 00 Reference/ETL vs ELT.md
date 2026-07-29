# AI Summary
None. | Aspect | ETL | ELT |

```table-of-contents
```

## ETL vs ELT — The Core Difference

| Aspect | ETL | ELT |
|--------|-----|-----|
| Order | Extract → Transform → Load | Extract → Load → Transform |
| Transform location | External engine (Spark, Informatica) | Inside the warehouse/lakehouse |
| Data arrives clean | Yes | No — raw first, transformed later |
| Requires knowing transforms upfront | Yes | No — transform after exploring |
| Typical tools | Informatica, Talend, SSIS | Fivetran, Airbyte, dbt, Spark |

---

## Modern Stack — Why ELT Became Dominant

Today most companies use:

```text
Sources
   ↓
Fivetran / Airbyte
   ↓
Raw Layer
   ↓
Snowflake / Databricks / BigQuery
   ↓
dbt Transformations
   ↓
Analytics Layer
```

Modern cloud warehouses and lakehouses provide massive scalable compute, making it efficient to load raw data first and transform later.

**ELT is generally preferred** in modern cloud data platforms.

**ETL is still common when:**

- Sensitive data must be masked before storage
- Legacy systems are involved
- Regulatory requirements demand preprocessing

---

## ETL Fundamentals — 5 Layers

Think of ETL as 5 layers:

```text
1. Data Movement
2. Data Transformation
3. Data Loading
4. Data Reliability
5. Data Lifecycle
```

Most people only study layers 1–3. Senior engineers focus on 4–5.

---

## Core Concepts — 19 Topics That Cover ETL/ELT End-to-End

### Pipeline Mechanics
- Extraction methods (API, DB query, file)
- Loading (full refresh, incremental, upsert)
- Transformations (aggregation, join, pivot, dedup)
- Incremental processing
- CDC (Change Data Capture) & watermarking
- Deletes (soft vs hard)
- Backfills

### Reliability
- Idempotency
- Exactly-once processing
- Error handling
- Data quality validation

### Operations
- Metadata & lineage
- SLAs
- Push vs Pull architectures
- Data integration patterns

---

## ETL/ELT Ecosystem

Think of ETL as sitting in the center of a larger ecosystem:

```text
           Data Modeling
                 ↑
                 |
Observability ← ETL → Orchestration
                 |
                 ↓
      Storage & Compute
```

---

## Related Sub-Topics

ETL/ELT fundamentals connect to:

- Data modeling
- SQL topics
- Data warehousing
- [[Spark]] concepts
- Streaming systems
- Orchestration
- Data quality & observability
- System design
- Senior-level architecture topics

---

## Interview Rule of Thumb

If someone asks "Which is preferred today?"

> ELT is generally preferred in modern cloud data platforms because warehouses and lakehouses provide massive scalable compute, making it efficient to load raw data first and transform later. ETL remains important for compliance, security, and legacy environments.

---

## See Also

- [[Data Modelling]]
- [[Data Engineering]]
- [[Apache Spark]]
- [[00 Reference/DuckDB]]
- [[Medallion Architecture]]
- [[Debezium]]
