---
id: dp6kfz2crmgau64fq59zym6
title: Pandas
desc: ''
updated: 1753449621811
created: 1753449617020
---
tags: [master, pandas, python, dataframe, datascience, etl]

## 📌 Topic Overview

**Pandas** is the **Swiss Army Knife of data wrangling** in Python. It's a fast, flexible, and expressive library built on top of NumPy — perfect for **tabular data** manipulation and analysis. At its core is the **DataFrame**, a 2D labeled structure similar to SQL tables or Excel sheets but fully programmable.

Used by data engineers, data scientists, analysts, and even ML engineers, Pandas lets you slice, dice, clean, pivot, reshape, group, join, and time-travel through data like a boss.

---

## 🚀 80/20 Roadmap

| Stage | Concept                     | Why It Matters                                              |
|-------|-----------------------------|-------------------------------------------------------------|
| 1️⃣    | Series and DataFrame        | Foundation blocks of pandas — know them cold                |
| 2️⃣    | Reading/Writing Data        | CSV, JSON, Excel, SQL — ingest and export like a pro        |
| 3️⃣    | Indexing & Slicing          | Master `.loc[]`, `.iloc[]`, and conditional filters         |
| 4️⃣    | Aggregations & GroupBy      | Summarize and segment data fast                             |
| 5️⃣    | Data Cleaning               | Nulls, types, renames, dedupes — daily Pandas grind         |
| 6️⃣    | Merge, Join, Concat         | Stitch data together like SQL                               |
| 7️⃣    | Apply, Map, Lambda          | Functional ops across rows and columns                      |
| 8️⃣    | Pivoting & Melting          | Reshape tall/wide data for analysis                         |
| 9️⃣    | Time Series                 | Date indexing, resampling, window ops                       |
| 🔟     | Performance & Memory        | Optimize with dtypes, chunking, and vectorization           |

---

## 🛠️ Practical Tasks

- ✅ Read CSV/JSON into a DataFrame and export to Excel  
- ✅ Filter rows by condition and select specific columns  
- ✅ Fill missing values and change data types  
- ✅ Group by a category and calculate summary stats  
- ✅ Merge two DataFrames on a key with different join types  
- ✅ Use `.apply()` to calculate new derived columns  
- ✅ Use `.pivot_table()` to reshape data  
- ✅ Convert a column to datetime and resample weekly  
- ✅ Use `query()` for expressive filtering  
- ✅ Save the cleaned DataFrame back to a database

---

## 🧾 Cheat Sheets

### 📖 Read/Write Data

```python
import pandas as pd

df = pd.read_csv("data.csv")
df.to_excel("output.xlsx")
df = pd.read_json("data.json")
````

### 🎯 Indexing & Filtering

```python
df.loc[df["age"] > 30, ["name", "salary"]]
df.iloc[0:5, 2:4]
df.query("age > 25 and city == 'Mumbai'")
```

### 📊 Grouping & Aggregation

```python
df.groupby("department")["salary"].mean()
df.groupby(["dept", "level"]).agg({"salary": ["mean", "max"]})
```

### 🧹 Cleaning & Transforming

```python
df.dropna()
df.fillna(0)
df["date"] = pd.to_datetime(df["date"])
df.rename(columns={"emp_id": "employee_id"}, inplace=True)
```

### 🔗 Join/Merge

```python
pd.merge(df1, df2, on="id", how="left")
pd.concat([df1, df2], axis=0)  # Stack rows
```

### 🌀 Apply/Map/Lambda

```python
df["tax"] = df["salary"].apply(lambda x: x * 0.1)
df["state_code"] = df["state"].map({"CA": "California", "NY": "New York"})
```

### ⏱ Time Series

```python
df["date"] = pd.to_datetime(df["date"])
df.set_index("date").resample("M")["sales"].sum()
```

---

## 🎯 Progressive Challenges

| Level           | Challenge                                                                 |
| --------------- | ------------------------------------------------------------------------- |
| 🥉 Beginner     | Load a CSV, clean nulls, filter by column, export to Excel                |
| 🥈 Intermediate | Join 2 datasets, compute aggregates, and generate a pivot table           |
| 🥇 Advanced     | Build a time series analysis with rolling averages and trend lines        |
| 🏆 Expert       | Create a pandas-based ETL pipeline that pulls from SQL and exports to API |

---

## 🎙️ Interview Q\&A

* **Q:** What are the key differences between `.loc[]` and `.iloc[]`?
* **Q:** How does Pandas handle missing data?
* **Q:** When would you use `groupby` vs `pivot_table`?
* **Q:** What are the common performance bottlenecks in Pandas?
* **Q:** How do you handle large datasets that don’t fit in memory?

---

## 🛣️ Next Tech Stack Recommendations

* **Dask** — Distributed dataframe operations for big data
* **Polars** — Lightning-fast dataframe engine with Rust core
* **DuckDB** — SQL-first analytics on Pandas DataFrames
* **Modin** — Parallelized Pandas drop-in replacement
* **pandas-profiling** — Auto-generate data exploration reports

---

## 🧠 Pro Tips

* Use `.astype()` to downcast dtypes (e.g., `float64` → `float32`)
* Prefer `.query()` and `.eval()` for readable and fast filtering
* Chain methods with `.pipe()` for cleaner pipelines
* Use `.memory_usage(deep=True)` to profile DataFrame size
* Avoid row-wise loops — always vectorize where possible
* Use `Categorical` dtype to save memory for repeated strings

---

## 🧬 Tactical Philosophy

> “Pandas turns raw data into insight-ready gold — if you can wrangle it properly.”

🎯 Think like a **data janitor**: clean first, analyze later
🪄 Embrace chaining — think in **transform pipelines**, not step-by-step
🧠 Read the docs! Most pandas magic is buried in lesser-known parameters
📈 Use Pandas not just for dataframes — but for **experiments, dashboards, and ETLs**
🐼 Mastering pandas means you speak the universal dialect of tabular data

---
