---
id: 2e4k2742z1sg7rkwi7zu7ra
title: Databases
desc: ''
updated: 1755756353868
created: 1755756347932
---

# **Enterprise Multi-DB Database Operations Cheat Sheet**

| Operation Category             | Operation                   | Basic Syntax                                               | DB Notes / Enterprise Tips                                                                                                           |
| ------------------------------ | --------------------------- | ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| **Database Creation / Drop**   | Create Database             | `CREATE DATABASE db_name;`                                 | SQLite: database is a file, created by connecting to a new file.                                                                     |
|                                | Drop Database               | `DROP DATABASE db_name;`                                   | Snowflake: `DROP DATABASE IF EXISTS db_name;`                                                                                        |
| **Table Creation / Drop**      | Create Table                | `CREATE TABLE table_name (col1 TYPE, col2 TYPE, ...);`     | All DBs support. Include constraints for enterprise-grade design.                                                                    |
|                                | Drop Table                  | `DROP TABLE table_name;`                                   | Add `IF EXISTS` for safety.                                                                                                          |
|                                | Alter Table                 | `ALTER TABLE table_name ADD COLUMN col TYPE;`              | Supports ADD, DROP, MODIFY (SQL Server: ALTER COLUMN, Oracle: MODIFY, PostgreSQL: ALTER COLUMN TYPE).                                |
| **Insert / Update / Delete**   | Insert Row                  | `INSERT INTO table_name (col1, col2) VALUES (val1, val2);` | SQLite supports `INSERT OR REPLACE` for upserts. PostgreSQL: `INSERT ... ON CONFLICT DO UPDATE`.                                     |
|                                | Update Row                  | `UPDATE table_name SET col1 = val1 WHERE condition;`       | Use WHERE carefully to avoid mass updates.                                                                                           |
|                                | Delete Row                  | `DELETE FROM table_name WHERE condition;`                  | Consider soft delete via a `deleted_at` timestamp in enterprise setups.                                                              |
| **Select / Query**             | Simple Select               | `SELECT col1, col2 FROM table_name WHERE condition;`       | All DBs support ANSI SQL. Use aliases and schema-qualified names in enterprise.                                                      |
|                                | Aggregates / Grouping       | `SELECT col, COUNT(*) FROM table GROUP BY col;`            | Supports HAVING, GROUPING SETS, ROLLUP, CUBE (DB-specific: Snowflake, Oracle, SQL Server).                                           |
| **Joins**                      | INNER / LEFT / RIGHT / FULL | See joins cheat sheet                                      | SQLite: RIGHT/FULL not supported.                                                                                                    |
| **Transactions**               | Begin / Commit / Rollback   | `BEGIN; ... COMMIT;` / `ROLLBACK;`                         | SQLite: autocommit by default. PostgreSQL, Oracle, SQL Server fully support. Snowflake: implicit transactions with some limitations. |
| **Indexes**                    | Create Index                | `CREATE INDEX idx_name ON table(col);`                     | Clustered indexes supported in SQL Server/Oracle. Snowflake: use cluster keys. PostgreSQL: B-tree default, GIN for JSONB.            |
|                                | Drop Index                  | `DROP INDEX idx_name;`                                     | SQLite: `DROP INDEX IF EXISTS idx_name;`                                                                                             |
| **Sequences / Auto-Increment** | Create Sequence             | `CREATE SEQUENCE seq_name START 1 INCREMENT 1;`            | PostgreSQL, Oracle, SQL Server support sequences. SQLite uses `AUTOINCREMENT` in table. Snowflake: `AUTOINCREMENT` column.           |
|                                | Next Value                  | `SELECT NEXTVAL('seq_name');`                              | DB-specific syntax: PostgreSQL `NEXTVAL`, Oracle `seq_name.NEXTVAL`, SQL Server `NEXT VALUE FOR seq_name`.                           |
| **Views**                      | Create / Replace            | `CREATE OR REPLACE VIEW view_name AS SELECT ...;`          | SQLite: no `OR REPLACE` in older versions. Snowflake: supports views & materialized views.                                           |
| **Triggers**                   | Create Trigger              | See triggers cheat sheet                                   | Snowflake: triggers not supported; use streams/tasks instead.                                                                        |

---

## **Enterprise Design Notes**

* **SQLite:** lightweight; database = file; limited ALTER TABLE, no materialized views or triggers.
* **PostgreSQL:** fully relational; supports advanced transactions, materialized views, JSONB, sequences, rich index types.
* **Snowflake:** cloud-native; auto-clustering optional; triggers not supported; constraints mostly metadata; streams + tasks replace triggers.
* **Oracle:** enterprise-grade; supports sequences, compound triggers, materialized views, partitioning, strong constraint enforcement.
* **SQL Server:** identity columns, indexed views, transactional support; JSON functions; constraints and triggers fully supported.
* **Transactions:** Always wrap critical operations in BEGIN/COMMIT/ROLLBACK.
* **Indexes & Performance:** Use indexes, cluster keys, or partitioning for large datasets.
* **Audit / Soft Deletes:** Recommended for enterprise; use triggers or timestamp fields.
* **Schema Management:** Use schemas/namespaces to separate environments or modules.

---

## **Quick Examples**

```sql
-- Insert / Upsert
INSERT INTO users (id, username) VALUES (1, 'alice');
-- PostgreSQL upsert
INSERT INTO users(id, username) VALUES(1, 'alice')
ON CONFLICT(id) DO UPDATE SET username = EXCLUDED.username;

-- Update
UPDATE users SET status='active' WHERE id=1;

-- Delete
DELETE FROM users WHERE id=1;

-- Transaction
BEGIN;
UPDATE accounts SET balance=balance-100 WHERE id=1;
UPDATE accounts SET balance=balance+100 WHERE id=2;
COMMIT;

-- Create Index
CREATE INDEX idx_users_email ON users(email);
```

---

This cheat sheet **covers core database operations across all major DBs** in a **compact, enterprise-ready reference**.
