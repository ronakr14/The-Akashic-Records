---
id: 94qsybe4t4qewu5fr07s3ew
title: Functions
desc: ''
updated: 1755756892515
created: 1755756887227
---

# **Enterprise Multi-DB Functions Cheat Sheet**

| Function Operation                         | Purpose                                    | Syntax                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | DB Notes / Enterprise Tips                                                                                                      |                                                                                                        |
| ------------------------------------------ | ------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| **CREATE FUNCTION**                        | Define reusable logic that returns a value | **PostgreSQL:** `CREATE OR REPLACE FUNCTION func_name(param1 TYPE, ...) RETURNS return_type LANGUAGE plpgsql AS $$ BEGIN ... END; $$;` <br> **SQL Server:** `CREATE FUNCTION func_name(@param1 TYPE, ...) RETURNS return_type AS BEGIN ... RETURN value; END;` <br> **Oracle:** `CREATE OR REPLACE FUNCTION func_name(p1 IN TYPE, ...) RETURN return_type IS BEGIN ... RETURN value; END;` <br> **Snowflake:** \`CREATE OR REPLACE FUNCTION func\_name(param1 TYPE, ...) RETURNS TYPE LANGUAGE SQL | JAVASCRIPT AS $...$;\` <br> **SQLite:** Supports scalar or aggregate functions via extensions or application-defined functions. | Enterprise: Use functions for reusable computations, derived columns, and encapsulated business logic. |
| **ALTER FUNCTION / REPLACE**               | Modify existing function                   | PostgreSQL / Oracle / Snowflake: `CREATE OR REPLACE FUNCTION ...` <br> SQL Server: `ALTER FUNCTION func_name ...`                                                                                                                                                                                                                                                                                                                                                                                  | Use “CREATE OR REPLACE” to safely redeploy in pipelines.                                                                        |                                                                                                        |
| **DROP FUNCTION**                          | Remove function                            | `DROP FUNCTION func_name([param_types]);`                                                                                                                                                                                                                                                                                                                                                                                                                                                          | Ensure no dependent views, procedures, or jobs before dropping.                                                                 |                                                                                                        |
| **EXECUTE / CALL / SELECT**                | Invoke function                            | PostgreSQL / Oracle / Snowflake: `SELECT func_name(args);` <br> SQL Server: `SELECT dbo.func_name(args);`                                                                                                                                                                                                                                                                                                                                                                                          | Use in queries, computed columns, or expressions.                                                                               |                                                                                                        |
| **IN / OUT / INOUT Parameters**            | Define parameter behavior                  | **Functions** generally use `IN` parameters; SQL Server does not support `OUT` in scalar functions.                                                                                                                                                                                                                                                                                                                                                                                                | Enterprise: Functions are pure expressions in most DBs; avoid side effects.                                                     |                                                                                                        |
| **RETURN / RETURNS**                       | Specify return type                        | PostgreSQL / Oracle / Snowflake: `RETURNS type` <br> SQL Server: `RETURNS type`                                                                                                                                                                                                                                                                                                                                                                                                                    | Can return scalar, table, or complex type (table-valued functions in SQL Server, Oracle).                                       |                                                                                                        |
| **Table-Valued / Set-Returning Functions** | Return multiple rows                       | PostgreSQL: `RETURNS TABLE(col1 TYPE, col2 TYPE)` <br> SQL Server: `RETURNS TABLE AS RETURN SELECT ...` <br> Oracle: `PIPELINED FUNCTION RETURN table_type`                                                                                                                                                                                                                                                                                                                                        | Useful for reusable query logic in reports, ETL, or analytics.                                                                  |                                                                                                        |
| **Error Handling**                         | Catch exceptions                           | PostgreSQL: `EXCEPTION WHEN others THEN ...` <br> SQL Server: `TRY ... CATCH ...` <br> Oracle: `EXCEPTION WHEN ... THEN ...` <br> Snowflake: JS: `try { ... } catch(err) { ... }`                                                                                                                                                                                                                                                                                                                  | Enterprise: Functions should fail gracefully, log errors if needed.                                                             |                                                                                                        |
| **Transactions**                           | Optional transaction management            | Generally functions should not include explicit COMMIT/ROLLBACK; keep functions deterministic                                                                                                                                                                                                                                                                                                                                                                                                      | Enterprise: avoid side-effects in functions; use procedures for DML.                                                            |                                                                                                        |
| **Deterministic / Immutable Functions**    | Mark pure functions                        | PostgreSQL: `IMMUTABLE` / `STABLE` / `VOLATILE` <br> Oracle: `DETERMINISTIC` <br> Snowflake: deterministic optional                                                                                                                                                                                                                                                                                                                                                                                | Enterprise: Helps optimizer; ensures repeatable results and index usage.                                                        |                                                                                                        |

---

## **Enterprise Design Notes**

* **SQLite:** Limited function support; user-defined scalar and aggregate functions possible via extensions or app code.
* **PostgreSQL:** Full-featured; supports scalar, set-returning, IMMUTABLE/STABLE functions, exception handling.
* **Snowflake:** SQL or JS-based functions; supports scalar and table returns. Transactions limited.
* **Oracle:** Scalar, pipelined, table-returning, deterministic; supports IN parameters, exception handling.
* **SQL Server:** Scalar and table-valued functions; cannot modify data directly inside functions; supports deterministic marking via `WITH SCHEMABINDING`.
* **Best Practices:**

  * Use functions for **computations, derived columns, and reusable expressions**.
  * Keep functions **side-effect free**; use procedures for DML.
  * Include robust **error handling**.
  * Leverage **deterministic/immutable** flags for performance optimization.
  * Version-control function scripts for enterprise change management.

---

## **Quick Examples**

```sql
-- PostgreSQL scalar function
CREATE OR REPLACE FUNCTION get_discount(price NUMERIC) RETURNS NUMERIC
LANGUAGE plpgsql AS $$
BEGIN
    RETURN price * 0.9;
END;
$$;

SELECT get_discount(100);

-- SQL Server scalar function
CREATE FUNCTION dbo.get_discount(@price NUMERIC)
RETURNS NUMERIC
AS
BEGIN
    RETURN @price * 0.9;
END;

SELECT dbo.get_discount(100);

-- Oracle scalar function
CREATE OR REPLACE FUNCTION get_discount(p_price NUMBER) RETURN NUMBER IS
BEGIN
    RETURN p_price * 0.9;
END;
/

SELECT get_discount(100) FROM dual;

-- PostgreSQL table-valued function
CREATE OR REPLACE FUNCTION top_customers(limit INT)
RETURNS TABLE(id INT, username TEXT) AS $$
BEGIN
    RETURN QUERY SELECT id, username FROM users ORDER BY total_orders DESC LIMIT limit;
END;
$$ LANGUAGE plpgsql;

SELECT * FROM top_customers(5);

-- Snowflake JS function
CREATE OR REPLACE FUNCTION get_discount(price NUMBER)
RETURNS NUMBER
LANGUAGE JAVASCRIPT
AS $$
    return price * 0.9;
$$;

SELECT get_discount(100);
```

---

This cheat sheet **covers all essential SQL function operations across major DBs**, highlighting **creation, execution, parameters, return types, error handling, and deterministic design**, making it **enterprise-ready for reusable computations, analytics, and derived data logic**.

