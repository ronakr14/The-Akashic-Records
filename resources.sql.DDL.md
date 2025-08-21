---
id: 4sqkzmiwqdgl1xy5lx9j7bh
title: DDL
desc: ''
updated: 1755756505406
created: 1755756498678
---

# **Enterprise Multi-DB DDL Operations Cheat Sheet**

| DDL Operation                        | Purpose                             | Syntax                                                                                                                                               | DB Notes / Enterprise Tips                                                                                           |                                                                     |                                           |                                                                                   |
| ------------------------------------ | ----------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- | ----------------------------------------- | --------------------------------------------------------------------------------- |
| **CREATE DATABASE**                  | Define a new database               | `CREATE DATABASE db_name;`                                                                                                                           | SQLite: database = file; PostgreSQL, Oracle, SQL Server, Snowflake fully support.                                    |                                                                     |                                           |                                                                                   |
| **DROP DATABASE**                    | Remove a database                   | `DROP DATABASE db_name [IF EXISTS];`                                                                                                                 | Use caution in production; some DBs require all connections closed.                                                  |                                                                     |                                           |                                                                                   |
| **CREATE SCHEMA / NAMESPACE**        | Logical grouping of objects         | `CREATE SCHEMA schema_name;`                                                                                                                         | SQLite does **not** support schemas; in Oracle, schema = user. Snowflake supports schema metadata.                   |                                                                     |                                           |                                                                                   |
| **DROP SCHEMA**                      | Remove schema and all objects       | \`DROP SCHEMA schema\_name \[CASCADE                                                                                                                 | RESTRICT];\`                                                                                                         | CASCADE drops all objects; RESTRICT prevents drop if objects exist. |                                           |                                                                                   |
| **CREATE TABLE**                     | Define new table                    | `CREATE TABLE table_name (col1 TYPE CONSTRAINTS, col2 TYPE ...);`                                                                                    | Include PK, FK, NOT NULL, DEFAULT for enterprise-grade tables.                                                       |                                                                     |                                           |                                                                                   |
| **ALTER TABLE**                      | Modify table structure              | Add / Drop / Modify Columns: `ALTER TABLE table_name ADD/DROP/MODIFY COLUMN col TYPE;` <br> Rename Table: `ALTER TABLE old_name RENAME TO new_name;` | SQLite limited (drop/modify requires table recreation). Snowflake supports renames and column modifications.         |                                                                     |                                           |                                                                                   |
| **DROP TABLE**                       | Remove table                        | `DROP TABLE table_name [IF EXISTS];`                                                                                                                 | Fast removal; consider TRUNCATE for staging tables.                                                                  |                                                                     |                                           |                                                                                   |
| **CREATE VIEW / MATERIALIZED VIEW**  | Define virtual or precomputed table | `CREATE [MATERIALIZED] VIEW view_name AS SELECT ...;`                                                                                                | Materialized views supported in PostgreSQL, Oracle, SQL Server, Snowflake; SQLite: no materialized views.            |                                                                     |                                           |                                                                                   |
| **DROP VIEW**                        | Remove a view                       | `DROP VIEW view_name [IF EXISTS];`                                                                                                                   | Use OR REPLACE in DBs that support it to redefine views safely.                                                      |                                                                     |                                           |                                                                                   |
| **CREATE INDEX**                     | Improve query performance           | `CREATE [UNIQUE] INDEX idx_name ON table_name(col);`                                                                                                 | Clustered indexes supported in Oracle/SQL Server; Snowflake uses clustering keys; PostgreSQL: B-tree default.        |                                                                     |                                           |                                                                                   |
| **DROP INDEX**                       | Remove index                        | `DROP INDEX idx_name;`                                                                                                                               | DB-specific syntax: SQL Server: `DROP INDEX idx_name ON table_name;` SQLite: `DROP INDEX IF EXISTS idx_name;`        |                                                                     |                                           |                                                                                   |
| **CREATE SEQUENCE / AUTO-INCREMENT** | Generate unique values              | `CREATE SEQUENCE seq_name START 1 INCREMENT 1;`                                                                                                      | PostgreSQL, Oracle, SQL Server support sequences. SQLite: `AUTOINCREMENT` column. Snowflake: `AUTOINCREMENT` column. |                                                                     |                                           |                                                                                   |
| **ALTER SEQUENCE**                   | Modify increment, min/max, cache    | `ALTER SEQUENCE seq_name INCREMENT BY 5;`                                                                                                            | Snowflake: limited sequence options; PostgreSQL/Oracle fully supported.                                              |                                                                     |                                           |                                                                                   |
| **DROP SEQUENCE**                    | Remove sequence                     | `DROP SEQUENCE seq_name;`                                                                                                                            | Consider dependent tables before dropping.                                                                           |                                                                     |                                           |                                                                                   |
| **CREATE / DROP TRIGGER**            | Execute logic on table events       | \`CREATE TRIGGER trg\_name BEFORE                                                                                                                    | AFTER INSERT                                                                                                         | UPDATE                                                              | DELETE ON table\_name FOR EACH ROW ...;\` | Snowflake: triggers not supported; use streams + tasks. SQLite: limited triggers. |
| **CREATE / DROP CONSTRAINT**         | Enforce data integrity              | `ALTER TABLE table_name ADD CONSTRAINT constraint_name PRIMARY KEY/FK/UNIQUE/CHECK(...);`                                                            | Enterprise best practice: always name constraints for maintainability.                                               |                                                                     |                                           |                                                                                   |

---

## **Enterprise Design Notes**

* **SQLite:** Lightweight; supports basic DDL, but lacks advanced features like schemas, materialized views, triggers.
* **PostgreSQL:** Fully-featured DDL; supports sequences, materialized views, schema management, table inheritance.
* **Snowflake:** Cloud-native; supports DDL with metadata-only constraints, clustering keys, and streams for reactive logic.
* **Oracle:** Enterprise-grade; supports partitions, materialized views, sequences, compound triggers.
* **SQL Server:** Fully-featured; supports identity columns, indexed views, schema management, robust DDL operations.
* **Best Practices:**

  * Always use explicit constraint names.
  * Use `CREATE OR REPLACE` for views and triggers where supported.
  * Wrap schema changes in transactions where possible (except DROP DATABASE).
  * Document all DDL operations for audit and compliance.

---

## **Quick Examples**

```sql
-- Create Table
CREATE TABLE users (
    id BIGINT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Alter Table: Add Column
ALTER TABLE users ADD COLUMN status VARCHAR(20) DEFAULT 'active';

-- Drop Table
DROP TABLE users;

-- Create View
CREATE VIEW user_emails AS
SELECT id, username, email FROM users;

-- Create Materialized View (PostgreSQL / Oracle / Snowflake)
CREATE MATERIALIZED VIEW mv_user_orders AS
SELECT user_id, SUM(amount) AS total
FROM orders GROUP BY user_id;

-- Create Index
CREATE INDEX idx_users_username ON users(username);

-- Create Sequence
CREATE SEQUENCE user_seq START 1 INCREMENT 1;

-- Create Trigger (PostgreSQL example)
CREATE TRIGGER trg_after_insert_users
AFTER INSERT ON users
FOR EACH ROW
EXECUTE FUNCTION log_user_insert();
```

---

This cheat sheet **covers all essential DDL operations across major DBs**, highlighting **differences in sequences, triggers, views, and schema management**, making it **enterprise-ready for database architects and developers**.
