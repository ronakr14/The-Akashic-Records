---
id: gs4vzqmyrj2ki67eagcuyu6
title: Core
desc: ''
updated: 1755766117738
created: 1755766111922
---

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
