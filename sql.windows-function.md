---
id: mlqsqg2de7bqqgw1veyrj1z
title: Windows Function
desc: ''
updated: 1755763920117
created: 1755763913792
---

# **Enterprise Multi-DB Windows Operations Cheat Sheet**

| Operation                       | Purpose                                  | Syntax / Example                                                                                                                                                                                                                                                                                                                                                    | DB Notes / Enterprise Tips                                                                                                  |
| ------------------------------- | ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| **Set Environment Variables**   | Set DB connection, credentials, or paths | `set DB_USER=admin` <br> `setx DB_USER admin` (persistent)                                                                                                                                                                                                                                                                                                          | Enterprise: Use persistent variables (`setx`) for scheduled jobs; keep secrets in Windows Credential Manager or .env files. |
| **Check Environment Variables** | View OS-level DB variables               | `echo %DB_USER%` <br> `set`                                                                                                                                                                                                                                                                                                                                         | Enterprise: Verify environment variables before running ETL, CLI scripts, or database clients.                              |
| **Path Management**             | Add DB binaries to PATH                  | `set PATH=%PATH%;C:\Program Files\PostgreSQL\15\bin`                                                                                                                                                                                                                                                                                                                | Enterprise: simplifies CLI access to database tools like `psql`, `sqlcmd`, `sqlplus`.                                       |
| **File Operations**             | Move, copy, delete, list files           | `copy source.txt dest.txt` <br> `move source.txt dest.txt` <br> `del file.txt` <br> `dir /B`                                                                                                                                                                                                                                                                        | Enterprise: ETL scripts often rely on moving/importing/exporting CSV, JSON, or SQL scripts.                                 |
| **Windows Task Scheduler**      | Schedule DB scripts, backups, ETL        | Use GUI to create a task or CLI: `schtasks /Create /SC DAILY /TN "DB_Backup" /TR "C:\scripts\backup.bat"`                                                                                                                                                                                                                                                           | Enterprise: automate backups, ETL, and maintenance tasks; ensure proper account permissions.                                |
| **PowerShell Integration**      | Execute DB scripts & manage files        | `Invoke-Sqlcmd -Query "SELECT * FROM Orders" -ServerInstance "localhost"` <br> `Get-Content file.txt`                                                                                                                                                                                                                                                               | Enterprise: PowerShell is preferred for automation over batch scripts; integrates with Windows security.                    |
| **Database CLI Access**         | Run DB commands from Windows             | PostgreSQL: `psql -U admin -d mydb -f script.sql` <br> SQL Server: `sqlcmd -S localhost -U sa -P Password -i script.sql` <br> Oracle: `sqlplus admin/password@ORCL @script.sql` <br> Snowflake: `snowsql -a <account> -u <user> -f script.sql`                                                                                                                      | Enterprise: keep CLI scripts in version control; parameterize for security.                                                 |
| **File Permissions / ACLs**     | Control access to DB files/scripts       | `icacls C:\db\scripts /grant AdminUser:F`                                                                                                                                                                                                                                                                                                                           | Enterprise: restrict access to sensitive scripts, backups, or DB configuration files.                                       |
| **Zip / Compress Files**        | Backup or move DB files                  | `Compress-Archive -Path C:\db\backup\* -DestinationPath C:\db\backup.zip`                                                                                                                                                                                                                                                                                           | Enterprise: compress logs, CSVs, and backups for storage or transfer.                                                       |
| **Best Practices**              | Enterprise usage                         | - Keep DB binaries in PATH <br> - Use PowerShell scripts for automation <br> - Store sensitive credentials in secure environment variables or Windows Credential Manager <br> - Automate backups & ETL with Task Scheduler <br> - Use proper file permissions for DB files and scripts <br> - Maintain a consistent folder structure for scripts, logs, and backups | Enterprise: Ensures Windows OS operations are secure, auditable, and repeatable in production environments.                 |

---

## **Quick Examples**

```bat
:: Set environment variable (session-only)
set DB_USER=admin

:: Set persistent environment variable
setx DB_USER admin

:: Check variable
echo %DB_USER%

:: Add PostgreSQL bin to PATH
set PATH=%PATH%;C:\Program Files\PostgreSQL\15\bin

:: Copy, move, delete files
copy C:\temp\data.csv C:\backup\data.csv
move C:\temp\data.csv C:\archive\
del C:\temp\oldfile.csv
dir /B C:\temp

:: Run PostgreSQL script via CLI
psql -U admin -d mydb -f C:\scripts\load_data.sql

:: Run SQL Server script via CLI
sqlcmd -S localhost -U sa -P Password -i C:\scripts\load_data.sql

:: Zip files via PowerShell
Compress-Archive -Path C:\db\backup\* -DestinationPath C:\db\backup.zip

:: Windows Task Scheduler CLI
schtasks /Create /SC DAILY /TN "DB_Backup" /TR "C:\scripts\backup.bat"
```

---

This cheat sheet **covers essential Windows OS operations for database interaction**, highlighting **environment variables, CLI access, file handling, scheduling, PowerShell integration, permissions, compression, and best practices**, making it **enterprise-ready for DBA, ETL, and automation tasks**.

