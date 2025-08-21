---
id: yx2d28mqeg3wmax76q40477
title: dateOperations
desc: ''
updated: 1755762588884
created: 1755762582342
---

# **Enterprise Multi-DB Date & Time Operations Cheat Sheet**

| Operation                            | Purpose                              | Syntax / Example                                                                                                                                                                                                                                                                              | DB Notes / Enterprise Tips                                                                   |
| ------------------------------------ | ------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| **Current Date / Time**              | Get system date/time                 | PostgreSQL: `CURRENT_DATE`, `CURRENT_TIMESTAMP` <br> SQLite: `DATE('now')`, `DATETIME('now')` <br> Snowflake: `CURRENT_DATE`, `CURRENT_TIMESTAMP()` <br> Oracle: `SYSDATE`, `SYSTIMESTAMP` <br> SQL Server: `GETDATE()`, `SYSDATETIME()`                                                      | Enterprise: use DB-native functions for consistency and performance.                         |
| **Date Arithmetic**                  | Add/subtract days, months, years     | PostgreSQL: `order_date + INTERVAL '7 days'` <br> SQLite: `DATE(order_date, '+7 days')` <br> Snowflake: `DATEADD(day, 7, order_date)` <br> Oracle: `order_date + 7` (days), `ADD_MONTHS(order_date, 2)` <br> SQL Server: `DATEADD(day, 7, order_date)`                                        | Enterprise: prefer native functions over manual calculations for accuracy.                   |
| **Date Difference / Interval**       | Calculate difference between dates   | PostgreSQL: `AGE(end_date, start_date)` or `end_date - start_date` <br> SQLite: `JULIANDAY(end_date) - JULIANDAY(start_date)` <br> Snowflake: `DATEDIFF(day, start_date, end_date)` <br> Oracle: `end_date - start_date` <br> SQL Server: `DATEDIFF(day, start_date, end_date)`               | Enterprise: standardize on units (days, months, years) for reporting consistency.            |
| **Extract Date Parts**               | Get year, month, day, hour, etc.     | PostgreSQL: `EXTRACT(YEAR FROM order_date)` <br> SQLite: `STRFTIME('%Y', order_date)` <br> Snowflake: `EXTRACT(YEAR FROM order_date)` <br> Oracle: `EXTRACT(YEAR FROM order_date)` <br> SQL Server: `DATEPART(YEAR, order_date)`                                                              | Enterprise: widely used in aggregation, reporting, and analytics.                            |
| **Truncate / Round Dates**           | Round to month, week, etc.           | PostgreSQL: `DATE_TRUNC('month', order_date)` <br> SQLite: `DATE(order_date, 'start of month')` <br> Snowflake: `DATE_TRUNC('MONTH', order_date)` <br> Oracle: `TRUNC(order_date, 'MM')` <br> SQL Server: `DATEFROMPARTS(YEAR(order_date), MONTH(order_date), 1)`                             | Enterprise: critical for grouping by time intervals in analytics.                            |
| **Format Dates**                     | Convert to string or specific format | PostgreSQL: `TO_CHAR(order_date, 'YYYY-MM-DD')` <br> SQLite: `STRFTIME('%Y-%m-%d', order_date)` <br> Snowflake: `TO_CHAR(order_date, 'YYYY-MM-DD')` <br> Oracle: `TO_CHAR(order_date, 'YYYY-MM-DD')` <br> SQL Server: `FORMAT(order_date, 'yyyy-MM-dd')`                                      | Enterprise: use consistent formatting for ETL, reporting, and presentation layers.           |
| **Parse / Convert Strings to Dates** | Convert string to date/time          | PostgreSQL: `TO_DATE('2025-08-01','YYYY-MM-DD')` <br> SQLite: `DATE('2025-08-01')` <br> Snowflake: `TO_DATE('2025-08-01','YYYY-MM-DD')` <br> Oracle: `TO_DATE('2025-08-01','YYYY-MM-DD')` <br> SQL Server: `CONVERT(DATE, '2025-08-01', 120)`                                                 | Enterprise: ensure correct parsing to avoid errors in ETL pipelines.                         |
| **Compare Dates**                    | Filter or join by date               | `WHERE order_date >= CURRENT_DATE - INTERVAL '30 days'` <br> Snowflake: `WHERE order_date >= DATEADD(day, -30, CURRENT_DATE)`                                                                                                                                                                 | Enterprise: always handle timezone-awareness if needed for global applications.              |
| **Best Practices**                   | Enterprise usage                     | - Store dates in DATE/TIMESTAMP type, not strings <br> - Use native functions for arithmetic and extraction <br> - Consider timezone with TIMESTAMP WITH TIME ZONE <br> - Standardize date formats across ETL & reporting <br> - Prefer DATEADD/DATE\_TRUNC/EXTRACT functions for performance | Enterprise: ensures consistent, performant, and auditable date handling across applications. |

---

## **Quick Examples**

```sql
-- PostgreSQL
SELECT CURRENT_DATE, CURRENT_TIMESTAMP;
SELECT order_date + INTERVAL '7 days';
SELECT AGE(NOW(), order_date);
SELECT EXTRACT(YEAR FROM order_date);
SELECT DATE_TRUNC('month', order_date);
SELECT TO_CHAR(order_date, 'YYYY-MM-DD');

-- SQLite
SELECT DATE('now'), DATETIME('now');
SELECT DATE(order_date, '+7 days');
SELECT JULIANDAY('2025-08-01') - JULIANDAY('2025-07-01');
SELECT STRFTIME('%Y', order_date);
SELECT DATE(order_date, 'start of month');
SELECT STRFTIME('%Y-%m-%d', order_date);

-- Snowflake
SELECT CURRENT_DATE, CURRENT_TIMESTAMP();
SELECT DATEADD(day, 7, order_date);
SELECT DATEDIFF(day, start_date, end_date);
SELECT EXTRACT(YEAR FROM order_date);
SELECT DATE_TRUNC('MONTH', order_date);
SELECT TO_CHAR(order_date, 'YYYY-MM-DD');

-- Oracle
SELECT SYSDATE, SYSTIMESTAMP FROM dual;
SELECT order_date + 7, ADD_MONTHS(order_date, 2) FROM orders;
SELECT end_date - start_date FROM orders;
SELECT EXTRACT(YEAR FROM order_date) FROM orders;
SELECT TRUNC(order_date, 'MM') FROM orders;
SELECT TO_CHAR(order_date, 'YYYY-MM-DD') FROM orders;

-- SQL Server
SELECT GETDATE(), SYSDATETIME();
SELECT DATEADD(day, 7, order_date);
SELECT DATEDIFF(day, start_date, end_date);
SELECT DATEPART(YEAR, order_date);
SELECT DATEFROMPARTS(YEAR(order_date), MONTH(order_date), 1);
SELECT FORMAT(order_date, 'yyyy-MM-dd');
```

---

This cheat sheet **covers all essential date and time operations across major DBs**, highlighting **current date, arithmetic, extraction, truncation, formatting, parsing, comparison, and best practices**, making it **enterprise-ready for analytics, ETL, reporting, and temporal logic in applications**.
