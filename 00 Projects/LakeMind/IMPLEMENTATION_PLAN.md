# Lakehouse Optimizer — Fresh Implementation Plan

> **Stack:** OpenRouter (LLM) + DuckDB (engine) + Ducklake (lake format) + LangGraph (agent) + Streamlit (UI) + XGBoost (prediction)

---

## Stack Recommendation

| Layer | Tool | Why |
|---|---|---|
| **LLM / Agent** | OpenRouter (existing) + LangGraph | Already have access; LangGraph is perfect for reasoning graph |
| **Query Engine** | DuckDB | Embedded, zero infra, reads Parquet/Delta/Iceberg natively |
| **Lake Storage Format** | Ducklake | DuckDB-native (ACID, time travel, Parquet-based), zero infra |
| **Data Generation** | Python + Faker + NumPy + PyArrow | Full control over pathological patterns |
| **ML Models** | scikit-learn + XGBoost | Runtime prediction, anomaly detection |
| **UI** | Streamlit | Fastest path to interactive reasoning trace demo |
| **File Formats** | Parquet, Delta Lake, JSONL, CSV | Covers real-world lakehouse diversity |

**Why Ducklake over Delta/Iceberg:**
- Zero infrastructure (no Spark, no Hive metastore)
- Native DuckDB integration — `ATTACH` a ducklake directly
- ACID transactions, schema evolution, time travel
- Parquet-based — generated data stays as Parquet files
- Perfect for demo; swap to Delta/Iceberg later if needed

---

## Project Structure

```
00 Projects/Lakehouse Optimizer/
├── README.md
├── pyproject.toml                  # uv-managed deps
├── data/
│   ├── generate.py                 # Synthetic data generation pipeline
│   ├── lakehouse.ducklake/         # Ducklake catalog (generated)
│   ├── raw/                        # Raw Parquet/CSV/JSONL files
│   │   ├── bronze/
│   │   ├── silver/
│   │   └── gold/
│   └── metadata.duckdb             # DuckDB metadata catalog
├── src/
│   ├── __init__.py
│   ├── config.py                   # OpenRouter model config, paths
│   ├── signals/
│   │   ├── __init__.py
│   │   ├── extractor.py            # Query plan feature extraction
│   │   ├── pathologies.py          # Pathology registry
│   │   └── features.py             # Feature vector assembly
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── state.py                # OptimizationState TypedDict
│   │   ├── nodes.py                # 6 LangGraph nodes
│   │   ├── graph.py                # Graph assembly + conditional edges
│   │   └── prompts.py              # All LLM prompts per node
│   ├── evidence/
│   │   ├── __init__.py
│   │   ├── store.py                # DuckDB evidence queries
│   │   └── validators.py           # Hypothesis validation logic
│   ├── prediction/
│   │   ├── __init__.py
│   │   ├── runtime_model.py        # XGBoost runtime/SLA prediction
│   │   └── cost_model.py           # Cost estimation
│   └── ui/
│       ├── __init__.py
│       ├── app.py                  # Streamlit entry point
│       ├── trace_view.py           # Reasoning trace visualization
│       └── dashboard.py            # Cost/performance overview
├── tests/
│   ├── test_signals.py
│   ├── test_agent.py
│   └── test_data.py
└── scripts/
    ├── run_demo.py                 # One-click demo launcher
    └── benchmark.py                # Run optimization on sample queries
```

---

## Phase 1: Synthetic Data Generation (Days 1-2)

**Goal:** Generate 6 months of realistic multi-format lakehouse data with embedded pathologies.

### 1.1 Entity Universe

```
Warehouses: PROD_ETL_XL, ANALYTICS_L, ML_TRAINING_XL, ADHOC_M, REPORTING_S
Tables:     10-12 tables across bronze/silver/gold layers
Pipelines:  8 ETL/ML pipelines with SLAs
Users:      8-10 service accounts + human users
```

### 1.2 File Format Distribution

| Layer | Format | Compression | Rationale |
|---|---|---|---|
| Bronze (raw) | Parquet + JSONL (some) | ZSTD | Realistic raw ingestion |
| Silver (cleaned) | Parquet (partitioned) | Snappy | Standard analytics |
| Gold (aggregated) | Parquet (partitioned) + Delta | Snappy | Business-facing |
| ML Features | Parquet + NumPy arrays | ZSTD | Feature store format |

### 1.3 Data Scale Targets

```
Total raw data:           ~50-100 GB (Parquet compressed)
Query history:            ~500K rows over 180 days
Pipeline runs:            ~1,440 rows (8 pipelines x 180 days)
Table access log:         ~2,160 rows (12 tables x 180 days)
Storage layout:           ~5,000-15,000 Parquet files across partitions
```

### 1.4 Pathology Registry (7 types)

```python
PATHOLOGIES = {
    "full_table_scan_no_partition": {
        "tables": ["orders_fact", "customer_events_raw", "ml_feature_store_v1"],
        "signal": {"bytes_scanned_ratio": (0.85, 1.0), "partition_pruning": (0.0, 0.05)},
        "severity": "critical"
    },
    "cartesian_join": {
        "pattern": "events JOIN orders without date filter",
        "signal": {"row_explosion_ratio": (50, 200), "spill_to_disk": True},
        "severity": "critical"
    },
    "warehouse_overprovisioned": {
        "warehouses": ["PROD_ETL_XL", "ML_TRAINING_XL"],
        "signal": {"avg_credit_utilization": (0.08, 0.22), "idle_pct": (0.45, 0.70)},
        "severity": "high"
    },
    "cold_table_high_storage": {
        "tables": ["returns_staging", "ml_feature_store_v1"],
        "signal": {"last_accessed_days_ago": (45, 180), "size_gb": (31, 890)},
        "severity": "medium"
    },
    "redundant_dataset": {
        "tables": ["ml_feature_store_v1", "ml_feature_store_v2"],
        "signal": {"schema_overlap_pct": (0.87, 0.95)},
        "severity": "high"
    },
    "sla_breach_pipeline": {
        "pipelines": ["orders_daily_rollup", "revenue_reconciliation"],
        "signal": {"breach_rate_30d": (0.35, 0.65), "trend": "degrading"},
        "severity": "critical"
    },
    "high_recurrence_identical_query": {
        "warehouse": "ANALYTICS_L",
        "signal": {"identical_runs_per_day": (80, 200), "cache_hit_rate": (0.0, 0.05)},
        "severity": "high"
    }
}
```

### 1.5 Generator Modules

```
data/generate.py
├── generate_entity_universe()     # Warehouses, tables, users, pipelines
├── generate_table_data()          # Parquet files per table with partitions
├── generate_query_history()       # 500K query execution records
├── generate_pipeline_runs()       # Pipeline execution telemetry
├── generate_table_access_log()    # Daily access patterns
├── generate_warehouse_credits()   # Credit consumption time series
└── build_lakehouse()              # Orchestrator — writes Ducklake + metadata DB
```

### 1.6 Ducklake Storage Layout

```
data/lakehouse.ducklake/
├── catalog/
├── tables/
│   ├── bronze/
│   │   ├── customer_events_raw/
│   │   │   ├── event_date=2025-01-01/
│   │   │   │   ├── part-00000.parquet
│   │   │   │   └── part-00001.parquet
│   │   │   └── ...
│   │   └── campaign_spend_raw/
│   ├── silver/
│   │   ├── marketing_attribution/
│   │   └── user_sessions/
│   └── gold/
│       ├── orders_fact/
│       └── revenue_daily_agg/
└── metadata/
    └── snapshots/
```

---

## Phase 2: Signal Extraction Layer (Day 3)

**Goal:** Extract 12 signal categories from query plans + telemetry.

```python
# src/signals/extractor.py

class QueryPlanExtractor:
    """Extracts features from DuckDB EXPLAIN ANALYZE output."""
    
    def extract(self, query: str, connection: duckdb.DuckDBPyConnection) -> dict:
        # Run EXPLAIN ANALYZE
        plan = connection.execute(f"EXPLAIN ANALYZE {query}").fetchall()
        return {
            "scan_features": self._extract_scans(plan),
            "join_features": self._extract_joins(plan),
            "shuffle_features": self._extract_shuffles(plan),
            "spill_features": self._extract_spills(plan),
            "cardinality_features": self._extract_cardinality(plan),
            "operator_cost": self._extract_operator_cost(plan),
        }

# 12 signal categories:
# 1. Query Shape Features
# 2. Scan-Level Metadata  
# 3. Join Intelligence
# 4. Shuffle Analysis
# 5. Data Skew Detection
# 6. Cardinality Estimation Accuracy
# 7. Operator Cost Breakdown
# 8. Spill Detection
# 9. Filter Effectiveness
# 10. Aggregation Efficiency
# 11. Data Movement Metrics
# 12. Runtime Telemetry Correlation
```

---

## Phase 3: Evidence Store (Day 3-4)

**Goal:** DuckDB-backed evidence that the agent can query to validate hypotheses.

```python
# src/evidence/store.py

class EvidenceStore:
    """DuckDB-backed evidence catalog."""
    
    def __init__(self, db_path: str):
        self.conn = duckdb.connect(db_path)
    
    def query_evidence(self, finding_type: str, affected_asset: str, 
                       metrics: dict) -> list:
        """Pull supporting/contradicting evidence for a hypothesis."""
        # Deterministic SQL queries — no LLM involved
        # Examples:
        # - "Show me partition pruning ratio for orders_fact last 30 days"
        # - "Compare actual vs estimated rows for this query pattern"
        # - "What's the warehouse utilization window?"
        pass
    
    def get_recurrence_pattern(self, query_hash: str, days: int = 30) -> dict:
        pass
    
    def get_cost_trend(self, table_name: str, warehouse: str) -> list:
        pass
```

---

## Phase 4: LangGraph Agent (Days 4-6)

**Goal:** The 6-node reasoning graph with critique loop.

### State Schema

```python
# src/agent/state.py
class OptimizationState(TypedDict):
    finding_id: str
    finding_type: str
    affected_asset: str
    raw_metrics: dict
    asset_metadata: dict
    query_text: Optional[str]
    
    # Accumulated through graph
    hypotheses: List[dict]
    validated_hypothesis: Optional[str]
    evidence: List[dict]
    severity_score: float
    cost_impact_monthly_usd: float
    perf_impact_estimate: str
    
    remediation_options: List[dict]
    selected_remediation: Optional[dict]
    
    generated_script: Optional[str]
    script_language: str
    
    critique_feedback: Optional[dict]
    revision_count: int
    confidence_score: float
    
    recommendation: Optional[dict]
    status: Literal["in_progress", "approved", "failed"]
```

### Node Definitions

```python
# src/agent/nodes.py

def hypothesis_generator(state: OptimizationState) -> OptimizationState:
    """Node 1: Generate 2-3 competing root cause hypotheses."""
    # Uses OpenRouter LLM with structured JSON output

def evidence_validator(state: OptimizationState) -> OptimizationState:
    """Node 2: Query DuckDB evidence to validate/refute each hypothesis."""
    # Calls EvidenceStore — deterministic, no LLM hallucination risk

def impact_quantifier(state: OptimizationState) -> OptimizationState:
    """Node 3: Translate to dollar + latency impact."""
    # LLM quantifies: "$2,100-2,800/month savings potential"

def remediation_planner(state: OptimizationState) -> OptimizationState:
    """Node 4: Generate 2-3 remediation options with tradeoffs."""
    # LLM generates ranked options with effort/risk assessment

def script_generator(state: OptimizationState) -> OptimizationState:
    """Node 5: Generate runnable optimization script."""
    # LLM produces SQL/DDL/Python with validation + rollback

def critique_node(state: OptimizationState) -> OptimizationState:
    """Node 6: Self-review — approve or loop back for revision."""
    # LLM acts as principal engineer reviewing its own output
```

### Graph Assembly

```python
# src/agent/graph.py
def build_graph() -> StateGraph:
    graph = StateGraph(OptimizationState)
    graph.add_node("hypothesis_generator", hypothesis_generator)
    graph.add_node("evidence_validator", evidence_validator)
    graph.add_node("impact_quantifier", impact_quantifier)
    graph.add_node("remediation_planner", remediation_planner)
    graph.add_node("script_generator", script_generator)
    graph.add_node("critique_node", critique_node)
    graph.add_node("finalize", finalize)
    
    graph.set_entry_point("hypothesis_generator")
    graph.add_edge("hypothesis_generator", "evidence_validator")
    graph.add_edge("evidence_validator", "impact_quantifier")
    graph.add_edge("impact_quantifier", "remediation_planner")
    graph.add_edge("remediation_planner", "script_generator")
    graph.add_edge("script_generator", "critique_node")
    graph.add_conditional_edges("critique_node", route_after_critique, {
        "remediation_planner": "remediation_planner",  # loop back
        "finalize": "finalize"
    })
    graph.add_edge("finalize", END)
    
    return graph.compile()
```

---

## Phase 5: Prediction Models (Day 6-7)

**Goal:** ML-based runtime and SLA prediction.

```python
# src/prediction/runtime_model.py

class RuntimePredictor:
    """Predict batch job runtime using telemetry features."""
    
    FEATURES = [
        "input_bytes", "input_rows", "shuffle_bytes", "file_count",
        "executor_count", "cpu_hours", "memory_gb_hours",
        "day_of_week", "hour_of_day", "skew_ratio", "small_file_ratio"
    ]
    
    def train(self, pipeline_runs_df: pd.DataFrame):
        # XGBoost regressor
        # Expected accuracy: 85-95%
        pass
    
    def predict(self, job_features: dict) -> dict:
        # Returns: {"predicted_runtime_sec": 4200, "confidence_interval": [3800, 4600]}
        pass
    
    def predict_sla_breach(self, job_features: dict, sla_minutes: int) -> float:
        # Returns: probability of SLA breach (0-1)
        pass
```

---

## Phase 6: Streamlit UI (Day 7-8)

**Goal:** Reasoning trace dashboard + optimization overview.

```
src/ui/app.py
├── Tab 1: "Upload Query Plan"
│   ├── Paste query or upload JSON plan
│   ├── Click "Analyze" → triggers LangGraph
│   └── Shows reasoning trace (expandable nodes)
│
├── Tab 2: "Reasoning Trace"
│   ├── ▼ Hypotheses Generated (3)
│   ├── ▼ Evidence Validated
│   ├── ▼ Impact Quantified ($2,100-2,800/mo)
│   ├── ▼ Remediation Options (ranked)
│   ├── ▼ Generated Script (copy button)
│   └── ▼ Critique (approved/revise)
│
├── Tab 3: "Cost Dashboard"
│   ├── Warehouse credit trends
│   ├── Top expensive queries
│   ├── Cold storage recommendations
│   └── Savings realized vs potential
│
└── Tab 4: "Batch Predictions"
    ├── Upload pipeline run history
    ├── Runtime prediction accuracy
    └── SLA breach risk heatmap
```

---

## Phase 7: Integration & Demo (Day 8-9)

```python
# scripts/run_demo.py

def run_full_demo():
    """One-click end-to-end demo."""
    # 1. Generate synthetic data (if not exists)
    # 2. Attach Ducklake
    # 3. Pick a pathological query
    # 4. Run through LangGraph agent
    # 5. Launch Streamlit with reasoning trace
    pass
```

---

## Dependencies (pyproject.toml)

```toml
[dependencies]
# Core
duckdb = ">=1.0"
ducklake = ">=0.2"

# Agent
langgraph = ">=0.3"
langchain = ">=0.3"
openai = ">=1.0"            # OpenRouter is OpenAI-compatible

# Data
pandas = ">=2.0"
pyarrow = ">=15.0"
numpy = ">=1.26"
faker = ">=25.0"

# ML
scikit-learn = ">=1.3"
xgboost = ">=2.0"

# UI
streamlit = ">=1.35"
plotly = ">=5.0"

# Dev
pytest = ">=8.0"
ruff = ">=0.4"
```

---

## Key Design Decisions

1. **Ducklake over Delta/Iceberg** — Zero infra, native DuckDB. Swap later if you need multi-engine.

2. **OpenRouter as LLM backend** — Already configured. Use OpenAI-compatible API with `base_url` pointing to OpenRouter. Cost-effective for iteration.

3. **Pathology-first data generation** — Decide what the agent should find, then reverse-engineer data. This guarantees the reasoning chain produces meaningful output.

4. **Evidence store is deterministic** — SQL queries only, no LLM. This prevents hallucination in the validation step.

5. **Critique loop is the moat** — The self-correction node is what makes this feel genuinely agentic vs a pipeline of prompts.

6. **Synthetic data scale: ~50-100GB** — Enough to demonstrate realistic behavior without being unwieldy on a laptop. Adjust `n_days` and `runs_per_day` to scale up/down.

---

## Execution Order

```
Day 1-2:  Phase 1 — Data generation (get the foundation right)
Day 3:    Phase 2 + 3 — Signal extraction + Evidence store
Day 4-6:  Phase 4 — LangGraph agent (the core)
Day 6-7:  Phase 5 — Prediction models (parallel with Phase 4 if split work)
Day 7-8:  Phase 6 — Streamlit UI
Day 8-9:  Phase 7 — Integration, polish, demo recording
```

**Total: ~9 days for a working end-to-end demo.**

---

## Competitive Landscape (Summary)

| Product | What It Does | Uses LLM? |
|---|---|---|
| Snowflake Acceleration | Auto-clustering, result caching | No (rule-based) |
| Databricks Predictive Optimization | Auto-stats, predictive I/O | No (ML stats only) |
| BigQuery Autoscaler | Slot allocation, recommendations | No (ML) |
| Spot by NetApp | Cloud cost optimization | No (rules + ML) |
| Vantage / Cloudability | FinOps dashboards | No |
| Releem (GitHub: 307★) | DB advisor for MySQL/PostgreSQL | No |
| datastoria (GitHub: 322★) | AI-native ClickHouse console | Partial (text-to-sql) |

**Your moat:** No product combines LLM-based agent reasoning (LangGraph multi-hop hypothesis validation) with query plan analysis for lakehouse cost optimization. The space is dominated by rule-based auto-tuning and ML prediction dashboards.
