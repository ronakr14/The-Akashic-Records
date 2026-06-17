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
       |
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

Let's break these down.

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



If you're interviewing for **Senior Data Engineer, Staff Engineer, Platform Engineer, Principal Architect, or Distributed Systems roles**, interviewers rarely ask "What is a modular monolith?" directly.

Instead, they test whether you understand:

- Architecture tradeoffs
    
- Domain boundaries
    
- Data ownership
    
- Team scaling
    
- Evolution to microservices
    
- Operational complexity
    
- Failure modes
    

Here are increasingly difficult questions.

# Level 1: Fundamentals

### 1. What problem does a modular monolith solve?

Expected discussion:

- Monolith simplicity
    
- Better separation of concerns
    
- Reduced coupling
    
- Easier migration path to services
    

---

### 2. How is a modular monolith different from a traditional layered monolith?

Expected:

Traditional:

```text
Controllers
Services
Repositories
```

Modular:

```text
Orders
Payments
Inventory
```

Organized by business capability.

---

### 3. What are the characteristics of a well-designed module?

Expected:

- High cohesion
    
- Low coupling
    
- Clear ownership
    
- Explicit interfaces
    
- Hidden implementation
    

---

### 4. Why is a modular monolith often preferred over microservices for startups?

Expected:

- Lower operational complexity
    
- Faster development
    
- Easier debugging
    
- Lower cloud cost
    
- Simpler deployment
    

---

# Level 2: Design Questions

### 5. Design a modular monolith for an e-commerce platform.

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

Discussion:

- Interfaces
    
- Dependencies
    
- Events
    
- Data ownership
    

---

### 6. How would modules communicate?

Compare:

```text
Direct API Calls
```

vs

```text
Domain Events
```

Tradeoffs:

- Simplicity
    
- Coupling
    
- Consistency
    
- Observability
    

---

### 7. Should modules share a database?

Trick question.

Good answer:

```text
Physical database: Yes
Logical ownership: Mandatory
```

Each module owns its schema/tables.

---

### 8. How would you prevent one module from directly querying another module's tables?

Expected:

- Repository isolation
    
- Internal APIs
    
- Architecture tests
    
- Code review policies
    

---

### 9. What rules would you enforce for module dependencies?

Expected:

- No circular dependencies
    
- Public interfaces only
    
- Dependency direction rules
    
- Explicit contracts
    

---

# Level 3: Real Engineering Challenges

### 10. Orders needs customer information. How should it access it?

Bad:

```sql
SELECT * FROM customers
```

Good:

```text
Customer API
```

or

```text
CustomerReadModel
```

Discussion around coupling.

---

### 11. How would you detect architectural erosion in a modular monolith?

Expected signals:

- Growing shared libraries
    
- Cross-module database access
    
- Circular dependencies
    
- Large God modules
    
- Increasing change coupling
    

---

### 12. What metrics would you collect to measure module health?

Potential answers:

- Dependency count
    
- Change frequency
    
- Bug rate
    
- Test coverage
    
- Ownership clarity
    
- Build impact
    

---

### 13. How would you identify modules that should become microservices?

Expected:

- Independent scaling needs
    
- Different SLAs
    
- Separate deployment cadence
    
- Team ownership
    
- Resource isolation
    

---

### 14. What modules should never become microservices?

Interesting discussion.

Expected:

- Tiny utility modules
    
- Highly coupled domains
    
- Low-change components
    

---

# Level 4: Evolution Questions

### 15. You inherit a 3-million-line monolith. How do you convert it into a modular monolith?

Look for:

```text
Domain identification
Boundary discovery
Dependency mapping
Incremental extraction
```

Not:

```text
Rewrite everything
```

---

### 16. How would you discover module boundaries?

Expected:

- Domain-Driven Design
    
- Event storming
    
- Dependency analysis
    
- Team ownership analysis
    
- Data ownership analysis
    

---

### 17. What are signs your modules are incorrectly defined?

Expected:

- Constant cross-module changes
    
- Frequent circular dependencies
    
- Shared database joins everywhere
    
- Large shared utility package
    

---

### 18. When does a modular monolith stop being modular?

Interesting answer:

When:

```text
Every module depends on every other module
```

or

```text
Shared package becomes central dependency
```

---

# Level 5: Data Engineering Specific

### 19. Design a modular monolith for a batch processing platform.

Possible modules:

```text
Scheduler
Execution Engine
Metadata
Lineage
Data Quality
Observability
Optimization Engine
Cost Management
```

Discussion:

- Ownership
    
- Interfaces
    
- Event flows
    

---

### 20. How would metadata flow through modules?

Expected:

```text
Execution
     |
     v
Metadata
     |
     v
Lineage
     |
     v
Optimization
```

Without tight coupling.

---

### 21. You are building an AI lakehouse optimization platform. Would you choose microservices or modular monolith first?

Strong answer:

Modular monolith first.

Reasoning:

- Fast iteration
    
- Shared metadata model
    
- Easier experimentation
    
- Lower operational burden
    

Split later if required.

---

### 22. How would you isolate the optimization engine from execution engine?

Expected:

```text
Execution publishes events

JobCompleted
QueryExecuted
PlanCaptured
```

Optimization subscribes.

Loose coupling.

---

# Level 6: Staff / Principal Level

### 23. A modular monolith has grown to 500 developers. What governance mechanisms do you introduce?

Expected:

- Architecture review board
    
- Module ownership
    
- Dependency rules
    
- Architecture tests
    
- Platform standards
    

---

### 24. How do Conway's Law influence modular monolith design?

Expected:

System structure mirrors team structure.

```text
Orders Team
Payments Team
Inventory Team
```

becomes:

```text
Orders Module
Payments Module
Inventory Module
```

---

### 25. How would you implement module boundaries that are enforceable rather than documented?

Expected:

- Separate packages
    
- Compile-time restrictions
    
- Static analysis
    
- Dependency validation
    
- Architecture tests
    

---

### 26. What is the biggest risk of a modular monolith?

Many candidates answer:

```text
Scaling
```

Better answer:

```text
Boundary erosion
```

Once boundaries erode:

```text
Modular Monolith
      ↓
Big Ball of Mud
```

---

### 27. Can a modular monolith support thousands of requests per second?

Answer:

Absolutely.

Examples include systems at companies like Shopify, GitHub, and many internal enterprise platforms that handled massive scale before introducing extensive service decomposition.

The real question is:

```text
Can it scale organizationally?
```

not

```text
Can it scale technically?
```

---

# Principal Architect Challenge

A favorite architecture interview question:

> Your company has a modular monolith with:
> 
> - 50 modules
>     
> - 200 engineers
>     
> - 1 deployment
>     
> - 1 database
>     
> 
> Deployment time is now 3 hours.
> 
> Teams want microservices.
> 
> How would you decide what to extract first?

A strong answer covers:

1. Dependency graph analysis
    
2. Change frequency analysis
    
3. Resource consumption analysis
    
4. Team ownership
    
5. SLA requirements
    
6. Operational cost
    
7. Business criticality
    

And concludes:

> "I would not start by extracting the easiest module. I would start by extracting the module with the strongest business justification and the weakest dependencies."

That's the kind of answer interviewers expect at Staff and Principal levels.


When interviewing senior engineers, monolith questions are rarely about definitions. They're designed to test whether you understand:

- Architecture tradeoffs
    
- Scalability limits
    
- Organizational scaling
    
- Operational complexity
    
- Evolutionary architecture
    
- Why companies leave or keep monoliths
    

The strongest candidates can argue both **for** and **against** monoliths.

---

# Level 1: Fundamentals

### 1. What is a monolithic architecture?

Follow-up:

- What makes something a monolith?
    
- Is one database enough to call something a monolith?
    
- Is one deployment enough?
    

---

### 2. Why do most startups begin with a monolith?

Expected discussion:

- Simplicity
    
- Faster delivery
    
- Lower cost
    
- Easier debugging
    
- Fewer operational concerns
    

---

### 3. What are the primary advantages of a monolith over microservices?

Expected:

- Simpler deployment
    
- Easier testing
    
- Strong consistency
    
- Better performance
    
- Simpler transactions
    

---

### 4. What are the primary disadvantages of a monolith?

Expected:

- Tight coupling
    
- Deployment risk
    
- Scaling limitations
    
- Team coordination challenges
    

---

### 5. Is a monolith inherently bad architecture?

Trick question.

Strong answer:

> No. Poor boundaries are bad architecture. A monolith can be well designed.

---

# Level 2: Architecture Design

### 6. Design a monolithic e-commerce platform.

Components:

```text
Users
Products
Orders
Payments
Inventory
Shipping
```

Questions:

- Structure?
    
- Layers?
    
- Database design?
    
- Deployment strategy?
    

---

### 7. How would you organize a large monolith?

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

Discuss maintainability.

---

### 8. How would you prevent a monolith from becoming a "Big Ball of Mud"?

Expected:

- Clear boundaries
    
- Domain ownership
    
- Dependency rules
    
- Architecture governance
    

---

### 9. How would you structure code ownership for a 200-person engineering organization working on a monolith?

Expected:

- Module ownership
    
- Code ownership rules
    
- Review policies
    
- Architecture standards
    

---

### 10. What architectural patterns work well inside monoliths?

Examples:

- Layered Architecture
    
- Hexagonal Architecture
    
- Clean Architecture
    
- Domain Driven Design
    

---

# Level 3: Scaling Questions

### 11. Can a monolith scale to millions of users?

Many candidates incorrectly answer:

```text
No
```

Strong answer:

```text
Yes
```

Discussion:

- Horizontal scaling
    
- Caching
    
- Database optimization
    
- Read replicas
    

---

### 12. How would you scale a monolith experiencing 10x traffic growth?

Explore:

- Load balancing
    
- Stateless services
    
- Caching
    
- CDN
    
- Database partitioning
    

---

### 13. A monolith consumes 95% CPU. What would you investigate?

Expected:

- Query bottlenecks
    
- Thread contention
    
- Locking
    
- Memory pressure
    
- Hot endpoints
    

---

### 14. One feature causes 90% of system load. What architectural options exist?

Expected:

```text
Scale entire monolith
Extract service
Caching
Async processing
```

Tradeoff discussion.

---

### 15. How do you scale only part of a monolith?

Interesting discussion because:

```text
You generally can't
```

without architectural changes.

---

# Level 4: Reliability & Operations

### 16. A monolith deployment fails halfway through. What happens?

Discuss:

- Rollbacks
    
- Database migrations
    
- Downtime
    
- Recovery plans
    

---

### 17. How would you deploy a monolith with zero downtime?

Expected:

- Blue-green deployments
    
- Rolling deployments
    
- Feature flags
    
- Backward-compatible schema changes
    

---

### 18. How would you monitor a large monolith?

Expected:

- Application metrics
    
- Business metrics
    
- Logs
    
- Traces
    
- Database telemetry
    

---

### 19. How do you identify bottlenecks in a monolith?

Areas:

```text
CPU
Memory
Disk
Database
Network
Locks
```

---

### 20. What happens when a monolith starts taking 3 hours to build?

Expected:

- Build decomposition
    
- Incremental builds
    
- Test optimization
    
- Modularization
    

---

# Level 5: Database & Data Engineering

### 21. Why are transactions easier in a monolith?

Expected:

Single process

Single database

Simple ACID transactions.

---

### 22. What happens when a monolith's database becomes the bottleneck?

Discuss:

- Indexing
    
- Partitioning
    
- Read replicas
    
- Sharding
    
- Caching
    

---

### 23. How would you migrate a 50 TB database supporting a monolith?

Expected:

- Dual writes
    
- CDC
    
- Incremental migration
    
- Validation strategies
    

---

### 24. Your monolith executes a query reading 10 TB to return 100 rows. How would you investigate?

Expected:

- Query plans
    
- Missing indexes
    
- Partition pruning
    
- Predicate pushdown
    
- Statistics
    

---

### 25. What telemetry would you collect from a monolith to predict future scaling problems?

Examples:

- Request latency
    
- Queue depth
    
- CPU
    
- Memory
    
- DB load
    
- Growth rates
    

---

# Level 6: Migration Questions

### 26. When should a company leave a monolith?

Strong answer:

Not because:

```text
Microservices are trendy
```

But because of:

- Independent scaling needs
    
- Team autonomy requirements
    
- Deployment bottlenecks
    
- Operational constraints
    

---

### 27. What signs indicate a monolith should remain a monolith?

Expected:

- Small teams
    
- Stable requirements
    
- Low scale
    
- Tight coupling
    

---

### 28. How would you migrate a monolith to microservices?

Look for:

```text
Incremental extraction
```

Not:

```text
Rewrite everything
```

---

### 29. Which component would you extract first?

Strong answers consider:

- Dependency graph
    
- Business value
    
- Scaling pressure
    
- Team ownership
    

---

### 30. What is the Strangler Fig Pattern?

Expected:

Gradually replacing parts of the monolith while keeping the system operational.

---

# Level 7: Staff / Principal Engineer

### 31. Your monolith supports:

```text
500 developers
20 million users
500 deployments/day
```

Would you keep it?

Expected:

Depends.

Evaluate:

- Organizational bottlenecks
    
- Deployment bottlenecks
    
- Coupling
    
- Cost
    

---

### 32. A company wants microservices because competitors use them. How would you evaluate the proposal?

Look for:

- Business drivers
    
- Cost analysis
    
- Complexity analysis
    
- Organizational readiness
    

---

### 33. What is the biggest scaling challenge of a monolith?

Many candidates say:

```text
Traffic
```

Stronger answer:

```text
Team scaling
```

Technology usually scales further than organizations.

---

### 34. What is the biggest misconception about monoliths?

Good answers:

- Monolith ≠ bad design
    
- Monolith ≠ unscalable
    
- Microservices ≠ automatically better
    

---

### 35. Explain Conway's Law in the context of monoliths.

Expected:

System structure reflects communication structure.

If teams are poorly organized:

```text
Architecture becomes poorly organized
```

---

# Scenario-Based Questions (Most Difficult)

### 36. Your monolith contains:

```text
5 million LOC
400 engineers
1 deployment
1 database
12-hour regression suite
```

What is your 3-year modernization strategy?

---

### 37. A monolith handles:

```text
100K requests/sec
```

Latency suddenly doubles.

Walk through your investigation process.

---

### 38. You discover that every major feature requires touching 15 different teams.

What architectural problems does this suggest?

---

### 39. Your monolith's deployment frequency has fallen from:

```text
100/day
```

to

```text
1/week
```

How would you identify root causes?

---

### 40. If you were CTO of a growing company today, under what circumstances would you intentionally choose a monolith over microservices?

This is arguably the most important monolith interview question because it reveals whether the candidate understands architecture as a tradeoff rather than a trend.

A strong answer recognizes that many modern systems should start as a **well-structured modular monolith**, and only introduce microservices when measurable business, scaling, or organizational pressures justify the added complexity.