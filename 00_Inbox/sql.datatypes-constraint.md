---
id: 15z50o2seaaj3j7m6934zlf
title: Datatypes Constraint
desc: ''
updated: 1755755844328
created: 1755755833452
---

# **Enterprise Multi-DB Table Design Cheat Sheet**

| Feature                    | SQLite                          | PostgreSQL                                             | Snowflake                                                        | Oracle                                                                            | SQL Server                                                                 |
| -------------------------- | ------------------------------- | ------------------------------------------------------ | ---------------------------------------------------------------- | --------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| **Integer / Numeric**      | `INTEGER`, `INT`, `BIGINT`      | `SMALLINT`, `INTEGER`, `BIGINT`, `SERIAL`, `BIGSERIAL` | `NUMBER`, `NUMERIC`, `DECIMAL`, `INT`, `BIGINT`                  | `NUMBER(p,s)`, `INTEGER`, `SMALLINT`, `DECIMAL`                                   | `TINYINT`, `SMALLINT`, `INT`, `BIGINT`, `DECIMAL(p,s)`, `NUMERIC(p,s)`     |
| **Floating Point**         | `REAL`, `FLOAT`, `DOUBLE`       | `REAL`, `DOUBLE PRECISION`, `NUMERIC(p,s)`             | `FLOAT`, `DOUBLE`                                                | `BINARY_FLOAT`, `BINARY_DOUBLE`                                                   | `FLOAT`, `REAL`, `DOUBLE PRECISION`                                        |
| **String / Text**          | `TEXT`, `CHAR(n)`, `VARCHAR(n)` | `CHAR(n)`, `VARCHAR(n)`, `TEXT`                        | `VARCHAR(n)`, `CHAR(n)`, `STRING`                                | `CHAR(n)`, `VARCHAR2(n)`, `CLOB`                                                  | `CHAR(n)`, `VARCHAR(n)`, `NVARCHAR(n)`, `TEXT`                             |
| **Boolean**                | `NUMERIC` (0/1)                 | `BOOLEAN`                                              | `BOOLEAN`                                                        | `NUMBER(1)` or PL/SQL BOOLEAN                                                     | `BIT`                                                                      |
| **Date / Time**            | `DATE`, `DATETIME`, `TEXT`      | `DATE`, `TIME`, `TIMESTAMP`, `TIMESTAMPTZ`             | `DATE`, `TIME`, `TIMESTAMP_NTZ`, `TIMESTAMP_LTZ`, `TIMESTAMP_TZ` | `DATE`, `TIMESTAMP`, `TIMESTAMP WITH TIME ZONE`, `TIMESTAMP WITH LOCAL TIME ZONE` | `DATE`, `DATETIME`, `DATETIME2`, `SMALLDATETIME`, `TIME`, `DATETIMEOFFSET` |
| **Binary / LOB**           | `BLOB`                          | `BYTEA`                                                | `BINARY`                                                         | `BLOB`, `BFILE`                                                                   | `VARBINARY`, `IMAGE`                                                       |
| **Semi-structured / JSON** | —                               | `JSON`, `JSONB`                                        | `VARIANT`, `OBJECT`, `ARRAY`                                     | `CLOB` or `JSON` (Oracle 21c+)                                                    | `JSON` (native functions)                                                  |

---

## **Constraints Across DBs**

| Constraint                   | SQLite                                      | PostgreSQL                                         | Snowflake                               | Oracle                                      | SQL Server                                  |
| ---------------------------- | ------------------------------------------- | -------------------------------------------------- | --------------------------------------- | ------------------------------------------- | ------------------------------------------- |
| **PRIMARY KEY**              | `id INTEGER PRIMARY KEY`                    | `id SERIAL PRIMARY KEY`                            | `id NUMBER PRIMARY KEY` (metadata only) | `id NUMBER PRIMARY KEY`                     | `id INT PRIMARY KEY`                        |
| **AUTOINCREMENT / Identity** | `INTEGER PRIMARY KEY AUTOINCREMENT`         | `SERIAL`, `BIGSERIAL`, `GENERATED ... AS IDENTITY` | `AUTOINCREMENT`                         | `GENERATED ALWAYS AS IDENTITY`              | `IDENTITY(1,1)`                             |
| **NOT NULL**                 | `name TEXT NOT NULL`                        | `name TEXT NOT NULL`                               | `name STRING NOT NULL`                  | `name VARCHAR2(50) NOT NULL`                | `name NVARCHAR(50) NOT NULL`                |
| **UNIQUE**                   | `email TEXT UNIQUE`                         | `email TEXT UNIQUE`                                | Metadata only                           | `email VARCHAR2(100) UNIQUE`                | `email NVARCHAR(100) UNIQUE`                |
| **CHECK**                    | `age INTEGER CHECK(age >= 0)`               | `age INT CHECK(age >= 0)`                          | `age NUMBER CHECK(age >= 0)`            | `age NUMBER CHECK(age >= 0)`                | `age INT CHECK(age >= 0)`                   |
| **DEFAULT**                  | `status TEXT DEFAULT 'active'`              | `status TEXT DEFAULT 'active'`                     | `status STRING DEFAULT 'active'`        | `status VARCHAR2(20) DEFAULT 'active'`      | `status NVARCHAR(20) DEFAULT 'active'`      |
| **FOREIGN KEY**              | `FOREIGN KEY(user_id) REFERENCES users(id)` | `FOREIGN KEY(user_id) REFERENCES users(id)`        | Metadata only                           | `FOREIGN KEY(user_id) REFERENCES users(id)` | `FOREIGN KEY(user_id) REFERENCES users(id)` |
| **Cascading**                | `ON DELETE CASCADE` (SQLite 3.6+)           | `ON DELETE CASCADE/SET NULL`                       | N/A                                     | `ON DELETE CASCADE/SET NULL`                | `ON DELETE CASCADE/SET NULL`                |
| **Compound / Composite PK**  | `PRIMARY KEY(col1, col2)`                   | `PRIMARY KEY(col1, col2)`                          | `PRIMARY KEY(col1, col2)`               | `PRIMARY KEY(col1, col2)`                   | `PRIMARY KEY(col1, col2)`                   |

---

## **Enterprise Design Notes**

* **SQLite:** lightweight, type-affinity; runtime enforcement limited; good for small apps.

* **PostgreSQL:** fully relational, strong type system, supports JSONB, rich constraints.

* **Snowflake:** cloud-native; constraints mostly metadata; use ETL pipelines for enforcement; semi-structured support via VARIANT.

* **Oracle:** traditional RDBMS; sequences/IDENTITY; supports deferrable constraints, LOBs, advanced datatypes.

* **SQL Server:** enterprise-grade; identity columns; strong constraints; JSON support; T-SQL extensions for business logic.

* **Timestamps & audit columns**: `created_at`, `updated_at` recommended for all DBs.

* **Boolean handling varies**: map appropriately per DB.

* **JSON / semi-structured**: PostgreSQL (`JSONB`), Snowflake (`VARIANT`), SQL Server (`JSON`), Oracle (CLOB or JSON 21c+).

* **Check & default constraints**: enforce business rules wherever possible.

---
