---
id: mw0w3mt5b6cuypsvplj3918
title: stringOperations
desc: ''
updated: 1755762616577
created: 1755762610351
---

# **Enterprise Multi-DB String Operations Cheat Sheet**

| Operation                                    | Purpose                         | Syntax / Example                                                                                                                                                                                                                                                           | DB Notes / Enterprise Tips                                                                                                     |                               |   |                                                                         |                                                                                    |                                               |                                                                                        |
| -------------------------------------------- | ------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ | ----------------------------- | - | ----------------------------------------------------------------------- | ---------------------------------------------------------------------------------- | --------------------------------------------- | -------------------------------------------------------------------------------------- |
| **Concatenation**                            | Join strings                    | PostgreSQL: \`'Hello '                                                                                                                                                                                                                                                     |                                                                                                                                | 'World'`<br> SQLite:`'Hello ' |   | 'World'`<br> Snowflake:`CONCAT('Hello ', 'World')`<br> Oracle:`'Hello ' |                                                                                    | 'World'`<br> SQL Server:`'Hello ' + 'World'\` | Enterprise: prefer native concatenation; avoid implicit conversions for numeric types. |
| **Substring**                                | Extract part of a string        | PostgreSQL/SQLite: `SUBSTR(name, 1, 5)` <br> Snowflake: `SUBSTR(name, 1, 5)` <br> Oracle: `SUBSTR(name, 1, 5)` <br> SQL Server: `SUBSTRING(name, 1, 5)`                                                                                                                    | Enterprise: 1-based indexing in most DBs; adjust for zero-based expectations in app code.                                      |                               |   |                                                                         |                                                                                    |                                               |                                                                                        |
| **String Length**                            | Get number of characters        | PostgreSQL: `LENGTH(name)` <br> SQLite: `LENGTH(name)` <br> Snowflake: `LENGTH(name)` <br> Oracle: `LENGTH(name)` <br> SQL Server: `LEN(name)`                                                                                                                             | Enterprise: use for validation, analytics, or conditional logic.                                                               |                               |   |                                                                         |                                                                                    |                                               |                                                                                        |
| **Upper / Lower Case**                       | Convert case                    | PostgreSQL: `UPPER(name)`, `LOWER(name)` <br> SQLite: `UPPER(name)`, `LOWER(name)` <br> Snowflake: `UPPER(name)`, `LOWER(name)` <br> Oracle: `UPPER(name)`, `LOWER(name)` <br> SQL Server: `UPPER(name)`, `LOWER(name)`                                                    | Enterprise: normalize text for comparisons, searches, or reporting.                                                            |                               |   |                                                                         |                                                                                    |                                               |                                                                                        |
| **Trim / LTRIM / RTRIM**                     | Remove spaces or characters     | PostgreSQL: `TRIM(name)`, `LTRIM(name)`, `RTRIM(name)` <br> SQLite: `TRIM(name)`, `LTRIM(name)`, `RTRIM(name)` <br> Snowflake: `TRIM(name)` <br> Oracle: `TRIM(name)` <br> SQL Server: `LTRIM(RTRIM(name))`                                                                | Enterprise: clean input data before inserts or comparisons; combine with UPPER/LOWER for normalized joins.                     |                               |   |                                                                         |                                                                                    |                                               |                                                                                        |
| **Replace / Translate**                      | Replace substring or characters | PostgreSQL/SQLite/Snowflake/Oracle: `REPLACE(name, 'old', 'new')` <br> SQL Server: `REPLACE(name, 'old', 'new')`                                                                                                                                                           | Enterprise: use for data cleansing or standardization; `TRANSLATE` for character-level mapping.                                |                               |   |                                                                         |                                                                                    |                                               |                                                                                        |
| **Pattern Matching (LIKE / ILIKE / REGEXP)** | Match strings                   | PostgreSQL: `name LIKE 'A%'` / `name ILIKE '%abc%'` / `name ~ 'regex'` <br> SQLite: `name LIKE 'A%'` <br> Snowflake: `name LIKE 'A%'` / `REGEXP='regex'` <br> Oracle: `name LIKE 'A%'` / `REGEXP_LIKE(name, 'regex')` <br> SQL Server: `name LIKE 'A%'`                    | Enterprise: use case-insensitive searches (ILIKE) in PostgreSQL/Snowflake for user input matching; regex for complex patterns. |                               |   |                                                                         |                                                                                    |                                               |                                                                                        |
| **Concatenation with Separator**             | Join multiple strings           | PostgreSQL: `CONCAT_WS('-', col1, col2)` <br> Snowflake: `CONCAT_WS('-', col1, col2)` <br> SQL Server: `CONCAT_WS('-', col1, col2)` <br> Oracle: \`col1                                                                                                                    |                                                                                                                                | '-'                           |   | col2\`                                                                  | Enterprise: improves readability; standard for CSV exports or formatted reporting. |                                               |                                                                                        |
| **Best Practices**                           | Enterprise usage                | - Normalize string case for comparisons <br> - Trim and clean input before storage <br> - Prefer `CONCAT`/`CONCAT_WS` for multi-part joins <br> - Use pattern matching judiciously for performance <br> - Use REGEXP functions for complex string extraction or validation | Enterprise: ensures consistent, clean, and performant string operations across ETL, analytics, and reporting workflows.        |                               |   |                                                                         |                                                                                    |                                               |                                                                                        |

---

## **Quick Examples**

```sql
-- Concatenation
SELECT 'Hello ' || 'World';       -- PostgreSQL, SQLite, Oracle
SELECT CONCAT('Hello ', 'World'); -- Snowflake
SELECT 'Hello ' + 'World';        -- SQL Server

-- Substring
SELECT SUBSTR(name, 1, 5);       -- PostgreSQL, SQLite, Snowflake, Oracle
SELECT SUBSTRING(name, 1, 5);    -- SQL Server

-- Length
SELECT LENGTH(name);              -- PostgreSQL, SQLite, Snowflake, Oracle
SELECT LEN(name);                 -- SQL Server

-- Upper / Lower
SELECT UPPER(name), LOWER(name);

-- Trim
SELECT TRIM(name), LTRIM(name), RTRIM(name); -- PostgreSQL, SQLite, Oracle
SELECT LTRIM(RTRIM(name));                   -- SQL Server

-- Replace
SELECT REPLACE(name, 'old', 'new');

-- Pattern Matching
SELECT * FROM users WHERE name LIKE 'A%';
SELECT * FROM users WHERE name ~ '^A.*';    -- PostgreSQL regex
SELECT * FROM users WHERE REGEXP_LIKE(name, '^A.*'); -- Oracle
SELECT * FROM users WHERE name REGEXP='^A.*'; -- Snowflake

-- Concatenation with separator
SELECT CONCAT_WS('-', first_name, last_name); -- PostgreSQL, Snowflake, SQL Server
SELECT first_name || '-' || last_name;       -- Oracle
```

---

This cheat sheet **covers all essential string operations across major DBs**, highlighting **concatenation, substring, length, case conversion, trimming, replace, pattern matching, and best practices**, making it **enterprise-ready for ETL, data cleaning, reporting, and analytics workflows**.

