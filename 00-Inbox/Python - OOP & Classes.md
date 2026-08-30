# AI Summary
A practical guide to object-oriented programming in Python covering class fundamentals, instance, class, and static methods, inheritance, polymorphism, encapsulation, properties, magic (dunder) methods, composition versus inheritance, common class patterns such as factory methods, singletons, and context managers, along with Pythonic practices including duck typing, mixins, and API design. The note concludes with a concise cheat sheet summarizing recommended patterns for writing maintainable and idiomatic Python classes.

---
## Class Basics

```python
class MyClass:
    class_var = 0  # shared across instances

    def __init__(self, name: str, age: int):
        self.name = name  # instance variable
        self.age = age

    def greet(self) -> str:
        return f"Hello, {self.name}"
```

- `__init__` → constructor
- `self` → instance reference
- Class variables shared; instance variables unique

---

## Methods

| Type | Syntax & Access | Notes |
|------|-----------------|-------|
| Instance method | `def f(self): ...` | Access instance attributes |
| Class method | `@classmethod def f(cls): ...` | Access class-level state; factory methods |
| Static method | `@staticmethod def f(): ...` | Utility function in class context |

---

## Inheritance & Polymorphism

```python
class Parent:
    def speak(self): return "Parent"

class Child(Parent):
    def speak(self): return "Child"

c = Child()
c.speak()  # polymorphic call
```

- Use `super()` for parent init / method call
- Multiple inheritance → Python uses **C3 MRO** (`C.mro()`)

---

## Properties & Encapsulation

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

- `_var` → protected by convention
- `__var` → name mangling (semi-private)
- `@property` → clean getter/setter interface

---

## Magic / Dunder Methods

| Method | Purpose |
|--------|---------|
| `__str__` | Human-readable string |
| `__repr__` | Debug representation |
| `__len__` | `len(obj)` |
| `__getitem__` | Indexing / slicing |
| `__setitem__` | Assign to index/key |
| `__iter__`, `__next__` | Iterable support |
| `__eq__`, `__lt__`, `__gt__` | Comparisons |
| `__call__` | Make instance callable |
| `__add__`, `__sub__`, ... | Operator overloading |

Example:

```python
class Vector:
    def __init__(self, x, y): self.x, self.y = x, y
    def __add__(self, other): return Vector(self.x + other.x, self.y + other.y)
    def __repr__(self): return f"Vector({self.x},{self.y})"
```

---

## Composition vs Inheritance

```python
class Engine: ...

class Car:
    def __init__(self):
        self.engine = Engine()  # composition
```

- **Inheritance** → "is-a"
- **Composition** → "has-a" (preferred for flexibility)

---

## Class Patterns / Tricks

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

## Pythonic OOP Idioms

```python
# Duck typing
def quack(duck): duck.quack()  # any object with quack() works

# Mixins
class JsonMixin:
    def to_json(self): return json.dumps(self.__dict__)

class Person(JsonMixin):
    def __init__(self, name): self.name = name
```

- Favor **composition over inheritance**
- Use **mixins** for reusable behavior
- Implement **dunder methods** for Pythonic integration

---

## Cheat Sheet Highlights

- Class/instance/static/class methods → clear separation
- LEGB & encapsulation → control state exposure
- Decorator-friendly design → scalable wrappers
- Magic methods → make classes integrate naturally with Python
- Composition & mixins → flexible, maintainable architectures

---

## See Also

- [[Python]]
- [[Python - Files & Serialization]]
- [[Python - Modules & Packages]]
- [[Python - Concurrency]]
