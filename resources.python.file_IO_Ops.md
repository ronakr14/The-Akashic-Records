---
id: 3a3k34flmwor82m6pgmaqj5
title: file_IO_Ops
desc: ''
updated: 1755766869395
created: 1755766863652
---

# **Python Fluency Cheat Sheet – File I/O + JSON + CSV**

### **1. File I/O Basics**

```python
# Read entire file
with open("data.txt", "r", encoding="utf-8") as f:
    content = f.read()

# Read line by line
with open("data.txt") as f:
    for line in f:
        print(line.strip())

# Write / overwrite
with open("output.txt", "w") as f:
    f.write("Hello\nWorld")

# Append
with open("output.txt", "a") as f:
    f.write("Append line\n")

# Pathlib (modern)
from pathlib import Path
p = Path("data.txt")
content = p.read_text()
p.write_text("Hello")
```

**Tips:**

* Always use `with` → auto-close
* `encoding="utf-8"` → avoid Unicode errors
* Pathlib → cross-platform, more readable

---

### **2. JSON Handling**

```python
import json

# Load JSON
data = json.loads('{"name":"Alice"}')
with open("data.json") as f:
    data = json.load(f)

# Dump JSON
json_str = json.dumps(data, indent=2)
with open("out.json", "w") as f:
    json.dump(data, f, indent=2)

# Custom object serialization
import datetime
json.dumps({"now": datetime.datetime.now()}, default=str)

# Exception handling
try:
    data = json.load(f)
except json.JSONDecodeError:
    print("Invalid JSON")
```

---

### **3. CSV Handling**

```python
import csv

# Read CSV
with open("data.csv", newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)

# DictReader
with open("data.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row["name"])

# Write CSV
rows = [["name","age"], ["Alice",25], ["Bob",30]]
with open("out.csv", "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerows(rows)

# DictWriter
with open("out.csv", "w", newline='') as f:
    writer = csv.DictWriter(f, fieldnames=["name","age"])
    writer.writeheader()
    writer.writerow({"name":"Alice","age":25})
```

**Tips:**

* `newline=''` → prevents extra blank lines on Windows
* Use `DictReader`/`DictWriter` → clearer and safer
* Process line by line → memory-efficient

---

### **4. Converting JSON ↔ CSV**

```python
# CSV → JSON
with open("data.csv") as f:
    reader = csv.DictReader(f)
    data = list(reader)
with open("data.json", "w") as f:
    json.dump(data, f, indent=2)

# JSON → CSV
with open("data.json") as f:
    data = json.load(f)
with open("out.csv", "w", newline='') as f:
    writer = csv.DictWriter(f, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)
```

---

### **5. Pythonic File Handling Idioms**

```python
# Lazy reading large files
with open("bigfile.txt") as f:
    for line in f:
        process(line)

# Temporary files
import tempfile
with tempfile.TemporaryFile(mode='w+t') as f:
    f.write("temp data")
    f.seek(0)
    print(f.read())

# Pathlib chaining
from pathlib import Path
p = Path("folder") / "subfolder" / "file.txt"
text = p.read_text()
```

---

✅ **Cheat Sheet Highlights**

* Always use **`with`** → context management
* **Pathlib** → modern, cross-platform paths
* **JSON** → dict/list, handle exceptions, `default=str` for objects
* **CSV** → `DictReader`/`DictWriter` for clarity, `newline=''` on Windows
* **Large files** → process lazily

---
