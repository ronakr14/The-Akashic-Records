```table-of-contents
```

Let's approach this the way I'd explain it to a new data engineer joining a project.

## What is Data Modeling?

Data modeling is the process of deciding:

> "What data do we need, how is it related, and how should it be stored so that the business can use it effectively?"

Think of it like designing a city before building roads, houses, and offices.

Without a blueprint:

- Data gets duplicated
- Reports become inconsistent
- Applications become difficult to maintain
- Performance becomes poor

A data model is the blueprint of your data.

---

## Simple Example

Imagine you run a hospital.

You need to store:

- Patients
- Doctors
- Appointments

A fresher might think:

|Patient Name|Doctor Name|Appointment Date|
|---|---|---|
|John|Smith|2026-06-21|
|John|Smith|2026-06-25|
|Mary|Brown|2026-06-21|

Looks fine initially.

But problems appear:

- What if Doctor Smith changes departments?
- What if John has 100 appointments?
- What if you want doctor details separately?

Now we model properly.

### Patient Table

|PatientID|Name|
|---|---|
|1|John|
|2|Mary|

### Doctor Table

|DoctorID|Name|
|---|---|
|101|Smith|
|102|Brown|

### Appointment Table

|AppointmentID|PatientID|DoctorID|Date|
|---|---|---|---|
|1001|1|101|2026-06-21|
|1002|1|101|2026-06-25|

This is data modeling.

---

## Why Data Modeling Matters

As a Data Engineer, your job is not just moving data.

Your job is ensuring:

- Correctness
- Scalability
- Performance
- Maintainability

Bad data model = expensive project.

I've seen projects where:

- ETL was perfect
- Infrastructure was perfect
- Reports were wrong

Reason?

Bad data model.

---

## Three Levels of Data Modeling

This is asked in interviews frequently.

### 1. Conceptual Model

Business view.

Very high level.

Example:

```
Patient
Doctor
Appointment
Hospital
Insurance
```

Only business entities.

No columns.

No data types.

No database details.

Question answered:

> "What business objects exist?"

---

### 2. Logical Model

More detailed.

Example:

```
Patient
-------
PatientID
FirstName
LastName
DOB

Doctor
------
DoctorID
Name
Specialization

Appointment
-----------
AppointmentID
PatientID
DoctorID
AppointmentDate
```

Still database independent.

Question answered:

> "What attributes and relationships exist?"

---

### 3. Physical Model

Database implementation.

Example PostgreSQL:

```sql
CREATE TABLE patient (
    patient_id BIGINT PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    dob DATE
);
```

Includes:

- Datatypes
- Indexes
- Constraints
- Partitioning

Question answered:

> "How exactly will it be stored?"

---

## Core Concepts

### ER Diagrams

ER (Entity-Relationship) diagrams visualize models before building them.

```
+-------------+       +-------------+       +-------------+
|  Patient    |       |  Doctor     |       | Appointment |
|-------------|       |-------------|       |-------------|
| PatientID PK|       | DoctorID PK |       | ApptID PK   |
| FirstName   |       | Name        |       | PatientID FK|
| LastName    |       | Specialization|     | DoctorID FK |
| DOB         |       +-------------+       | Date        |
+-------------+                           +-------------+
      |                                       |
      +-------- 1:N --------+-------- N:1 -----+
```

Tools: dbdiagram.io, Lucidchart, draw.io, ERwin.

---

### Entities

An entity is something we want to store data about.

Examples:

- Customer
- Product
- Employee
- Patient

Entity → Table

Example:

```
Customer
```

becomes

```sql
customer
```

---

### Attributes

Attributes describe an entity.

Example:

Customer

- CustomerID
- Name
- Email
- Phone

These become columns.

```sql
customer
(
 customer_id,
 name,
 email,
 phone
)
```

---

### Relationships

The most important concept.

#### One-to-One

```
Person
   |
Passport
```

One person has one passport.

---

#### One-to-Many

```
Customer
    |
Orders
```

One customer can have many orders.

Most common relationship.

---

#### Many-to-Many

```
Students
    |
Courses
```

One student takes many courses.

One course has many students.

Need a bridge table.

```
student_course
```

---

### Keys

Very important.

#### Primary Key

Uniquely identifies a record.

```sql
customer_id
```

Example:

|CustomerID|
|---|
|1|
|2|
|3|

No duplicates.

---

#### Foreign Key

Connects tables.

```sql
order.customer_id
```

references

```sql
customer.customer_id
```

This creates relationships.

---

### Normalization

A huge topic.

Purpose:

> Reduce redundancy and improve consistency.

Bad design:

|CustomerID|CustomerName|City|
|---|---|---|
|1|John|Rotterdam|
|1|John|Rotterdam|

Data duplicated.

Good design:

Customer Table

|CustomerID|Name|
|---|---|
|1|John|

City Table

|CityID|City|
|---|---|
|10|Rotterdam|

Less duplication.

#### Normal Forms

| Form | Rule |
|------|------|
| 1NF | No repeating groups; atomic values only |
| 2NF | 1NF + no partial dependency on composite key |
| 3NF | 2NF + no transitive dependency |
| BCNF | Every determinant is a candidate key |

Most OLTP systems target 3NF. Warehouses often denormalize intentionally.

---

## OLTP vs OLAP — Modeling Approaches

As a Data Engineer you'll work with both.

### OLTP (Application Databases)

Examples:

- Banking
- Healthcare
- Ecommerce

Goal:

```
Fast inserts
Fast updates
Data integrity
```

Model:

```
Highly normalized
```

Example:

PostgreSQL
MySQL
SQL Server

---

### OLAP (Analytics)

Examples:

- Power BI
- Tableau
- Data Warehouse

Goal:

```
Fast reporting
Fast aggregation
```

Model:

```
Denormalized
```

Example:

Snowflake
Databricks
BigQuery
Redshift

---

## Dimensional Modeling

### Star Schema

Most common warehouse model.

Example Sales Warehouse

#### Fact Table

```
fact_sales
```

Contains:

- Quantity
- Revenue
- Cost

Example:

|ProductID|CustomerID|Revenue|
|---|---|---|
|10|100|500|

---

#### Dimension Tables

```
dim_product
dim_customer
dim_date
```

Example:

Product dimension:

|ProductID|ProductName|
|---|---|
|10|Laptop|

Fact stores measurements.

Dimensions store descriptions.

---

Visual:

```
          dim_product

               |
               |
dim_customer - fact_sales - dim_date
               |
               |
          dim_store
```

Looks like a star.

Hence Star Schema.

---

### Snowflake Schema

Normalized version of Star Schema.

Example:

```
dim_product
      |
dim_category
```

Less duplication.

More joins.

Usually slower for analytics.

Most modern warehouses prefer Star Schema.

---

### Slowly Changing Dimensions (SCD)

Dimensions change over time — how do we handle it?

| Type | Strategy | Use Case |
|------|----------|----------|
| SCD Type 1 | Overwrite old value | Typos, corrections |
| SCD Type 2 | Add new row with version/date | Full history tracking |
| SCD Type 3 | Add "previous value" column | Limited history |

**SCD Type 2** is the most common in data warehouses:

|CustomerID|Name|City|ValidFrom|ValidTo|IsCurrent|
|---|---|---|---|---|---|
|1|John|Rotterdam|2024-01-01|2025-06-30|0|
|1|John|Amsterdam|2025-07-01|9999-12-31|1|

---

### Data Vault

Alternative to Star Schema — designed for enterprise data warehouses with high change velocity.

Three building blocks:

| Component | Purpose |
|-----------|---------|
| **Hub** | Business key (e.g. CustomerID) |
| **Link** | Relationship between hubs (e.g. Order-Customer) |
| **Satellite** | Descriptive attributes + history (e.g. Customer details) |

```
       +------------------+
       |  Sat_Customer    |
       | (name, address)  |
       +--------+---------+
                |
+-------+   +---+----+   +-------+
| Hub   +--+ Link   +--+ Hub   |
| Cust  |  | OrdCust|  | Ord   |
+-------+  +--------+  +-------+
```

Pros: Highly auditable, scalable, handles change well.
Cons: More joins, harder to query for business users.

---

### Lakehouse Modeling

Modern approach combining data lake flexibility with warehouse structure.

| Technology | Purpose |
|------------|---------|
| Delta Lake | ACID transactions on data lake (Databricks) |
| Apache Iceberg | Open table format (Netflix, used by Snowflake/BigQuery) |
| Apache Hudi | Stream-friendly incremental processing |

Key features:
- Schema enforcement + evolution
- Time travel (query historical snapshots)
- Partitioning + clustering

---

## Data Modeling in Real Projects

When I start a project, I usually ask:

### Business Questions

What are we solving?

Examples:

- Revenue reporting?
- Patient tracking?
- Fraud detection?

---

### Grain

Most important warehouse question.

What does one row represent?

Examples:

```
One sale
One appointment
One claim
One click
```

Never start building facts without defining grain.

**Bad:** Mixing daily and hourly grain in the same fact table → metrics double-count.

**Good:** Explicit grain definition → `fact_sales_daily`, `fact_clicks_hourly`.

---

### Entities

Identify:

- Customer
- Product
- Order
- Patient
- Doctor

---

### Relationships

Map:

```
Customer → Orders
Doctor → Appointments
Patient → Claims
```

---

### Design

Choose:

- Normalized OLTP
- Star Schema
- Data Vault
- Lakehouse

based on use case.

---

## Common Mistakes (Junior Engineers)

### Mistake 1

Building tables before understanding business.

Wrong.

Business first.

Database second.

---

### Mistake 2

Ignoring grain.

Results in duplicate metrics.

---

### Mistake 3

Using natural keys everywhere.

Bad:

```sql
email
username
```

Good:

```sql
customer_id
```

Surrogate key.

---

### Mistake 4

Over-normalization in warehouses.

Too many joins.

Slow reports.

---

### Mistake 5

Not thinking about future growth.

Today:

```
1 million rows
```

Tomorrow:

```
10 billion rows
```

Design accordingly.

---

## What a Senior Data Engineer Thinks About

A fresher thinks:

> "How do I create this table?"

A senior thinks:

> "How will this model behave when there are 10 billion rows, 500 pipelines, 100 reports, and 50 engineers depending on it?"

That shift in thinking is what turns someone from a SQL developer into a data engineer.

---

## Learning Roadmap

### Core (Week 1-2)

1. Entities & Relationships
2. Primary & Foreign Keys
3. Normalization (1NF, 2NF, 3NF)
4. ER Diagrams

### Intermediate (Week 3-4)

5. OLTP Modeling
6. Star Schema
7. Slowly Changing Dimensions (SCD)
8. Fact & Dimension Modeling

### Advanced (Week 5+)

9. Data Vault
10. Lakehouse Modeling (Delta Lake, Iceberg)

Once you're comfortable with Star Schema and dimensional modeling, you'll understand about 70% of the data modeling work done in most Data Engineering projects. The remaining 30% is learning how to adapt those principles to specific business domains like healthcare, finance, telecom, or e-commerce.

---

## See Also

- [[Data Engineering]]
- [[Data Warehousing]]
- [[Distributed Systems — Storage]]
- [[SQL — Indexing & Query Optimization]]
