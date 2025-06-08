# SQL Tutorial

## Overview

SQL (Structured Query Language) is a standard language for managing and manipulating relational databases. This document provides an introduction to SQL commands with examples.

## Basic SQL Commands

### 1. SELECT

The `SELECT` statement retrieves data from a database.

```sql
SELECT column1, column2
FROM table_name;
```

#### Example

```sql
SELECT first_name, last_name
FROM employees;
```

### 2. WHERE

The `WHERE` clause filters records based on specific conditions.

```sql
SELECT column1, column2
FROM table_name
WHERE condition;
```

#### Example

```sql
SELECT first_name, last_name
FROM employees
WHERE department = 'Sales';
```

### 3. INSERT INTO

The `INSERT INTO` statement adds new rows to a table.

```sql
INSERT INTO table_name (column1, column2)
VALUES (value1, value2);
```

#### Example

```sql
INSERT INTO employees (first_name, last_name, department)
VALUES ('John', 'Doe', 'Marketing');
```

### 4. UPDATE

The `UPDATE` statement modifies existing records.

```sql
UPDATE table_name
SET column1 = value1, column2 = value2
WHERE condition;
```

#### Example

```sql
UPDATE employees
SET department = 'HR'
WHERE last_name = 'Doe';
```

### 5. DELETE

The `DELETE` statement removes rows from a table.

```sql
DELETE FROM table_name
WHERE condition;
```

#### Example

```sql
DELETE FROM employees
WHERE last_name = 'Doe';
```

### 6. CREATE TABLE

The `CREATE TABLE` statement creates a new table.

```sql
CREATE TABLE table_name (
    column1 datatype,
    column2 datatype,
    ...
);
```

#### Example

```sql
CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    department VARCHAR(50)
);
```

### 7. ALTER TABLE

The `ALTER TABLE` statement modifies an existing table structure.

```sql
ALTER TABLE table_name
ADD column_name datatype;
```

#### Example

```sql
ALTER TABLE employees
ADD hire_date DATE;
```

### 8. DROP TABLE

The `DROP TABLE` statement deletes an entire table.

```sql
DROP TABLE table_name;
```

#### Example

```sql
DROP TABLE employees;
```

### 9. JOIN

The `JOIN` clause combines rows from two or more tables based on a related column.

#### INNER JOIN

```sql
SELECT columns
FROM table1
INNER JOIN table2
ON table1.common_column = table2.common_column;
```

#### Example

```sql
SELECT employees.first_name, departments.department_name
FROM employees
INNER JOIN departments
ON employees.department_id = departments.department_id;
```

#### LEFT JOIN

```sql
SELECT columns
FROM table1
LEFT JOIN table2
ON table1.common_column = table2.common_column;
```

#### Example

```sql
SELECT employees.first_name, departments.department_name
FROM employees
LEFT JOIN departments
ON employees.department_id = departments.department_id;
```

## Advanced SQL Commands

### 1. GROUP BY

The `GROUP BY` statement groups rows sharing a property.

```sql
SELECT column1, COUNT(*)
FROM table_name
GROUP BY column1;
```

#### Example

```sql
SELECT department, COUNT(*)
FROM employees
GROUP BY department;
```

### 2. HAVING

The `HAVING` clause filters groups based on conditions.

```sql
SELECT column1, COUNT(*)
FROM table_name
GROUP BY column1
HAVING COUNT(*) > value;
```

#### Example

```sql
SELECT department, COUNT(*)
FROM employees
GROUP BY department
HAVING COUNT(*) > 5;
```

### 3. ORDER BY

The `ORDER BY` clause sorts the result set.

```sql
SELECT column1, column2
FROM table_name
ORDER BY column1 [ASC|DESC];
```

#### Example

```sql
SELECT first_name, last_name
FROM employees
ORDER BY last_name ASC;
```

### 4. DISTINCT

The `DISTINCT` keyword removes duplicate values.

```sql
SELECT DISTINCT column1
FROM table_name;
```

#### Example

```sql
SELECT DISTINCT department
FROM employees;
```

### 5. Subqueries

A subquery is a query within another query.

```sql
SELECT column1
FROM table_name
WHERE column2 = (SELECT column2 FROM table2 WHERE condition);
```

#### Example

```sql
SELECT first_name
FROM employees
WHERE department_id = (SELECT department_id FROM departments WHERE department_name = 'Marketing');
```

## Summary

This tutorial introduces fundamental SQL commands used to interact with relational databases. Understanding these commands will enable you to effectively query and manipulate data. For more advanced features and detailed information, refer to the [official SQL documentation](https://www.w3schools.com/sql/).
