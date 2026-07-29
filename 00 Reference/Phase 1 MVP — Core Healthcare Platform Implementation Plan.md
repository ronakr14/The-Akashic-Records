
# Phase 1 — Trimmed Scope

## What changed vs `1. Core Healthcare Platform.md`


| Item | Original | Trimmed | Defer to |
|---|---|---|---|
| Auth | JWT + RBAC matrix | Simple JWT, no roles | Phase 1.5 |
| Docker | Compose, networks, volumes | Local venv + local Postgres | Phase 1.5 |
| Seed | "Realistic" | 50 patients / 10 doctors / 20+ appts | Phase 1.5 (expand) |
| Tests | Unit + Integration + API | Unit + API smoke | Phase 1.5 |
| Logging | Observability framework | Stdlib `logging` + JSON formatter | Phase 1.5 |
| JSON columns | Yes | No (plain relational) | Phase 2 if needed |
| Query plans | Analysis + tuning | Just `EXPLAIN` for sanity | Phase 2/3 |

**Time estimate**: 50-60 hrs (~2 weeks @ 4-5 hr/day)

---

## Core entities (10)

Minimum set to feed Phase 2+ ETL and analytics:

1. `Patient`
2. `Doctor`
3. `Department`
4. `Appointment`
5. `Encounter` (consultation event)
6. `LabOrder` + `LabResult`
7. `Prescription` + `PrescriptionItem`
8. `Medication`
9. `Admission` + `BedAssignment`
10. `Invoice` + `Claim`

**Defer**: Nurse, Caregiver, ICU specifics, Workforce, Documents, Communication, full Emergency dept. Keep `EmergencyVisit` as a stub enum on `Encounter` for now.

---

## Tech stack

- Python 3.11+
- FastAPI
- SQLAlchemy 2.0 (sync first; async only if needed)
- Alembic
- Pydantic v2
- PostgreSQL 15 (local install)
- pytest + httpx

---

## Folder structure

```text
healthcare-platform/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── db.py
│   ├── core/
│   │   └── security.py
│   ├── models/          # SQLAlchemy
│   ├── schemas/         # Pydantic
│   ├── repositories/
│   ├── services/
│   └── api/
│       └── v1/
│           ├── auth.py
│           ├── patients.py
│           ├── doctors.py
│           └── ...
├── alembic/
├── scripts/
│   └── seed.py
├── tests/
│   ├── unit/
│   └── api/
├── pyproject.toml
└── .env.example
```

---

## Implementation order (8 steps)

1. **Domain model** — 4 hrs
   ER diagram for 10 entities. Cardinality, FK strategy, soft-delete vs hard-delete decision.

2. **Schema + migrations** — 6 hrs
   SQLAlchemy models, Alembic init, first migration. Constraints: `NOT NULL`, `UNIQUE`, `CHECK`, FK `ON DELETE`.

3. **Pydantic schemas** — 4 hrs
   Create / Read / Update per entity. Nested where needed (e.g. `Prescription` → items).

4. **Repository layer** — 8 hrs
   Generic CRUD base + per-entity extensions. Pagination, filtering, sorting helpers.

5. **Service layer** — 6 hrs
   Business logic. Example: `book_appointment` checks doctor availability + patient collision.

6. **API routes** — 8 hrs
   REST endpoints per entity. OpenAPI auto-generated. Consistent error envelope.

7. **Auth (basic)** — 4 hrs
   `POST /auth/login` → JWT. `get_current_user` dependency. **No role checks yet.**

8. **Seed + tests** — 8 hrs
   Faker-based seed. Unit tests on services (>70% coverage target). API smoke tests on every route.

**Buffer**: 10 hrs for refactor, bugs, docs.

---

## API surface

```text
POST   /api/v1/auth/login
GET    /api/v1/patients
POST   /api/v1/patients
GET    /api/v1/patients/{id}
PATCH  /api/v1/patients/{id}
DELETE /api/v1/patients/{id}
```

Mirror the same 5-endpoint pattern for: `doctors`, `departments`, `appointments`, `encounters`, `lab_orders`, `prescriptions`, `medications`, `admissions`, `invoices`, `claims`.

---

## Deferred to Phase 1.5

- Docker + docker-compose
- RBAC role matrix (use table from `Business Doc.md`)
- Structured logging (JSON, correlation IDs)
- Integration tests (testcontainers)
- OpenTelemetry traces
- Rate limiting
- Refresh tokens / password reset

---

## Done criteria

- [ ] All 10 entities modeled + migrated
- [ ] CRUD works for every entity
- [ ] `POST /auth/login` returns JWT
- [ ] Seed produces: 50 patients, 10 doctors, 5 departments, 20+ appointments, 30+ lab orders, 25+ prescriptions, 15+ admissions, 40+ invoices
- [ ] pytest passes, >70% coverage on `services/`
- [ ] `uvicorn app.main:app` starts cleanly
- [ ] `/docs` shows full OpenAPI
- [ ] End-to-end flow: register patient → book appointment → consultation → lab order → result → prescription → invoice

---

## Phasing

- **Phase 1** (this file) — Backend MVP, 2 weeks
- **Phase 1.5** — Docker + RBAC + observability, 1 week
- **Phase 2** — Batch ETL (Bronze → Silver → Gold) on Phase 1 data
- **Phase 3+** — per `00 Proposal.md`


```yaml
id: 8n4k2p

title: Phase 1 MVP — Core Healthcare Platform Implementation Plan

folder: Projects/Healthcare-Data-AI-Platform/Phase-01-Core-Healthcare-Platform

categorical:
  domain:
    value: software-engineering
    reason: Focuses on implementing the backend application architecture, APIs, database, authentication, and testing.

  subdomain: backend-mvp

  note_type:
    value: project
    reason: Defines the execution plan, milestones, scope, deliverables, and acceptance criteria for a project phase.

  source_type:
    value: self
    reason: Self-authored implementation roadmap.

  status:
    value: curated
    reason: Mature planning document with clear scope, sequencing, and measurable completion criteria.

  level:
    value: advanced
    reason: Requires understanding of backend architecture, relational database design, authentication, migrations, testing, and API development.

ratings:
  confidence:
    score: 5
    reason: Self-authored project plan with no external factual claims.

  completeness:
    score: 5
    reason: Includes scope changes, architecture, implementation order, technology stack, API design, deliverables, deferred work, timeline, and done criteria.

  complexity:
    score: 4
    reason: Covers several backend engineering disciplines while remaining focused on a single application layer.

  importance:
    score: 5
    reason: Produces the operational system that powers every downstream Data Engineering, ML, and AI phase.

  career_relevance:
    score: 5
    reason: Demonstrates production backend engineering, architecture, API design, database modeling, testing, and security skills.

  freshness:
    score: 5
    reason: Uses current ecosystem technologies including FastAPI, SQLAlchemy 2.x, Pydantic v2, Alembic, PostgreSQL 15, and pytest.

  reusability:
    score: 5
    reason: The implementation plan and architecture can be reused as a blueprint for future backend services.

  review_priority:
    score: 4
    reason: Active implementation document that should be updated throughout development.

  connectedness:
    score: 5
    reason: Central hub connecting domain models, ADRs, APIs, repositories, services, database schema, authentication, testing, and later ETL phases.

  actionability:
    score: 5
    reason: Provides sequential implementation steps, estimated effort, API surface, acceptance criteria, and phased roadmap.

  quality_score:
    score: 98
    reason: Exceptionally well-scoped implementation plan with realistic sequencing, explicit non-goals, measurable deliverables, and clear project boundaries.

custom:
  tags:
    - healthcare
    - backend
    - fastapi
    - postgresql
    - mvp

ai_summary: >
  Defines the Minimum Viable Product implementation plan for Phase 1 of the Intelligent Healthcare Data & AI Platform. The document narrows the original scope to a two-week backend implementation covering ten core healthcare entities, PostgreSQL schema design, FastAPI REST APIs, repository and service layers, JWT authentication, Alembic migrations, Faker-based seed data, and automated testing. It specifies implementation order, project structure, API endpoints, deferred features, acceptance criteria, and the transition path to later phases including ETL, analytics, and AI.
```

### Classification rationale

|Field|Choice|Why|
|---|---|---|
|**Domain**|`software-engineering`|This note is about implementing a production backend, not data pipelines.|
|**Note Type**|`project`|It's an execution plan with milestones, timeline, deliverables, and acceptance criteria.|
|**Status**|`curated`|This is a stable planning artifact that should evolve slowly during implementation.|
|**Subdomain**|`backend-mvp`|Precisely captures the focus: building the minimum viable backend platform.|
|**Folder**|`Projects/Healthcare-Data-AI-Platform/Phase-01-Core-Healthcare-Platform`|Fits naturally as the implementation guide for Phase 1 under the parent project.|

This is exactly the kind of note I'd make the **primary implementation document** for Phase 1, while keeping the broader "Core Healthcare Platform" note as the high-level overview. The high-level note answers **what** and **why**; this trimmed MVP note answers **how**, **when**, and **what constitutes done**.