---
id: 5555i9st7g3tgps01c95yzp
title: Dcl
desc: ''
updated: 1755756686202
created: 1755756680565
---

# **Enterprise Multi-DB DCL (Data Control Language) Cheat Sheet**

| DCL Operation                          | Purpose                    | Syntax                                                                                                                                                                                      | DB Notes / Enterprise Tips                                                                                                                   |
| -------------------------------------- | -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| **GRANT Privileges**                   | Give access to users/roles | `GRANT privilege_list ON object TO user_or_role;`                                                                                                                                           | Privileges: `SELECT, INSERT, UPDATE, DELETE, REFERENCES, EXECUTE, USAGE, ALL`. Object can be table, schema, database, sequence, or function. |
| **REVOKE Privileges**                  | Remove access              | `REVOKE privilege_list ON object FROM user_or_role;`                                                                                                                                        | Revoke cascades differently in each DB; enterprise systems often audit REVOKEs.                                                              |
| **GRANT Role / Group Membership**      | Assign user to role        | `GRANT role_name TO user_or_role;`                                                                                                                                                          | PostgreSQL, Oracle, SQL Server, Snowflake support roles; SQLite does not support roles.                                                      |
| **REVOKE Role**                        | Remove user from role      | `REVOKE role_name FROM user_or_role;`                                                                                                                                                       | Useful for dynamic access management in enterprises.                                                                                         |
| **CREATE ROLE**                        | Define new role / group    | `CREATE ROLE role_name [WITH options];`                                                                                                                                                     | Options: `LOGIN, NOLOGIN, PASSWORD, SUPERUSER` depending on DB. Enterprise practice: use roles for permission management.                    |
| **DROP ROLE**                          | Remove role                | `DROP ROLE role_name;`                                                                                                                                                                      | Ensure no dependent users or objects before dropping.                                                                                        |
| **ALTER ROLE**                         | Modify role properties     | `ALTER ROLE role_name [options];`                                                                                                                                                           | Change password, privileges, login capability, or default schema.                                                                            |
| **CREATE USER / LOGIN**                | Define new user            | PostgreSQL / SQL Server / Oracle / Snowflake: `CREATE USER user_name [WITH PASSWORD 'pwd'];`                                                                                                | Enterprise: enforce strong password policies and default roles. SQLite: no user management.                                                  |
| **ALTER USER**                         | Modify user properties     | `ALTER USER user_name [WITH PASSWORD 'newpwd'];`                                                                                                                                            | Use to update roles, passwords, or default schema.                                                                                           |
| **DROP USER / LOGIN**                  | Remove user                | `DROP USER user_name;`                                                                                                                                                                      | Ensure ownership transfer of objects; otherwise DROP may fail in Oracle/PostgreSQL.                                                          |
| **Audit / Review Privileges**          | List user permissions      | PostgreSQL: `\du` or `SELECT * FROM information_schema.role_table_grants;` <br> SQL Server: `SELECT * FROM sys.database_permissions;` <br> Snowflake: `SHOW GRANTS TO USER user_name;`      | Enterprise: regular audits required for compliance and security.                                                                             |
| **Schema / Object Ownership Transfer** | Transfer object ownership  | PostgreSQL: `ALTER TABLE table_name OWNER TO new_owner;` <br> Oracle: `ALTER TABLE table_name TRANSFER TO user;` <br> SQL Server: `ALTER AUTHORIZATION ON OBJECT::table_name TO new_owner;` | Enterprise: critical when rotating responsibilities or decommissioning users.                                                                |

---

## **Enterprise Design Notes**

* **SQLite:** Minimal/no DCL support; relies on OS-level file permissions.
* **PostgreSQL:** Full DCL support; roles, groups, and privileges can be audited; supports `GRANT ALL PRIVILEGES` at table/schema/database level.
* **Snowflake:** Fine-grained access control; supports roles, role hierarchy, and grants for objects (tables, schemas, databases, stages, warehouses).
* **Oracle:** Robust enterprise security; supports roles, profiles, privileges, auditing, and object ownership transfer.
* **SQL Server:** Supports users, logins, roles, and database-level or object-level permissions; enterprise auditing via `sys.database_permissions` and server-level logs.
* **Best Practices:**

  * Use **roles** instead of direct user grants.
  * Regularly **audit and revoke** unnecessary privileges.
  * Maintain **least privilege principle** for all users and roles.
  * Use **default schemas** and ownership transfer to manage enterprise object lifecycle.

---

## **Quick Examples**

```sql
-- Create role
CREATE ROLE analyst;

-- Grant privileges
GRANT SELECT, INSERT ON sales.orders TO analyst;

-- Revoke privileges
REVOKE INSERT ON sales.orders FROM analyst;

-- Create user and assign role
CREATE USER alice WITH PASSWORD 'StrongPass123';
GRANT analyst TO alice;

-- Alter user password
ALTER USER alice WITH PASSWORD 'NewStrongPass!';

-- Drop user
DROP USER alice;

-- Transfer table ownership (PostgreSQL example)
ALTER TABLE sales.orders OWNER TO analyst;

-- Audit grants for a user (Snowflake example)
SHOW GRANTS TO USER alice;
```

---

This cheat sheet **covers all essential DCL operations across major DBs**, highlighting **roles, privileges, user management, and ownership transfer**, making it **enterprise-ready for security, compliance, and governance workflows**.

