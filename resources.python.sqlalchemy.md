---
id: 2bkl2tab7oa5l7a9v20lrqe
title: Sqlalchemy
desc: ''
updated: 1753336603298
created: 1753335981853
---
tags: [master, sqlalchemy]

## 📌 Topic Overview

**SQLAlchemy** is:

* A **Python SQL toolkit and Object-Relational Mapping (ORM) library**.
* Designed to provide a full suite of well-known enterprise-level persistence patterns.
* Supports both **high-level ORM** for database interaction using Python classes and **low-level Core** for direct SQL expression construction.
* Offers:
  * **Declarative ORM** for mapping Python classes to database tables.
  * **SQL Expression Language** for building complex SQL queries in a programmatic, composable way.
  * **Connection pooling and transaction management**.
  * Support for multiple databases including PostgreSQL, MySQL, SQLite, Oracle, and MS SQL Server.
* Widely used in Python web frameworks like Flask, FastAPI, and Django (as an alternative ORM).

## 🚀 80/20 Roadmap

| Stage | Concept                                | Reason                                          |
| ----- | ------------------------------------ | ------------------------------------------------|
| 1️⃣   | SQLAlchemy Core Basics                | Understand SQL expressions and engine basics     |
| 2️⃣   | Declarative ORM Setup                 | Mapping Python classes to tables                  |
| 3️⃣   | Querying with ORM                    | Basic CRUD using session and query interface     |
| 4️⃣   | Relationships and Joins               | One-to-many, many-to-many, eager vs lazy loading|
| 5️⃣   | Transactions & Session Management     | Controlling commit, rollback, session lifecycle |
| 6️⃣   | Migrations with Alembic               | Managing schema changes safely                    |
| 7️⃣   | Advanced Query Techniques             | Subqueries, CTEs, window functions                |
| 8️⃣   | Performance Tuning                    | Lazy loading strategies, query optimization      |
| 9️⃣   | Integration with Async frameworks     | Async ORM usage with async DB drivers             |
| 🔟    | Custom Types & Extensibility           | Custom column types, event listeners, hooks      |

---

## 🛠️ Practical Tasks

* ✅ Install SQLAlchemy and set up a basic engine and metadata.
* ✅ Define a simple declarative model with columns and primary keys.
* ✅ Insert, query, update, and delete records using the ORM session.
* ✅ Create one-to-many and many-to-many relationships and query related data.
* ✅ Use filters, ordering, and limit queries with the ORM.
* ✅ Perform joins and eager loading to optimize queries.
* ✅ Handle transactions with session commit and rollback.
* ✅ Write and apply migrations using Alembic.
* ✅ Use raw SQL expressions and SQLAlchemy Core for custom queries.
* ✅ Integrate SQLAlchemy in a FastAPI or Flask app.

---

## 🧾 Cheat Sheets

### 🔹 Engine and Session Setup

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///example.db")
Session = sessionmaker(bind=engine)
session = Session()
````

### 🔹 Declarative Model Example

```python
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
```

### 🔹 Basic CRUD

```python
# Create
new_user = User(name="Ronak", email="ronak@example.com")
session.add(new_user)
session.commit()

# Read
user = session.query(User).filter_by(name="Ronak").first()

# Update
user.email = "ronak_updated@example.com"
session.commit()

# Delete
session.delete(user)
session.commit()
```

### 🔹 Relationships

```python
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    email_address = Column(String)
    user = relationship("User", back_populates="addresses")

User.addresses = relationship("Address", order_by=Address.id, back_populates="user")
```

---

## 🎯 Progressive Challenges

| Level           | Task                                                                  |
| --------------- | --------------------------------------------------------------------- |
| 🥉 Easy         | Define models with simple relationships and perform CRUD operations   |
| 🥈 Intermediate | Write custom queries using SQLAlchemy Core and raw SQL                |
| 🥇 Advanced     | Implement migrations with Alembic and integrate with a web framework  |
| 🏆 Expert       | Optimize complex queries with eager loading and handle async DB calls |

---

## 🎙️ Interview Q\&A

* **Q:** Explain the difference between SQLAlchemy Core and ORM.
* **Q:** How do you manage sessions and transactions in SQLAlchemy?
* **Q:** What is lazy loading vs eager loading? When would you use each?
* **Q:** How does SQLAlchemy handle relationships and foreign keys?
* **Q:** Describe how Alembic manages migrations.
* **Q:** How do you write custom SQL queries with SQLAlchemy?
* **Q:** What are common performance pitfalls when using SQLAlchemy?

---

## 🛣️ Next Tech Stack Recommendations

* **Alembic** — Migration tool for SQLAlchemy
* **FastAPI / Flask** — Web frameworks integrating with SQLAlchemy
* **Databases** — Async DB access library to pair with SQLAlchemy for async support
* **PostgreSQL** — A performant, feature-rich backend commonly used with SQLAlchemy
* **GraphQL (e.g., Ariadne)** — To build flexible APIs on top of SQLAlchemy models

---

## 🧠 Pro Tips

* Use `session.flush()` to push pending changes without committing.
* Avoid long-lived sessions; keep transactions short and sweet.
* Use `joinedload()` and `selectinload()` for eager loading to reduce queries.
* Use parameterized queries to prevent SQL injection.
* Prefer SQLAlchemy Core for complex queries that ORM can’t express cleanly.
* Leverage Alembic’s autogenerate feature but always review migration scripts manually.

---

## 🧬 Tactical Philosophy

> **SQLAlchemy empowers Python developers to write database-agnostic, maintainable, and performant data access layers. It’s both a toolbox and a mindset — blending raw SQL power with Pythonic abstractions to keep your data logic clean, scalable, and future-proof.**

⚙️ Abstract your DB layer but keep access explicit.
🔐 Guard your sessions and transactions carefully.
📈 Profile generated SQL to avoid hidden performance bottlenecks.
💥 Use migrations as part of your CI/CD pipeline, never skip schema versioning.
🤖 Automate repetitive tasks with declarative models and custom types.

---
