---
id: 3k4zqahqz09xxbmsunm7f6t
title: Cte
desc: ''
updated: 1755756946177
created: 1755756938321
---
# **Enterprise Multi-DB CTE (Common Table Expression) Cheat Sheet**

| CTE Type                              | Purpose                                                      | Syntax / Example                                                                                                                                                                                         | DB Notes / Enterprise Tips                                                                                                                                        |
| ------------------------------------- | ------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Basic / Non-Recursive CTE**         | Modular subquery; improves readability                       | `sql WITH cte_name AS (SELECT col1, col2 FROM table_name WHERE condition) SELECT * FROM cte_name WHERE col2 > 100;`                                                                                      | Supported in all DBs. Enterprise: use to break complex queries into readable blocks.                                                                              |
| **Recursive CTE**                     | Iterative queries (hierarchies, graph, tree traversal)       | `sql WITH RECURSIVE cte_name(col1, col2) AS (SELECT col1, col2 FROM table WHERE condition UNION ALL SELECT t.col1, t.col2 FROM table t JOIN cte_name c ON t.parent_id = c.col1) SELECT * FROM cte_name;` | PostgreSQL, SQL Server, Oracle, Snowflake support recursion. SQLite supports `WITH RECURSIVE`. Use for org charts, bill of materials, hierarchical relationships. |
| **Multiple CTEs**                     | Define multiple temporary result sets                        | `sql WITH cte1 AS (...), cte2 AS (...) SELECT * FROM cte1 JOIN cte2 ON cte1.id = cte2.ref_id;`                                                                                                           | Modular approach improves maintainability. All DBs support multiple CTEs in one query.                                                                            |
| **CTE with INSERT / UPDATE / DELETE** | Use CTE as input to DML                                      | `sql WITH recent_orders AS (SELECT * FROM orders WHERE order_date > CURRENT_DATE - INTERVAL '30 days') DELETE FROM orders o WHERE o.id IN (SELECT id FROM recent_orders);`                               | Enterprise: improves performance and readability. Snowflake & PostgreSQL fully support CTE-based DML. SQL Server supports `UPDATE FROM CTE`.                      |
| **CTE with Aggregates**               | Compute intermediate aggregates                              | `sql WITH order_totals AS (SELECT user_id, SUM(amount) AS total_amount FROM orders GROUP BY user_id) SELECT * FROM order_totals WHERE total_amount > 1000;`                                              | Enterprise reporting and analytics use-case; avoids nested subqueries.                                                                                            |
| **CTE with Window Functions**         | Apply ranking, running totals, analytics                     | `sql WITH ranked_orders AS (SELECT *, ROW_NUMBER() OVER(PARTITION BY user_id ORDER BY order_date DESC) AS rn FROM orders) SELECT * FROM ranked_orders WHERE rn = 1;`                                     | Supported in PostgreSQL, SQL Server, Oracle, Snowflake, SQLite >=3.25.                                                                                            |
| **Materialized vs Inline CTE**        | Materialized = reusable block; Inline = optimizer may inline | DB-dependent; Snowflake and PostgreSQL optimize automatically; SQL Server may inline unless `OPTION (MAXRECURSION)`.                                                                                     | Enterprise: understand materialization for performance tuning.                                                                                                    |

---

## **Enterprise Design Notes**

* **SQLite:** Supports `WITH` and `WITH RECURSIVE` for hierarchical queries; inline execution.
* **PostgreSQL:** Full-featured; supports recursive, multiple, DML-based, window-function CTEs.
* **Snowflake:** Supports CTEs in all queries; optimized for analytics workloads.
* **Oracle:** Supports CTEs (`WITH`) and recursive queries; can be used for hierarchical queries (`CONNECT BY` alternative).
* **SQL Server:** Supports CTEs, recursive CTEs, DML from CTEs, and ranking/window functions.
* **Best Practices:**

  * Use CTEs for **readability and modular query design**.
  * Avoid excessive recursion depth; use `MAXRECURSION` in SQL Server.
  * Combine CTEs with DML carefully; may affect performance if materialized repeatedly.
  * Prefer CTEs over deeply nested subqueries for maintainability and debugging.
  * Use descriptive CTE names for enterprise clarity.

---

## **Quick Examples**

```sql
-- Basic CTE
WITH recent_orders AS (
    SELECT * FROM orders WHERE order_date > CURRENT_DATE - INTERVAL '30 days'
)
SELECT * FROM recent_orders;

-- Recursive CTE (hierarchy)
WITH RECURSIVE org_chart AS (
    SELECT employee_id, manager_id, name FROM employees WHERE manager_id IS NULL
    UNION ALL
    SELECT e.employee_id, e.manager_id, e.name
    FROM employees e
    JOIN org_chart o ON e.manager_id = o.employee_id
)
SELECT * FROM org_chart;

-- Multiple CTEs
WITH cte1 AS (SELECT id, name FROM users),
     cte2 AS (SELECT user_id, SUM(amount) AS total FROM orders GROUP BY user_id)
SELECT cte1.name, cte2.total
FROM cte1 JOIN cte2 ON cte1.id = cte2.user_id;

-- CTE with window function
WITH ranked_orders AS (
    SELECT user_id, order_id, ROW_NUMBER() OVER(PARTITION BY user_id ORDER BY order_date DESC) AS rn
    FROM orders
)
SELECT * FROM ranked_orders WHERE rn = 1;

-- CTE with DML (PostgreSQL / Snowflake)
WITH recent_orders AS (
    SELECT id FROM orders WHERE order_date < CURRENT_DATE - INTERVAL '1 year'
)
DELETE FROM orders o WHERE o.id IN (SELECT id FROM recent_orders);
```

---

This cheat sheet **covers all essential CTE operations across major DBs**, highlighting **basic, recursive, multiple, DML, aggregate, and window-function CTEs**, making it **enterprise-ready for modular, maintainable, and high-performance queries**.
