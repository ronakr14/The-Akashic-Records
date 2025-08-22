---
id: n7ppy35aqr86au8dg3co5tg
title: Stored Procedures
desc: ''
updated: 1755756813103
created: 1755756806958
---

# **Enterprise Multi-DB Stored Procedures Cheat Sheet**

| SP Operation                    | Purpose                         | Syntax                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | DB Notes / Enterprise Tips                                                                    |
| ------------------------------- | ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| **CREATE PROCEDURE**            | Define a stored procedure       | **PostgreSQL:** `CREATE OR REPLACE PROCEDURE proc_name(param1 TYPE, param2 TYPE) LANGUAGE plpgsql AS $$ BEGIN ... END; $$;` <br> **SQL Server:** `CREATE PROCEDURE proc_name @param1 INT, @param2 VARCHAR(50) AS BEGIN ... END;` <br> **Oracle:** `CREATE OR REPLACE PROCEDURE proc_name(p1 IN NUMBER, p2 OUT VARCHAR2) IS BEGIN ... END;` <br> **Snowflake:** `CREATE PROCEDURE proc_name(param1 TYPE, param2 TYPE) RETURNS STRING LANGUAGE JAVASCRIPT AS $$ ... $$;` <br> **SQLite:** Not natively supported; use triggers, views, or application logic. | Enterprise: Use procedures for encapsulating business logic in the DB layer.                  |
| **ALTER PROCEDURE / REPLACE**   | Modify existing procedure       | PostgreSQL / Oracle: `CREATE OR REPLACE PROCEDURE ...` <br> SQL Server: `ALTER PROCEDURE proc_name ...`                                                                                                                                                                                                                                                                                                                                                                                                                                                    | Use “CREATE OR REPLACE” to safely redeploy in dev/prod pipelines.                             |
| **DROP PROCEDURE**              | Remove procedure                | `DROP PROCEDURE proc_name;`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Ensure dependent jobs or triggers are updated first.                                          |
| **EXEC / CALL**                 | Execute stored procedure        | SQL Server: `EXEC proc_name @param1 = 10, @param2 = 'abc';` <br> PostgreSQL / Oracle: `CALL proc_name(10, 'abc');` <br> Snowflake: `CALL proc_name(10, 'abc');`                                                                                                                                                                                                                                                                                                                                                                                            | Enterprise: Use parameterized calls for security and maintainability.                         |
| **IN / OUT / INOUT Parameters** | Define parameter behavior       | `IN` = input, `OUT` = output, `INOUT` = input & output                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | Supported in Oracle, PostgreSQL, Snowflake; SQL Server: all parameters input unless `OUTPUT`. |
| **RETURN / RETURNING**          | Return values from procedure    | SQL Server: `RETURN int_value;` <br> PostgreSQL/Oracle: use `OUT` parameters or raise notice for messages. Snowflake: use `RETURN`.                                                                                                                                                                                                                                                                                                                                                                                                                        | Enterprise: Prefer OUT parameters or result sets over scalar returns for complex operations.  |
| **Error Handling**              | Catch exceptions                | **PostgreSQL:** `EXCEPTION WHEN others THEN ...` <br> **SQL Server:** `TRY ... CATCH ...` <br> **Oracle:** `EXCEPTION WHEN OTHERS THEN ...` <br> **Snowflake (JS):** `try { ... } catch(err) { ... }`                                                                                                                                                                                                                                                                                                                                                      | Always wrap business logic in error handling for robustness.                                  |
| **Transaction Control**         | Optional transaction management | Procedures can include `BEGIN/COMMIT/ROLLBACK` (except Snowflake: some DDL auto-commit).                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | Enterprise: Encapsulate multi-step DML safely within SPs.                                     |
| **Calling from DML / Triggers** | Encapsulate reusable logic      | SPs can be called from triggers, scheduled jobs, or applications                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | Standard enterprise practice: use SPs to centralize logic and reduce duplication.             |
| **Audit / Logging**             | Capture procedure execution     | Use logging tables or system logs inside SPs                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Enterprise: include metadata like user, timestamp, input parameters for audit trails.         |

---

## **Enterprise Design Notes**

* **SQLite:** No native stored procedures; use triggers or app logic.
* **PostgreSQL:** PL/pgSQL SPs support complex logic, exception handling, OUT parameters, transactions.
* **Snowflake:** Supports JS-based stored procedures with parameter passing, transactions, and logging.
* **Oracle:** Full-featured SPs with IN/OUT/INOUT parameters, exception handling, and transaction support.
* **SQL Server:** SPs support input/output parameters, error handling, transactions, and can return scalar values.
* **Best Practices:**

  * Use descriptive parameter names and types.
  * Include robust error handling and logging.
  * Version-control procedures in source repos.
  * Avoid hard-coded values; use parameters for dynamic logic.
  * Keep SPs modular to simplify testing and maintenance.

---

## **Quick Examples**

```sql
-- PostgreSQL
CREATE OR REPLACE PROCEDURE add_user(IN p_name TEXT, OUT p_id INT)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO users(username) VALUES (p_name) RETURNING id INTO p_id;
END;
$$;

-- Execute procedure
CALL add_user('alice', p_id);

-- SQL Server
CREATE PROCEDURE AddUser
    @username VARCHAR(50),
    @user_id INT OUTPUT
AS
BEGIN
    INSERT INTO users(username) VALUES (@username);
    SET @user_id = SCOPE_IDENTITY();
END;
-- Execute
DECLARE @id INT;
EXEC AddUser @username='bob', @user_id=@id OUTPUT;

-- Oracle
CREATE OR REPLACE PROCEDURE add_user(p_name IN VARCHAR2, p_id OUT NUMBER) IS
BEGIN
    INSERT INTO users(username) VALUES (p_name) RETURNING id INTO p_id;
END;
/

-- Snowflake (JS)
CREATE OR REPLACE PROCEDURE add_user(p_name STRING)
RETURNS STRING
LANGUAGE JAVASCRIPT
AS $$
try {
    var stmt = snowflake.createStatement({sqlText: "INSERT INTO users(username) VALUES(?)", binds: [p_name]});
    stmt.execute();
    return 'User added';
} catch(err) {
    return 'Error: ' + err;
}
$$;

CALL add_user('charlie');
```

---

This cheat sheet **covers all essential stored procedure operations across major DBs**, highlighting **creation, execution, parameters, error handling, transactions, and logging**, making it **enterprise-ready for reusable business logic, ETL tasks, and automated pipelines**.

