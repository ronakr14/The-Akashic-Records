---
id: yh6tro37i9l1altq51is6bm
title: Columns
desc: ''
updated: 1755756445790
created: 1755756440269
---

# **Enterprise Multi-DB Column Operations Cheat Sheet**

| Operation                                      | Purpose                                 | Syntax                                                                                                                                                                                                                                                                                 | DB Notes / Enterprise Tips                                                                                                                 |
| ---------------------------------------------- | --------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| **Add Column**                                 | Add a new column to an existing table   | `ALTER TABLE table_name ADD COLUMN col_name TYPE [CONSTRAINTS];`                                                                                                                                                                                                                       | Supported in all DBs. SQLite: adds one column at a time. Snowflake allows multiple additions.                                              |
| **Drop Column**                                | Remove a column                         | `ALTER TABLE table_name DROP COLUMN col_name;`                                                                                                                                                                                                                                         | SQLite (<3.35) requires table recreation. PostgreSQL, Oracle, SQL Server, Snowflake support directly.                                      |
| **Rename Column**                              | Change column name                      | PostgreSQL: `ALTER TABLE table_name RENAME COLUMN old TO new;` <br> Oracle: `ALTER TABLE table_name RENAME COLUMN old TO new;` <br> SQL Server: `sp_rename 'table.old', 'new', 'COLUMN';` <br> Snowflake: `ALTER TABLE table_name RENAME COLUMN old TO new;`                           | SQLite requires table recreation in older versions.                                                                                        |
| **Modify Column Type**                         | Change data type                        | PostgreSQL: `ALTER TABLE table_name ALTER COLUMN col TYPE new_type;` <br> Oracle: `ALTER TABLE table_name MODIFY col new_type;` <br> SQL Server: `ALTER TABLE table_name ALTER COLUMN col new_type;` <br> Snowflake: `ALTER TABLE table_name ALTER COLUMN col SET DATA TYPE new_type;` | SQLite cannot alter type directly; must recreate table.                                                                                    |
| **Set / Drop DEFAULT**                         | Add or remove default value             | PostgreSQL: `ALTER TABLE table_name ALTER COLUMN col SET DEFAULT val;` <br> DROP: `ALTER TABLE table_name ALTER COLUMN col DROP DEFAULT;`                                                                                                                                              | All DBs support; SQLite syntax: `ALTER TABLE table_name ADD COLUMN col TYPE DEFAULT val`.                                                  |
| **Set / Drop NOT NULL**                        | Add/remove NOT NULL constraint          | PostgreSQL: `ALTER TABLE table_name ALTER COLUMN col SET NOT NULL;` <br> DROP: `ALTER TABLE table_name ALTER COLUMN col DROP NOT NULL;`                                                                                                                                                | SQLite: requires table recreation. Snowflake, Oracle, SQL Server support directly.                                                         |
| **Add / Drop UNIQUE Constraint**               | Ensure column uniqueness                | `ALTER TABLE table_name ADD CONSTRAINT uq_name UNIQUE(col);`                                                                                                                                                                                                                           | Dropping: `ALTER TABLE table_name DROP CONSTRAINT uq_name;` Support varies slightly: SQLite supports simple UNIQUE; others fully-featured. |
| **Add / Drop CHECK Constraint**                | Enforce business rules on column values | `ALTER TABLE table_name ADD CONSTRAINT chk_name CHECK(col > 0);`                                                                                                                                                                                                                       | Dropping: DB-specific syntax; PostgreSQL/Oracle/SQL Server support by constraint name. Snowflake: metadata only.                           |
| **Column Comments / Description**              | Document purpose                        | PostgreSQL: `COMMENT ON COLUMN table_name.col IS 'desc';` <br> Oracle: `COMMENT ON COLUMN table_name.col IS 'desc';` <br> Snowflake: `ALTER TABLE table_name MODIFY COLUMN col COMMENT = 'desc';`                                                                                      | Enterprise best practice: always document columns for maintainability.                                                                     |
| **Rename / Drop Column Default / Constraints** | Adjust column rules                     | Combine ALTER TABLE + ALTER COLUMN / DROP CONSTRAINT syntax per DB                                                                                                                                                                                                                     | Enterprise: use naming conventions for constraints (`chk_`, `uq_`, `fk_`) for easier management.                                           |

---

## **Enterprise Design Notes**

* **SQLite:** Limited ALTER TABLE support; cannot drop or rename columns directly in older versions; often requires table recreation.
* **PostgreSQL:** Fully-featured ALTER COLUMN, supports defaults, constraints, renaming, and comments.
* **Snowflake:** Supports adding, dropping, renaming columns; constraints are mostly metadata; supports column comments.
* **Oracle:** Strong ALTER TABLE support; MODIFY allows type, default, and nullability changes; supports column comments.
* **SQL Server:** ALTER COLUMN supports type and nullability changes; use `sp_rename` for column renames; supports comments via extended properties.
* **Best Practices:**

  * Always use meaningful names and consistent conventions for columns and constraints.
  * Document columns with comments for enterprise maintainability.
  * Avoid dropping columns in production without a backup; consider soft delete approach.
  * For large tables, some ALTER operations may lock the table; plan maintenance windows.

---

## **Quick Examples**

```sql
-- Add Column
ALTER TABLE users ADD COLUMN last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- Drop Column
ALTER TABLE users DROP COLUMN last_login;  -- PostgreSQL, Snowflake, Oracle, SQL Server
-- SQLite (<3.35): requires table recreation

-- Rename Column
ALTER TABLE users RENAME COLUMN username TO user_name;  -- PostgreSQL, Oracle, Snowflake
EXEC sp_rename 'users.username', 'user_name', 'COLUMN'; -- SQL Server

-- Modify Column Type
ALTER TABLE users ALTER COLUMN id TYPE BIGINT;         -- PostgreSQL
ALTER TABLE users MODIFY id NUMBER(20);               -- Oracle
ALTER TABLE users ALTER COLUMN id BIGINT;            -- SQL Server
ALTER TABLE users ALTER COLUMN id SET DATA TYPE NUMBER; -- Snowflake

-- Set / Drop DEFAULT
ALTER TABLE users ALTER COLUMN status SET DEFAULT 'active';
ALTER TABLE users ALTER COLUMN status DROP DEFAULT;

-- Set / Drop NOT NULL
ALTER TABLE users ALTER COLUMN email SET NOT NULL;
ALTER TABLE users ALTER COLUMN email DROP NOT NULL;

-- Add UNIQUE constraint
ALTER TABLE users ADD CONSTRAINT uq_email UNIQUE(email);

-- Add CHECK constraint
ALTER TABLE users ADD CONSTRAINT chk_age CHECK(age >= 0);

-- Add column comment
COMMENT ON COLUMN users.email IS 'User email address';
ALTER TABLE users MODIFY COLUMN email COMMENT = 'User email address';  -- Snowflake
```

---

This cheat sheet **covers all column-level operations across major DBs**, highlighting **differences in ALTER capabilities, constraints, and documentation**, making it **enterprise-ready for schema evolution and governance**.

