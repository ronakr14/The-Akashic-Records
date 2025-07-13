# Cheatsheet

## Cheatsheets

### Data Types Quick Map

```python
type(123)         # int
type("abc")       # str
type([1,2])       # list
type({'a':1})     # dict
```

### Control Flow Mental Model

- **For**: iterate over collections
- **While**: run until a condition is False
- **If/Elif/Else**: make decisions

### Function Skeleton

```python
def my_func(arg1, arg2="default"):
    return arg1 + arg2
```

### Try/Except Template

```python
try:
    risky_stuff()
except ValueError as e:
    print(f"Error: {e}")
finally:
    print("Cleanup")
```

### File I/O

```python
with open("file.txt", "r") as f:
    data = f.read()
```

## Mental Models

- Python is **object-oriented by default** – everything is an object.
- Prefer **explicit over implicit** (Zen of Python).
- Use **duck typing**, but verify with `isinstance()` when needed.
- **“Ask for forgiveness, not permission”** – use try/except liberally.