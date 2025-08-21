---
id: rzdal3n6r2nffaoq08ste54
title: Basics
desc: ''
updated: 1755708260885
created: 1755706792840
---

## 🔹 What is a `.sqlite` File?

* A `.sqlite` file is literally the **entire database** stored in a single disk file.
* No server, no background daemon, no client-server communication overhead.
* It’s **self-contained**: tables, indexes, triggers, views, and even the schema all live inside that one file.

Think of it like carrying around a whole mini-Postgres instance inside a single USB stick file.

---

## 🔹 How SQLite File Storage Works

1. **Single File = Whole Database**

   * When you `sqlite3 mydata.sqlite`, that file is your database.
   * Tables, schemas, and even transactions are serialized into that file.

2. **Page-based Storage**

   * Internally, SQLite organizes data in fixed-size **pages** (commonly 4KB).
   * Each page can hold B-Trees for tables and indexes.

3. **Self-contained Engine**

   * The `.sqlite` file has everything needed — no dependencies.
   * If you copy the file to another machine, you’ve just “migrated the database.”

4. **Atomicity & Journals**

   * SQLite ensures ACID compliance using **journaling** (rollback journal or WAL mode).
   * Example: When you `INSERT`, SQLite writes changes to a journal file before committing, so corruption is prevented even on a crash.

5. **Portability**

   * Same file works across OS (Windows/Linux/Mac).
   * Endian issues? Nope, SQLite handles that.

---

## 🔹 Why File-Based is a Big Deal

* **No server setup**: Just open the file with SQLite library.
* **Great for small apps, prototyping, embedded systems, mobile apps (Android/iOS)**.
* **Easy backups**: Copy the file, done.
* **Integration-friendly**: Ship the database file inside your app as read-only or pre-populated.

---

## 🔹 Example Workflow

```bash
# Create a new SQLite DB
sqlite3 mydata.sqlite

# Inside the SQLite shell
sqlite> CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT);
sqlite> INSERT INTO users(name) VALUES ('Ronak');
sqlite> SELECT * FROM users;
1 | Ronak
```

👉 All of this data is stored in **mydata.sqlite**, a single portable file.

---

## ⚖️ Tradeoffs

* ✅ Lightweight, portable, zero-config
* ✅ ACID transactions, full SQL support
* ❌ Not built for massive concurrent writes (multi-user server DBs handle that better)
* ❌ File-locking limits scalability in write-heavy environments

---

**TL;DR**:
`.sqlite` files are **self-contained databases** stored in a single file, using page-based storage and journaling to stay consistent. Perfect for apps, prototypes, and embedded systems, but not a replacement for a full-blown server in high-concurrency workloads.


# 🔍 Anatomy of a `.sqlite` File

A SQLite database file isn’t just random bytes — it has a very strict structure. Think of it like a **mini filesystem** optimized for SQL.

---

## 1. **File Header (First 100 Bytes)**

* Every SQLite file starts with the text string:

  ```
  "SQLite format 3\000"
  ```

  That’s the signature (magic number).
* The header also contains:

  * Page size (commonly 4096 bytes)
  * Write-ahead log (WAL) or rollback journal settings
  * Schema format number
  * Encoding (UTF-8, UTF-16, etc.)

👉 This tells the SQLite engine how to read everything else.

---

## 2. **Page-Based Storage**

* The file is divided into **pages** (default: 4KB).
* Each page has a role:

  * **B-Tree Pages** (tables & indexes)
  * **Freelist Pages** (unused space for future inserts)
  * **Overflow Pages** (for values too big to fit in one page)

---

## 3. **How Tables are Stored**

* SQLite tables are stored as **B-Trees** inside pages:

  * **Interior Nodes**: branch points for searching
  * **Leaf Nodes**: actual rows (records)
* Example: A table with users:

  ```
  users(id INTEGER PRIMARY KEY, name TEXT)
  ```

  is stored in a B-Tree keyed on `id`.

---

## 4. **How Indexes are Stored**

* Indexes get their own B-Tree, separate from the table.
* Instead of storing the row, they store the **key + a pointer** back to the table row.

---

## 5. **Schema Storage (sqlite\_master table)**

* The **database schema** (your `CREATE TABLE`, `CREATE INDEX`, etc.) lives in a special table:

  ```sql
  sqlite> .schema
  CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT);
  ```
* Behind the scenes, this is stored in a hidden table:

  ```sql
  SELECT * FROM sqlite_master;
  ```

  Columns:

  * `type` (table, index, trigger, view)
  * `name` (object name)
  * `tbl_name` (table it belongs to)
  * `rootpage` (page number of the B-Tree root)
  * `sql` (the actual CREATE statement)

---

## 6. **Large Values (Overflow Pages)**

* If you insert a massive `TEXT` or `BLOB`, it won’t fit in one page.
* SQLite splits it across **overflow pages** linked together like a chain.

---

## 7. **Transaction Journaling**

* Two main modes:

  * **Rollback Journal** → extra temporary file, roll back if crash
  * **WAL (Write Ahead Log)** → separate WAL file for concurrent reads/writes
* Journaling ensures **ACID** (Atomicity, Consistency, Isolation, Durability).

---

## 🔧 Demo: Peeking Inside a `.sqlite` File

```bash
# Create db
sqlite3 demo.sqlite "CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT);"

# Look at schema
sqlite3 demo.sqlite "SELECT * FROM sqlite_master;"

# Dump raw header
hexdump -C demo.sqlite | head
```

You’ll see `"SQLite format 3"` at the very top, and page data after that.

---

## 🧠 Visualization

```
[ Header (100B) ]
   |
   v
[ Page 1: B-Tree Root for sqlite_master ]
   |
   +--> Table root pages (users, orders, etc.)
   |
   +--> Index root pages
   |
   +--> Overflow pages (if needed)
   |
   +--> Freelist pages (empty slots)
```

So your `.sqlite` file is basically a **linked set of B-Trees with a catalog table (`sqlite_master`) that keeps track of them**.

---

⚡ **Bottom Line**:
SQLite doesn’t just dump rows into a file — it builds a mini database engine in that file. The header + pages + B-Trees + journals all work together to make it ACID-compliant, portable, and incredibly robust for a “just a file” database.

---
