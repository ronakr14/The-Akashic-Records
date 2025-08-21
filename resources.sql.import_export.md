---
id: b3x858pkmr5jifyry40owvd
title: Import_export
desc: ''
updated: 1755757326117
created: 1755757318857
---

# **Enterprise Multi-DB Data Import / Export Cheat Sheet**

| Operation                          | Purpose                              | Syntax / Example                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | DB Notes / Enterprise Tips                                                                                          |
| ---------------------------------- | ------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Export Table to File**           | Backup or ETL                        | **PostgreSQL:** `COPY orders TO '/tmp/orders.csv' DELIMITER ',' CSV HEADER;` <br> **SQLite:** `.mode csv` `.output orders.csv` `SELECT * FROM orders;` <br> **Snowflake:** `COPY INTO 's3://bucket/orders.csv' FROM orders FILE_FORMAT=(TYPE=CSV FIELD_OPTIONALLY_ENCLOSED_BY='"');` <br> **Oracle:** `SQL*Plus: SPOOL orders.csv` or `Data Pump: expdp user/password tables=orders directory=DATA_PUMP_DIR dumpfile=orders.dmp` <br> **SQL Server:** `bcp dbo.orders out orders.csv -c -t, -S server -U user -P password` | Enterprise: Use CSV, Parquet, or JSON for ETL pipelines; compress large files for cloud storage.                    |
| **Import File into Table**         | Load data into DB                    | **PostgreSQL:** `COPY orders FROM '/tmp/orders.csv' DELIMITER ',' CSV HEADER;` <br> **SQLite:** `.mode csv` `.import orders.csv orders` <br> **Snowflake:** `COPY INTO orders FROM 's3://bucket/orders.csv' FILE_FORMAT=(TYPE=CSV FIELD_OPTIONALLY_ENCLOSED_BY='"');` <br> **Oracle:** `impdp user/password tables=orders directory=DATA_PUMP_DIR dumpfile=orders.dmp` <br> **SQL Server:** `bcp dbo.orders in orders.csv -c -t, -S server -U user -P password`                                                            | Enterprise: Validate schema compatibility, handle duplicates, and enforce constraints.                              |
| **Incremental / CDC-based Import** | Load only new or changed rows        | Combine with **CDC**, timestamp columns, or staging tables                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | Enterprise: reduces load time; avoids full table reload.                                                            |
| **File Formats Supported**         | Format flexibility for ETL           | CSV, TSV, JSON, Parquet, Avro                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | Enterprise: choose format based on downstream analytics/storage (CSV for simplicity, Parquet for columnar queries). |
| **Data Validation / Cleaning**     | Ensure integrity                     | Pre-process with Python/Pandas, Spark, or DB-native transformations                                                                                                                                                                                                                                                                                                                                                                                                                                                        | Enterprise: validate column types, NULLs, duplicates, and encoding before load.                                     |
| **Bulk Loading Tools**             | Optimize large volume imports        | PostgreSQL: `COPY` <br> SQL Server: `bcp`, `BULK INSERT` <br> Oracle: `Data Pump` <br> Snowflake: `COPY INTO`                                                                                                                                                                                                                                                                                                                                                                                                              | Enterprise: faster than row-by-row inserts; ensure transactional safety.                                            |
| **Export Automation**              | Schedule exports for ETL / reporting | Use **cron**, **Airflow**, or DB-native tasks                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | Enterprise: automate nightly or incremental exports for analytics pipelines.                                        |
| **Compression & Encryption**       | Reduce storage, ensure security      | Compress with gzip, zip; encrypt at rest or in transit                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | Enterprise: essential for cloud storage and compliance.                                                             |
| **Error Handling**                 | Capture and report failed rows       | Use staging tables, error logs, or file-based reject handling                                                                                                                                                                                                                                                                                                                                                                                                                                                              | Enterprise: ensures reliability for ETL processes.                                                                  |
| **Transactional Control**          | Ensure atomic import                 | Wrap in `BEGIN/COMMIT` or use transactional import tools                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | Enterprise: prevent partial loads and maintain data integrity.                                                      |

---

## **Enterprise Design Notes**

* **SQLite:** Lightweight; supports CSV import/export via CLI; limited bulk/format options.
* **PostgreSQL:** `COPY` is fastest for bulk operations; supports CSV, JSON, and programmatic ETL.
* **Snowflake:** `COPY INTO` / `PUT` + `GET` commands for cloud storage; supports large-scale analytic data pipelines.
* **Oracle:** Data Pump (`expdp` / `impdp`) preferred for large enterprise tables; supports CSV, binary dump.
* **SQL Server:** `bcp` or `BULK INSERT` for high-performance bulk operations; integrates with SSIS for ETL.
* **Best Practices:**

  * Use **staging tables** to validate data before final load.
  * **Compress large files** for cloud transfers.
  * Maintain **logs and error files** for auditing.
  * Prefer **bulk commands** over individual inserts for performance.
  * Automate recurring imports/exports via **ETL pipelines**.

---

## **Quick Examples**

```sql
-- PostgreSQL export to CSV
COPY orders TO '/tmp/orders.csv' DELIMITER ',' CSV HEADER;

-- PostgreSQL import from CSV
COPY orders FROM '/tmp/orders.csv' DELIMITER ',' CSV HEADER;

-- SQLite export
sqlite3 mydb.db
.mode csv
.output orders.csv
SELECT * FROM orders;

-- SQLite import
.mode csv
.import orders.csv orders

-- Snowflake export to S3
COPY INTO 's3://bucket/orders.csv' FROM orders FILE_FORMAT=(TYPE=CSV FIELD_OPTIONALLY_ENCLOSED_BY='"');

-- Snowflake import from S3
COPY INTO orders FROM 's3://bucket/orders.csv' FILE_FORMAT=(TYPE=CSV FIELD_OPTIONALLY_ENCLOSED_BY='"');

-- SQL Server bulk export
bcp dbo.orders out orders.csv -c -t, -S server -U user -P password

-- SQL Server bulk import
bcp dbo.orders in orders.csv -c -t, -S server -U user -P password

-- Oracle Data Pump export
expdp user/password tables=orders directory=DATA_PUMP_DIR dumpfile=orders.dmp

-- Oracle Data Pump import
impdp user/password tables=orders directory=DATA_PUMP_DIR dumpfile=orders.dmp
```

---

This cheat sheet **covers all essential data import/export operations across major DBs**, highlighting **bulk load/unload, file formats, automation, transactional control, and enterprise best practices**, making it **ready for ETL pipelines, reporting, and data warehouse workflows**.

