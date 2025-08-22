---
id: xn1pm45t3mbz49kxfnqw9iv
title: Query Planner
desc: ''
updated: 1755757067455
created: 1755757059193
---

# **Enterprise Multi-DB Query Planner & Optimization Cheat Sheet**

| Feature / Operation                      | Purpose                              | Syntax / Example                                                                                                                                                             | DB Notes / Enterprise Tips                                                                                                                                                  |
| ---------------------------------------- | ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **EXPLAIN**                              | Show query execution plan            | `EXPLAIN SELECT * FROM orders WHERE amount > 100;`                                                                                                                           | PostgreSQL, SQLite, SQL Server, Snowflake, Oracle support. Enterprise: use to understand cost, join order, and index usage.                                                 |
| **EXPLAIN ANALYZE**                      | Execute query + show runtime stats   | `EXPLAIN ANALYZE SELECT * FROM orders WHERE amount > 100;`                                                                                                                   | PostgreSQL, SQLite, Oracle (`EXPLAIN PLAN FOR` + `DBMS_XPLAN.DISPLAY`), Snowflake (`EXPLAIN` + query), SQL Server: `SET STATISTICS PROFILE ON`. Use for performance tuning. |
| **Query Cost / Estimated Rows**          | Estimate query cost for optimization | Displayed in explain plan                                                                                                                                                    | Enterprise: use cost to detect expensive joins, missing indexes, or scans.                                                                                                  |
| **Index Scan / Table Scan**              | Execution method for retrieving rows | Shown in `EXPLAIN` output                                                                                                                                                    | Prefer **index scans** for large tables; table scans okay for small tables.                                                                                                 |
| **Nested Loop / Hash Join / Merge Join** | Join algorithm chosen by planner     | Displayed in EXPLAIN                                                                                                                                                         | Enterprise: understand join strategy to optimize multi-join queries.                                                                                                        |
| **CTE / Subquery Optimization**          | Planner may inline or materialize    | EXPLAIN shows if CTE is materialized                                                                                                                                         | PostgreSQL: `MATERIALIZED` vs `NOT MATERIALIZED`. SQL Server: CTE usually inline.                                                                                           |
| **Query Hints**                          | Influence optimizer behavior         | SQL Server: `OPTION (LOOP JOIN, HASH JOIN)` <br> Oracle: `/*+ USE_HASH(t1 t2) */` <br> PostgreSQL: generally no hints, adjust planner cost constants                         | Use hints only when necessary; prefer rewriting query first.                                                                                                                |
| **Statistics / ANALYZE / UPDATE STATS**  | Update table stats for better plans  | PostgreSQL: `ANALYZE table_name;` <br> SQL Server: `UPDATE STATISTICS table_name;` <br> Oracle: `DBMS_STATS.GATHER_TABLE_STATS(...)` <br> SQLite: auto-analyze or `ANALYZE;` | Enterprise: essential for large tables and periodic ETL loads.                                                                                                              |
| **Execution Plan Output**                | Visualize / debug query              | PostgreSQL: `EXPLAIN (ANALYZE, VERBOSE, BUFFERS)` <br> SQL Server: `SET STATISTICS XML ON` <br> Oracle: `DBMS_XPLAN.DISPLAY_CURSOR` <br> Snowflake: `EXPLAIN SELECT ...`     | Enterprise: review row estimates vs actual rows for bottleneck detection.                                                                                                   |
| **Parallel Execution**                   | Leverage multiple CPU cores          | PostgreSQL: parallel queries for large tables <br> Oracle / SQL Server / Snowflake: automatic or hinted                                                                      | Enterprise: enable for heavy analytics queries; monitor CPU/memory usage.                                                                                                   |
| **Query Rewriting / Optimization Tips**  | Reduce runtime, improve plan         | - Replace correlated subqueries with joins or CTEs <br> - Use EXISTS over IN for large datasets <br> - Limit SELECT columns <br> - Index join/filter columns                 | Enterprise: query rewrites often outperform optimizer hints; always test.                                                                                                   |

---

## **Enterprise Design Notes**

* **SQLite:** Limited query planner; EXPLAIN shows opcode instructions. Use for small to medium tables.
* **PostgreSQL:** Advanced planner; supports nested loop, hash, merge joins; parallel queries; cost-based optimizer.
* **Snowflake:** Cloud-native query optimizer; uses automatic clustering and pruning; explain shows physical and logical plan.
* **Oracle:** Cost-based optimizer; supports hints, parallel execution, materialized views.
* **SQL Server:** Cost-based optimizer; supports query hints, plan guides, parallel execution, statistics management.
* **Best Practices:**

  * Always **analyze query plans before production deployment**.
  * Maintain **up-to-date statistics** on large tables.
  * Prefer **query rewrites** over hints for maintainability.
  * Use **execution plan visualizations** in enterprise dashboards.
  * Monitor **actual vs estimated rows** for performance anomalies.

---

## **Quick Examples**

```sql
-- PostgreSQL basic explain
EXPLAIN SELECT * FROM orders WHERE amount > 100;

-- PostgreSQL with runtime stats
EXPLAIN ANALYZE SELECT * FROM orders WHERE amount > 100;

-- SQL Server execution plan
SET STATISTICS XML ON;
SELECT * FROM orders WHERE amount > 100;
SET STATISTICS XML OFF;

-- Oracle explain plan
EXPLAIN PLAN FOR
SELECT * FROM orders WHERE amount > 100;
SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);

-- Snowflake explain
EXPLAIN SELECT * FROM orders WHERE amount > 100;

-- PostgreSQL with CTE optimization hint
WITH recent_orders AS MATERIALIZED (
    SELECT * FROM orders WHERE order_date > CURRENT_DATE - INTERVAL '30 days'
)
SELECT * FROM recent_orders;
```

---

This cheat sheet **covers all essential query planning and optimization features across major DBs**, highlighting **explain plans, execution methods, join algorithms, statistics, query hints, parallelism, and optimization strategies**, making it **enterprise-ready for performance tuning, ETL pipelines, and analytics workloads**.

