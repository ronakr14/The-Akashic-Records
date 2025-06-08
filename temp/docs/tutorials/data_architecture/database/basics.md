# Database Management Systems (DBMS) Tutorial

## Overview

A Database Management System (DBMS) is software that facilitates the creation, manipulation, and management of databases. It provides an interface for interacting with the data stored in databases, ensuring data integrity, security, and efficient retrieval.

## Database Basics

### What is a Database?

A database is an organized collection of data, typically stored and accessed electronically from a computer system. Databases are managed by Database Management Systems (DBMS), which provide tools for storing, querying, and manipulating data.

### Types of Databases

- **Relational Databases:** Store data in tables with rows and columns. Examples: MySQL, PostgreSQL, Oracle.
- **NoSQL Databases:** Designed for unstructured data and can be document-based, key-value pairs, wide-column stores, or graph databases. Examples: MongoDB, Redis, Cassandra.

## Relational Databases

### Tables

In a relational database, data is organized into tables. Each table consists of rows and columns.

#### Example

**Table: Employees**

| EmployeeID | FirstName | LastName | Department |
|------------|-----------|----------|------------|
| 1          | John      | Doe      | HR         |
| 2          | Jane      | Smith    | IT         |

### Relationships

Tables can have relationships with other tables using keys:

- **Primary Key:** A unique identifier for each row in a table.
- **Foreign Key:** A key used to link two tables together.

#### Example

**Table: Departments**

| DepartmentID | DepartmentName |
|--------------|----------------|
| 1            | HR             |
| 2            | IT             |

**Table: Employees**

| EmployeeID | FirstName | LastName | DepartmentID |
|------------|-----------|----------|--------------|
| 1          | John      | Doe      | 1            |
| 2          | Jane      | Smith    | 2            |

In this example, `DepartmentID` in the `Employees` table is a foreign key referencing the `Departments` table.

## NoSQL Databases

### Document-Based Databases

Store data in JSON-like documents.

#### Example (MongoDB)

```json
{
  "EmployeeID": 1,
  "FirstName": "John",
  "LastName": "Doe",
  "Department": "HR"
}
```

### Key-Value Stores

Store data as key-value pairs.

#### Example (Redis)

```plaintext
SET Employee:1 "John Doe, HR"
GET Employee:1
```

### Column-Family Stores

Store data in columns rather than rows.

#### Example (Cassandra)

```plaintext
CREATE TABLE employees (
  employee_id UUID PRIMARY KEY,
  first_name TEXT,
  last_name TEXT,
  department TEXT
);
```

### Graph Databases

Store data as nodes and edges.

#### Example (Neo4j)

```cypher
CREATE (john:Person {name: "John Doe", department: "HR"})
CREATE (jane:Person {name: "Jane Smith", department: "IT"})
CREATE (john)-[:WORKS_IN]->(hr:Department {name: "HR"})
CREATE (jane)-[:WORKS_IN]->(it:Department {name: "IT"})
```

## Normalization

Normalization is the process of organizing data to reduce redundancy and improve data integrity. It involves dividing a database into two or more tables and defining relationships between them.

### Normal Forms

- **First Normal Form (1NF):** Ensure that each column contains atomic values and each row is unique.
- **Second Normal Form (2NF):** Ensure that all non-key attributes are fully functionally dependent on the primary key.
- **Third Normal Form (3NF):** Ensure that all the attributes are functionally dependent only on the primary key.

## Indexes

Indexes are used to speed up the retrieval of rows by creating a quick lookup for columns.

### Example

```sql
CREATE INDEX idx_lastname ON Employees (LastName);
```

## Transactions

A transaction is a sequence of operations performed as a single logical unit of work. Transactions ensure data integrity and consistency.

### ACID Properties

- **Atomicity:** All operations in a transaction are completed; otherwise, the transaction is aborted.
- **Consistency:** A transaction brings the database from one valid state to another.
- **Isolation:** Transactions are isolated from each other.
- **Durability:** Once a transaction is committed, it remains so, even in the case of a system failure.

### Example

```sql
START TRANSACTION;

UPDATE Accounts SET balance = balance - 100 WHERE account_id = 1;
UPDATE Accounts SET balance = balance + 100 WHERE account_id = 2;

COMMIT;
```

## Backup and Recovery

Regular backups are crucial for protecting data from loss. Recovery involves restoring data from backups.

### Backup Example

```bash
mysqldump -u username -p database_name > backup.sql
```

### Recovery Example

```bash
mysql -u username -p database_name < backup.sql
```

## Summary

This document provides an overview of essential database concepts, including relational and NoSQL databases, SQL commands, normalization, indexing, transactions, and backup and recovery. For more detailed information, refer to the documentation of specific database systems or additional resources.