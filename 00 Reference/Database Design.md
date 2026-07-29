# AI Summary
1. What is Database Design?. Database design is one of those topics that looks deceptively simple until you build a system that has millions of rows, multiple developers, changing business rules, and performance requirements. A good database design makes applications easier to build, faster to qu...

Database design is one of those topics that looks deceptively simple until you build a system that has millions of rows, multiple developers, changing business rules, and performance requirements. A good database design makes applications easier to build, faster to query, and cheaper to maintain.

I'll explain it from first principles rather than jumping into SQL syntax.

---

# 1. What is Database Design?

Database design is the process of deciding:

- What data should be stored
    
- How the data relates
    
- How to avoid duplication
    
- How to query it efficiently
    
- How to keep data consistent
    

Think of it as designing a city before constructing buildings.

You decide:

- roads (relationships)
    
- houses (tables)
    
- addresses (primary keys)
    
- traffic rules (constraints)
    
- maps (indexes)
    

before people move in.

---

# 2. Mental Model

Forget SQL for a moment.

Imagine running Amazon.

You have

- Customers
    
- Orders
    
- Products
    
- Payments
    
- Reviews
    

Should everything go into one giant spreadsheet?

|Customer|Address|Product|Price|Order Date|Payment|
|---|---|---|---|---|---|

No.

Problems immediately appear.

- Customer repeats hundreds of times.
    
- Product price changes.
    
- Address changes.
    
- Multiple products per order.
    

Instead, we separate information into logical groups.

---

# 3. Entities

Every database starts with entities.

An entity is simply a real-world object.

Examples

```
Customer

Product

Employee

Order

Invoice

Department

Course
```

Usually, one entity becomes one table.

Example

Customer Table

```
Customer
-------------
CustomerID
Name
Email
Phone
```

Product

```
Product
------------
ProductID
Name
Price
Category
```

Order

```
Order
------------
OrderID
CustomerID
OrderDate
```

---

# 4. Attributes

Attributes describe an entity.

Customer

```
Customer

ID
Name
Email
Phone
DateOfBirth
```

These become columns.

---

# 5. Relationships

This is the heart of database design.

Ask:

"How are things connected?"

Example

Customer places Order

One customer

↓

Many orders

```
Customer

1 ----------- *

Order
```

This is called

One-to-Many

---

Another example

Department

↓

Employees

One department has many employees.

```
Department

1 -------- *

Employee
```

---

# 6. Primary Key

Every row must be uniquely identifiable.

Example

```
Customer

CustomerID
Name
Email
```

CustomerID is unique.

```
1

2

3

4
```

Never duplicates.

Primary Key (PK)

Think of it as Aadhaar for a row.

---

# 7. Foreign Key

Suppose

```
Order

OrderID

CustomerID

Date
```

CustomerID points to Customer table.

```
Customer

1 Ronak

2 Alice
```

Order

```
101  -> Customer 1

102  -> Customer 1

103  -> Customer 2
```

CustomerID is a Foreign Key.

It links tables.

---

# 8. Relationship Types

## One-to-One

```
Person

1 -------- 1

Passport
```

One passport belongs to one person.

---

## One-to-Many

```
Customer

1 ------- *

Orders
```

Most common relationship.

---

## Many-to-Many

Students

↓

Courses

A student can join many courses.

A course has many students.

Impossible to store directly.

Need a bridge table.

```
Student

StudentID
```

```
Course

CourseID
```

```
Enrollment

StudentID

CourseID
```

This bridge table resolves the many-to-many relationship.

---

# 9. Normalization

One of the biggest concepts.

Goal:

Avoid duplicate data.

Suppose

```
Employee

ID

Name

Department

Department Manager

Department Phone
```

Every employee repeats department information.

```
John

Sales

Raj

9999
```

```
Alice

Sales

Raj

9999
```

```
Mike

Sales

Raj

9999
```

Redundant.

Instead

Department

```
DepartmentID

DepartmentName

Manager

Phone
```

Employee

```
EmployeeID

Name

DepartmentID
```

Now department info exists only once.

Benefits

- less storage
    
- fewer update mistakes
    
- better consistency
    

---

# 10. Denormalization

Sometimes speed matters more than perfect normalization.

Suppose joining 15 tables takes 2 seconds.

Instead you duplicate a small amount of data.

```
Orders

CustomerName

CustomerCity
```

Even though Customer table already has it.

This improves reporting speed.

Data warehouses do this frequently.

---

# 11. Constraints

Constraints protect data quality.

Examples

Primary Key

```
Cannot repeat.
```

Unique

```
Email cannot repeat.
```

Not Null

```
Name cannot be empty.
```

Check

```
Age > 18
```

Foreign Key

```
Customer must exist.
```

---

# 12. Indexes

Imagine a book.

Without index:

You read 800 pages.

With index:

Go directly to page 621.

Database indexes work exactly the same.

Without Index

```
Search Email

↓

Scan 10 million rows
```

With Index

```
Search Email

↓

Jump directly
```

Huge performance improvement.

---

# 13. Transaction

Suppose

Transfer ₹500

```
A -500

B +500
```

What if power fails after deducting from A?

Money disappears.

Transactions solve this.

Either

Everything succeeds

OR

Everything rolls back.

---

# 14. ACID Properties

Transactions follow ACID.

**Atomicity:** All or nothing.

**Consistency:** Rules remain valid before and after the transaction.

**Isolation:** Concurrent transactions don't interfere with each other.

**Durability:** Once committed, data survives crashes.

---

# 15. OLTP vs OLAP

### OLTP (Operational Database)

Designed for day-to-day operations.

Examples

- Banking
    
- E-commerce
    
- Hospital
    
- Payroll
    

Characteristics

- Many small writes
    
- Normalized
    
- Fast inserts
    
- Fast updates
    

---

### OLAP (Analytics)

Designed for reporting.

Examples

- Power BI
    
- Tableau
    
- Snowflake
    
- Databricks
    

Characteristics

- Large scans
    
- Aggregations
    
- Star/Snowflake schemas
    
- Denormalized facts and dimensions
    

---

# 16. Database Design Process

A practical workflow looks like this:

1. Understand the business problem.
    
2. Identify entities (nouns like Customer, Product, Order).
    
3. List attributes for each entity.
    
4. Determine relationships between entities.
    
5. Assign primary keys.
    
6. Add foreign keys to model relationships.
    
7. Normalize to reduce redundancy.
    
8. Add constraints to enforce data quality.
    
9. Create indexes for common queries.
    
10. Test with realistic use cases and refine.
    

---

# 17. Example: E-commerce Database

```text
Customer
--------
CustomerID (PK)
Name
Email

Product
--------
ProductID (PK)
Name
Price

Order
-----
OrderID (PK)
CustomerID (FK)
OrderDate

OrderItem
---------
OrderItemID (PK)
OrderID (FK)
ProductID (FK)
Quantity
PriceAtPurchase

Payment
-------
PaymentID (PK)
OrderID (FK)
Amount
Status
```

Relationships:

```text
Customer
   |
   | 1:N
   |
 Order
   |
   | 1:N
   |
OrderItem
   |
   | N:1
   |
Product

Order
   |
   | 1:1 (or 1:N depending on business rules)
   |
Payment
```

---

# 18. Common Beginner Mistakes

- Using one huge table for everything.
    
- Storing comma-separated values in a column (e.g., `"Python,SQL,Java"` instead of a separate skills table).
    
- Not defining primary keys.
    
- Avoiding foreign keys and relying on application logic alone.
    
- Choosing natural keys (like email) as primary keys when they can change.
    
- Creating indexes on every column, which slows writes.
    
- Ignoring how the application will query the data.
    

---

# 19. How This Relates to Data Engineering

Since you work in data engineering, you'll typically interact with two styles of database design:

|Operational (OLTP)|Analytical (OLAP)|
|---|---|
|Highly normalized (3NF)|Often denormalized (Star Schema)|
|Supports inserts and updates|Optimized for large analytical queries|
|Many small transactions|Fewer, large batch loads|
|PostgreSQL, MySQL, SQL Server|Snowflake, BigQuery, Databricks, Redshift|

Understanding normalized OLTP design helps you ingest and model source systems correctly, while understanding dimensional modeling (facts and dimensions) helps you build efficient data warehouses.

## A good learning progression

To build strong database design skills, study these topics in order:

1. Relational database fundamentals (tables, rows, columns).
    
2. Keys (primary, foreign, candidate, surrogate).
    
3. Relationship types (1:1, 1:N, N:M).
    
4. Entity-Relationship (ER) diagrams.
    
5. Normalization (1NF, 2NF, 3NF, BCNF).
    
6. Constraints and referential integrity.
    
7. Indexes and query performance.
    
8. Transactions and ACID.
    
9. Dimensional modeling (Star and Snowflake schemas).
    
10. Database design patterns for common domains (e-commerce, HR, finance, healthcare).
    

Once you're comfortable with these fundamentals, you'll be able to design databases that are both correct and scalable, and you'll find it much easier to reason about ETL pipelines, data warehouses, and application backends.