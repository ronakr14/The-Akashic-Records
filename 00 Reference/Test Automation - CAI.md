```table-of-contents
```

I need to create a test automation framework for my client.
Goal : understand requriements -> create testdata/ testsql -> run script -> report in html format

Techstack: databricks, SQL, excel, txt file, python notebook/scripts

Phase 1:
1. convert excel requirements to markdown file using caveman mode.
2. Extract scope, assumptions, requirement, process stages, BDD scenarios, DDL
3. This will only happen onetime, so I can use claude code for conversion.
4. For future, it will be HITL everytime, unless we get complete new requirement.
5. I am ready to remove striked out part from the excel before sharing.
6. Excel is not structures, it is just detailed instructions.

Phase 2:
1. Based on markdown file extracted from phase 1, use claude code to generate testcases, test sql, test data.
2. testcases should cover happy path, edge cases, negative scenarios. Each testcase should provide testID, testcase, test description, acceptance criteria, generic sql
3. test sql should only use DDL provided in markdown. I do not want anything extra.
4. testdata should cover all testcases.
5. All this we can store in sqlite.md file with proper metadata. We will do HITL scenario to get feedback if sql, testdata is correct or not, and if not then why its not.

phase 3:
1. a python notebook which prepares test environment by performing following steps.
	1. create test env by taking backups and truncating original table.
	2. ingest test data
	3. run the original process script
	4. run test sql and then capture all test details, sql, result and status in html report.
	5. once all testcases done, then reload the original table using backup table.

Before starting, grill me if I am clear about my requirement, do not assume anything

Good—this is a solid skeleton, but right now it’s still “idea-shaped,” not “execution-shaped.” If you tried to build it today, you’d hit ambiguity walls within a day. Let’s tighten it.

I’m going to push on the weak joints. Answer these properly and your framework will practically design itself.

---

## 1. Input Reality Check (Excel → Markdown)

You’re calling Excel “unstructured,” which is fine—but then you’re expecting structured outputs like BDD, DDL, scope, etc.

So the real question:

- What _patterns_ actually exist in that Excel?
    
    - Are there repeated sections like:
        
        - “Step 1: do X”
            
        - “Table: ABC”
            
        - “Logic: If X then Y”
            
    - Or is it pure chaos?
        

If it’s chaos, LLM extraction will be inconsistent.

👉 I want you to clarify:

- What % of rows follow a repeatable pattern?
    
- Do you have **any anchor signals** (keywords like “table”, “column”, “rule”)?
    

If not, your Phase 1 becomes fragile and expensive HITL forever.

---

## 2. DDL Source of Truth (this is critical)

You said:

> test SQL should only use DDL provided in markdown

That’s a constraint—but also a risk.

- Where is DDL coming from?
    
    - Extracted from Excel?
        
    - Pulled from Databricks catalog?
        
    - Manually curated?
        

Because:

- If DDL is incomplete → test SQL breaks
    
- If DDL is wrong → your whole framework lies confidently
    

👉 Decide this clearly:

- Is DDL **authoritative** or **best-effort extraction**?
    

If it's best-effort, you need:

- validation layer
    
- or fallback to actual schema introspection (Databricks)
    

---

## 3. What exactly is a “test SQL”?

Right now it’s vague.

Are you expecting:

### Option A — Assertion style

```sql
SELECT COUNT(*) = 0 FROM table WHERE condition
```

### Option B — Data diff style

```sql
SELECT * FROM actual
EXCEPT
SELECT * FROM expected
```

### Option C — Metric validation

```sql
SELECT SUM(col) = expected_sum
```

These are **very different execution models**.

👉 Pick one primary pattern, or define:

- allowed SQL templates
    
- expected output shape (boolean / rowset / metric)
    

Otherwise your reporting layer will become messy.

---

## 4. Test Data Strategy (this will bite you later)

You said:

> testdata should cover all testcases

That’s not trivial.

Questions:

- Are you generating:
    
    - minimal synthetic data?
        
    - or realistic production-like data?
        
- Do testcases:
    
    - share datasets?
        
    - or each testcase has isolated dataset?
        
- How do you avoid:
    
    - data collision across tests?
        
    - dependency between tests?
        

👉 Decide:

- **Test isolation model**
    
    - per-test dataset (clean, slower)
        
    - shared dataset (fast, risky)
        

---

## 5. Environment Handling (Databricks specifics)

You said:

> truncate original table → run → restore backup

This is dangerous in real environments.

Questions:

- Are you running on:
    
    - dev workspace?
        
    - shared QA?
        
    - production clone?
        
- What if:
    
    - process fails mid-run?
        
    - restore fails?
        
    - someone else is using tables?
        

👉 Better approach might be:

- clone tables (if Delta)
    
- or use temp schema / namespace
    

So:

- Why not:
    
    - `schema_test_run_123` instead of touching originals?
        

I’d challenge your current approach here.

---

## 6. Process Script Execution

You said:

> run the original process script

What form is this?

- Databricks notebook?
    
- SQL job?
    
- Python pipeline?
    

And:

- How do you parameterize it for test data?
    
- Does it support:
    
    - input table override?
        
    - schema override?
        

👉 If not, you’ll need:

- wrapper layer
    
- or monkey patching (which gets ugly)
    

---

## 7. HTML Report — what does “good” mean?

Don’t say “HTML report” casually. Define it.

Do you want:

- Per test:
    
    - SQL executed
        
    - Result preview
        
    - Pass/Fail
        
    - Execution time
        
- Aggregation:
    
    - pass %
        
    - failed test summary
        
    - grouping by requirement?
        
- Debuggability:
    
    - failed row samples?
        
    - diff visualization?
        

👉 Also:

- static HTML?
    
- or interactive (JS, filtering)?
    

---

## 8. Metadata Design (sqlite.md idea)

This is interesting but unclear.

You said:

> store in sqlite.md with metadata

Questions:

- Why `.md` and not:
    
    - SQLite DB
        
    - JSON/YAML
        
- What metadata?
    
    - version?
        
    - requirement mapping?
        
    - lineage (which test came from which requirement)?
        

👉 If this becomes central, design it like a **contract**, not a scratchpad.

---

## 9. HITL Workflow (this is underspecified)

You said:

> HITL for validation

But:

- Where does HITL happen?
    
    - after markdown extraction?
        
    - after test generation?
        
    - after execution?
        
- How do you capture feedback?
    
    - inline edits?
        
    - comments?
        
    - structured corrections?
        

👉 Without structure, you’ll lose feedback signal over time.

---

## 10. Success Criteria (big one)

How do you know this framework is “working”?

Not philosophically—operationally.

- % automation vs manual effort?
    
- accuracy of generated SQL?
    
- reduction in testing time?
    

👉 Define 2–3 hard metrics.

---

## Where I think you're slightly off

Two pushbacks:

1. **Over-reliance on LLM for structure extraction**
    
    - If input is messy, you’ll spend more time correcting than benefiting.
        
    - Consider light preprocessing rules before LLM.
        
2. **Touching original tables**
    
    - That’s risky and unnecessary in modern data stacks.
        
    - Isolation via schema or clone is cleaner.
        

---

## What I need from you next

Answer these in order (don’t skip):

1. What does your Excel actually look like? (describe a real example)
    
2. Where does DDL come from?
    
3. What is your test SQL pattern?
    
4. Do you want isolated or shared test data?
    
5. What form is the “process script”?
    
6. What must be visible in the HTML report?
    

Once you answer these, I can help you:

- lock architecture
    
- define file formats
    
- design prompts for Claude
    
- sketch Python notebook structure
    

Right now you’re 70% there conceptually—but the missing 30% is exactly where projects fail.

step 1: excel contains clear rule, columns, and table. It;s not pure chaos.
step 2: DDL will be from excel and manually curated.
step 3: testsql should be assertion style
step 4: I will like realistic production data, we will do shared dataset
step 5: I am running on shared QA. If process fails, it should reload data from backupd tables. No one will use tables used in testing. I cannot use other tables instead of originals, since I cannot modify original process scripts.
step 6: original script is databricks notebook. I can provide path.
step 7: static html reports, for initial implementation we will only record sql, result, status, test case detail.
step 8: we can sqlite db, this is to ensure user can review testsql, testcases and versioning, lineage.
step 9: HITL after all stages mentioned by you. capture structured corrections
step 10: accuracy of sql generation, reduction in testing time.


Good, this is much tighter. Now we can move from “idea” to something you can actually implement without surprises.

I’m going to do three things:

1. Pressure-test a couple of your decisions (briefly)
    
2. Lock a concrete architecture (files + flow)
    
3. Give you a practical execution blueprint (what to build first)
    

---

## Quick pushback (just two things)

### 1. “Shared dataset + realistic data”

This is efficient, but you’re implicitly accepting:

- hidden coupling between test cases
    
- debugging complexity when one test pollutes another
    

You can still do it, but you _must_ introduce:

- **test tagging in data** (e.g. `test_run_id`, `test_case_id`)
    
- or **deterministic dataset slices per test**
    

Otherwise, when something fails, you’ll be reverse-engineering state instead of testing.

---

### 2. “Backup → truncate → restore original tables”

Given you **can’t change the Databricks notebook**, this constraint is real. Fine.

But then your framework’s reliability depends on one thing:

> restore must be bulletproof even on partial failure

So you need:

- idempotent restore
    
- fail-safe checkpoints
    
- “always restore on exception” guard
    

Treat restore as a **first-class feature**, not a cleanup step.

---

## Locked Architecture (practical, not theoretical)

### Phase 1 Output (Markdown contract)

Your markdown needs to be **structured enough for machines**, not pretty for humans.

Think like this:

```markdown
# METADATA
- requirement_id: R001
- source: excel_v1

# TABLES
## table_name: customer
- column: id INT
- column: status STRING
- column: created_at TIMESTAMP

# RULES
## rule_id: RULE_01
If status = 'active' then created_at should not be null

# PROCESS_STAGES
1. ingest customer
2. filter active users

# BDD
Scenario: Active customer must have created_at
Given status = 'active'
When processed
Then created_at is not null

# ASSUMPTIONS
- status values are clean
```

👉 Key point:  
You’re not generating “documentation”—you’re generating a **machine-readable spec disguised as markdown**.

---

### Phase 2 Output (SQLite schema)

You made a good call moving to SQLite. Now make it structured:

#### Tables:

**1. test_cases**

- test_id
    
- requirement_id
    
- description
    
- type (happy / edge / negative)
    
- acceptance_criteria
    

**2. test_sql**

- test_id (FK)
    
- sql_query
    
- expected_result (boolean / count / etc.)
    

**3. test_data**

- test_id (nullable since shared dataset)
    
- table_name
    
- insert_sql OR data_blob
    

**4. lineage**

- test_id
    
- rule_id
    
- source_section
    

---

### Assertion SQL Pattern (standardize this hard)

You said assertion style—good. Lock it like this:

```sql
SELECT 
  CASE 
    WHEN COUNT(*) = 0 THEN TRUE 
    ELSE FALSE 
  END AS test_pass
FROM customer
WHERE status = 'active'
AND created_at IS NULL
```

👉 Contract:

- ALWAYS returns 1 row
    
- ALWAYS returns boolean column: `test_pass`
    

No exceptions. This makes reporting trivial.

---

## Phase 3 Notebook Design (Databricks)

This is your execution engine. Keep it deterministic.

---

### Step 0: Run Context

Generate:

- `test_run_id`
    
- timestamp
    
- log path
    

---

### Step 1: Backup

For each table:

```sql
CREATE TABLE backup_<table>_<run_id> AS SELECT * FROM <table>
```

Store mapping in memory (or temp table)

---

### Step 2: Truncate

```sql
TRUNCATE TABLE <table>
```

---

### Step 3: Load Test Data

- Load shared dataset
    
- Optionally tag rows:
    

```sql
INSERT INTO customer
SELECT *, '<run_id>' as test_run_id FROM test_data_customer
```

---

### Step 4: Execute Original Notebook

Use:

```python
dbutils.notebook.run("/path/to/notebook", timeout_seconds)
```

You’ll need:

- error capture
    
- execution timing
    

---

### Step 5: Run Assertions

For each test:

- execute SQL
    
- capture:
    
    - result
        
    - status (pass/fail)
        
    - execution time
        

---

### Step 6: Restore (non-negotiable reliability)

Always run in `finally` block:

```sql
TRUNCATE TABLE <table>;

INSERT INTO <table>
SELECT * FROM backup_<table>_<run_id>;
```

Then optionally:

```sql
DROP TABLE backup_<table>_<run_id>;
```

---

## HTML Report (keep it simple but useful)

Structure:

- Summary
    
    - total tests
        
    - passed
        
    - failed
        
- Table:
    

|Test ID|Description|SQL|Result|Status|
|---|---|---|---|---|

For failed tests:

- show **sample failing rows** (limit 10)
    

Don’t overengineer v1. Just make debugging possible.

---

## HITL Layer (make it structured or it will rot)

You said structured corrections—good. Define format:

Example:

```json
{
  "test_id": "T001",
  "issue": "SQL incorrect",
  "reason": "wrong column name",
  "fix": "use created_ts instead of created_at"
}
```

Store this back into SQLite:

- versioning
    
- audit trail
    

---

## Claude Usage Strategy (important)

Don’t just “use Claude”—constrain it.

### Phase 1 prompt should:

- extract into **fixed markdown schema**
    
- reject hallucinated fields
    

### Phase 2 prompt should:

- only use provided DDL
    
- follow strict SQL template
    
- output JSON → then convert to SQLite
    

---

## What you now have (in plain terms)

You’ve essentially designed:

> a lightweight, LLM-assisted data testing platform on top of Databricks

Not just a framework.

---

## Final sanity check (answer this before building)

If I give your system:

- 1 messy Excel
    
- 1 Databricks notebook
    
- 5 tables
    

Can it:

1. Generate structured spec
    
2. Produce deterministic test cases
    
3. Execute safely without corrupting QA
    
4. Give me a clear failure reason
    

If the answer is “yes with minor manual correction,” you’re in a good place.

---

If you want, next step I can:

- design exact Claude prompts
    
- or give you a starter notebook skeleton (clean, production-ready)
    
- or define SQLite schema as actual DDL
    

Where do you want to go deeper?

start with exact claude prompts

Good call. If prompts are sloppy, everything downstream becomes expensive to fix. I’ll give you **production-grade prompts**, not “try this and hope.”

The strategy here is simple:

- Force **structured output**
    
- Minimize hallucination
    
- Keep everything **machine-consable first, human-readable second**
    

We’ll define **3 prompts**:

1. Excel → Markdown (Phase 1)
    
2. Markdown → Test Assets JSON (Phase 2)
    
3. HITL Correction Prompt
    

---

# 1. Phase 1 — Excel → Structured Markdown

You said Excel has rules, columns, tables. So we lean into that and **force schema extraction**.

## Prompt

```text
You are a data QA analyst.

Your task is to convert the given Excel content into a STRICT structured markdown format.

IMPORTANT RULES:
- Do NOT invent any tables, columns, or rules
- Only extract what is explicitly present
- If something is unclear, mark it as "UNKNOWN"
- Keep output MACHINE-READABLE, not descriptive prose
- Follow the exact structure below
- Do NOT skip sections

OUTPUT FORMAT:

# METADATA
- requirement_id: <generate_unique_id>
- source: excel

# TABLES
For each table:
## table_name: <name>
- column: <column_name> <data_type or UNKNOWN>

# RULES
For each rule:
## rule_id: <unique_id>
- description: <raw rule text cleaned>
- tables_involved: [list]
- columns_involved: [list]

# PROCESS_STAGES
- step_1: <text>
- step_2: <text>

# BDD_SCENARIOS
For each rule:
## scenario_id: <id>
Given <context>
When <action>
Then <expected outcome>

# ASSUMPTIONS
- <only if explicitly implied, else leave empty>

# DDL
For each table:
CREATE TABLE <table_name> (
  <column_name> <data_type or STRING if unknown>
);

INPUT:
<PASTE EXCEL CONTENT HERE>
```

---

## Why this works

- You’re forcing:
    
    - structure
        
    - traceability
        
    - zero creativity
        
- “UNKNOWN” is **critical** → avoids hallucinated schemas
    

---

## Optional Improvement (worth it)

Before sending to Claude:

- remove strike-through (you already said)
    
- normalize spacing
    
- maybe label sections like:
    
    - `TABLE:`
        
    - `RULE:`
        

Even small preprocessing improves output quality significantly.

---

# 2. Phase 2 — Markdown → Test Cases + SQL + Data (JSON)

This is the most important prompt. This is where things usually go wrong.

We will:

- enforce JSON
    
- enforce SQL pattern
    
- enforce DDL usage constraint
    

---

## Prompt

```text
You are a senior data test engineer.

You are given a structured markdown specification.

Your task is to generate:
1. Test cases
2. Assertion SQL
3. Test data

STRICT RULES:

GENERAL:
- Output MUST be valid JSON
- Do NOT include explanations
- Do NOT invent new tables or columns
- Use ONLY DDL provided
- Every test must map to a rule_id

TEST CASE RULES:
- Cover:
  - happy path
  - edge cases
  - negative cases
- Each test must include:
  - test_id
  - rule_id
  - type (happy | edge | negative)
  - description
  - acceptance_criteria

SQL RULES:
- MUST follow assertion pattern
- MUST return exactly ONE row
- MUST return boolean column named: test_pass
- MUST NOT use columns outside DDL

SQL TEMPLATE:

SELECT 
  CASE 
    WHEN COUNT(*) = 0 THEN TRUE 
    ELSE FALSE 
  END AS test_pass
FROM <table>
WHERE <failure_condition>;

TEST DATA RULES:
- Must support ALL test cases
- Use realistic values
- Keep dataset minimal but sufficient
- Shared dataset across tests

OUTPUT FORMAT:

{
  "test_cases": [
    {
      "test_id": "T001",
      "rule_id": "RULE_01",
      "type": "happy",
      "description": "...",
      "acceptance_criteria": "..."
    }
  ],
  "test_sql": [
    {
      "test_id": "T001",
      "sql": "SELECT ..."
    }
  ],
  "test_data": [
    {
      "table": "table_name",
      "rows": [
        { "col1": "value", "col2": 123 }
      ]
    }
  ]
}

INPUT MARKDOWN:
<PASTE MARKDOWN FROM PHASE 1>
```

---

## Subtle but important design choices

- SQL is written as **failure detection**
    
    - cleaner
        
    - consistent logic
        
- Shared dataset
    
    - ensures cross-test reuse
        
    - reduces data explosion
        

---

## Common failure modes (watch for these)

Claude will try to:

- invent columns → your DDL constraint prevents this
    
- generate multi-row SQL → your template prevents this
    
- over-generate data → your “minimal dataset” constraint helps
    

Still, expect ~10–20% correction in HITL.

---

# 3. HITL Prompt (Correction Loop)

This is where most people get sloppy. You need **structured feedback**, not chatty edits.

---

## Prompt

```text
You are a data QA reviewer.

You are given:
1. Generated test assets (JSON)
2. Reviewer feedback

Your task:
- Apply corrections EXACTLY as specified
- Do NOT modify anything not mentioned
- Preserve JSON structure
- Ensure final output is valid JSON

RULES:
- If SQL is wrong → fix only SQL
- If test case is wrong → fix only that field
- If test data is insufficient → extend minimally
- Do NOT regenerate everything

INPUT:

TEST ASSETS:
<PASTE JSON>

FEEDBACK:
<PASTE STRUCTURED FEEDBACK JSON>

OUTPUT:
<UPDATED JSON ONLY>
```

---

## Feedback Format (you enforce this)

```json
{
  "corrections": [
    {
      "test_id": "T001",
      "field": "sql",
      "issue": "wrong column",
      "fix": "replace created_at with created_ts"
    },
    {
      "test_id": "T002",
      "field": "test_data",
      "issue": "missing edge case",
      "fix": "add null value for status"
    }
  ]
}
```

---

# Practical Workflow (don’t skip this)

Your pipeline should look like:

1. Excel cleaned → Claude Prompt 1 → Markdown
    
2. Markdown → Claude Prompt 2 → JSON
    
3. JSON → Review → Feedback JSON
    
4. Claude Prompt 3 → Corrected JSON
    
5. Store in SQLite
    

---

# Final Opinion (straight talk)

This setup will work **if you enforce discipline**:

- strict formats
    
- no “just tweak manually” shortcuts
    
- always store versions
    

If you loosen any of these, you’ll end up with:

> a pile of semi-correct SQL and no trust in the system

---

If you want next step, I’d suggest:

- SQLite DDL schema (so you can persist this cleanly)
    
- or Databricks notebook skeleton wired to this JSON
    

Which one do you want to lock next?

sqlite ddl schema

Alright, now we’re getting into the part that either makes this system clean and scalable—or turns it into a pile of JSON blobs nobody trusts.

You’re right to use SQLite, but don’t treat it like a dump. Treat it like a **control plane** for your testing system: versioning, lineage, auditability.

I’ll give you a schema that supports:

- versioning (critical)
    
- traceability (requirement → rule → test)
    
- execution tracking (runs, results)
    
- HITL corrections (audit trail)
    

---

# Core Design Principle

Every artifact must answer:

> where did this come from, what version is it, and what changed?

---

# 1. Requirements & Rules Layer

This is your Phase 1 output persisted.

```sql
CREATE TABLE requirements (
    requirement_id TEXT PRIMARY KEY,
    source TEXT,
    version INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

```sql
CREATE TABLE rules (
    rule_id TEXT PRIMARY KEY,
    requirement_id TEXT,
    description TEXT,
    raw_text TEXT,
    FOREIGN KEY (requirement_id) REFERENCES requirements(requirement_id)
);
```

---

```sql
CREATE TABLE tables_metadata (
    table_name TEXT,
    column_name TEXT,
    data_type TEXT,
    requirement_id TEXT,
    PRIMARY KEY (table_name, column_name, requirement_id)
);
```

---

# 2. Test Design Layer (Phase 2 output)

This is your generated + corrected test assets.

---

```sql
CREATE TABLE test_cases (
    test_id TEXT PRIMARY KEY,
    rule_id TEXT,
    requirement_id TEXT,
    version INTEGER,
    type TEXT CHECK(type IN ('happy', 'edge', 'negative')),
    description TEXT,
    acceptance_criteria TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (rule_id) REFERENCES rules(rule_id),
    FOREIGN KEY (requirement_id) REFERENCES requirements(requirement_id)
);
```

---

```sql
CREATE TABLE test_sql (
    test_id TEXT,
    version INTEGER,
    sql_query TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (test_id, version),
    FOREIGN KEY (test_id) REFERENCES test_cases(test_id)
);
```

---

```sql
CREATE TABLE test_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    table_name TEXT,
    data_json TEXT, -- store rows as JSON
    version INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

👉 Why JSON here?

- flexible schema
    
- easier ingestion into Spark/Databricks
    
- avoids rigid column mapping issues
    

---

# 3. Lineage Layer (don’t skip this)

This is what lets you debug later without crying.

---

```sql
CREATE TABLE lineage (
    test_id TEXT,
    rule_id TEXT,
    requirement_id TEXT,
    source_section TEXT, -- e.g. BDD, RULES, PROCESS
    PRIMARY KEY (test_id, rule_id),
    FOREIGN KEY (test_id) REFERENCES test_cases(test_id),
    FOREIGN KEY (rule_id) REFERENCES rules(rule_id)
);
```

---

# 4. HITL Corrections Layer

This is your learning system.

---

```sql
CREATE TABLE corrections (
    correction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    test_id TEXT,
    field TEXT, -- sql, test_data, description
    issue TEXT,
    fix TEXT,
    applied BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (test_id) REFERENCES test_cases(test_id)
);
```

---

# 5. Test Execution Layer (Phase 3)

This is where things get real.

---

```sql
CREATE TABLE test_runs (
    run_id TEXT PRIMARY KEY,
    requirement_id TEXT,
    started_at TIMESTAMP,
    ended_at TIMESTAMP,
    status TEXT, -- SUCCESS / FAILED / PARTIAL
    FOREIGN KEY (requirement_id) REFERENCES requirements(requirement_id)
);
```

---

```sql
CREATE TABLE test_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id TEXT,
    test_id TEXT,
    sql_executed TEXT,
    result BOOLEAN,
    status TEXT, -- PASS / FAIL / ERROR
    error_message TEXT,
    execution_time_ms INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (run_id) REFERENCES test_runs(run_id),
    FOREIGN KEY (test_id) REFERENCES test_cases(test_id)
);
```

---

# 6. Backup Tracking (you’ll thank yourself later)

Since you’re touching real tables:

```sql
CREATE TABLE backups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id TEXT,
    table_name TEXT,
    backup_table_name TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

# Versioning Strategy (don’t overcomplicate)

Keep it simple:

- Every regeneration → increment `version`
    
- Never overwrite:
    
    - test_cases
        
    - test_sql
        
    - test_data
        

👉 This gives you:

- rollback
    
- audit trail
    
- comparison across versions
    

---

# Minimal Query You’ll Use a Lot

Get latest test SQL:

```sql
SELECT ts.test_id, ts.sql_query
FROM test_sql ts
JOIN (
    SELECT test_id, MAX(version) as max_version
    FROM test_sql
    GROUP BY test_id
) latest
ON ts.test_id = latest.test_id AND ts.version = latest.max_version;
```

---

# What You Now Have (in plain terms)

This schema supports:

- Requirement → Rule → Test traceability
    
- Controlled evolution via versioning
    
- Execution observability
    
- HITL feedback loop
    

You’ve basically built a **mini test management system + execution tracker**.

---

# Where people usually mess this up

Let me call it out early:

1. **They skip lineage**  
    → later they don’t know why a test exists
    
2. **They overwrite instead of version**  
    → lose history, lose trust
    
3. **They don’t store execution results properly**  
    → debugging becomes guesswork
    
4. **They mix test data per test without strategy**  
    → chaos in shared dataset
    

---

# If you want to go one level deeper

Next logical steps:

- Python layer to:
    
    - read SQLite → generate Spark DataFrames
        
    - execute SQL
        
    - write results back
        
- OR
    
- HTML report generator from `test_results`
    
- OR
    
- strict JSON ↔ SQLite ingestion pipeline
    

---

My recommendation:  
👉 Next, build **Python ingestion + execution layer**. That’s where most hidden complexity lives.

Say the word and I’ll sketch that cleanly.

build python ingestion + execution layer

Good—this is the layer where the whole thing either feels like a clean system or a fragile script. I’ll give you a design that is:

- deterministic
    
- restart-safe
    
- easy to debug
    
- not overengineered
    

We’ll treat this as a **Databricks notebook–friendly execution engine**.

---

# High-Level Flow (what this code must guarantee)

1. Read latest test assets from SQLite
    
2. Backup real tables
    
3. Truncate + load test data
    
4. Run original notebook
    
5. Execute assertion SQL
    
6. Persist results
    
7. Restore tables (even if everything explodes)
    

If any one of these is weak → your framework becomes untrustworthy.

---

# Folder / Logical Structure

Think in modules (even inside a notebook):

```text
/dbfs/test_framework/
    ├── config.py
    ├── db.py
    ├── ingestion.py
    ├── execution.py
    ├── reporting.py
```

In notebook, you can inline them as sections.

---

# 1. Config (centralize everything)

```python
# config.py

SQLITE_PATH = "/dbfs/test_framework/test.db"

TABLES_TO_TEST = ["customer", "orders"]  # dynamically load later

NOTEBOOK_PATH = "/Repos/project/original_notebook"

TEST_DATA_TAG_COL = "test_run_id"
```

---

# 2. SQLite Access Layer

Keep it simple, don’t overabstract.

```python
# db.py

import sqlite3
import pandas as pd

def get_connection():
    return sqlite3.connect("/dbfs/test_framework/test.db")


def fetch_latest_test_sql():
    conn = get_connection()
    query = """
    SELECT ts.test_id, ts.sql_query
    FROM test_sql ts
    JOIN (
        SELECT test_id, MAX(version) as max_version
        FROM test_sql
        GROUP BY test_id
    ) latest
    ON ts.test_id = latest.test_id 
    AND ts.version = latest.max_version
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df


def fetch_test_cases():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM test_cases", conn)
    conn.close()
    return df


def fetch_test_data():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM test_data", conn)
    conn.close()
    return df


def insert_test_results(results_df):
    conn = get_connection()
    results_df.to_sql("test_results", conn, if_exists="append", index=False)
    conn.close()
```

---

# 3. Backup & Restore (make this bulletproof)

This is where most people cut corners. Don’t.

```python
# execution.py

import uuid
from pyspark.sql import SparkSession

spark = SparkSession.getActiveSession()

def create_run_id():
    return str(uuid.uuid4())
```

---

### Backup

```python
def backup_tables(tables, run_id):
    backup_map = {}

    for table in tables:
        backup_table = f"{table}_backup_{run_id.replace('-', '_')}"
        
        spark.sql(f"""
        CREATE TABLE {backup_table} AS 
        SELECT * FROM {table}
        """)

        backup_map[table] = backup_table

    return backup_map
```

---

### Truncate

```python
def truncate_tables(tables):
    for table in tables:
        spark.sql(f"TRUNCATE TABLE {table}")
```

---

### Restore (must never fail silently)

```python
def restore_tables(backup_map):
    for table, backup_table in backup_map.items():
        spark.sql(f"TRUNCATE TABLE {table}")
        spark.sql(f"INSERT INTO {table} SELECT * FROM {backup_table}")
```

---

# 4. Test Data Ingestion

You stored JSON in SQLite → convert to Spark.

```python
import json
from pyspark.sql import Row

def load_test_data(test_data_df, run_id):
    for _, row in test_data_df.iterrows():
        table = row["table_name"]
        data_json = json.loads(row["data_json"])

        rows = []
        for r in data_json:
            r["test_run_id"] = run_id  # tag data
            rows.append(Row(**r))

        df = spark.createDataFrame(rows)
        df.write.mode("append").insertInto(table)
```

---

# 5. Execute Original Notebook

```python
def run_original_notebook():
    try:
        result = dbutils.notebook.run(
            "/Repos/project/original_notebook",
            timeout_seconds=0
        )
        return "SUCCESS", None
    except Exception as e:
        return "FAILED", str(e)
```

---

# 6. Execute Assertion SQL

This is where your standardization pays off.

```python
import time

def run_tests(test_sql_df, run_id):
    results = []

    for _, row in test_sql_df.iterrows():
        test_id = row["test_id"]
        sql = row["sql_query"]

        start = time.time()

        try:
            df = spark.sql(sql)
            result_value = df.collect()[0]["test_pass"]

            status = "PASS" if result_value else "FAIL"
            error = None

        except Exception as e:
            result_value = False
            status = "ERROR"
            error = str(e)

        execution_time = int((time.time() - start) * 1000)

        results.append({
            "run_id": run_id,
            "test_id": test_id,
            "sql_executed": sql,
            "result": result_value,
            "status": status,
            "error_message": error,
            "execution_time_ms": execution_time
        })

    return results
```

---

# 7. Main Orchestrator (this is your control tower)

This is where discipline matters.

```python
def run_test_framework():
    run_id = create_run_id()

    test_sql_df = fetch_latest_test_sql()
    test_data_df = fetch_test_data()

    tables = list(set(test_data_df["table_name"]))

    backup_map = {}

    try:
        # Step 1: Backup
        backup_map = backup_tables(tables, run_id)

        # Step 2: Truncate
        truncate_tables(tables)

        # Step 3: Load Data
        load_test_data(test_data_df, run_id)

        # Step 4: Run Process
        proc_status, proc_error = run_original_notebook()

        # Step 5: Run Tests
        results = run_tests(test_sql_df, run_id)

    except Exception as e:
        print("Critical failure:", e)
        raise

    finally:
        # Step 6: Restore ALWAYS
        restore_tables(backup_map)

    # Step 7: Save Results
    import pandas as pd
    results_df = pd.DataFrame(results)
    insert_test_results(results_df)

    return results_df
```

---

# 8. (Optional but Smart) Failure Row Sampling

When test fails, fetch sample rows:

```python
def get_failure_sample(sql):
    sample_sql = sql.replace("COUNT(*) = 0", "*") + " LIMIT 10"
    return spark.sql(sample_sql).toPandas()
```

Add later to HTML.

---

# What You Now Have

This layer gives you:

- reproducible runs
    
- isolation via backup/restore
    
- consistent assertion execution
    
- audit trail in SQLite
    

In plain terms:

> You now have a deterministic test runner for data pipelines.

---

# Where this will break (if you’re not careful)

Let me save you future pain:

### 1. Schema drift

If DDL ≠ actual table → inserts fail  
→ consider validation step later

---

### 2. Notebook side effects

If original notebook:

- writes to unexpected tables
    
- uses hardcoded paths
    

→ your framework won’t catch everything

---

### 3. Large datasets

Shared “realistic” data can slow tests  
→ you may need sampling strategy later

---

# What I’d build next (priority order)

1. HTML report generator (from `test_results`)
    
2. Validation layer (DDL vs actual schema)
    
3. Parallel test execution (later optimization)
    

---

If you want, next I can:

- build HTML report generator (clean, readable)
    
- or add schema validation + guardrails (very useful in Databricks setups)
    

What direction do you want?

summarize this whole chat into clear instructions, include all corrections, approach in it

Here’s the cleaned, execution-ready version of everything we discussed. No fluff—just a system you can build from.

---

# 🎯 Objective

Build a **data test automation framework** that:

1. Converts Excel requirements → structured spec
    
2. Generates test cases + SQL + test data using LLM
    
3. Executes tests on Databricks
    
4. Produces HTML report
    
5. Maintains traceability, versioning, and auditability
    

---

# 🧠 Core Principles (non-negotiable)

- **No hallucination** → everything tied to DDL
    
- **Assertion-based SQL only** (returns 1 boolean row)
    
- **Version everything** (never overwrite)
    
- **Restore environment always** (fail-safe)
    
- **Structured HITL feedback** (no ad-hoc edits)
    
- **Machine-readable > human-readable**
    

---

# ⚙️ End-to-End Architecture

## Phase 1 — Excel → Structured Markdown

### Input

- Semi-structured Excel (rules, tables, columns exist)
    

### Process

- Clean Excel (remove strike-through, normalize text)
    
- Use Claude to extract structured markdown
    

### Output (strict schema)

- Metadata
    
- Tables + columns
    
- Rules
    
- Process stages
    
- BDD scenarios
    
- Assumptions
    
- DDL (critical)
    

### Key Constraints

- No invented fields
    
- Unknown values explicitly marked `"UNKNOWN"`
    

---

## Phase 2 — Markdown → Test Assets

### Input

- Structured markdown from Phase 1
    

### Process

- Use Claude to generate:
    
    - test_cases
        
    - test_sql
        
    - test_data
        

### Output (JSON → stored in SQLite)

### Test Case Rules

- Cover:
    
    - happy path
        
    - edge cases
        
    - negative cases
        
- Each test includes:
    
    - test_id
        
    - rule_id
        
    - type
        
    - description
        
    - acceptance_criteria
        

---

### SQL Rules (STRICT)

All SQL must follow:

```sql
SELECT 
  CASE 
    WHEN COUNT(*) = 0 THEN TRUE 
    ELSE FALSE 
  END AS test_pass
FROM <table>
WHERE <failure_condition>;
```

Constraints:

- Only use columns from DDL
    
- Return exactly **1 row**
    
- Column must be `test_pass`
    

---

### Test Data Strategy

- Use **shared dataset**
    
- Must cover all test cases
    
- Use **realistic production-like data**
    
- Add:
    
    - `test_run_id` column (critical for traceability)
        

---

## Phase 3 — Execution Engine (Databricks)

### Steps

1. Generate `test_run_id`
    
2. Backup original tables
    
3. Truncate tables
    
4. Load test data
    
5. Run original Databricks notebook
    
6. Execute test SQL
    
7. Store results
    
8. Restore original tables (ALWAYS)
    

---

### ⚠️ Critical Constraint

You **cannot modify original notebook**, so:

- Must use original tables
    
- Must rely on **backup + restore**
    
- Restore must run in `finally` block
    

---

# 🗄️ SQLite Schema (Control Plane)

## Requirements Layer

- `requirements`
    
- `rules`
    
- `tables_metadata`
    

## Test Design Layer

- `test_cases`
    
- `test_sql` (versioned)
    
- `test_data` (JSON)
    

## Lineage Layer

- `lineage` (test ↔ rule ↔ requirement)
    

## HITL Layer

- `corrections` (structured feedback)
    

## Execution Layer

- `test_runs`
    
- `test_results`
    

## Backup Tracking

- `backups`
    

---

# 🔁 HITL Workflow (Structured)

### Happens after:

- markdown extraction
    
- test generation
    
- execution (if failures unclear)
    

### Feedback format (strict JSON)

```json
{
  "corrections": [
    {
      "test_id": "T001",
      "field": "sql",
      "issue": "wrong column",
      "fix": "replace created_at with created_ts"
    }
  ]
}
```

### Rules

- Only fix what’s specified
    
- No regeneration of entire dataset
    
- Store corrections in SQLite
    

---

# 🧩 Python Execution Layer

## Responsibilities

- Read latest test assets from SQLite
    
- Convert test data JSON → Spark DataFrames
    
- Execute SQL
    
- Track results
    
- Ensure safe restore
    

---

## Key Components

### 1. SQLite Access

- fetch test cases, SQL, data
    
- insert results
    

### 2. Backup System

- create backup tables per run
    
- track mapping
    

### 3. Data Loading

- insert shared dataset
    
- tag with `test_run_id`
    

### 4. Notebook Execution

```python
dbutils.notebook.run(path, timeout)
```

### 5. Test Execution

- run assertion SQL
    
- capture:
    
    - result
        
    - status (PASS/FAIL/ERROR)
        
    - execution time
        

### 6. Restore (critical)

- truncate
    
- reload from backup
    
- must run even on failure
    

---

# 📊 HTML Report (v1 scope)

Keep it simple:

### Summary

- total tests
    
- passed
    
- failed
    

### Per Test

- test_id
    
- description
    
- SQL
    
- result
    
- status
    

### For failures

- include sample failing rows (optional enhancement)
    

---

# ⚠️ Key Risks + Fixes

## 1. Shared Dataset Coupling

**Risk:** tests affect each other  
**Fix:**

- use `test_run_id`
    
- design deterministic data
    

---

## 2. Backup/Restore Fragility

**Risk:** corrupt QA environment  
**Fix:**

- always restore in `finally`
    
- track backups in SQLite
    

---

## 3. DDL Inaccuracy

**Risk:** invalid SQL  
**Fix:**

- manual curation required
    
- optionally validate vs Databricks schema later
    

---

## 4. LLM Hallucination

**Risk:** wrong SQL / columns  
**Fix:**

- strict prompts
    
- enforce DDL-only usage
    
- HITL correction loop
    

---

## 5. Notebook Side Effects

**Risk:** writes to unexpected tables  
**Fix:**

- document impacted tables
    
- expand backup scope if needed
    

---

# 📈 Success Metrics

Track these:

1. **SQL accuracy**
    
    - % of generated SQL needing correction
        
2. **Time reduction**
    
    - manual testing vs automated runtime
        

---

# 🧭 Recommended Build Order

Don’t try to build everything at once.

### Step 1

- Phase 1 prompt → Markdown
    

### Step 2

- Phase 2 prompt → JSON
    

### Step 3

- SQLite schema + ingestion
    

### Step 4

- Python execution engine (core)
    

### Step 5

- HTML report
    

### Step 6

- HITL correction loop
    

---

# 🧠 Final Positioning

What you’re building is not just a framework.

It’s effectively:

> a lightweight LLM-driven data testing platform on top of Databricks

If you stay strict on:

- structure
    
- versioning
    
- SQL contracts
    

this will scale.

If you loosen discipline:  
you’ll end up with a system nobody trusts.

---

If you want to go further, the next high-leverage additions would be:

- schema validation layer (DDL vs actual tables)
    
- test impact analysis (which rules break most)
    
- parallel execution
    

But right now, this is enough to build a solid v1.
