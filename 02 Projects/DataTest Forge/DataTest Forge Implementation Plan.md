---
domain: data-engineering
subdomain: data-testing
note_type: project
source_type: self
status: active
level: advanced
tags:
  - datatest-forge
  - databricks
  - llm
  - data-testing
  - automation
  - claude
---
# AI Summary
Master implementation roadmap for DataTest Forge, an LLM-powered data testing framework for Databricks. The project transforms Excel-based business requirements into structured specifications, automatically generates test cases, SQL assertions, and test data using Claude, executes tests safely through backup and restore mechanisms, and produces HTML reports. The document defines a three-phase architecture, SQLite control plane, Databricks execution engine, human-in-the-loop correction workflow, reporting system, validation strategy, implementation milestones, and recommended build order, serving as the primary execution guide for the project.

---
# DataTest Automation - Implementation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** Build an LLM-driven data test automation framework on Databricks that converts Excel requirements into structured specs, generates test cases + SQL + test data via Claude, executes tests safely with backup/restore, and produces HTML reports.

**Architecture:** Three-phase pipeline (Excel->Markdown->Test Assets->Execution) with SQLite as the control plane for versioning, lineage, and auditability. Python modules run inside Databricks notebooks. HITL gates at each phase with structured JSON feedback.

**Tech Stack:** Python 3, Databricks (Spark SQL), SQLite, Claude (via notebook), Pandas, dbutils

---

## Project Name

**DataTest Forge** -- LLM-powered data pipeline test automation on Databricks

---

## Current Context / Assumptions

- User (Ronak) has a Databricks QA workspace with shared tables
- Original process scripts are Databricks notebooks that CANNOT be modified
- Excel requirements are semi-structured (contain rules, tables, columns -- not pure chaos)
- DDL is manually curated from Excel (not auto-extracted from Databricks catalog)
- Test environment: shared QA, no one else uses the test tables during runs
- Claude is available via Databricks notebook (AI assistant / SQL generation features)
- SQLite DB lives at `/dbfs/test_framework/test.db`
- Python code runs inside Databricks notebooks (SparkSession available, dbutils available)

---

## Step-by-Step Plan

### Task 1: Project Scaffolding

**Objective:** Create the project folder structure and empty module files.

**Files:**
- Create: `00 Projects/DataTest Forge/`
- Create: `00 Projects/DataTest Forge/config.py`
- Create: `00 Projects/DataTest Forge/db.py`
- Create: `00 Projects/DataTest Forge/ingestion.py`
- Create: `00 Projects/DataTest Forge/execution.py`
- Create: `00 Projects/DataTest Forge/reporting.py`
- Create: `00 Projects/DataTest Forge/prompts.py`
- Create: `00 Projects/DataTest Forge/main.py`
- Create: `00 Projects/DataTest Forge/README.md`

**Step 1:** Create directory `00 Projects/DataTest Forge/`

**Step 2:** Create all empty Python files listed above with module-level docstrings only.

**Step 3:** Create `README.md` with project overview (2-3 sentences: "DataTest Forge is an LLM-driven data test automation framework for Databricks").

**Verification:**
```
dir "00 Projects/DataTest Forge/" should show 8 files
```

---

### Task 2: SQLite Schema (Control Plane)

**Objective:** Define and create the SQLite database with all 8 tables for versioning, lineage, auditability.

**Files:**
- Modify: `00 Projects/DataTest Forge/db.py`

**Step 1:** Implement `init_db()` function that creates all tables:

Tables to create (in order):
1. `requirements` -- requirement_id TEXT PK, source TEXT, version INTEGER, created_at TIMESTAMP
2. `rules` -- rule_id TEXT PK, requirement_id TEXT FK, description TEXT, raw_text TEXT
3. `tables_metadata` -- table_name TEXT, column_name TEXT, data_type TEXT, requirement_id TEXT FK (composite PK)
4. `test_cases` -- test_id TEXT PK, rule_id TEXT FK, requirement_id TEXT FK, version INTEGER, type TEXT CHECK(happy/edge/negative), description TEXT, acceptance_criteria TEXT, created_at TIMESTAMP
5. `test_sql` -- test_id TEXT FK, version INTEGER, sql_query TEXT, created_at TIMESTAMP (composite PK)
6. `test_data` -- id INTEGER PK AUTOINCREMENT, table_name TEXT, data_json TEXT, version INTEGER, created_at TIMESTAMP
7. `lineage` -- test_id TEXT FK, rule_id TEXT FK, requirement_id TEXT, source_section TEXT (composite PK)
8. `corrections` -- correction_id INTEGER PK AUTOINCREMENT, test_id TEXT FK, field TEXT, issue TEXT, fix TEXT, applied BOOLEAN DEFAULT 0, created_at TIMESTAMP
9. `test_runs` -- run_id TEXT PK, requirement_id TEXT FK, started_at TIMESTAMP, ended_at TIMESTAMP, status TEXT
10. `test_results` -- id INTEGER PK AUTOINCREMENT, run_id TEXT FK, test_id TEXT FK, sql_executed TEXT, result BOOLEAN, status TEXT, error_message TEXT, execution_time_ms INTEGER, created_at TIMESTAMP
11. `backups` -- id INTEGER PK AUTOINCREMENT, run_id TEXT FK, table_name TEXT, backup_table_name TEXT, created_at TIMESTAMP

**Step 2:** Implement `get_connection()` returning `sqlite3.connect(db_path)`.

**Step 3:** Implement helper: `fetch_latest_test_sql()` -- returns DataFrame of latest version test SQL per test_id.

**Step 4:** Implement helper: `fetch_test_cases()` -- returns all test cases.

**Step 5:** Implement helper: `fetch_test_data()` -- returns all test data.

**Step 6:** Implement helper: `insert_test_results(results_df)` -- appends results to test_results table.

**Step 7:** Implement helper: `insert_correction(test_id, field, issue, fix)` -- stores HITL feedback.

**Verification:**
```python
# Run in Python
from db import init_db, get_connection
init_db()
conn = get_connection()
tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
assert len(tables) == 11  # all tables created
```

---

### Task 3: Config Module

**Objective:** Centralize all configurable parameters.

**Files:**
- Modify: `00 Projects/DataTest Forge/config.py`

**Step 1:** Define config variables:
- `SQLITE_PATH` -- default `/dbfs/test_framework/test.db`
- `TABLES_TO_TEST` -- empty list (populated dynamically at runtime)
- `NOTEBOOK_PATH` -- default `/Repos/project/original_notebook`
- `TEST_DATA_TAG_COL` -- `"test_run_id"`
- `BACKUP_TABLE_SUFFIX` -- `"_backup_"`
- `REPORT_OUTPUT_DIR` -- `/dbfs/test_framework/reports/`

**Step 2:** Define SQL template constant:
```python
ASSERTION_SQL_TEMPLATE = """
SELECT
  CASE
    WHEN COUNT(*) = 0 THEN TRUE
    ELSE FALSE
  END AS test_pass
FROM {table}
WHERE {failure_condition};
"""
```

**Step 3:** Define HITL feedback JSON schema constant for reference.

**Verification:**
```python
from config import SQLITE_PATH, ASSERTION_SQL_TEMPLATE
assert "test_pass" in ASSERTION_SQL_TEMPLATE
```

---

### Task 4: Phase 1 Prompt -- Excel to Structured Markdown

**Objective:** Define the Claude prompt for extracting structured specs from Excel content.

**Files:**
- Modify: `00 Projects/DataTest Forge/prompts.py`

**Step 1:** Implement `phase1_excel_to_markdown_prompt(excel_content: str) -> str` that returns the full prompt string.

The prompt must enforce:
- Output format: strict markdown with sections: METADATA, TABLES, RULES, PROCESS_STAGES, BDD_SCENARIOS, ASSUMPTIONS, DDL
- No invention of tables/columns/rules -- only extract what is present
- Unknown values marked as `"UNKNOWN"`
- Machine-readable, not descriptive prose
- DDL section with CREATE TABLE statements

**Step 2:** Implement `preprocess_excel_content(raw_content: str) -> str` that:
- Removes strike-through text (text between ~~ markers or marked with strikethrough flag)
- Normalizes whitespace (collapse multiple spaces, strip leading/trailing per line)
- Returns cleaned content ready for Claude

**Verification:**
```python
from prompts import phase1_excel_to_markdown_prompt
prompt = phase1_excel_to_markdown_prompt("sample excel")
assert "METADATA" in prompt
assert "UNKNOWN" in prompt
assert "DDL" in prompt
```

---

### Task 5: Phase 2 Prompt -- Markdown to Test Assets

**Objective:** Define the Claude prompt for generating test cases, SQL, and test data from structured markdown.

**Files:**
- Modify: `00 Projects/DataTest Forge/prompts.py`

**Step 1:** Implement `phase2_markdown_to_test_assets_prompt(markdown_content: str) -> str` that returns the full prompt string.

The prompt must enforce:
- Output: valid JSON only (no explanations, no markdown fences)
- Three arrays: `test_cases`, `test_sql`, `test_data`
- Test cases cover happy path, edge cases, negative scenarios
- Each test has: test_id, rule_id, type, description, acceptance_criteria
- SQL MUST follow assertion template (1 row, boolean `test_pass` column)
- SQL MUST only use columns from DDL
- Test data: shared dataset, realistic values, covers all test cases
- Test data includes `test_run_id` tagging

**Step 2:** Implement `validate_test_assets_json(assets: dict) -> list` that validates:
- All required keys present in each test case
- SQL returns exactly 1 row (basic syntax check for SELECT...AS test_pass)
- All test_ids referenced in test_sql exist in test_cases
- Returns list of validation errors (empty = valid)

**Verification:**
```python
from prompts import phase2_markdown_to_test_assets_prompt
prompt = phase2_markdown_to_test_assets_prompt("sample markdown")
assert "test_pass" in prompt
assert "JSON" in prompt
```

---

### Task 6: Phase 3 Prompt -- HITL Correction

**Objective:** Define the Claude prompt for applying structured corrections to test assets.

**Files:**
- Modify: `00 Projects/DataTest Forge/prompts.py`

**Step 1:** Implement `phase3_correction_prompt(test_assets_json: str, feedback_json: str) -> str` that returns the full prompt string.

The prompt must enforce:
- Apply corrections exactly as specified
- Do NOT modify anything not mentioned
- Preserve JSON structure
- Output valid JSON only
- Rules: fix only the field specified, no full regeneration

**Verification:**
```python
from prompts import phase3_correction_prompt
prompt = phase3_correction_prompt("{}", '{"corrections":[]}')
assert "corrections" in prompt
assert "valid JSON" in prompt
```

---

### Task 7: Ingestion Module -- JSON to SQLite

**Objective:** Ingest Claude-generated test assets (JSON) into SQLite with versioning and lineage.

**Files:**
- Modify: `00 Projects/DataTest Forge/ingestion.py`

**Step 1:** Implement `ingest_requirement(source: str) -> requirement_id` -- creates requirement record.

**Step 2:** Implement `ingest_rules(requirement_id: str, rules: list)` -- stores each rule from Phase 1 output.

**Step 3:** Implement `ingest_tables_metadata(requirement_id: str, tables: list)` -- stores table/column metadata.

**Step 4:** Implement `ingest_test_assets(requirement_id: str, assets: dict) -> None` that:
- Iterates over `test_cases` array, inserts into `test_cases` table with version
- Iterates over `test_sql` array, inserts into `test_sql` table with version
- Iterates over `test_data` array, serializes rows to JSON, inserts into `test_data` table
- Creates lineage entries linking test_id -> rule_id -> requirement_id
- Increments version on re-ingestion (never overwrites)

**Step 5:** Implement `apply_corrections(corrections: list)` that:
- For each correction, updates the specified field in the appropriate table
- Marks correction as `applied = 1`
- Stores in `corrections` table for audit trail

**Verification:**
```python
from ingestion import ingest_test_assets
# After ingesting sample assets:
# - test_cases row count matches input
# - test_sql row count matches input
# - lineage entries exist for all tests
# - re-ingestion increments version, doesn't duplicate
```

---

### Task 8: Execution Module -- Backup, Restore, Data Loading

**Objective:** Implement bulletproof backup/restore and test data loading for Databricks.

**Files:**
- Modify: `00 Projects/DataTest Forge/execution.py`

**Step 1:** Implement `create_run_id() -> str` -- returns UUID string.

**Step 2:** Implement `backup_tables(tables: list, run_id: str) -> dict` that:
- For each table, creates `<table>_backup_<run_id>` via `CREATE TABLE ... AS SELECT *`
- Returns mapping `{original_table: backup_table_name}`
- Stores backup records in `backups` table

**Step 3:** Implement `truncate_tables(tables: list)` -- runs `TRUNCATE TABLE` for each.

**Step 4:** Implement `restore_tables(backup_map: dict)` that:
- For each table: TRUNCATE original, INSERT from backup
- Must be idempotent (safe to call multiple times)
- Drops backup tables after successful restore

**Step 5:** Implement `load_test_data(test_data_df, run_id: str)` that:
- Reads test data from DataFrame (table_name, data_json columns)
- Parses JSON rows into Spark DataFrames
- Tags each row with `test_run_id`
- Writes to target tables using `insertInto`

**Step 6:** Implement `validate_schema(tables: list) -> list` that:
- Compares DDL columns (from SQLite `tables_metadata`) vs actual Databricks table schema
- Returns list of mismatches (missing columns, type differences)
- This is the "schema drift" guardrail

**Verification:**
```python
# In Databricks notebook context:
# backup_map = backup_tables(["customer"], "test-123")
# truncate_tables(["customer"])
# restore_tables(backup_map)
# -- original data should be intact
```

---

### Task 9: Execution Module -- Notebook Runner and Test Runner

**Objective:** Implement the original notebook execution and assertion SQL runner.

**Files:**
- Modify: `00 Projects/DataTest Forge/execution.py`

**Step 1:** Implement `run_original_notebook(notebook_path: str, timeout: int = 0) -> tuple` that:
- Calls `dbutils.notebook.run(notebook_path, timeout)`
- Returns `(status: str, error_message: str or None)`
- Catches all exceptions, returns ("FAILED", str(e))

**Step 2:** Implement `run_single_test(test_id: str, sql: str, run_id: str) -> dict` that:
- Executes SQL via `spark.sql(sql)`
- Collects result: `df.collect()[0]["test_pass"]`
- Returns dict: `{run_id, test_id, sql_executed, result, status, error_message, execution_time_ms}`
- On exception: returns with status="ERROR" and error_message

**Step 3:** Implement `run_all_tests(test_sql_df, run_id: str) -> list` that:
- Iterates over all test SQL rows
- Calls `run_single_test` for each
- Returns list of result dicts

**Step 4:** Implement `run_test_framework(requirement_id: str) -> DataFrame` -- the main orchestrator:
1. Generate `run_id`
2. Fetch latest test SQL and test data from SQLite
3. Backup tables
4. Truncate tables
5. Load test data
6. Run original notebook
7. Execute all tests
8. **In `finally` block:** restore tables (ALWAYS)
9. Persist results to SQLite
10. Return results DataFrame

**Verification:**
```python
# In Databricks notebook:
# results = run_test_framework("REQ-001")
# assert all tests have status in (PASS, FAIL, ERROR)
# assert original tables are restored
```

---

### Task 10: Reporting Module -- HTML Report Generator

**Objective:** Generate a static HTML report from test results.

**Files:**
- Modify: `00 Projects/DataTest Forge/reporting.py`

**Step 1:** Implement `generate_html_report(results_df, run_id: str, output_dir: str) -> str` that:
- Creates summary section: total tests, passed, failed, pass rate
- Creates results table: test_id, description, SQL, result, status
- For failed tests: includes sample failing rows (up to 10)
- Uses minimal inline CSS (dark theme, clean table styling)
- Saves to `{output_dir}/report_{run_id}_{timestamp}.html`
- Returns the file path

**Step 2:** Implement `generate_failure_sample(sql: str) -> DataFrame` that:
- Transforms assertion SQL to fetch failing rows (replaces COUNT(*)=0 with *)
- Adds LIMIT 10
- Returns sample DataFrame for display in report

**Step 3:** Implement `fetch_test_descriptions(results_df) -> DataFrame` that:
- Joins results with `test_cases` table to get descriptions
- Returns enriched DataFrame for report

**Verification:**
```python
# report_path = generate_html_report(results_df, "run-123", "/tmp/reports")
# assert os.path.exists(report_path)
# assert report_path.endswith(".html")
```

---

### Task 11: Main Orchestrator

**Objective:** Wire all modules together into a single entry point.

**Files:**
- Modify: `00 Projects/DataTest Forge/main.py`

**Step 1:** Implement `run_pipeline(excel_path: str, notebook_path: str) -> DataFrame` that:
1. Read Excel content
2. Preprocess (Task 4's preprocess function)
3. Call Phase 1 prompt -> get markdown
4. Call Phase 2 prompt -> get test assets JSON
5. Validate assets (Task 5's validate function)
6. Ingest into SQLite (Task 7)
7. Run execution engine (Task 9's orchestrator)
8. Generate HTML report (Task 10)
9. Return results DataFrame

**Step 2:** Implement `run_correction_loop(feedback_json: str)` that:
1. Parse feedback JSON
2. Call Phase 3 prompt (Task 6)
3. Apply corrections to SQLite (Task 7's apply_corrections)

**Step 3:** Implement `re_run_tests(requirement_id: str) -> DataFrame` that:
- Re-executes tests using existing test assets (no regeneration)
- Useful after corrections are applied

**Step 4:** Add `if __name__ == "__main__"` block with argparse:
- `--mode pipeline` (full run from Excel)
- `--mode re-run` (re-execute existing tests)
- `--mode report` (regenerate report from last run)
- `--excel` path to Excel file
- `--notebook` path to Databricks notebook
- `--requirement-id` requirement identifier

**Verification:**
```bash
python main.py --mode pipeline --excel "requirements.xlsx" --notebook "/Repos/project/notebook"
# Should produce HTML report and print summary
```

---

### Task 12: Documentation

**Objective:** Write clear README with setup, usage, and architecture.

**Files:**
- Modify: `00 Projects/DataTest Forge/README.md`

**Step 1:** Write README sections:
- What is DataTest Forge (2 sentences)
- Architecture diagram (ASCII art showing 3-phase pipeline)
- Setup instructions (dependencies, SQLite init, Databricks setup)
- Usage examples (pipeline mode, re-run mode, correction mode)
- Folder structure explanation
- Configuration options
- Known limitations

**Step 2:** Update the project file `00 Projects/Test Automation - CAI/Test Automation - CAI.md` to add a link/reference to the new DataTest Forge implementation.

---

## Files Summary

| File | Purpose |
|---|---|
| `00 Projects/DataTest Forge/config.py` | Central configuration (paths, SQL template, constants) |
| `00 Projects/DataTest Forge/db.py` | SQLite schema creation + query helpers |
| `00 Projects/DataTest Forge/prompts.py` | All 3 Claude prompts + preprocessing + validation |
| `00 Projects/DataTest Forge/ingestion.py` | JSON-to-SQLite ingestion with versioning + corrections |
| `00 Projects/DataTest Forge/execution.py` | Backup/restore, data loading, notebook runner, test runner |
| `00 Projects/DataTest Forge/reporting.py` | HTML report generation from test results |
| `00 Projects/DataTest Forge/main.py` | CLI entry point wiring all modules |
| `00 Projects/DataTest Forge/README.md` | Setup + usage documentation |

---

## Tests / Validation

Since this is a Databricks notebook-based framework, testing happens in two layers:

**Unit tests (local Python, no Spark needed):**
- `db.py` -- test all CRUD operations with in-memory SQLite
- `prompts.py` -- test prompt generation contains required sections
- `ingestion.py` -- test JSON ingestion, versioning, lineage creation
- `reporting.py` -- test HTML generation from mock DataFrame

**Integration tests (Databricks notebook):**
- Backup/restore round-trip on a sample table
- Test SQL execution against known data
- Full pipeline run with sample Excel + notebook
- Restore-on-failure scenario (intentionally fail mid-run, verify restore)

---

## Risks, Tradeoffs, and Open Questions

| Risk | Mitigation |
|---|---|
| LLM SQL accuracy (~10-20% need correction) | Strict SQL template + DDL-only constraint + HITL loop |
| Shared dataset coupling between tests | `test_run_id` tagging + deterministic data design |
| Restore failure corrupts QA env | Restore in `finally` block + idempotent restore + backup tracking in SQLite |
| DDL drift (Excel DDL != actual table) | Schema validation layer (Task 8, Step 6) |
| Notebook side effects (writes to unexpected tables) | Document all impacted tables; expand backup scope |
| Large realistic data slows tests | Sampling strategy (future optimization, not v1) |

**Open questions to resolve during implementation:**
1. How is Claude invoked in the Databricks notebook? (AI assistant API, SQL generation cell, external API call?)
2. What is the exact format of the Excel file? (Column headers, sheet structure)
3. Should the framework support multiple requirement sets (multiple Excel files) in one SQLite DB?

---

## Build Order (Recommended)

1. Task 1 (Scaffolding) -- 5 min
2. Task 2 (SQLite Schema) -- 20 min
3. Task 3 (Config) -- 10 min
4. Task 4 (Phase 1 Prompt) -- 15 min
5. Task 5 (Phase 2 Prompt) -- 20 min
6. Task 6 (Phase 3 Prompt) -- 10 min
7. Task 7 (Ingestion) -- 25 min
8. Task 8 (Backup/Restore/Load) -- 30 min
9. Task 9 (Execution/Test Runner) -- 30 min
10. Task 10 (Reporting) -- 25 min
11. Task 11 (Main Orchestrator) -- 15 min
12. Task 12 (Documentation) -- 15 min

**Total estimated: ~3.5 hours of focused work**

---

## Recommended Execution Strategy

Build and validate each task locally (Tasks 1-7, 10-12 can run without Databricks). Then deploy to Databricks for integration testing (Tasks 8-9).

Start with Task 1. Do not proceed to Task 8-9 until all LLM prompts and SQLite schema are locked.