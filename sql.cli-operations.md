---
id: z4jukh9so1d33slqqwjpvb9
title: CLI Operations
desc: ''
updated: 1755757268045
created: 1755757261707
---

# **Enterprise Multi-DB CLI Operations Cheat Sheet**

| Operation                    | Purpose                 | CLI Syntax / Example                                                                                                                                                                                                                                                                                                             | DB Notes / Enterprise Tips                                                                  |
| ---------------------------- | ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| **Connect to Database**      | Open DB session         | **SQLite:** `sqlite3 mydb.db` <br> **PostgreSQL:** `psql -h host -U user -d dbname` <br> **Snowflake:** `snowsql -a account -u user -d dbname -s schema` <br> **Oracle:** `sqlplus user/password@//host:port/service_name` <br> **SQL Server:** `sqlcmd -S server -U user -P password -d dbname`                                 | Enterprise: use environment variables for credentials; prefer secure connections (SSL/TLS). |
| **List Databases / Schemas** | Inspect DB structure    | **PostgreSQL:** `\l` <br> **SQLite:** `.databases` <br> **Snowflake:** `SHOW DATABASES;` <br> **Oracle:** `SELECT username FROM all_users;` <br> **SQL Server:** `SELECT name FROM sys.databases;`                                                                                                                               | Use to quickly verify available environments and access rights.                             |
| **List Tables**              | Inspect tables          | **PostgreSQL:** `\dt` <br> **SQLite:** `.tables` <br> **Snowflake:** `SHOW TABLES;` <br> **Oracle:** `SELECT table_name FROM user_tables;` <br> **SQL Server:** `SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES;`                                                                                                              | Enterprise: ensure proper schema context; some DBs require `schema.table`.                  |
| **Describe Table / Columns** | Inspect schema          | **PostgreSQL:** `\d table_name` <br> **SQLite:** `.schema table_name` <br> **Snowflake:** `DESC TABLE table_name;` <br> **Oracle:** `DESCRIBE table_name;` <br> **SQL Server:** `sp_help 'table_name';`                                                                                                                          | Enterprise: quickly validate columns, data types, constraints.                              |
| **Execute SQL Queries**      | Run ad-hoc queries      | `SELECT * FROM table_name;`                                                                                                                                                                                                                                                                                                      | All DBs support standard SQL; CLI sessions good for testing or batch jobs.                  |
| **Execute SQL Scripts**      | Run multiple statements | **PostgreSQL:** `psql -f script.sql` <br> **SQLite:** `.read script.sql` <br> **Snowflake:** `snowsql -f script.sql` <br> **Oracle:** `@script.sql` <br> **SQL Server:** `sqlcmd -i script.sql`                                                                                                                                  | Enterprise: use scripts for repeatable deployments, schema migrations.                      |
| **Export / Dump Data**       | Backup or ETL           | **PostgreSQL:** `pg_dump -U user -d dbname -f backup.sql` <br> **SQLite:** `.dump > backup.sql` <br> **Snowflake:** `COPY INTO 's3://bucket/file.csv' FROM table_name` <br> **Oracle:** `expdp user/password tables=table_name` <br> **SQL Server:** `bcp table_name out file.csv -c -t, -S server -U user -P password`          | Enterprise: automate backups, incremental extracts for ETL pipelines.                       |
| **Import / Load Data**       | Load data into DB       | **PostgreSQL:** `psql -d dbname -f file.sql` <br> **SQLite:** `.read file.sql` <br> **Snowflake:** `COPY INTO table_name FROM 's3://bucket/file.csv' FILE_FORMAT = (TYPE = CSV)` <br> **Oracle:** `impdp user/password tables=table_name` <br> **SQL Server:** `bcp table_name in file.csv -c -t, -S server -U user -P password` | Enterprise: ensure correct file formats, encoding, and permissions.                         |
| **Transaction Control**      | Commit / Rollback       | Execute SQL commands: `BEGIN; ... COMMIT;` / `ROLLBACK;`                                                                                                                                                                                                                                                                         | All DBs support transactions; useful in CLI for testing scripts or DML batches.             |
| **Exit CLI**                 | Close session           | **PostgreSQL:** `\q` <br> **SQLite:** `.exit` <br> **Snowflake:** `!exit` <br> **Oracle:** `EXIT;` <br> **SQL Server:** `QUIT`                                                                                                                                                                                                   | Enterprise: always exit cleanly to release connections.                                     |

---

## **Enterprise Design Notes**

* **SQLite:** Lightweight CLI; best for development, testing, or embedded apps.
* **PostgreSQL:** Full-featured CLI (`psql`) with meta-commands (`\d`, `\l`, `\dt`) for schema inspection.
* **Snowflake:** `snowsql` CLI supports queries, scripts, and data unloading/loading; integrates with cloud storage.
* **Oracle:** `sqlplus` CLI for ad-hoc queries, scripts, and DML; supports batch processing and automation.
* **SQL Server:** `sqlcmd` CLI for queries, scripts, and data import/export; integrates with Windows scheduler or automation.
* **Best Practices:**

  * Use **scripts for repeatable tasks** in CI/CD or ETL pipelines.
  * **Avoid hardcoding passwords**; use environment variables or secure credential stores.
  * **Combine CLI with automation** (cron, Airflow, CI/CD pipelines) for enterprise workflows.
  * Test scripts in **development environments** before production deployment.

---

## **Quick Examples**

```bash
# PostgreSQL connect and list tables
psql -h localhost -U admin -d mydb
\dt
SELECT * FROM orders;

# SQLite connect and describe table
sqlite3 mydb.db
.schema orders

# Snowflake query via CLI
snowsql -a myaccount -u user -d mydb -s public
SELECT * FROM orders;

# SQL Server export table to CSV
bcp dbo.orders out orders.csv -c -t, -S servername -U admin -P password

# Oracle execute SQL script
sqlplus user/password@//localhost:1521/XEPDB1
@script.sql
EXIT;
```

---

This cheat sheet **covers all essential CLI operations across major DBs**, highlighting **connection, schema inspection, query execution, data import/export, transactions, and scripting**, making it **enterprise-ready for DB administration, ETL pipelines, and automation**.

