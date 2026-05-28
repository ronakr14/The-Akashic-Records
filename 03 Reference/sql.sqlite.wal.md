---
id: 6pm5bieczc6nmlupqxdrgxl
title: Wa
desc: ''
updated: 1755708233712
created: 1755708227170
---

# 🔹 What is WAL Mode?

By default, SQLite uses **rollback journals**:

* When a transaction starts, SQLite copies affected pages to a temporary file (`-journal`).
* On crash, it rolls back using this journal.
* Problem: **writers block readers** — only one writer at a time.

**WAL (Write-Ahead Log)** changes this:

* Instead of overwriting the DB, SQLite **appends changes to a WAL file** (`dbname-wal`).
* Readers continue reading the old DB while writes go into WAL.
* Periodically, WAL is **checkpointed** back into the main DB.

💡 Key benefit: **readers never block writers**.

---

# 🔹 Enabling WAL Mode

CLI:

```sql
PRAGMA journal_mode=WAL;
```

Python:

```python
import sqlite3

conn = sqlite3.connect("mydb.sqlite")
conn.execute("PRAGMA journal_mode=WAL;")
```

Check mode:

```sql
PRAGMA journal_mode;
```

---

# 🔹 WAL Characteristics

| Feature        | Rollback Journal           | WAL Mode                          |
| -------------- | -------------------------- | --------------------------------- |
| Concurrency    | 1 writer, multiple readers | 1 writer, multiple readers        |
| Crash Recovery | Rollback journal           | WAL replay                        |
| Write Speed    | Moderate                   | Faster (append-only)              |
| File Size      | Small                      | WAL file grows, checkpoint needed |

---

# 🔹 WAL Performance Tips

1. **Checkpointing**

   * WAL grows over time; checkpoint to merge changes:

   ```sql
   PRAGMA wal_checkpoint;
   ```

   * Automatic: `PRAGMA wal_autocheckpoint = 1000;` (every 1000 pages)

2. **Synchronous Mode**

   * Controls how safely SQLite writes to disk:

   ```sql
   PRAGMA synchronous=NORMAL;  -- balance speed + durability
   PRAGMA synchronous=FULL;    -- safest, slower
   PRAGMA synchronous=OFF;     -- fastest, risky
   ```

3. **Page Size**

   * Default 4 KB, can increase for large transactions:

   ```sql
   PRAGMA page_size = 8192;
   ```

4. **Bulk Inserts**

   * Wrap multiple inserts in a transaction for massive speedup:

   ```python
   conn.execute("BEGIN")
   for row in data:
       conn.execute("INSERT INTO table VALUES (?,?)", row)
   conn.commit()
   ```

5. **Indexes**

   * Keep them minimal — too many indexes slow down writes.
   * Use **covering indexes** to reduce table lookups on reads.

6. **Analyze**

   * Helps query planner choose best indexes:

   ```sql
   ANALYZE;
   ```

---

# 🔹 Python Example: WAL + Bulk Insert

```python
import sqlite3

conn = sqlite3.connect("wal_demo.sqlite")
conn.execute("PRAGMA journal_mode=WAL;")
conn.execute("PRAGMA synchronous=NORMAL;")

conn.execute("CREATE TABLE IF NOT EXISTS logs(id INTEGER PRIMARY KEY, msg TEXT)")

# Bulk insert
data = [(f"log {i}",) for i in range(100000)]
conn.execute("BEGIN")
conn.executemany("INSERT INTO logs(msg) VALUES (?)", data)
conn.commit()
conn.close()
```

✅ Result: concurrent reads can still happen while the bulk insert is running.

---

# 🧾 Cheat Sheet

* Enable WAL: `PRAGMA journal_mode=WAL;`
* Check WAL size / auto-checkpoint: `PRAGMA wal_autocheckpoint = 1000;`
* Synchronous modes: OFF | NORMAL | FULL
* Wrap multiple writes in **BEGIN / COMMIT** for speed
* Use `ANALYZE` to help the query planner
* Minimize unnecessary indexes for faster writes

---

⚡ **TL;DR**:

* WAL mode boosts **concurrency** (reads aren’t blocked by writes)
* Write performance is much faster (append-only)
* Combine with **transactions, synchronous tuning, and bulk inserts** for best results

