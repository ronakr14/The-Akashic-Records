---
id: yqc5du90lutnc8xzk2576ih
title: Backup_restore
desc: ''
updated: 1755757605048
created: 1755757598547
---

# **Enterprise Multi-DB Backup & Restore Cheat Sheet**

| Operation                             | Purpose                                | Syntax / Example                                                                                                                                                                                                                                                                                                                                                                     | DB Notes / Enterprise Tips                                                         |                                                                              |
| ------------------------------------- | -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| **Full Database Backup**              | Complete copy of database              | **PostgreSQL:** `pg_dump -U user -F c -f backup.dump dbname` <br> **SQLite:** `sqlite3 mydb.db ".backup backup.db"` <br> **Snowflake:** `CREATE DATABASE dbname CLONE dbname;` (logical snapshot) <br> **Oracle:** `expdp user/password full=Y directory=BACKUP_DIR dumpfile=full_db.dmp` <br> **SQL Server:** `BACKUP DATABASE dbname TO DISK='C:\backups\dbname.bak' WITH FORMAT;` | Enterprise: schedule regular full backups; store in secure, redundant storage.     |                                                                              |
| **Incremental / Differential Backup** | Capture only changes since last backup | **PostgreSQL:** WAL archiving with `pg_basebackup` <br> **SQL Server:** `BACKUP DATABASE dbname TO DISK='C:\backups\db_diff.bak' WITH DIFFERENTIAL;` <br> **Oracle:** RMAN incremental backups <br> **SQLite / Snowflake:** rely on snapshots or cloud versioning                                                                                                                    | Enterprise: reduces storage, speeds up restore; requires base full backup.         |                                                                              |
| **Logical Backup**                    | Backup DB structure & data as SQL      | **PostgreSQL:** `pg_dump -U user -F p dbname > db.sql` <br> **SQLite:** `.dump > db.sql` <br> **Oracle:** `expdp user/password full=Y directory=BACKUP_DIR dumpfile=full_db.dmp`                                                                                                                                                                                                     | Enterprise: good for migrations, version control, or cross-DB restores.            |                                                                              |
| **Physical Backup**                   | Backup raw database files              | PostgreSQL: copy data directory + WAL <br> SQLite: copy DB file <br> Oracle / SQL Server: backup database files                                                                                                                                                                                                                                                                      | Enterprise: faster for large DBs; requires DB offline or hot-backup capability.    |                                                                              |
| **Restore Database**                  | Recover DB from backup                 | **PostgreSQL:** `pg_restore -U user -d dbname backup.dump` <br> **SQLite:** `sqlite3 mydb.db ".restore backup.db"` <br> **Snowflake:** `CREATE DATABASE db_clone CLONE dbname;` <br> **Oracle:** `impdp user/password full=Y directory=BACKUP_DIR dumpfile=full_db.dmp` <br> **SQL Server:** `RESTORE DATABASE dbname FROM DISK='C:\backups\dbname.bak';`                            | Enterprise: test restores regularly; ensure backup compatibility with DB version.  |                                                                              |
| **Point-in-Time Recovery (PITR)**     | Restore DB to specific time            | PostgreSQL: WAL + base backup <br> SQL Server: Transaction log restore <br> Oracle: RMAN + archive logs                                                                                                                                                                                                                                                                              | Enterprise: critical for accidental deletes or data corruption.                    |                                                                              |
| **Cloud / Snapshot Backup**           | Near-instant backup for cloud DBs      | Snowflake: `CREATE DATABASE dbname CLONE dbname;`                                                                                                                                                                                                                                                                                                                                    | Enterprise: supports minimal downtime; integrates with automated pipelines.        |                                                                              |
| **Automated Backup Scheduling**       | Ensure regular backups                 | Use **cron, Airflow, SQL Agent Jobs, RMAN scripts**                                                                                                                                                                                                                                                                                                                                  | Enterprise: automate full + incremental backups; monitor failures via logs/alerts. |                                                                              |
| **Compression & Encryption**          | Reduce storage, secure backups         | PostgreSQL: \`pg\_dump -F c                                                                                                                                                                                                                                                                                                                                                          | gzip > backup.dump.gz`<br> SQL Server:`WITH COMPRESSION, ENCRYPTION\`              | Enterprise: store backups encrypted in offsite/cloud storage for compliance. |
| **Verification / Test Restore**       | Ensure backup integrity                | Restore to staging/test DB                                                                                                                                                                                                                                                                                                                                                           | Enterprise: never rely solely on backup existence; always test restore procedures. |                                                                              |

---

## **Enterprise Design Notes**

* **SQLite:** Lightweight; backup is file copy or `.backup` command; suitable for small DBs.
* **PostgreSQL:** Supports logical (`pg_dump`) and physical (`pg_basebackup`) backups; WAL allows PITR.
* **Snowflake:** Use **database cloning** and **time travel** for near real-time snapshots.
* **Oracle:** RMAN preferred for enterprise; supports full, incremental, and point-in-time recovery.
* **SQL Server:** Full, differential, transaction log backups; integrate with SQL Agent for scheduling.
* **Best Practices:**

  * Use **full + incremental strategy** to balance recovery speed and storage.
  * Encrypt backups, especially for cloud storage.
  * Automate backups and monitor for failures.
  * Test restores periodically in staging environment.
  * Retain multiple backup versions based on RPO/RTO requirements.

---

## **Quick Examples**

```bash
-- PostgreSQL full backup
pg_dump -U admin -F c -f /backups/db_full.dump mydb

-- PostgreSQL restore
pg_restore -U admin -d mydb /backups/db_full.dump

-- SQLite backup
sqlite3 mydb.db ".backup backup.db"

-- SQLite restore
sqlite3 mydb.db ".restore backup.db"

-- Snowflake clone (snapshot)
CREATE DATABASE db_clone CLONE mydb;

-- SQL Server full backup
BACKUP DATABASE mydb TO DISK='C:\backups\mydb.bak' WITH FORMAT;

-- SQL Server restore
RESTORE DATABASE mydb FROM DISK='C:\backups\mydb.bak';

-- Oracle Data Pump export
expdp user/password full=Y directory=BACKUP_DIR dumpfile=full_db.dmp

-- Oracle Data Pump import
impdp user/password full=Y directory=BACKUP_DIR dumpfile=full_db.dmp
```

---

This cheat sheet **covers all essential backup and restore operations across major DBs**, highlighting **full/incremental/logical/physical backups, PITR, automation, compression/encryption, and enterprise best practices**, making it **ready for disaster recovery planning, ETL, and compliance workflows**.

