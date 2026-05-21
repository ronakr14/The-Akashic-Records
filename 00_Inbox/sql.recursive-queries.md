---
id: k9734oixao6buu5ovgx3tc1
title: Recursive Queries
desc: ''
updated: 1755757000349
created: 1755756994106
---

# **Enterprise Multi-DB Recursive Queries Cheat Sheet**

| Recursive Query Type             | Purpose                                                           | Syntax / Example                                                                                                                                                                                         | DB Notes / Enterprise Tips                                                                                                                                                                  |
| -------------------------------- | ----------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Recursive CTE**                | Iterative queries like hierarchies, org charts, bill of materials | `sql WITH RECURSIVE cte_name(col1, col2) AS (SELECT col1, col2 FROM table WHERE condition UNION ALL SELECT t.col1, t.col2 FROM table t JOIN cte_name c ON t.parent_id = c.col1) SELECT * FROM cte_name;` | Supported in SQLite (`WITH RECURSIVE`), PostgreSQL, Snowflake, SQL Server, Oracle (with `CONNECT BY` as alternative). Enterprise: ideal for hierarchical reporting and dependency analysis. |
| **Anchor Member**                | Starting point of recursion                                       | `SELECT col1, col2 FROM table WHERE parent_id IS NULL`                                                                                                                                                   | Defines root nodes for tree traversal.                                                                                                                                                      |
| **Recursive Member**             | Iterative step                                                    | `SELECT t.col1, t.col2 FROM table t JOIN cte_name c ON t.parent_id = c.col1`                                                                                                                             | Joins back to CTE to fetch next level of hierarchy.                                                                                                                                         |
| **Termination / Stop Condition** | Ensures recursion ends                                            | Implicit via `UNION ALL` or optional `WHERE` clause                                                                                                                                                      | Avoid infinite recursion; SQL Server: use `OPTION (MAXRECURSION n)`.                                                                                                                        |
| **Depth / Level Tracking**       | Track hierarchy level                                             | `SELECT cte_name.*, ROW_NUMBER() OVER() AS level FROM cte_name` or add `level + 1` in recursive member                                                                                                   | Useful for org charts, nested categories, or BOMs.                                                                                                                                          |
| **Multiple Recursive CTEs**      | Handle multiple hierarchies                                       | `sql WITH RECURSIVE cte1 AS (...), cte2 AS (...) SELECT ...`                                                                                                                                             | Enterprise: modular design improves readability and maintainability.                                                                                                                        |
| **Recursive DML**                | Apply recursive updates                                           | Rare; usually retrieve hierarchical info and then use DML                                                                                                                                                | PostgreSQL/Snowflake allow using recursive query results in CTE-based DML. SQL Server: `UPDATE FROM CTE`. Oracle: use PL/SQL.                                                               |
| **Performance Optimization**     | Index parent/foreign keys, limit recursion                        | Add `WHERE` clauses, limit depth, or materialize results                                                                                                                                                 | Enterprise: essential for large datasets; prevent performance bottlenecks.                                                                                                                  |
| **Alternative Oracle Syntax**    | Oracle hierarchical queries                                       | `SELECT employee_id, manager_id, LEVEL FROM employees START WITH manager_id IS NULL CONNECT BY PRIOR employee_id = manager_id;`                                                                          | Oracle’s `CONNECT BY` can be simpler for small hierarchies; CTE preferred for portability.                                                                                                  |

---

## **Enterprise Design Notes**

* **SQLite:** Supports `WITH RECURSIVE`; max recursion depth can be set via pragma.
* **PostgreSQL:** Full recursive CTE support; use anchor + recursive member.
* **Snowflake:** Supports recursive CTEs; optimized for hierarchical analytics.
* **Oracle:** Supports `WITH` recursive CTEs and `CONNECT BY` for hierarchical queries.
* **SQL Server:** Supports `WITH` recursive CTEs; limit recursion with `OPTION (MAXRECURSION n)`.
* **Best Practices:**

  * Always define **anchor and recursive members clearly**.
  * Track **depth/level** to avoid infinite loops.
  * Use **indexes** on parent/child columns for performance.
  * Prefer **CTEs over nested subqueries** for readability.
  * Use **MAXRECURSION** or stop conditions in enterprise pipelines.

---

## **Quick Examples**

```sql
-- PostgreSQL / SQLite / Snowflake / SQL Server recursive CTE
WITH RECURSIVE org_chart AS (
    -- Anchor member (top-level managers)
    SELECT employee_id, manager_id, name, 1 AS level
    FROM employees
    WHERE manager_id IS NULL
    UNION ALL
    -- Recursive member
    SELECT e.employee_id, e.manager_id, e.name, c.level + 1
    FROM employees e
    JOIN org_chart c ON e.manager_id = c.employee_id
)
SELECT * FROM org_chart;

-- Oracle recursive CTE
WITH org_chart (employee_id, manager_id, name, lvl) AS (
    SELECT employee_id, manager_id, name, 1
    FROM employees
    WHERE manager_id IS NULL
    UNION ALL
    SELECT e.employee_id, e.manager_id, e.name, c.lvl + 1
    FROM employees e
    JOIN org_chart c ON e.manager_id = c.employee_id
)
SELECT * FROM org_chart;

-- Oracle alternative using CONNECT BY
SELECT employee_id, manager_id, LEVEL AS lvl
FROM employees
START WITH manager_id IS NULL
CONNECT BY PRIOR employee_id = manager_id;

-- Recursive CTE with limited depth (SQL Server)
WITH org_chart AS (
    SELECT employee_id, manager_id, name, 1 AS level
    FROM employees
    WHERE manager_id IS NULL
    UNION ALL
    SELECT e.employee_id, e.manager_id, e.name, c.level + 1
    FROM employees e
    JOIN org_chart c ON e.manager_id = c.employee_id
)
SELECT * FROM org_chart
OPTION (MAXRECURSION 10);
```

---

This cheat sheet **covers all essential recursive query operations across major DBs**, highlighting **recursive CTEs, anchor/recursive members, depth tracking, alternative Oracle syntax, and performance considerations**, making it **enterprise-ready for hierarchical reporting, BOMs, and org chart analytics**.

