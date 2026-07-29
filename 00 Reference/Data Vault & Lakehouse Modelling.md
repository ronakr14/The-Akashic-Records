# AI Summary
Why Kimball Alone Starts Failing. Based on your background (Databricks, Snowflake, PySpark, PostgreSQL, architecture-focused learning), this is the right time to study **Data Vault** and **Lakehouse Modeling**. These are where modern data architecture starts diverging from traditional Kimball dim...

```table-of-contents
```

Based on your background (Databricks, Snowflake, PySpark, PostgreSQL, architecture-focused learning), this is the right time to study **Data Vault** and **Lakehouse Modeling**. These are where modern data architecture starts diverging from traditional Kimball dimensional modeling.

One assumption I'd challenge first:

> Many engineers think Data Vault replaces Star Schema.

It doesn't.

In most mature platforms:

```text
Source Systems
      ↓
Data Vault
      ↓
Business Vault
      ↓
Star Schema / Data Marts
      ↓
Power BI / ML / APIs
```

Data Vault and Star Schema solve different problems.

---

# Why Kimball Alone Starts Failing

Imagine your Healthcare Platform.

Initially:

```text
Patient
Doctor
Appointment
Prescription
```

Easy.

Then business adds:

```text
Insurance
Claims
Lab Results
Radiology
Pharmacy
Wearables
IoT Devices
```

Then:

```text
Epic EMR
Cerner
SAP
Salesforce
External APIs
```

Then requirements change every month.

Your beautiful Star Schema starts becoming difficult to maintain.

This is the problem Data Vault tries to solve.

---

# When to Use What — Quick Decision Matrix

| Scenario | Best Fit | Why |
|---|---|---|
| Stable business requirements, reporting-heavy | **Star Schema (Kimball)** | Fast queries, intuitive for analysts |
| Multiple source systems, frequent schema changes | **Data Vault** | Absorbs change without redesign |
| Regulated industry (healthcare, finance) | **Data Vault + Business Vault** | Full audit trail, historical tracking |
| Startup, small team, rapid iteration | **Wide Tables (Lakehouse)** | Low ceremony, fast time-to-value |
| ML/AI feature engineering | **Lakehouse + Feature Store** | Direct ML consumption of silver/gold layers |
| Real-time + batch unified | **Lakehouse (Delta/Iceberg)** | ACID transactions + streaming support |

Rule of thumb: if your sources change more than once a quarter, Data Vault pays for itself. If they never change, Star Schema is simpler.

---

# What is Data Vault?

Created by Dan Linstedt.

Core idea:

> Separate business keys, relationships, and descriptive attributes.

Traditional models mix them together.

Data Vault separates them.

---

# Three Core Components

## 1. Hubs

Store business keys.

Example:

```text
Hub_Patient
```

Contains:

```text
Patient_Number
Load_Date
Record_Source
```

Only business identifiers.

Not names.

Not addresses.

Not demographics.

---

Example:

|Patient_Key|
|---|
|P1001|
|P1002|
|P1003|

That's It.

DDL example:

```sql
CREATE TABLE hub_patient (
    patient_key     VARCHAR(64)  NOT NULL,  -- hash of patient_number
    patient_number  VARCHAR(50)  NOT NULL,  -- business key from source
    load_date       TIMESTAMP    NOT NULL,
    record_source   VARCHAR(100) NOT NULL,
    CONSTRAINT pk_hub_patient PRIMARY KEY (patient_key)
);
```

---

## 2. Links

Store relationships.

Example:

```text
Patient
   |
Appointment
   |
Doctor
```

Becomes:

```text
Link_Appointment
```

|Patient_Key|Doctor_Key|
|---|---|
|P1001|D101|

Links connect hubs.

DDL example:

```sql
CREATE TABLE link_appointment (
    appointment_key  VARCHAR(64)  NOT NULL,  -- hash of composite business keys
    patient_key      VARCHAR(64)  NOT NULL,  -- FK to hub_patient
    doctor_key       VARCHAR(64)  NOT NULL,  -- FK to hub_doctor
    load_date        TIMESTAMP    NOT NULL,
    record_source    VARCHAR(100) NOT NULL,
    CONSTRAINT pk_link_appointment PRIMARY KEY (appointment_key)
);
```

---

## 3. Satellites

Store descriptive attributes.

Example:

```text
Patient Name
DOB
Gender
Address
```

goes into:

```text
Sat_Patient_Demographics
```

|Patient_Key|Name|DOB|
|---|---|---|

DDL example:

```sql
CREATE TABLE sat_patient_demographics (
    patient_key     VARCHAR(64)  NOT NULL,  -- FK to hub_patient
    load_date       TIMESTAMP    NOT NULL,
    record_source   VARCHAR(100) NOT NULL,
    name            VARCHAR(200),
    dob             DATE,
    gender          VARCHAR(20),
    address         VARCHAR(500),
    is_current      BOOLEAN      NOT NULL DEFAULT TRUE,
    valid_from      TIMESTAMP    NOT NULL,
    valid_to        TIMESTAMP,              -- NULL = current record
    hash_diff       VARCHAR(64),             -- hash of non-key columns for change detection
    CONSTRAINT pk_sat_patient_demo PRIMARY KEY (patient_key, load_date)
);
```

---

Visual:

```text
           Sat_Patient
                |
                |
Hub_Patient --- Link_Appointment --- Hub_Doctor
                                      |
                                      |
                                Sat_Doctor
```

This pattern repeats everywhere.

---

# Why Enterprises Like Data Vault

## Auditability

Every record keeps:

```text
Load Date
Source System
```

Perfect for healthcare and finance.

---

## Historical Tracking

Nothing is overwritten.

Everything is append-only.

Example:

```text
Address Change
```

Old version remains.

New version inserted.

---

## Scalability

Adding a new source:

```text
Salesforce
```

doesn't require redesigning existing models.

Just add:

```text
New Hub
New Link
New Satellite
```

---

## Parallel Development

One team builds:

```text
Patient
```

Another builds:

```text
Claims
```

No conflicts.

Very useful in large organizations.

---

# Why People Hate Data Vault

Let's be honest.

Data Vault can become ugly.

Simple query:

```sql
Get Patient Name
```

may require:

```text
Hub
+
Satellite
+
Link
+
Another Satellite
```

multiple joins.

Analysts hate this.

Power BI developers hate this.

Data Scientists hate this.

Which is why...

---

# Data Vault Is Rarely the Final Layer

Usually:

```text
Raw Vault
      ↓
Business Vault
      ↓
Star Schema
```

Users consume Star Schema.

Engineers maintain Data Vault.

---

# Mitigating Data Vault's Complexity

The join problem is real. Here's how teams address it:

| Mitigation | How It Works |
|---|---|
| **Point-to-point views** | Pre-joined views that materialize common analyst queries |
| **Information Marts** | Curated star schemas built on top of the vault (not direct access) |
| **Hash key joins** | Integer-based hash keys join faster than string business keys |
| **Business Vault pre-aggregation** | Compute common metrics in the vault layer, not at query time |
| **Data virtualization** | Tools like Denodo/Dremio auto-join vault tables at query time |

The pattern is consistent: **build the vault for integrity, expose it through simplified layers for consumption.**

---

# What is Business Vault?

Raw Vault contains raw source truth.

Business Vault contains:

```text
Business Rules
Aggregations
Calculated Logic
Reference Data
```

Think:

```text
Raw Vault = Storage

Business Vault = Business Processing
```

---

# Where Data Vault Fits in Modern Platforms

```text
SAP
Salesforce
EMR
APIs

     ↓

Bronze

     ↓

Data Vault

     ↓

Business Vault

     ↓

Gold Star Schema

     ↓

Power BI
ML
Reports
```

This is becoming common in healthcare and banking.

---

# Data Vault vs. Lakehouse — Side-by-Side

They solve different problems and are often combined, not chosen between.

| Dimension | Data Vault | Lakehouse |
|---|---|---|
| **Purpose** | Raw integration layer with full audit trail | Unified storage for analytics + ML |
| **Data Structure** | Hubs, Links, Satellites (normalized) | Bronze/Silver/Gold (layered) |
| **Query Complexity** | High (many joins) | Low to moderate (wider tables) |
| **Historical Tracking** | Built-in (append-only satellites) | Via Delta/Iceberg time travel |
| **Schema Evolution** | Add new satellite/link, no migration | Schema enforcement + evolution in catalog |
| **Best For** | Regulated data integration | Analytics, ML, reporting |
| **Consumers** | Data engineers (build) | Analysts, data scientists, ML engineers |
| **Maturity** | 1990s–2000s, proven at scale | 2020s, rapidly maturing |
| **Typical Pairing** | → feeds into Lakehouse Gold layer | ← ingests from Data Vault as Silver |

Key insight: **Data Vault is an integration pattern. Lakehouse is a storage architecture.** They coexist — Vault handles raw integration and audit, Lakehouse handles consumption and serving.

---

# Now Let's Talk Lakehouse Modeling

This is more relevant to your Databricks work.

---

# Traditional Architecture

```text
OLTP
   ↓
Data Warehouse
   ↓
Data Mart
```

Storage and compute were separate concerns.

---

# Lakehouse Idea

Combine:

```text
Data Lake
+
Data Warehouse
```

into one architecture.

Examples:

- Databricks
    
- Apache Iceberg
    
- Delta Lake
    
- Apache Hudi
    

---

# Medallion Architecture

Databricks popularized:

```text
Bronze
Silver
Gold
```

---

## **Bronze**

Raw ingestion.

Store everything.

Minimal transformations.

Example:

```text
patient_raw.json
```

---

## **Silver**

Cleaned and standardized.

Example:

```text
patient_clean
```

Rules:

- Deduplication
    
- Type casting
    
- Data quality checks
    

---

## **Gold**

Business-ready.

Example:

```text
patient_summary
appointment_metrics
claim_dashboard
```

Used by reporting and ML.

---

# Lakehouse Modeling Philosophy

Traditional modelers ask:

> What tables should I build?

Lakehouse architects ask:

> What transformations should move data through Bronze → Silver → Gold?

The focus shifts from database design to data product design.

---

# Modern Lakehouse Modeling Patterns

Today you commonly see:

### Pattern 1

```text
Bronze
 ↓
Silver
 ↓
Gold Star Schema
```

Most common.

---

### Pattern 2

```text
Bronze
 ↓
Silver
 ↓
Wide Tables
```

Popular in startups.

---

### Pattern 3

```text
Bronze
 ↓
Data Vault
 ↓
Gold Star Schema
```

Common in regulated industries.

---

### Pattern 4

```text
Bronze
 ↓
Feature Store
 ↓
ML Models
```

AI-focused architectures.

---

# What I Would Learn Next

For your career trajectory toward Senior Data Engineer → Data Architect:

### Priority 1

Master:

- **Data Vault 2.0** — the standard reference architecture (Dan Linstedt)
- **Hubs, Links, Satellites** — core structural patterns
- **Hash Keys** — MD5/SHA1-based surrogate keys for fast joins
- **Business Vault** — where raw data becomes business-meaningful

Resource: *Data Vault 2.0* by Dan Linstedt & Michael Olschimke

### Priority 2

Master:

- **Medallion Architecture** — Bronze/Silver/Gold layering pattern
- **Delta Lake internals** — ACID on object storage, time travel, compaction
- **Iceberg internals** — schema evolution, hidden partitioning, snapshot isolation
- **CDC pipelines** — Debezium, Fivetran, native database log capture
- **Incremental Loading** — watermark-based, CDC-based, snapshot-based

Resource: Databricks official docs + *Designing Data-Intensive Applications* (Martin Kleppmann)

### Priority 3

Learn:

- **Data Products** — treating data as a product with SLAs and ownership
- **Data Mesh** — domain-oriented decentralized architecture (Zhamak Dehghani)
- **Domain-driven modeling** — bounded contexts applied to data
- **Event-driven architectures** — Kafka/Event Hubs as data backbone

Resource: *Data Mesh* by Zhamak Dehghani

---

# Key Interview Questions

### Q1: "When would you choose Data Vault over a Star Schema?"

**Answer:** When source systems change frequently, auditability is required (healthcare/finance), or multiple teams need to load data independently without conflict. Star Schema is better for stable, query-optimized reporting layers.

### Q2: "What's the difference between a Link and a Satellite?"

**Answer:** A **Link** stores relationships between two or more Hubs (business key associations). A **Satellite** stores descriptive attributes that change over time, attached to a Hub or Link. Links have no descriptive data; Satellites have no business keys of their own.

### Q3: "How does Data Vault handle historical tracking?"

**Answer:** Satellites are append-only. Each insert includes `load_date` and `record_source`. Old records are never overwritten — new rows are added with newer `load_date`. Current records are typically flagged with `is_current = TRUE` or `valid_to = NULL`.

### Q4: "Why use hash keys instead of natural keys as primary keys?"

**Answer:** Hash keys (MD5/SHA1 of business keys) provide fixed-width, join-optimized keys that are: (1) deterministic across systems, (2) never affected by business key format changes, (3) faster to join than composite string keys, and (4) enable uniform key structure across all Hubs and Links.

### Q5: "How does the Medallion Architecture relate to Data Vault?"

**Answer:** They complement each other. **Bronze** = raw ingestion. **Silver** can be a Data Vault (raw integration layer). **Gold** = Business Vault + Star Schema (consumption layer). Medallion is the layering pattern; Data Vault is a modeling technique for the silver/integration layer.

### Q6: "What's the biggest drawback of Data Vault and how do you mitigate it?"

**Answer:** Query complexity — simple analytical queries require 4–8 joins across Hubs, Links, and Satellites. Mitigation: build Information Marts (star schemas on top), use point-to-point views, or pre-aggregate in the Business Vault layer.

### Q7: "What is a Business Vault vs. Raw Vault?"

**Answer:** **Raw Vault** stores source-system-faithful data with no transformation. **Business Vault** applies business rules, aggregations, calculated fields, and reference data on top of the Raw Vault. It's where raw data becomes business-meaningful.

### Q8: "How do you handle late-arriving data in Data Vault?"

**Answer:** Late-arriving records are simply new inserts into the appropriate Satellite with their actual `load_date`. The append-only model handles this naturally — no updates or deletes needed. For dimensions that arrive after facts, the Link still references the Hub; the Satellite data fills in when available.

---

My recommendation for your Healthcare Intelligence Platform would be:

```text
PostgreSQL OLTP
      ↓
CDC
      ↓
Bronze (Delta Lake)
      ↓
Raw Data Vault
      ↓
Business Vault
      ↓
Gold Star Schema
      ↓
Power BI / ML
```

That architecture gives you exposure to traditional modeling, modern lakehouse design, CDC, Data Vault, dimensional modeling, and analytics engineering—all in a single end-to-end platform that resembles what you'd encounter in a large enterprise healthcare environment.

---

## Related Notes

- [[Data Modelling]] — foundational modeling concepts (normalization, star schema, snowflake)
- [[Data Lake]] — object storage and table formats (Iceberg, Delta, Hudi)
- [[Data Mesh]] — domain-oriented decentralized data architecture
- [[Incremental Load Strategy]] — CDC and change data capture patterns
- [[Partition Strategy]] — data partitioning for performance at scale
- [[Bloom Filters]] — probabilistic lookups for join optimization
- [[Idempotency]] — exactly-once semantics in data pipelines