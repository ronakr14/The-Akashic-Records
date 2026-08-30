---
domain: architecture
subdomain: data-modelling
note_type: tutorial
source_type: self
status: evergreen
level: advanced
tags:
  - database-design
  - system-design
---
# AI Summary
Comprehensive framework for designing data models from a senior engineer's perspective. Introduces a six-layer methodology covering read/write patterns, business understanding, domain discovery, data engineering concerns, analytics design, and architecture, followed by architect-level considerations and a reusable project checklist. Emphasizes asking the right questions before creating tables, helping engineers build scalable, maintainable, and business-aligned data models across operational and analytical systems.

---
> This is exactly the question that separates a junior engineer from a senior one.
>
> Most engineers jump into: *"Let's create tables."*
>
> Experienced data modelers start with: *"What problem are we solving, and what assumptions are we making?"*
>
> For any project, mentally walk through these six layers before drawing a single table.

---

## Layer 0: Read/Write Patterns

This layer is often skipped — but it drives indexing, partitioning, and storage decisions more than volume alone.

- **What is the expected read/write ratio?**
    - Read-heavy (100:1) → denormalize aggressively, cache, use read replicas
    - Write-heavy (1:100) → normalize, batch writes, consider append-only
    - Balanced → design for both, avoid extremes

- **What is the query frequency?**
    - Hundreds/sec → need indexing, possibly materialized views
    - Thousands/sec → consider pre-aggregation or CQRS
    - Millions/sec → stream processing, hot partitioning

- **What are the concurrency expectations?**
    - Single-user → simple locking sufficient
    - Multi-tenant → row-level isolation, tenant-aware partitioning

- **What is the SLA for freshness?**
    - Seconds → streaming / CDC
    - Minutes → microbatch
    - Hours → batch ETL

→ **Risk:** Skipping this leads to either over-engineered batch pipelines for real-time needs, or OLTP schemas that collapse under analytical queries.

---

## Layer 1: Business Understanding

Before drawing a single table, answer:

### Why does this system exist?

Examples:

- Patient management
- Claims processing
- Customer analytics
- Fraud detection
- Order fulfillment

If you can't explain the business purpose in one sentence, don't start modeling.

### What decisions will be made using this data?

Examples:

- Operational decisions
- Strategic decisions
- Regulatory reporting
- Machine learning

Different decisions require different models.

### Who are the users?

Examples:

- Doctors
- Patients
- Operations teams
- Finance
- Analysts
- Data Scientists

Different users have different needs.

### What are the key business processes?

Example Healthcare:

- Patient Registration
- Appointment Booking
- Consultation
- Billing
- Insurance Claim

Example E-commerce:

- Product Catalog
- Cart / Checkout
- Payment
- Shipping
- Returns

Usually processes become major entities.

---

## Layer 2: Domain Discovery

This is where modeling actually begins.

### What are the core business entities?

Example Healthcare:

```text
Patient
Doctor
Appointment
Claim
Prescription
Invoice
```

Example E-commerce:

```text
Customer
Product
Order
Payment
Shipment
Review
```

### What uniquely identifies each entity?

Examples:

```text
PatientID
DoctorID
AppointmentID
ClaimID
```

Never assume business names are unique.

### What attributes belong to each entity?

Patient:

```text
FirstName
LastName
DOB
Gender
Phone
```

### What are the relationships?

Examples:

```text
Patient → Appointment
Doctor → Appointment
Appointment → Prescription
Patient → Insurance Policy
```

Draw these before creating tables.

### What are the cardinalities?

Ask:

```text
One-to-One?
One-to-Many?
Many-to-Many?
```

Example:

```text
Patient → Appointments
1 : Many
```

→ **Risk:** Undefined cardinalities produce fan-out joins, missing junction tables, and ambiguous foreign keys.

---

## Layer 3: Data Engineering Questions

This is where many business analysts stop and data engineers begin.

### What is the expected volume?

Examples:

```text
100 rows/day
10 million rows/day
1 billion events/day
```

Volume changes design decisions.

### How fast does data arrive?

```text
Batch?
Microbatch?
Streaming?
Real-time?
```

### How long must data be retained?

Examples:

```text
30 days
7 years
Forever
```

Healthcare and finance often require long retention.

### What is the growth rate?

Today:

```text
100 GB
```

Future:

```text
10 TB
```

Plan ahead.

### Which fields are frequently searched?

Examples:

```text
PatientID
OrderID
Email
ClaimNumber
```

Useful for indexing strategy.

### What data quality expectations exist?

- Are duplicates acceptable?
- Is null handling defined per field?
- Are there uniqueness constraints beyond primary keys?
- What happens on late-arriving data?

### Is any field PII or sensitive?

Examples:

```text
SSN / Aadhaar
Credit card numbers
Medical records
Email / Phone
```

→ Drives encryption, masking, column-level access control, and compliance classification.

### What are the idempotency requirements?

- Can the same event be processed twice safely?
- Is upsert semantics defined?
- Are there deduplication windows?

→ **Risk:** Missing quality and PII analysis leads to regulatory violations, silent data corruption, and expensive retrofits.

---

## Layer 4: Analytics Questions

Critical for warehouses. (Assumes dimensional modeling — Kimball-style. For Data Vault or OBT, adapt accordingly.)

### What business questions must be answered?

Examples:

```text
Revenue by month
Appointments by doctor
Claim approval rates
Patient retention
```

Model should support these naturally.

### What metrics matter?

Examples:

```text
Revenue
Cost
Profit
Appointment Count
Claim Amount
```

These often become fact table measures.

### What dimensions matter?

Examples:

```text
Date
Patient
Doctor
Location
Department
```

These become dimensions.

### What is the grain?

The most important question.

#### What does one row represent?

Examples:

```text
One appointment
One order
One claim
One transaction
```

Never skip this.

→ **Risk:** Most warehouse disasters happen because grain wasn't defined — leading to double-counting, ambiguous joins, and unreproducible reports.

### Is historical tracking required?

Example:

Doctor changes department.

Need:

```text
Current department only?
```

or

```text
Full history?
```

This determines Slowly Changing Dimensions (SCD Type 1/2/3/6).

---

## Layer 5: Architecture Questions

This is where architects spend most of their time.

### Is this OLTP or OLAP?

- Operational system → normalized, write-optimized
- Analytical system → denormalized, read-optimized
- Hybrid (HTAP) → separate stores or CQRS pattern

Different answers produce different models.

### Will data come from multiple systems?

Example:

```text
CRM
ERP
Billing
Hospital Management
```

Need master data strategy and entity resolution.

### Are there regulatory requirements?

Healthcare:

```text
HIPAA
GDPR
```

Financial:

```text
SOX
PCI-DSS
```

Can influence design heavily (encryption, audit trails, retention policies).

### Is auditability required?

Can we answer:

```text
Who changed what?
When?
Why?
```

Many enterprises require this → drives audit columns, append-only patterns, or temporal tables.

### Is data shared across domains or teams?

- Single team → schema ownership is simple
- Cross-domain → need data contracts, schema registry, ownership boundaries

→ **Risk:** Skipping architecture questions leads to tightly coupled systems, data silos, and painful migration when requirements change.

---

## Architect-Level Addition

As you move toward Data Architect, add these cross-cutting concerns:

### Business Layer

- Why are we collecting this data?
- What is the cost of being wrong?
- What is the cost of being late?

### Information Layer

- How should it be represented?
- Are there industry-standard models (HL7, ACORD, etc.)?
- What is the canonical representation?

### Integration Layer

- How does it connect with other systems?
- What are the interface contracts?
- Is event-driven or request-driven the right pattern?

### Storage Layer

- Where does it live? (warehouse, lake, lakehouse, operational store)
- What partitioning strategy fits the access pattern?
- What are the backup and disaster recovery requirements?

### Consumption Layer

- How will users consume it? (BI, API, ML, ad-hoc SQL)
- What are the latency requirements per consumer?
- Is self-service access possible or required?

### Governance Layer

- Who owns it?
- Who can access it?
- How is quality enforced? (monitoring, alerts, SLAs)
- How is lineage tracked?
- What is the deprecation policy?

---

## Quick Reference Card

Use this when you need a fast checklist. Each item maps to its layer.

- [ ] Business objective defined (Layer 1)
- [ ] Main users identified (Layer 1)
- [ ] Core business processes mapped (Layer 1)
- [ ] Core entities listed (Layer 2)
- [ ] Entity relationships drawn (Layer 2)
- [ ] Business keys identified (Layer 2)
- [ ] Cardinalities defined (Layer 2)
- [ ] Read/write patterns understood (Layer 0)
- [ ] Data volume estimated (Layer 3)
- [ ] Data velocity classified (Layer 3)
- [ ] Retention period defined (Layer 3)
- [ ] PII/sensitive fields classified (Layer 3)
- [ ] Data quality expectations agreed (Layer 3)
- [ ] Reporting requirements documented (Layer 4)
- [ ] Metrics required (Layer 4)
- [ ] Dimensions required (Layer 4)
- [ ] Grain definition agreed (Layer 4)
- [ ] Historical tracking needs (Layer 4)
- [ ] OLTP vs OLAP decided (Layer 5)
- [ ] Multi-system integration planned (Layer 5)
- [ ] Compliance requirements listed (Layer 5)
- [ ] Auditability designed (Layer 5)
- [ ] Governance ownership assigned (Architect)

If any of these are unknown, the model is incomplete.

---

Changing requirements after modeling is far more expensive than spending a few extra days asking the right questions upfront. This approach is used in large healthcare, banking, and insurance platforms — and it scales to any domain.
