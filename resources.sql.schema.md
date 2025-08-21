---
id: jdxamo9uultxm6ckhqrzm7t
title: Schema
desc: ''
updated: 1755756417085
created: 1755756410815
---

# **Enterprise Multi-DB Schema Operations Cheat Sheet**

| Operation                            | Purpose                                              | Syntax                                                                                                                                                                                                                            | DB Notes / Enterprise Tips                                                                                                        |                                                                                   |
| ------------------------------------ | ---------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| **Create Schema / Namespace**        | Logical grouping of tables, views, and other objects | `CREATE SCHEMA schema_name;`                                                                                                                                                                                                      | PostgreSQL, Oracle, SQL Server, Snowflake support. SQLite does **not support schemas**; database file acts as a single namespace. |                                                                                   |
| **Drop Schema**                      | Remove schema and all objects                        | \`DROP SCHEMA schema\_name \[CASCADE                                                                                                                                                                                              | RESTRICT];\`                                                                                                                      | `CASCADE` drops all contained objects. `RESTRICT` prevents drop if objects exist. |
| **Alter Schema**                     | Rename or change ownership                           | PostgreSQL: `ALTER SCHEMA schema_name RENAME TO new_name;` <br>Oracle: `ALTER USER username RENAME;` (schemas tied to users) <br>SQL Server: `ALTER SCHEMA new_schema TRANSFER object;`                                           | Ownership changes vary by DB. Snowflake allows `ALTER SCHEMA` to change comment, owner, retention policy.                         |                                                                                   |
| **Grant / Revoke Permissions**       | Control access at schema level                       | `GRANT SELECT, INSERT ON ALL TABLES IN SCHEMA schema_name TO role;` <br> `REVOKE ...`                                                                                                                                             | PostgreSQL, Oracle, SQL Server, Snowflake support schema-level grants. SQLite: no schema privileges.                              |                                                                                   |
| **Schema Inspection**                | List objects within schema                           | PostgreSQL: `\dn` for schemas, `\dt schema.*` for tables <br> Oracle: `SELECT table_name FROM all_tables WHERE owner='SCHEMA_NAME';` <br> SQL Server: `SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='schema_name';` | Essential for enterprise audits and automated scripts.                                                                            |                                                                                   |
| **Set Search Path / Default Schema** | Specify default schema for operations                | PostgreSQL: `SET search_path TO schema_name;` <br> SQL Server: `ALTER USER user_name WITH DEFAULT_SCHEMA = schema_name;` <br> Snowflake: `USE SCHEMA db_name.schema_name;`                                                        | Improves query clarity; avoids cross-schema ambiguity.                                                                            |                                                                                   |
| **Schema Comments / Metadata**       | Document schema purpose                              | PostgreSQL: `COMMENT ON SCHEMA schema_name IS 'description';` <br> Snowflake: `ALTER SCHEMA schema_name SET COMMENT = 'desc';`                                                                                                    | Enterprise best practice: always document schemas for maintainability.                                                            |                                                                                   |

---

## **Enterprise Design Notes**

* **SQLite:** No schema support; everything lives in the database file. Use naming conventions for pseudo-namespacing (`schema_table_name`).
* **PostgreSQL:** Fully supports multiple schemas per database; search\_path allows default schema for session; great for multi-tenant designs.
* **Snowflake:** Database → Schema → Object hierarchy; schemas can have comments, retention policies, and access controls.
* **Oracle:** Schemas are tightly coupled with users; creating a user creates a schema; object ownership follows schema/user.
* **SQL Server:** Supports multiple schemas per database; `dbo` is default; can transfer objects between schemas.
* **Permissions:** Always grant/revoke at schema level to simplify enterprise security management.
* **Naming Conventions:** Prefix schema names with team, module, or project identifiers for clarity.

---

## **Quick Examples**

```sql
-- Create Schema
CREATE SCHEMA sales;

-- Drop Schema
DROP SCHEMA sales CASCADE;  -- Removes all tables, views, etc.

-- Rename Schema (PostgreSQL)
ALTER SCHEMA sales RENAME TO sales_archive;

-- Transfer Object to Another Schema (SQL Server)
ALTER SCHEMA archive TRANSFER sales.orders;

-- Set Default Schema for User (SQL Server)
ALTER USER john WITH DEFAULT_SCHEMA = archive;

-- Grant Permissions
GRANT SELECT, INSERT ON ALL TABLES IN SCHEMA sales TO analyst_role;

-- Snowflake: Use Schema
USE SCHEMA analytics.sales;

-- Add Comment to Schema
COMMENT ON SCHEMA sales IS 'Sales module for Q2 reporting';
```

---

This **one-page cheat sheet** covers **schema operations across major DBs**, highlighting **differences in schema support, ownership, and permissions**, making it **enterprise-ready for design, access control, and multi-tenant systems**.

