---
id: qw1c1yl7f89p4fowghkrhh2
title: Information Schema
desc: ''
updated: 1755756477468
created: 1755756472047
---

# **Enterprise Multi-DB INFORMATION\_SCHEMA Operations Cheat Sheet**

| Metadata Task              | Purpose                               | Query / Syntax                                                                                                                                                                                                                                                                    | DB Notes / Enterprise Tips                                                                                                                                                                                                         |
| -------------------------- | ------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **List Schemas**           | Get all schemas in a database         | `sql SELECT schema_name FROM information_schema.schemata;`                                                                                                                                                                                                                        | SQLite: no schemas; database = single namespace. Snowflake: `SHOW SCHEMAS;` Oracle: use `ALL_USERS`.                                                                                                                               |
| **List Tables**            | Get tables in a schema                | `sql SELECT table_name FROM information_schema.tables WHERE table_schema='schema_name';`                                                                                                                                                                                          | SQLite: use `sqlite_master`. PostgreSQL, Oracle, SQL Server: fully supported.                                                                                                                                                      |
| **List Columns**           | Inspect column metadata               | `sql SELECT column_name, data_type, is_nullable, column_default FROM information_schema.columns WHERE table_name='table_name';`                                                                                                                                                   | Enterprise: Use for automated ETL mapping, schema documentation.                                                                                                                                                                   |
| **Primary Keys**           | Identify table PKs                    | `sql SELECT kcu.column_name FROM information_schema.table_constraints tc JOIN information_schema.key_column_usage kcu ON tc.constraint_name = kcu.constraint_name WHERE tc.table_name='table_name' AND tc.constraint_type='PRIMARY KEY';`                                         | Snowflake & PostgreSQL fully supported; SQLite PK info in `PRAGMA table_info(table_name);`.                                                                                                                                        |
| **Foreign Keys**           | Inspect FK relationships              | `sql SELECT kcu.column_name, ccu.table_name AS foreign_table, ccu.column_name AS foreign_column FROM information_schema.key_column_usage kcu JOIN information_schema.constraint_column_usage ccu ON kcu.constraint_name = ccu.constraint_name WHERE kcu.table_name='table_name';` | Useful for dependency tracking and ERD generation.                                                                                                                                                                                 |
| **Indexes**                | List table indexes                    | `sql SELECT indexname, indexdef FROM pg_indexes WHERE tablename='table_name';`                                                                                                                                                                                                    | PostgreSQL only. SQL Server: `SELECT * FROM sys.indexes WHERE object_id = OBJECT_ID('table_name');` Oracle: `SELECT * FROM user_indexes;` Snowflake: `SHOW INDEXES IN TABLE table_name;` SQLite: `PRAGMA index_list(table_name);`. |
| **Constraints**            | Inspect CHECK, UNIQUE, FK, PK         | `sql SELECT * FROM information_schema.table_constraints WHERE table_name='table_name';`                                                                                                                                                                                           | Combine with `key_column_usage` for column-level info.                                                                                                                                                                             |
| **Views**                  | List views                            | `sql SELECT table_name FROM information_schema.views WHERE table_schema='schema_name';`                                                                                                                                                                                           | SQLite: `sqlite_master` WHERE type='view'.                                                                                                                                                                                         |
| **Routine / Functions**    | Inspect stored procedures / functions | `sql SELECT routine_name, routine_type, data_type FROM information_schema.routines WHERE routine_schema='schema_name';`                                                                                                                                                           | Useful for dependency management in enterprise applications.                                                                                                                                                                       |
| **Tables by Owner / User** | List all tables for a user            | PostgreSQL / Snowflake: filter on `table_schema` <br> Oracle: `ALL_TABLES WHERE owner='USERNAME'` <br> SQL Server: `INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='schema_name'`                                                                                                   | Helpful for security audits.                                                                                                                                                                                                       |

---

## **Enterprise Design Notes**

* **SQLite:** Minimal metadata support; use `sqlite_master` or `PRAGMA table_info`.
* **PostgreSQL:** Full INFORMATION\_SCHEMA support; combine with `pg_catalog` for advanced introspection.
* **Snowflake:** INFORMATION\_SCHEMA fully available per database/schema; also supports `SHOW` commands for quick inspection.
* **Oracle:** INFORMATION\_SCHEMA not standard; use `ALL_TABLES`, `ALL_TAB_COLUMNS`, `ALL_CONSTRAINTS`, etc.
* **SQL Server:** INFORMATION\_SCHEMA views available; combine with `sys.tables`, `sys.columns` for deeper insights.
* **Best Practices:**

  * Use these queries in automated schema audits, ETL pipelines, and documentation.
  * Combine table, column, and constraint metadata for generating ER diagrams.
  * Use filters by schema or owner to avoid multi-tenant collisions.

---

## **Quick Examples**

```sql
-- List all tables in schema
SELECT table_name
FROM information_schema.tables
WHERE table_schema='public';

-- List columns for a table
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name='users';

-- List primary keys
SELECT kcu.column_name
FROM information_schema.table_constraints tc
JOIN information_schema.key_column_usage kcu
ON tc.constraint_name = kcu.constraint_name
WHERE tc.table_name='orders' AND tc.constraint_type='PRIMARY KEY';

-- List foreign keys
SELECT kcu.column_name, ccu.table_name AS foreign_table, ccu.column_name AS foreign_column
FROM information_schema.key_column_usage kcu
JOIN information_schema.constraint_column_usage ccu
ON kcu.constraint_name = ccu.constraint_name
WHERE kcu.table_name='orders';

-- SQLite table info
PRAGMA table_info(users);

-- Snowflake show tables in schema
SHOW TABLES IN SCHEMA analytics.sales;
```

---

This cheat sheet **covers all essential INFORMATION\_SCHEMA / metadata operations across major DBs**, highlighting **differences in support, metadata inspection, and alternative commands** for DBs like **SQLite and Oracle**, making it **enterprise-ready for auditing, ETL, and schema management**.
