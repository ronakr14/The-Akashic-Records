
# python
Best use case:  
Rapid backend, data engineering, and AI/ML development—ideal for building pipelines, APIs, and automation with rich libraries.

Alternative: — Go when you need high concurrency, low latency, and simpler deployment for production services


# **Python Fluency Cheat Sheet – Core Syntax + Data Types**

### **1. Variables & Assignment**

```python
x = 5                 # dynamic typing
a, b, c = 1, 2, 3     # multiple assignment
x = y = z = 0         # chain assignment
a, b = b, a           # swap without temp
first, *_ , last = lst # ignore middle elements
```

---

### **2. Data Types & Tricks**

| Type      | Example                   | Notes / Tricks                                |                            |
| --------- | ------------------------- | --------------------------------------------- | -------------------------- |
| int       | `x = 42`                  | Arbitrary precision                           |                            |
| float     | `y = 3.14`                | Use `decimal` for precision                   |                            |
| complex   | `z = 1 + 2j`              | `z.real`, `z.imag`                            |                            |
| bool      | `flag = True`             | Subclass of int (`True + 2 == 3`)             |                            |
| str       | `s = "hello"`             | Immutable, slicing, `.join()` for fast concat |                            |
| list      | `lst = [1,2,3]`           | Mutable, slicing, comprehensions              |                            |
| tuple     | `t = (1,2,3)`             | Immutable, usable as dict keys                |                            |
| set       | `st = {1,2,3}`            | Unique, \`                                    | &\` for union/intersection |
| frozenset | `fs = frozenset([1,2,3])` | Immutable set                                 |                            |
| dict      | `d = {'a':1}`             | `dict.get(k, default)` avoids KeyError        |                            |
| NoneType  | `x = None`                | Use `is` to check (`x is None`)               |                            |

**Unpacking tricks:**

```python
first, *middle, last = [1,2,3,4,5]
```

---

### **3. Control Flow**

**If / Else / Elif:**

```python
if x > 0:
    ...
elif x == 0:
    ...
else:
    ...
```

**Loops:**

```python
for i in range(5): ...
while condition: ...
```

**Loop else (runs if no break):**

```python
for x in lst:
    if x==0: break
else:
    print("No zeros")
```

**Comprehensions (Pythonic one-liners):**

```python
squares = [x*x for x in range(10) if x%2==0]
```

---

### **4. Functions & Lambdas**

```python
def add(a, b=0, *args, **kwargs):
    return a + b + sum(args) + sum(kwargs.values())

f = lambda x: x**2
```

**Gotchas / Tips:**

```python
# Mutable default args -> use None
def append_to_list(x, lst=None):
    lst = lst or []
    lst.append(x)
    return lst

# Keyword-only args after *
def foo(a, *, b): ...
```

---

### **5. Type Hints**

```python
from typing import Optional, Union, List, Dict

def greet(name: str) -> str: ...
def process(data: Optional[List[int]]) -> Union[int, None]: ...
```

---

### **6. Built-in Functions / Utilities**

* `len(), sum(), any(), all(), zip(), enumerate(), sorted(), reversed()`
* `isinstance(obj, type)`, `issubclass(cls, Base)`, `type(obj)`
* `min(), max(), abs(), round()`
* `dir(obj)` → attributes & methods
* `help(obj)` → docstring

---

### **7. Pythonic Idioms**

* Truthy/falsy: `[]`, `{}`, `0`, `None`, `''` → False
* EAFP (ask forgiveness, not permission):

```python
try:
    value = d['key']
except KeyError:
    value = default
```

* Context manager:

```python
with open('file.txt') as f:
    content = f.read()
```

* `_` as throwaway variable

---

### **8. Advanced Tricks**

```python
# Swapping with tuple unpacking
a, b = b, a

# Flatten list of lists
flat = [item for sublist in nested for item in sublist]

# Enumerate with index
for idx, val in enumerate(lst): ...

# Zip for parallel iteration
for a, b in zip(list1, list2): ...

# Ternary operator
x = "Yes" if condition else "No"
```

---

✅ **Cheat Sheet Highlights**

* Immutable vs mutable types → avoid bugs
* EAFP pattern → cleaner than `if key in dict`
* Comprehensions & unpacking → Pythonic, readable
* Type hints → improves readability and IDE support
* `_` & `*` tricks → neat, clean, avoids boilerplate

---



# **Python Fluency Cheat Sheet – Functions + Lambdas**

### **1. Function Definition**

```python
def func_name(arg1, arg2=default, *args, **kwargs):
    """Docstring describing purpose."""
    return arg1 + arg2
```

* `*args` → variable positional args
* `**kwargs` → variable keyword args
* Functions are **first-class objects** (assign, pass, return)

---

### **2. Argument Types**

| Type            | Example                       | Notes                             |
| --------------- | ----------------------------- | --------------------------------- |
| Positional      | `def f(a, b): ...`            | Order matters                     |
| Default         | `def f(a=1): ...`             | Avoid mutable defaults (`lst=[]`) |
| Keyword-only    | `def f(*, b): ...`            | Forces keyword usage              |
| Variadic        | `def f(*args, **kwargs): ...` | Flexible argument passing         |
| Positional-only | `def f(a,b,/): ...`           | Python 3.8+                       |

**Mutable default fix:**

```python
def append_val(x, lst=None):
    lst = lst or []
    lst.append(x)
    return lst
```

---

### **3. Scope & Closures**

```python
x = 10  # global

def outer(a):
    b = 5  # enclosing
    def inner(c):
        return a + b + c
    return inner

f = outer(2)
f(3)  # 10
```

* LEGB Rule: Local → Enclosing → Global → Built-in
* `nonlocal` modifies enclosing scope:

```python
def counter():
    count = 0
    def inc():
        nonlocal count
        count += 1
        return count
    return inc
```

---

### **4. Lambda Functions**

```python
f = lambda x, y=2: x + y
f(3)  # 5
```

* **Use:** small, single-expression functions
* Often used with `map`, `filter`, `sorted`, `reduce`

**Examples:**

```python
points = [(1,2),(3,1),(0,0)]
points.sort(key=lambda p: p[1])  # sort by y
squared = list(map(lambda x: x**2, range(5)))
evens = list(filter(lambda x: x%2==0, range(10)))
```

---

### **5. Decorators**

```python
def decorator(func):
    def wrapper(*args, **kwargs):
        print("Before call")
        result = func(*args, **kwargs)
        print("After call")
        return result
    return wrapper

@decorator
def greet(name): return f"Hello {name}"
greet("Alice")
```

* Use for logging, timing, caching, authentication
* Can stack decorators: `@dec1 @dec2 def f(): ...`

---

### **6. Higher-Order Functions**

```python
def apply_func(x, func):
    return func(x)

apply_func(5, lambda x: x**2)  # 25
```

* Tools from `functools`:

  * `partial(func, arg1=val)` → pre-fill args
  * `lru_cache(maxsize=None)` → memoization
  * `reduce(func, iterable)` → accumulate values

---

### **7. Function Annotations / Type Hints**

```python
from typing import Callable, Optional, List

def greet(name: str) -> str: ...
def operate(x: int, func: Callable[[int], int]) -> int: ...
```

* Improves readability and IDE support

---

### **8. Pythonic Tricks**

```python
# Ternary operator
def sign(x): return "pos" if x>0 else "neg"

# Swap
a, b = b, a

# Functions as dict values
ops = {'add': lambda x,y:x+y, 'mul': lambda x,y:x*y}
ops['add'](2,3)  # 5

# Unpacking
args = [1,2,3]; f(*args)
kwargs = {'a':1,'b':2,'c':3}; f(**kwargs)
```

---

✅ **Cheat Sheet Highlights**

* LEGB & closures → control scoping
* Mutable default args → watch out
* Lambdas → concise, functional usage
* Decorators → reusable wrappers
* Higher-order functions → functional pipelines
* Pythonic tricks → unpacking, dict-of-functions, ternary, swaps

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


```table-of-contents
```
# Summary

They’re three different approaches to **concurrency / parallelism** with different trade-offs:
1. **Async (async/await)** = best for _many_ I/O-bound tasks with low CPU usage (network, disk). Single thread, tiny memory footprint, high throughput, lower latency handling thousands+ connections.
2. **Multithread** = good for _I/O-bound_ work when you want simpler synchronous-style code or need blocking libs; in CPython threads are _concurrent_ but not truly parallel for Python bytecode because of the GIL.
3. **Multiprocess** = use when you need _true parallelism_ for CPU-bound work — each process has its own Python interpreter and memory; heavier but runs on multiple CPU cores.

# Quick rules of thumb

- If your problem is **waiting on network/db/files** → use **async** or **threads**.
- If your problem is **heavy CPU work** (ML, big loops, compression) → use **multiprocess**.
- If you need **shared memory and low complexity**, threads are easier but beware of GIL and race conditions.
- If you need **isolation, robustness, parallel CPU**, use processes (or native C extensions, or move heavy work to GPU/worker service).

# Practical pros/cons (short)

## **Async**

- Pros: low memory, high concurrency, explicit flow control, predictable scheduling.
- Cons: needs async-aware libraries, callback-style mental model, debugging & stack traces can be trickier. 
## **Threads**
- Pros: easy to reuse sync libraries, simpler code for blocking libs, shared memory (no serialization).
- Cons: GIL in CPython limits CPU parallelism; locking/race conditions; context-switch overhead. 
## **Processes**
- Pros: true parallelism, isolation (crash one process, others survive).
- Cons: higher memory/IPC cost, serialization overhead, more complex orchestration.

# Python mini-examples

**Async (IO-bound)**
```python
import asyncio
import aiohttp
async def fetch(url):
    async with aiohttp.ClientSession() as s:
        async with s.get(url) as r:
            return await r.text()
async def main(urls):
    tasks = [asyncio.create_task(fetch(u)) for u in urls]
    return await asyncio.gather(*tasks)
```

**Threads (easier with blocking libs)**
```python
from concurrent.futures import ThreadPoolExecutor
import requests
def fetch(url):
    return requests.get(url).text
with ThreadPoolExecutor(max_workers=20) as ex:
    results = list(ex.map(fetch, urls))
```

**Processes (CPU-bound)**
```python
from concurrent.futures import ProcessPoolExecutor
def heavy(x):
    # cpu-expensive
    return sum(i*i for i in range(10_000_000))
with ProcessPoolExecutor() as ex:
    results = list(ex.map(heavy, inputs))
```

# Performance considerations & pitfalls

- **GIL**: CPython only allows one thread executing Python bytecode at a time — threads help with I/O but not CPU.
- **Memory**: processes duplicate memory (copy-on-write helps initially). Threads share memory — less memory but need locks.
- **Latency vs Throughput**: async often gives best throughput for many connections; threads/processes can reduce per-task latency if blocking libs dominate.
- **Debugging & Observability**: async stack traces and race conditions can be hard to debug; processes are easier to isolate and attach profilers to.

# When to pick what (quick decision flow)

1. Need to handle thousands of concurrent network connections → **async**.
2. Using synchronous libraries that block and you don’t want to refactor → **threads**.
3. Doing CPU-heavy tasks you want across multiple cores → **processes** (or move to C/NumPy/GPU).
4. Need isolation and fault-tolerance → **processes / separate services**.


# **Python Fluency Cheat Sheet – Classes + OOP**

### **1. Class Basics**

```python
class MyClass:
    class_var = 0  # shared across instances

    def __init__(self, name: str, age: int):
        self.name = name  # instance variable
        self.age = age

    def greet(self) -> str:
        return f"Hello, {self.name}"
```

* `__init__` → constructor
* `self` → instance reference
* Class variables shared; instance variables unique

---

### **2. Methods**

| Type            | Syntax & Access                 | Notes                                     |
| --------------- | ------------------------------- | ----------------------------------------- |
| Instance method | `def f(self): ...`              | Access instance attributes                |
| Class method    | `@classmethod\ndef f(cls): ...` | Access class-level state; factory methods |
| Static method   | `@staticmethod\ndef f(): ...`   | Utility function in class context         |

---

### **3. Inheritance & Polymorphism**

```python
class Parent:
    def speak(self): return "Parent"

class Child(Parent):
    def speak(self): return "Child"

c = Child()
c.speak()  # polymorphic call
```

* Use `super()` for parent init / method call
* Multiple inheritance → Python uses **C3 MRO** (`C.mro()`)

---

### **4. Properties & Encapsulation**

```python
class Person:
    def __init__(self, age):
        self._age = age

    @property
    def age(self): return self._age

    @age.setter
    def age(self, value):
        if value < 0: raise ValueError("Age cannot be negative")
        self._age = value
```

* `_var` → protected by convention
* `__var` → name mangling (semi-private)
* `@property` → clean getter/setter interface

---

### **5. Magic / Dunder Methods**

| Method                       | Purpose                |
| ---------------------------- | ---------------------- |
| `__str__`                    | Human-readable string  |
| `__repr__`                   | Debug representation   |
| `__len__`                    | `len(obj)`             |
| `__getitem__`                | Indexing / slicing     |
| `__setitem__`                | Assign to index/key    |
| `__iter__`, `__next__`       | Iterable support       |
| `__eq__`, `__lt__`, `__gt__` | Comparisons            |
| `__call__`                   | Make instance callable |
| `__add__`, `__sub__`, ...    | Operator overloading   |

Example:

```python
class Vector:
    def __init__(self, x, y): self.x, self.y = x, y
    def __add__(self, other): return Vector(self.x + other.x, self.y + other.y)
    def __repr__(self): return f"Vector({self.x},{self.y})"
```

---

### **6. Composition vs Inheritance**

```python
class Engine: ...
class Car:
    def __init__(self):
        self.engine = Engine()  # composition
```

* **Inheritance** → “is-a”
* **Composition** → “has-a” (preferred for flexibility)

---

### **7. Class Patterns / Tricks**

```python
# Factory method
class User:
    @classmethod
    def from_dict(cls, data): return cls(data['name'])

# Singleton
class Singleton:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance: cls._instance = super().__new__(cls)
        return cls._instance

# Context manager
class ManagedFile:
    def __enter__(self): self.f = open('file.txt'); return self.f
    def __exit__(self, exc_type, exc_val, exc_tb): self.f.close()
```

---

### **8. Pythonic OOP Idioms**

```python
# Duck typing
def quack(duck): duck.quack()  # any object with quack() works

# Mixins
class JsonMixin:
    def to_json(self): return json.dumps(self.__dict__)

class Person(JsonMixin):
    def __init__(self, name): self.name = name
```

* Favor **composition over inheritance**
* Use **mixins** for reusable behavior
* Implement **dunder methods** for Pythonic integration

---

✅ **Cheat Sheet Highlights**

* Class/instance/static/class methods → clear separation
* LEGB & encapsulation → control state exposure
* Decorator-friendly design → scalable wrappers
* Magic methods → make classes integrate naturally with Python
* Composition & mixins → flexible, maintainable architectures

---

