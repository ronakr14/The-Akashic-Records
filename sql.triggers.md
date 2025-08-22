---
id: g1n3vdqj3ru7ip9jvw6nvhh
title: Triggers
desc: ''
updated: 1755756205385
created: 1755756193530
---

# **Enterprise Multi-DB TRIGGER Cheat Sheet**

| Feature / Trigger Type           | Purpose                                                             | Basic Syntax                                                                             | DB Notes / Enterprise Tips                                                                               |
| -------------------------------- | ------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| **BEFORE INSERT**                | Execute logic before a row is inserted                              | `sql CREATE TRIGGER trg_name BEFORE INSERT ON table_name FOR EACH ROW BEGIN ... END;`    | SQLite, PostgreSQL, Oracle, SQL Server support; Snowflake does **not** support triggers natively.        |
| **AFTER INSERT**                 | Execute logic after a row is inserted                               | `sql CREATE TRIGGER trg_name AFTER INSERT ON table_name FOR EACH ROW BEGIN ... END;`     | Useful for audit logging or cascading updates.                                                           |
| **BEFORE UPDATE**                | Logic before row update                                             | `sql CREATE TRIGGER trg_name BEFORE UPDATE ON table_name FOR EACH ROW BEGIN ... END;`    | Always use `OLD` and `NEW` pseudo-records to access row values (DB-specific names).                      |
| **AFTER UPDATE**                 | Logic after row update                                              | `sql CREATE TRIGGER trg_name AFTER UPDATE ON table_name FOR EACH ROW BEGIN ... END;`     | Useful for recalculations, audit history, or maintaining summary tables.                                 |
| **BEFORE DELETE**                | Logic before row deletion                                           | `sql CREATE TRIGGER trg_name BEFORE DELETE ON table_name FOR EACH ROW BEGIN ... END;`    | Prevents deletion or logs deleted rows.                                                                  |
| **AFTER DELETE**                 | Logic after row deletion                                            | `sql CREATE TRIGGER trg_name AFTER DELETE ON table_name FOR EACH ROW BEGIN ... END;`     | Common for audit trails or cascading deletes.                                                            |
| **INSTEAD OF**                   | Used for views to allow DML                                         | `sql CREATE TRIGGER trg_name INSTEAD OF INSERT ON view_name FOR EACH ROW BEGIN ... END;` | Supported in PostgreSQL, Oracle, SQL Server; SQLite does **not** support `INSTEAD OF` triggers on views. |
| **Row-level vs Statement-level** | Row-level: fires per row; Statement-level: fires once per statement | `FOR EACH ROW` vs omit                                                                   | SQLite only supports row-level triggers. PostgreSQL, Oracle, SQL Server support both.                    |

---

## **Enterprise Design Notes**

* **SQLite:** Supports only row-level triggers; BEFORE/AFTER only; limited procedural code (uses SQL).
* **PostgreSQL:** Supports row-level & statement-level triggers; powerful with PL/pgSQL; supports triggers on tables and views.
* **Snowflake:** Does **not support triggers**; use **streams + tasks** for reactive behavior.
* **Oracle:** Full-featured; supports BEFORE/AFTER, row/statement, INSTEAD OF, compound triggers, and triggers on views.
* **SQL Server:** Supports AFTER/INSTEAD OF triggers; row-level triggers are simulated per statement; use `INSERTED` and `DELETED` pseudo-tables.
* **Best Practices:**

  * Avoid heavy logic in triggers to prevent performance issues.
  * Use triggers for **audit logging, cascading updates, or enforcing business rules**.
  * Always document triggers and maintain naming conventions (`trg_table_event`).
  * Prefer explicit constraints over triggers where possible (CHECK, FK, etc.).

---

## **Quick Examples**

```sql
-- SQLite / PostgreSQL / Oracle
CREATE TRIGGER trg_before_insert_users
BEFORE INSERT ON users
FOR EACH ROW
BEGIN
    -- Example: auto-fill created_at
    SET NEW.created_at = CURRENT_TIMESTAMP;
END;

-- AFTER UPDATE trigger example
CREATE TRIGGER trg_after_update_orders
AFTER UPDATE ON orders
FOR EACH ROW
BEGIN
    INSERT INTO orders_audit(order_id, old_amount, new_amount, updated_at)
    VALUES (OLD.id, OLD.amount, NEW.amount, CURRENT_TIMESTAMP);
END;

-- SQL Server AFTER INSERT trigger
CREATE TRIGGER trg_after_insert_users
ON users
AFTER INSERT
AS
BEGIN
    INSERT INTO users_audit(user_id, action_time)
    SELECT id, GETDATE() FROM inserted;
END;

-- Oracle INSTEAD OF trigger on a view
CREATE TRIGGER trg_instead_of_update_user_view
INSTEAD OF UPDATE ON user_view
FOR EACH ROW
BEGIN
    UPDATE users SET username = :NEW.username WHERE id = :OLD.id;
END;
```

---

This **one-page reference** covers **trigger types, DB support, syntax, and enterprise best practices**, highlighting differences like **Snowflake lacking triggers** and **row vs statement-level behavior**.
