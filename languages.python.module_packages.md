---
id: 2met3b2djflfm75v07hco16
title: Module_packages
desc: ''
updated: 1755767184079
created: 1755767177856
---

# **Python Fluency Cheat Sheet – Modules + Packages**

### **1. Modules**

* A `.py` file containing Python code (functions, classes, variables)

```python
# math_utils.py
def add(a, b): return a + b
def multiply(a, b): return a * b
```

**Importing Modules**

```python
import math_utils
math_utils.add(2, 3)

from math_utils import add
add(2, 3)

import math_utils as mu
mu.multiply(2, 3)
```

**Tips:**

* Modules cached in `sys.modules` → fast subsequent imports
* Use `if __name__ == "__main__":` for test/demo code

---

### **2. Packages**

* A folder containing an `__init__.py` file

```
my_project/
├── utils/
│   ├── __init__.py
│   ├── math_utils.py
│   └── string_utils.py
└── main.py
```

**Importing**

```python
from utils.math_utils import add      # absolute
from .math_utils import add            # relative (inside package)
```

**Expose package API via `__init__.py`**

```python
# utils/__init__.py
from .math_utils import add, multiply
from .string_utils import capitalize
```

Then:

```python
from utils import add, capitalize
```

---

### **3. Project Structuring Best Practices**

```
project_name/
├── project_name/
│   ├── __init__.py
│   ├── core.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── file_ops.py
│   │   └── data_ops.py
│   └── models/
│       ├── __init__.py
│       └── user.py
├── tests/
│   └── test_core.py
├── setup.py
└── README.md
```

* Absolute imports preferred: `from project_name.utils import ...`
* Modules → single responsibility
* Nested packages → organize by functionality
* Avoid circular imports → refactor common utilities

---

### **4. Dynamic & Conditional Imports**

```python
module_name = "math_utils"
math_mod = __import__(module_name)
math_mod.add(2,3)

import importlib
importlib.reload(math_utils)  # reload module for dev/testing
```

* Useful for plugin systems or optional dependencies

---

### **5. Python Path & Environment**

```python
import sys
sys.path.append("/path/to/project")  # temporary path extension
```

* Or set `PYTHONPATH` environment variable
* Avoid modifying `sys.path` in production if possible

---

### **6. Inspection & Utilities**

```python
import inspect
print(inspect.getmembers(math_utils))  # list all functions/classes

import pkgutil
for loader, name, is_pkg in pkgutil.iter_modules(utils.__path__):
    print(name, is_pkg)  # list submodules in a package
```

---

### **7. Pythonic Tricks**

```python
# Relative imports for intra-package modules
from .submodule import func

# Package API exposure via __init__.py
__all__ = ["add", "multiply"]  # restrict public API

# Conditional imports
try:
    import optional_lib
except ImportError:
    optional_lib = None
```

---

✅ **Cheat Sheet Highlights**

* **Module = .py file**, **Package = folder with `__init__.py`**
* Prefer **absolute imports**; use **relative imports** internally
* Keep modules **focused**, packages **organized and nested**
* `__init__.py` → central API exposure
* Use **dynamic imports** and **inspection tools** for flexibility
* Avoid **circular imports** → structure wisely

---
