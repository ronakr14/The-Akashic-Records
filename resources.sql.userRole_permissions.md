---
id: b93l0atr682m4woamqa9vrj
title: userRole_permissions
desc: ''
updated: 1755757862611
created: 1755757856698
---

# **Enterprise Multi-DB User, Role & Permission Cheat Sheet**

| Feature / Operation      | Purpose                             | Syntax / Example                                                                                                                                                                                                                                                                                                                                                       | DB Notes / Enterprise Tips                                                                    |
| ------------------------ | ----------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| **Create User**          | Create a new database user          | **PostgreSQL:** `CREATE USER analyst WITH PASSWORD 'secret';` <br> **SQL Server:** `CREATE LOGIN analyst WITH PASSWORD = 'secret'; CREATE USER analyst FOR LOGIN analyst;` <br> **Oracle:** `CREATE USER analyst IDENTIFIED BY secret;` <br> **Snowflake:** `CREATE USER analyst PASSWORD='SecretPass';` <br> **SQLite:** No native users; rely on OS/file permissions | Enterprise: enforce strong passwords and separate users for roles/tasks.                      |
| **Drop User**            | Remove user from DB                 | PostgreSQL: `DROP USER analyst;` <br> SQL Server: `DROP USER analyst; DROP LOGIN analyst;` <br> Oracle: `DROP USER analyst CASCADE;` <br> Snowflake: `DROP USER analyst;`                                                                                                                                                                                              | Enterprise: always revoke roles/permissions before dropping user.                             |
| **Create Role**          | Group privileges for multiple users | PostgreSQL: `CREATE ROLE read_only;` <br> SQL Server: `CREATE ROLE read_only;` <br> Oracle: `CREATE ROLE read_only;` <br> Snowflake: `CREATE ROLE read_only;`                                                                                                                                                                                                          | Enterprise: use roles to simplify privilege management and enforce least privilege.           |
| **Assign Role to User**  | Grant role-based access             | PostgreSQL: `GRANT read_only TO analyst;` <br> SQL Server: `ALTER ROLE read_only ADD MEMBER analyst;` <br> Oracle: `GRANT read_only TO analyst;` <br> Snowflake: `GRANT ROLE read_only TO USER analyst;`                                                                                                                                                               | Enterprise: assign roles, not individual privileges, wherever possible.                       |
| **Grant Privileges**     | Grant object-level permissions      | PostgreSQL/Oracle: `GRANT SELECT, INSERT ON orders TO read_only;` <br> SQL Server: `GRANT SELECT, INSERT ON dbo.orders TO read_only;` <br> Snowflake: `GRANT SELECT, INSERT ON TABLE orders TO ROLE read_only;`                                                                                                                                                        | Enterprise: use fine-grained grants for sensitive data; prefer roles over direct user grants. |
| **Revoke Privileges**    | Remove access rights                | PostgreSQL/Oracle: `REVOKE INSERT ON orders FROM read_only;` <br> SQL Server: `REVOKE INSERT ON dbo.orders FROM read_only;` <br> Snowflake: `REVOKE INSERT ON TABLE orders FROM ROLE read_only;`                                                                                                                                                                       | Enterprise: periodically audit privileges; revoke unnecessary access promptly.                |
| **View Users and Roles** | Inspect DB security                 | PostgreSQL: `\du` <br> SQL Server: `SELECT name, type_desc FROM sys.database_principals;` <br> Oracle: `SELECT username FROM dba_users; SELECT * FROM dba_roles;` <br> Snowflake: `SHOW USERS; SHOW ROLES;`                                                                                                                                                            | Enterprise: maintain inventory of users and roles; integrate with IAM where possible.         |
| **Best Practices**       | Enterprise security                 | - Follow principle of least privilege <br> - Use roles for grouping privileges <br> - Separate roles for read, write, admin <br> - Audit permissions regularly <br> - Use multi-factor authentication where supported <br> - Avoid using default admin users for day-to-day operations                                                                                 | Enterprise: reduces risk of accidental/unauthorized access and simplifies audits.             |

---

## **Enterprise Design Notes**

* **SQLite:** No native users or roles; rely on OS-level file permissions.
* **PostgreSQL:** Supports users, roles, and granular grants; role hierarchy is supported.
* **Snowflake:** Fully role-based; users gain privileges via roles; supports hierarchical roles.
* **Oracle:** Users and roles; can assign privileges at system/object level; `DBA` role for admin tasks.
* **SQL Server:** Users, logins, and database roles; supports schema-bound and object-bound permissions.
* **Best Practices:**

  * Always use **roles** for access management.
  * **Separate environments** (dev/test/prod) with distinct users/roles.
  * Regular **privilege audits** to maintain compliance.
  * Integrate with **centralized identity management** where possible.

---

## **Quick Examples**

```sql
-- PostgreSQL: Create user and role
CREATE ROLE read_only;
CREATE USER analyst WITH PASSWORD 'secret';
GRANT read_only TO analyst;
GRANT SELECT ON orders TO read_only;

-- SQL Server: Create user and role
CREATE ROLE read_only;
CREATE LOGIN analyst WITH PASSWORD = 'secret';
CREATE USER analyst FOR LOGIN analyst;
ALTER ROLE read_only ADD MEMBER analyst;
GRANT SELECT ON dbo.orders TO read_only;

-- Oracle: Create user and role
CREATE ROLE read_only;
CREATE USER analyst IDENTIFIED BY secret;
GRANT read_only TO analyst;
GRANT SELECT ON orders TO read_only;

-- Snowflake: Create user and role
CREATE ROLE read_only;
CREATE USER analyst PASSWORD='SecretPass';
GRANT ROLE read_only TO USER analyst;
GRANT SELECT ON TABLE orders TO ROLE read_only;
```

---

This cheat sheet **covers all essential user, role, and permission operations across major DBs**, highlighting **creation, assignment, grants/revoke, inspection, and best practices**, making it **enterprise-ready for secure access management, auditing, and compliance**.
