---
id: 6wymbfqd1kstlkuzd3hw3o4
title: Table
desc: ''
updated: 1755756385355
created: 1755756375533
---

# **Enterprise Multi-DB Table Operations Cheat Sheet**

| Operation                       | Purpose                                  | Syntax                                                                                                                                                        | DB Notes / Enterprise Tips                                                                                            |
| ------------------------------- | ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| **CREATE TABLE**                | Define a new table                       | `CREATE TABLE table_name (col1 TYPE CONSTRAINTS, col2 TYPE ...);`                                                                                             | All DBs support. Include PK, FK, NOT NULL, DEFAULT for enterprise-grade design.                                       |
| **DROP TABLE**                  | Remove a table                           | `DROP TABLE table_name;`                                                                                                                                      | Add `IF EXISTS` where supported. Snowflake: automatically handles underlying storage. SQLite: drops file-level table. |
| **ALTER TABLE – Add Column**    | Add a new column                         | `ALTER TABLE table_name ADD COLUMN col_name TYPE;`                                                                                                            | PostgreSQL, Snowflake, Oracle, SQL Server support multiple additions. SQLite only allows one column at a time.        |
| **ALTER TABLE – Drop Column**   | Remove a column                          | `ALTER TABLE table_name DROP COLUMN col_name;`                                                                                                                | SQLite (>=3.35) supports DROP COLUMN; earlier versions require table recreation.                                      |
| **ALTER TABLE – Modify Column** | Change data type / default / constraints | PostgreSQL: `ALTER TABLE table_name ALTER COLUMN col TYPE new_type;` <br>Oracle: `MODIFY`; SQL Server: `ALTER COLUMN`; Snowflake: `ALTER TABLE ALTER COLUMN`. | SQLite limited; often requires `CREATE TABLE` replacement.                                                            |
| **RENAME TABLE**                | Rename table                             | `ALTER TABLE old_name RENAME TO new_name;`                                                                                                                    | Supported in SQLite, PostgreSQL, Snowflake, Oracle, SQL Server (`sp_rename 'old','new'`).                             |
| **TRUNCATE TABLE**              | Remove all rows, keep structure          | `TRUNCATE TABLE table_name;`                                                                                                                                  | Fast; resets auto-increment IDs in some DBs (PostgreSQL, SQL Server). SQLite: use `DELETE FROM table;`.               |
| **CLONE / COPY TABLE**          | Create a copy                            | Snowflake: `CREATE TABLE new_table CLONE old_table;` <br>Other DBs: `CREATE TABLE new_table AS SELECT * FROM old_table;`                                      | Enterprise: Use for testing, ETL staging, or schema migration.                                                        |
| **Partition / Cluster Table**   | Performance optimization                 | Snowflake: `CLUSTER BY(col)` <br>PostgreSQL: `PARTITION BY RANGE/ LIST` <br>Oracle: `PARTITION BY RANGE/LIST/ HASH` <br>SQL Server: Partition schemes         | SQLite does **not** support partitioning. Essential for large-scale analytics.                                        |
| **Add / Drop Constraints**      | Enforce rules after creation             | `ALTER TABLE table_name ADD CONSTRAINT fk_name FOREIGN KEY (col) REFERENCES ref_table(col);`                                                                  | Supported in PostgreSQL, Oracle, SQL Server, Snowflake (metadata only). SQLite supports basic FK enforcement.         |
| **Comment / Documentation**     | Add description                          | PostgreSQL: `COMMENT ON TABLE table_name IS 'desc';` <br>Oracle: `COMMENT ON TABLE` <br>SQL Server: use extended properties                                   | Enterprise best practice: document tables and columns for maintainability.                                            |

---

## **Enterprise Design Notes**

* **SQLite:** Lightweight; ALTER TABLE limited; often recreate table for complex schema changes.
* **PostgreSQL:** Fully featured; supports ALTER TABLE, partitioning, table inheritance.
* **Snowflake:** Cloud-native; CLONE, clustering, zero-copy operations; constraints metadata-only.
* **Oracle:** Enterprise-grade; supports partitions, table compression, materialized tables, full ALTER capabilities.
* **SQL Server:** Supports identity columns, partitioning, clustered tables, schema binding; ALTER TABLE rich support.
* **Best Practices:**

  * Always include PK, FK, NOT NULL, DEFAULT for production-grade tables.
  * Use partitioning / clustering for large tables to improve query performance.
  * Use table comments / documentation for maintainability.
  * Use `TRUNCATE` for staging tables to quickly remove data without logging every row.
  * Avoid inline `SELECT *` in `CREATE TABLE AS SELECT` for enterprise clarity; specify columns.

---

## **Quick Examples**

```sql
-- Create Table
CREATE TABLE users (
    id BIGINT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Alter Table: Add Column
ALTER TABLE users ADD COLUMN status VARCHAR(20) DEFAULT 'active';

-- Alter Table: Drop Column (PostgreSQL/Oracle/SQL Server)
ALTER TABLE users DROP COLUMN status;

-- Rename Table
ALTER TABLE users RENAME TO app_users;  -- SQLite, PostgreSQL, Snowflake, Oracle
EXEC sp_rename 'users', 'app_users';   -- SQL Server

-- Truncate Table
TRUNCATE TABLE app_users;

-- Copy Table
CREATE TABLE users_copy AS SELECT * FROM users;  -- PostgreSQL, SQLite, Oracle, SQL Server
CREATE TABLE users_clone CLONE users;            -- Snowflake

-- Partition Table (PostgreSQL example)
CREATE TABLE orders (
    order_id BIGINT,
    order_date DATE,
    amount NUMERIC
) PARTITION BY RANGE (order_date);
```

---

This cheat sheet **covers all essential table operations across major DBs**, highlighting **differences in ALTER capabilities, partitioning, and cloning**, making it **enterprise-ready and portable across platforms**.

