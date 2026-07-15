```table-of-contents
```
Great place to start. Understanding monoliths first makes distributed systems, microservices, data platforms, and lakehouses much easier to understand later.

# What is a Monolithic System?

A **monolith** is an application where everything is built, deployed, and run as a single unit.

Imagine an online shopping application:

- User Login
    
- Product Catalog
    
- Cart
    
- Orders
    
- Payments
    
- Notifications
    

In a monolith, all of these live inside **one application**.

```text
+----------------------------------+
|          Ecommerce App           |
|----------------------------------|
| Login                            |
| Products                         |
| Cart                             |
| Orders                           |
| Payments                         |
| Notifications                    |
+----------------------------------+
```

You build it together.  
You deploy it together.  
You scale it together.

Think of it as a **single large building** containing all departments.

---

# Real-World Analogy

Imagine a restaurant.

## Monolith

```text
Restaurant
 ├── Kitchen
 ├── Billing
 ├── Waiters
 ├── Inventory
 └── Cleaning
```

Everything is inside one building.

If the kitchen becomes busy:

You cannot move only the kitchen to a larger building.

You must expand the entire restaurant.

---

# Why Were Monoliths Popular?

Because they are simple.

A small team can:

- Build faster
    
- Deploy faster
    
- Debug easier
    
- Test easier
    

Most successful companies started with monoliths.

Examples include:

- Amazon (early years)
    
- Netflix (early years)
    
- Shopify (initial architecture)
    

Many startups still begin this way.

---

# Typical Monolith Architecture

```text
                User
                  |
                  V
          +---------------+
          | Web Server    |
          +---------------+
                  |
                  V
     +-------------------------+
     |      Application         |
     |-------------------------|
     | Authentication          |
     | Orders                  |
     | Payments                |
     | Inventory               |
     | Reporting               |
     +-------------------------+
                  |
                  V
           +-------------+
           | Database    |
           +-------------+
```

One application.

Often one database.

---

# Components of a Monolith

## 1. UI Layer

Handles:

- Web pages
    
- APIs
    
- User requests
    

Example:

```text
GET /orders/123
```

---

## 2. Business Logic Layer

Contains rules.

Example:

```text
If inventory > 0
    create order
Else
    reject order
```

This is the brain of the application.

---

## 3. Data Layer

Stores information.

```text
Users
Orders
Products
Payments
```

Usually one database.

Example:

```text
PostgreSQL
MySQL
Oracle
```

---

# How a Request Flows

Suppose you order a laptop.

```text
User clicks Buy
       |
       V
Web Server
       |
       V
Order Service Code
       |
       +--> Check Inventory
       |
       +--> Calculate Price
       |
       +--> Process Payment
       |
       +--> Create Order
       V
Database
```

Everything happens inside one process.

No network calls between services.

This is important.

---

# Advantages of Monoliths

## 1. Simpler Development

Developer clones repository.

```bash
git clone app
```

Runs application.

```bash
start-app
```

Done.

No need to start:

- Kafka
    
- Service Mesh
    
- Multiple services
    
- API gateways
    

---

## 2. Easier Debugging

You can follow execution step by step.

```text
Controller
 ↓
Service
 ↓
Database
```

No distributed tracing.

No cross-service debugging.

---

## 3. Better Performance

Method calls happen in memory.

```text
Function A
    calls
Function B
```

This is extremely fast.

Compared to:

```text
Service A
  ->
Network
  ->
Service B
```

which is much slower.

---

## 4. Easier Transactions

Suppose:

```text
Deduct inventory
Create order
Charge payment
```

All can be wrapped inside one database transaction.

```sql
BEGIN;
...
COMMIT;
```

Either everything succeeds or everything fails.

Very simple.

---

# Problems with Monoliths

As systems grow, pain starts appearing.

---

## Problem 1: Huge Codebase

Initially:

```text
10,000 lines
```

Later:

```text
1 million lines
```

Then:

```text
10 million lines
```

Finding things becomes difficult.

---

## Problem 2: Slow Deployments

Small change:

```text
Fix typo in notification
```

But you redeploy:

```text
Entire application
```

Risk increases.

---

## Problem 3: Scaling Issues

Suppose:

```text
Orders = 10%
Search = 90%
```

Search is overloaded.

In a monolith:

```text
Scale everything
```

```text
Instance 1
Instance 2
Instance 3
Instance 4
```

Even if Orders don't need more resources.

Expensive.

---

## Problem 4: Technology Lock-In

Imagine application written in Java.

Now AI team wants Python.

Analytics team wants Rust.

Too bad.

Entire application is tied together.

---

## Problem 5: Team Bottlenecks

When 500 engineers work in one repository:

```text
Merge conflicts
Deployment coordination
Ownership confusion
```

become common.

---

# Monolith Scaling

Many people think monoliths cannot scale.

Not true.

There are two ways.

---

## Vertical Scaling

Buy bigger machine.

```text
8 CPU
  ->
64 CPU
```

```text
32 GB RAM
  ->
512 GB RAM
```

Simple but expensive.

---

## Horizontal Scaling

Run multiple copies.

```text
          Load Balancer
                |
   -----------------------------
   |            |             |
 App1         App2          App3
```

Requests are distributed.

This works surprisingly well.

---

# Types of Monoliths

## 1. Good Monolith

Well-structured.

```text
Orders Module
Payments Module
Users Module
```

Clear boundaries.

Easy maintenance.

---

## 2. Modular Monolith

A very important concept.

```text
Application
 ├── Orders
 ├── Payments
 ├── Inventory
 └── Customers
```

Modules are separated logically.

But deployed together.

Many modern architects prefer this.

---

## 3. Big Ball of Mud

The nightmare.

```text
Orders calls Payments
Payments calls Inventory
Inventory calls Orders
```

Everything depends on everything.

Nobody understands it anymore.

---

# Monolith vs Microservices

|Feature|Monolith|Microservices|
|---|---|---|
|Deployment|Single|Multiple|
|Complexity|Low|High|
|Development Speed|Fast initially|Slower initially|
|Debugging|Easier|Harder|
|Scalability|Coarse-grained|Fine-grained|
|Network Calls|Minimal|Many|
|Operational Overhead|Low|High|
|Team Independence|Lower|Higher|

---

# Monoliths in Data Engineering

You are a data engineer, so think about batch processing.

### Monolithic ETL

```text
Extract
   |
Transform
   |
Load
```

One giant Spark job.

Or one Python application.

```text
nightly_etl.py
```

containing:

```text
20 steps
100 tables
500 transformations
```

This is a monolith.

---

### Problems

When step 19 fails:

```text
Restart entire pipeline
```

Difficult debugging.

Poor reuse.

---

### Modular Alternative

```text
Extract Job
      |
Clean Job
      |
Enrich Job
      |
Aggregate Job
```

Still may be deployed together but logically separated.

---

# Why Senior Engineers Often Prefer a Modular Monolith First

Many organizations prematurely adopt microservices.

They get:

```text
100 services
500 APIs
Thousands of deployments
```

before they need them.

A modular monolith often provides:

- Simpler architecture
    
- Faster development
    
- Lower cloud costs
    
- Easier debugging
    
- Easier testing
    

while preserving clear boundaries.

That's why a common modern progression is:

```text
Monolith
    ↓
Modular Monolith
    ↓
Selective Microservices
    ↓
Distributed Platform
```

instead of jumping directly to microservices.

# Key Mental Model

Think of a monolith as a **single executable containing many business capabilities**.

```text
One Codebase
One Deployment
One Runtime
Often One Database
```

The biggest mistake is assuming monolith means "bad architecture."

A **well-designed modular monolith** can support hundreds of developers and millions of users. The real enemy is not the monolith itself—it's poor boundaries and uncontrolled complexity inside it.

The next natural step after this is understanding:

1. Modular Monoliths in depth
    
2. Why organizations move to microservices
    
3. Distributed systems challenges introduced by microservices
    
4. How data platforms and lakehouses fit into distributed architectures.

This is one of the most misunderstood architecture topics.

Many engineers think the evolution is:

```text
Monolith -> Microservices -> Success
```

In reality, many companies eventually discover:

```text
Monolith
   ↓
Modular Monolith
   ↓
A Few Microservices
   ↓
Only split when necessary
```

A modular monolith tries to get **most of the benefits of microservices without the operational complexity**.

---

# What is a Modular Monolith?

A modular monolith is:

```text
One Application
One Deployment
One Runtime
```

but internally divided into **strict business modules**.

Instead of:

```text
src/
 ├── controllers/
 ├── services/
 ├── repositories/
 └── models/
```

you organize by business domain:

```text
src/
 ├── orders/
 ├── payments/
 ├── inventory/
 └── customers/
```

Each module owns its:

- Logic
    
- Data access
    
- APIs
    
- Rules
    

---

# The House Analogy

## Traditional Monolith

Imagine a house with no rooms.

```text
+----------------------+
|                      |
| Everything mixed     |
| together             |
|                      |
+----------------------+
```

Kitchen inside bedroom.

Bathroom inside living room.

Chaos.

---

## Modular Monolith

Same house.

But now:

```text
+----------------------+
| Living Room          |
+----------------------+
| Kitchen              |
+----------------------+
| Bedroom              |
+----------------------+
| Bathroom             |
+----------------------+
```

Still one building.

But boundaries exist.

---

# Core Principle

A module should be able to answer:

> "Can another module directly touch my internal implementation?"

Answer:

```text
NO
```

Only through public interfaces.

---

# Bad Monolith Structure

```text
OrderService
   |
   +--> InventoryTable
   |
   +--> PaymentTable
   |
   +--> CustomerTable
```

Everything accesses everything.

This creates coupling.

---

# Good Modular Structure

```text
Orders
   |
   +--> Inventory API
   |
   +--> Payment API
```

Orders does not know:

- Inventory tables
    
- Inventory implementation
    
- Inventory business rules
    

Only inventory knows those.

---

# Module Anatomy

A typical module contains:

```text
orders/
 ├── api/
 ├── domain/
 ├── persistence/
 ├── events/
 └── tests/
```

---

## API Layer

What other modules can call.

```python
class OrderAPI:
    create_order()
    cancel_order()
```

Public contract.

---

## Domain Layer

Business rules.

```python
if inventory_available:
    create_order()
```

This is the heart.

---

## Persistence Layer

Database access.

```python
OrderRepository
```

Only this module should access order tables.

---

## Events

Things the module publishes.

```text
OrderCreated
OrderCancelled
OrderCompleted
```

Other modules can subscribe.

---

# Example Ecommerce System

Modules:

```text
Customers
Products
Inventory
Orders
Payments
Shipping
Notifications
```

Still:

```text
One Deployment
```

---

# How Modules Interact

## Option 1: Direct API Calls

```text
Orders
   |
   +--> Inventory.reserve()
```

Simple.

Common.

---

## Option 2: Domain Events

```text
Order Created
        |
        V
Inventory Module
        |
        V
Payment Module
```

Modules communicate through events.

Example:

```text
Orders
   |
   +--> publish(OrderCreated)
```

Inventory listens.

```text
Inventory
   |
   +--> reserve stock
```

---

# Internal Events vs Distributed Events

Important distinction.

Inside modular monolith:

```text
OrderCreated
```

may simply be:

```python
event_bus.publish()
```

inside memory.

No Kafka.

No RabbitMQ.

No network.

Fast and simple.

---

# Data Ownership

This is where many modular monoliths fail.

Every module should own its data.

Example:

```text
Orders
   └── orders table

Inventory
   └── inventory table

Customers
   └── customer table
```

Even though:

```text
One Database
```

ownership still exists.

---

# What NOT To Do

Avoid:

```sql
SELECT *
FROM inventory
```

inside Order module.

Instead:

```python
inventory_api.get_stock()
```

This preserves boundaries.

---

# Dependency Rules

Think of modules as teams.

Allowed:

```text
Orders -> Inventory
Orders -> Payments
```

Not allowed:

```text
Orders -> Inventory -> Orders
```

Circular dependency.

Nightmare.

---

# Dependency Graph

Good:

```text
Customers
    |
Orders
   / \
Inventory Payments
```

Bad:

```text
Orders
  |
Inventory
  |
Payments
  |
Orders
```

Circle.

---

# Layered Architecture Inside Modules

A mature module often contains:

```text
orders
 ├── API
 ├── Application
 ├── Domain
 └── Infrastructure
```

---

## API

Receives request.

```text
CreateOrder
```

---

## Application

Coordinates workflow.

```text
Reserve stock
Charge payment
Create order
```

---

## Domain

Business rules.

```text
Can order be cancelled?
```

---

## Infrastructure

Database.

External APIs.

Message queues.

---

# Why This Matters

Suppose payment provider changes.

Only:

```text
Payments Module
```

changes.

Not:

```text
Orders
Inventory
Customers
```

This reduces blast radius.

---

# Team Ownership

As companies grow:

```text
Team Orders
Team Payments
Team Inventory
```

Each team owns a module.

Still one deployment.

Still one application.

---

# Testing Becomes Easier

Without modules:

```text
Test Order
   |
   -> Entire application
```

With modules:

```text
Test Order Module
```

in isolation.

---

# Performance Benefits

Microservices:

```text
Orders
  |
HTTP
  |
Inventory
```

Network latency.

Serialization.

Retries.

Failures.

---

Modular Monolith:

```text
Orders
   |
Method Call
   |
Inventory
```

Microseconds.

Very fast.

---

# Migration Path to Microservices

This is the hidden superpower.

Suppose:

```text
Orders
Payments
Inventory
```

are already clean modules.

Later:

```text
Payments
```

needs independent scaling.

You can extract only Payments.

Before:

```text
Monolith
```

After:

```text
Orders
Inventory
Customers

inside Monolith

+
Payment Service
```

Minimal disruption.

---

# Example Folder Structure

```text
ecommerce/

├── orders/
│   ├── api/
│   ├── domain/
│   ├── persistence/
│   └── events/
│
├── inventory/
│   ├── api/
│   ├── domain/
│   ├── persistence/
│   └── events/
│
├── payments/
│   ├── api/
│   ├── domain/
│   ├── persistence/
│   └── events/
│
└── shared/
```

Notice:

```text
No giant services folder
No giant models folder
No giant repositories folder
```

Everything belongs to a business capability.

---

# Common Anti-Patterns

## Shared Database Free-for-All

```text
Everybody queries everybody's tables
```

Boundaries disappear.

---

## Shared Utility Monster

```text
shared/
   50,000 files
```

Eventually:

```text
shared = monolith inside monolith
```

---

## God Module

```text
CoreModule
```

Everything depends on it.

Nothing can change.

---

## Circular Dependencies

```text
Orders -> Payments
Payments -> Orders
```

Creates tight coupling.

---

# How This Applies to Data Engineering

Imagine a batch platform.

Bad:

```text
batch_platform/
    200,000 lines
```

Everything mixed.

---

Modular:

```text
scheduler/
metadata/
quality/
execution/
optimization/
lineage/
observability/
```

Each capability becomes a module.

Still:

```text
One Deployment
One Platform
```

but clear ownership.

This is exactly how many modern internal data platforms evolve before parts are split into independent services.

# The Architecture Goal

The goal of a modular monolith is **not** to avoid microservices forever.

The goal is to create:

```text
High Cohesion
Low Coupling
```

Where:

- Things that belong together stay together.
    
- Things that change independently are separated.
    

If you achieve that, you can stay a monolith for years—or extract microservices later with far less pain.

---

# Interview Questions

## Level 1: Fundamentals

**1. What is a monolithic architecture?**

Expected:
- Single codebase, single deployment, single runtime
- One database is common but not required
- All business capabilities in one process

**2. Why do most startups begin with a monolith?**

Expected:
- Simplicity, faster delivery, lower cost
- Easier debugging, fewer operational concerns
- Small team can move fast

**3. What are the primary advantages of a monolith over microservices?**

Expected:
- Simpler deployment, easier testing, strong consistency
- Better performance (in-memory calls vs network)
- Simpler transactions (single DB, ACID)

**4. What are the primary disadvantages of a monolith?**

Expected:
- Tight coupling, deployment risk, scaling limitations
- Technology lock-in, team coordination challenges

**5. Is a monolith inherently bad architecture?**

Expected: No. Poor boundaries are bad architecture. A well-designed modular monolith can support hundreds of developers and millions of users.

---

## Level 2: Design

**6. How would you organize a large monolith?**

Compare:
```text
controllers/
services/
repositories/
```
vs
```text
orders/
payments/
inventory/
```

Organized by business capability, not technical layer.

**7. How would you prevent a monolith from becoming a "Big Ball of Mud"?**

Expected:
- Clear boundaries, domain ownership, dependency rules
- Architecture governance, code review policies

**8. How would you structure code ownership for 200 engineers on a monolith?**

Expected:
- Module ownership, CODEOWNERS, review policies
- Architecture standards per team

**9. What architectural patterns work well inside monoliths?**

Expected:
- Layered Architecture, Hexagonal Architecture
- Clean Architecture, Domain-Driven Design

---

## Level 3: Scaling

**10. Can a monolith scale to millions of users?**

Expected: Yes. Horizontal scaling, caching, read replicas, database optimization.

**11. How would you scale a monolith experiencing 10x traffic growth?**

Expected:
- Load balancing, stateless services, caching, CDN
- Database partitioning, read replicas

**12. One feature causes 90% of system load. What architectural options exist?**

Expected:
```text
Scale entire monolith
Extract service
Caching
Async processing
```

**13. How do you scale only part of a monolith?**

Interesting because you generally can't without architectural changes. Leads to extraction discussion.

---

## Level 4: Reliability & Operations

**14. A monolith deployment fails halfway through. What happens?**

Expected:
- Rollback strategy, database migration safety
- Downtime assessment, recovery plans

**15. How would you deploy a monolith with zero downtime?**

Expected:
- Blue-green deployments, rolling deployments
- Feature flags, backward-compatible schema changes

**16. How would you monitor a large monolith?**

Expected:
- Application metrics, business metrics
- Logs, traces, database telemetry

**17. How do you identify bottlenecks in a monolith?**

Expected:
```text
CPU
Memory
Disk
Database
Network
Locks
```

---

## Level 5: Migration

**18. When should a company leave a monolith?**

Expected: Not because microservices are trendy. Because of independent scaling needs, team autonomy, deployment bottlenecks.

**19. What signs indicate a monolith should remain a monolith?**

Expected: Small teams, stable requirements, low scale, tight coupling.

**20. How would you migrate a monolith to microservices?**

Expected:
```text
Incremental extraction
```
Not:
```text
Rewrite everything
```

**21. Which component would you extract first?**

Expected: Look for low dependencies, high scaling pressure, clear ownership. Not the easiest module—the most justified one.

**22. What is the Strangler Fig Pattern?**

Expected: Gradually replacing parts of the monolith while keeping the system operational.

---

## Level 6: Staff / Principal

**23. A modular monolith has grown to 500 developers. What governance mechanisms do you introduce?**

Expected:
- Architecture review board, module ownership
- Dependency rules, architecture tests, platform standards

**24. How does Conway's Law influence modular monolith design?**

Expected: System structure mirrors team structure. Teams become modules.

**25. How would you implement module boundaries that are enforceable rather than documented?**

Expected:
- Separate packages, compile-time restrictions
- Static analysis, dependency validation, architecture tests

**26. What is the biggest risk of a modular monolith?**

Expected: Boundary erosion. Once boundaries erode, modular monolith becomes big ball of mud.

**27. Can a modular monolith support thousands of requests per second?**

Expected: Absolutely. Shopify, GitHub, many enterprise platforms. The real question is: can it scale organizationally?

---

## Scenario-Based

**28. Your monolith contains 5 million LOC, 400 engineers, 12-hour regression suite. What is your 3-year modernization strategy?**

**29. A monolith handles 100K requests/sec. Latency suddenly doubles. Walk through your investigation.**

**30. Every major feature requires touching 15 different teams. What architectural problems does this suggest?**

**31. Deployment frequency has fallen from 100/day to 1/week. How would you identify root causes?**

**32. If you were CTO of a growing company today, under what circumstances would you intentionally choose a monolith over microservices?**

Expected: Start with a well-structured modular monolith. Only introduce microservices when measurable business, scaling, or organizational pressures justify the added complexity.

---

## Further Reading

- [[Microservice]]
- [[Distributed System]]
- [[Data Lake]]
- [[ETL vs ELT]]
- [[Incremental Load Strategy]]
- [[Batch pipeline design patterns]]
