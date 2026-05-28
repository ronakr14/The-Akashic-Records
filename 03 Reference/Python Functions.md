---
id: 55qtuqsj4kwljunakhq4986
title: Functions Lambdas
desc: ''
updated: 1755766367506
created: 1755766359526
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
