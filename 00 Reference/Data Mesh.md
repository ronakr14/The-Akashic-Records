```table-of-contents
```

# Data Mesh

Data Mesh is **not a technology** — it is an organizational and architectural approach to managing data at scale. It sits **above** technologies like [[Data Lake]], [[Data Warehouse]], and [[Data Lakehouse]], defining ownership, responsibility, and governance rather than storage or compute.

## Why Data Mesh Exists

As companies grow, the centralized data team model breaks:

- Central team becomes a bottleneck under hundreds of data requests
- Domain experts don't understand data engineering; data engineers don't understand business rules
- Knowledge is lost in translation (e.g., "active customer" means different things to Marketing vs the data team)
- Data quality deteriorates as the central team scales beyond its capacity

Data Mesh solves this by moving ownership to business domains — the teams that know the data best.

## The Four Principles

### 1. Domain-Oriented Ownership

Each business domain owns its data end-to-end: pipelines, quality, documentation, and SLAs — just like they own their applications.

```
Sales Domain          Marketing Domain
  ├── Orders            ├── Campaigns
  ├── Customers         ├── Leads
  └── Revenue           └── Attribution

Owned by Sales Team    Owned by Marketing Team
```

### 2. Data as a Product

Treat every dataset like a software product. Each data product should have:

| Attribute | Example |
|---|---|
| **Owner** | Marketing Analytics Team |
| **Description** | "Customer 360 — unified profile across touchpoints" |
| **Business definition** | "Active = purchased within 90 days" |
| **Refresh frequency** | Hourly |
| **Data quality score** | 98.5% |
| **Contact** | marketing-data@company.com |
| **Version** | v2.1 |

### 3. Self-Service Data Platform

Domains should not build infrastructure from scratch. A platform team provides the underlying capabilities:

- Storage, compute, catalog, monitoring
- CI/CD for pipelines
- Governance tooling
- Security and access control

This is the "AWS for internal data teams" — enabling domains to focus on their data products, not plumbing.

### 4. Federated Governance

Governance standards are set centrally; implementation is decentralized.

**Central rules**: [[PII]] must be encrypted, [[GDPR]] compliance, naming standards, retention policies.

**Decentralized execution**: each domain applies these rules independently to their own data products.

## Architecture

```
              Platform Team
     (Self-Service Infrastructure)
                    |
    ┌───────────────┼───────────────┐
    |               |               |
Sales Domain   Marketing Domain   Finance Domain
    |               |               |
Sales Data     Campaign Data    Revenue Data
    Product        Product        Product
    └───────────────┬───────────────┘
                    |
         Data Discovery Layer
         (Catalog + Governance)
```

## Data Mesh vs Related Concepts

A common misconception is that Data Mesh replaces [[Data Lake]], [[Data Warehouse]], or [[Data Lakehouse]]. It does not — it defines **who owns and operates** data, while those technologies define **how data is stored and processed**.

| | Technology | Focus |
|---|---|---|
| **Data Lake** | [[S3]], [[ADLS]], [[GCS]] | Centralized storage |
| **Data Warehouse** | [[Snowflake]], [[BigQuery]], [[Redshift]] | Centralized analytics |
| **Data Lakehouse** | [[Databricks]], [[Delta Lake]], [[Apache Iceberg]], [[Apache Hudi]] | Unified batch + streaming with [[ACID]] |
| **Data Mesh** | Organizational pattern | Decentralized ownership + governance |

A modern enterprise platform typically combines all four:

```
Data Mesh (ownership model)
    + Lakehouse (technology layer)
    = Modern Enterprise Data Platform
```

## Maturity Model

Data Mesh is a **Stage 4–5 maturity** pattern, not a starting point. Most organizations fail by skipping prerequisites.

```
Stage 1: Operational Databases
    ↓
Stage 2: Central Data Warehouse
    ↓
Stage 3: Data Lake / Lakehouse
    ↓
Stage 4: Data Products
    ↓
Stage 5: Data Mesh
```

**Prerequisites before attempting Data Mesh:**

- [[Data Catalog]] with discoverability
- [[Data Governance]] framework (ownership, lineage, quality)
- Platform engineering (self-service infrastructure)
- [[Data Contracts]] between producers and consumers
- [[Data Quality]] monitoring and alerting
- CI/CD for data pipelines

## Anti-Patterns

- **"We reorganized our data lake and now we're doing Data Mesh"** — renaming centralized teams is not decentralization
- **No platform team** — domains end up rebuilding the same infrastructure independently
- **Domains without data engineering skills** — ownership without capability leads to worse outcomes
- **Skipping data products** — jumping to "mesh" without first treating datasets as products with owners, SLAs, and quality metrics
- **Governance theater** — publishing standards that no one enforces or can enforce

## Related

- [[Data Lakehouse]]
- [[Data Lake]]
- [[Data Warehouse]]
- [[Data Products]]
- [[Data Contracts]]
- [[Data Governance]]
- [[Data Catalog]]
- [[Delta Lake]]
- [[Apache Iceberg]]
- [[Dimensional Modeling]]
- [[Data Vault]]
