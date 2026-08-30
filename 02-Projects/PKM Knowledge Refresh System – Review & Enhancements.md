# AI Summary
A comprehensive architecture proposal for an automated knowledge refresh system that continuously resurfaces, synthesizes, and prioritizes valuable notes instead of merely collecting information. The design includes daily knowledge refreshes, weekly synthesis reports, monthly growth reviews, weighted note scoring, project-aware prioritization, stale knowledge detection, question tracking, knowledge evolution analysis, capture-to-insight metrics, implementation phases, and a lightweight Python-based architecture integrated with Obsidian and Discord. The emphasis is on long-term knowledge compounding through retrieval, reflection, and synthesis while avoiding unnecessary complexity such as RAG or vector databases.

---
## Objective
Create a lightweight, automated knowledge resurfacing system that improves retention, synthesis, and long-term expertise development. The system should prioritize rediscovering and connecting existing knowledge rather than generating notifications about newly created notes.

---
## Core Components
### Daily Knowledge Refresh
Deliver a daily summary containing:
* 1 Concept Note
* 1 Architecture Decision Record (ADR)
* 1 Project Insight
* 1 Open Question
Goal:
* Reinforce important knowledge
* Encourage retrieval and reflection
* Surface forgotten but valuable information
Preferred delivery channels:
* Discord
* Slack
* Email
Preferred channel: Discord.
---
### Weekly Knowledge Synthesis
Analyze notes modified during the previous seven days and generate:
* Major concepts explored
* New connections discovered
* Decisions made
* Emerging questions
* Career-relevant insights
Goal:
* Move from information collection to knowledge synthesis.
---
### Monthly Growth Review
Generate a report containing:
### Activity Metrics
* Notes created
* Notes modified
* ADRs created
* Questions resolved
* Projects active
* Links added
### Learning Analysis
* Major themes explored
* Areas of increasing expertise
* Neglected topics
* Repeated questions
* Potential blind spots
* Suggested focus areas for next month
Goal:
* Act as a personal engineering and learning review.
---
## Daily Note Selection Strategy
Notes should not be selected randomly.
### Base Scoring Formula
```python
score = (
    days_since_last_surfaced * 0.7 +
    note_age_days * 0.2 +
    link_count * 0.1
)
```
### Factors
#### Days Since Last Surfaced (70%)
Primary factor.
* Older resurfacing intervals increase priority.
* Creates a lightweight spaced-repetition effect.
* Track when the system last surfaced a note rather than relying on manual review tracking.
#### Note Age (20%)
* Gives historical knowledge a chance to reappear.
* Prevents older notes from being forgotten.
#### Link Count (10%)
* Prioritizes foundational and highly connected concepts.
* Encourages resurfacing of important knowledge hubs.
### Enhanced Scoring Formula
```python
score = (
    days_since_last_surfaced * 0.5 +
    note_age_days * 0.1 +
    link_count * 0.1 +
    open_question_bonus * 0.15 +
    active_project_bonus * 0.15
)
```
### Additional Signals
* Open questions
* Active project relevance
* Recent edits
* ADR importance
* Career-related content
### Cooldown Rules
Avoid resurfacing the same note within a configurable cooldown period.
Suggested range:
* 14–30 days
---
## Required Metadata
### Note Classification
Every note should belong to a category:
```yaml
type: concept
type: adr
type: project
type: question
```
Purpose:
* Prevent random notes from entering refresh cycles.
* Ensure balanced daily summaries.
### Surfacing Metadata
Track:
```json
{
  "note_id": "iceberg-metadata",
  "last_surfaced": "2026-06-24",
  "surfaced_count": 4
}
```
Store externally to avoid cluttering notes.

---
## Synthesis Notes
Not all notes are equally valuable.
The system should prioritize synthesis notes periodically.
Example:
Individual Notes:
```text
CDC
Data Vault
Medallion
Event Streaming
```
Synthesis Note:
```text
Patterns for Near Real-Time Data Platforms
```
Goal:
* Surface conclusions and frameworks, not just facts.
---
## Active Project Weighting
Knowledge related to active work should receive additional priority.
Example:
```yaml
project: healthcare-platform
```
Scoring bonus:
```python
score += active_project_bonus
```
Potential projects:
* Healthcare Platform
* Data Engineering
* AI Agents
* Career Development
Goal:
* Increase relevance of daily refreshes.
---
## Open Questions Dashboard
Maintain a centralized repository of unresolved questions.
Track:
### New Questions
Recently discovered areas for exploration.
### Oldest Questions
Questions unresolved for extended periods.
### Most Referenced Questions
Questions appearing across multiple notes and projects.
Example:
```text
Top Unresolved Topics
- Iceberg Metadata Internals
- AQE Optimization
- Data Contract Governance
```
Goal:
* Turn unanswered questions into a learning roadmap.
---
## Stale Knowledge Detection
Some notes become outdated.
Monthly analysis should identify:
* Version-specific content
* Notes untouched for 12+ months
* Topics superseded by newer information
Example:
```text
Potentially Stale Notes
- Databricks Runtime 13 Notes
- Deprecated LangChain Patterns
- Legacy Snowflake Features
```
Goal:
* Keep the knowledge base relevant.
---
## Knowledge Evolution Tracking
Monthly reports should identify shifts in understanding.
Example:
```text
January:
Data Vault appears overly complex.
June:
Data Vault is useful when auditability and historical lineage matter.
```
Goal:
* Track changes in reasoning and expertise over time.
---
## Capture-to-Insight Metrics
Monitor whether the system is creating understanding or simply collecting information.
Track:
```text
Notes Created: 42
Notes Referenced: 19
Synthesis Notes Created: 3
ADRs Created: 2
Questions Closed: 7
```
Interpretation:
```text
Created >> Referenced
```
Indicates excessive collection.
```text
Referenced >> Created
```
Indicates active learning and knowledge reuse.
Goal:
* Measure knowledge compounding rather than note accumulation.
---
## Recommended Architecture
```text
Obsidian Vault
     ↓
Git
     ↓
Python Scripts
     ↓
OpenRouter / Local LLM
     ↓
Discord / Slack / Email
```
---
## Technology Recommendations
### Orchestration
* Python (preferred)
* n8n (optional)
* Hermes Agent (optional orchestration layer)
### LLM Usage
Daily Refresh:
* Gemini Flash
* Qwen
* DeepSeek
Weekly Synthesis:
* Claude Sonnet
* Gemini Pro
* Strong reasoning models
Monthly Review:
* Claude Opus
* GPT-class flagship models
* Gemini Pro tier
---
## Implementation Roadmap
### Phase 1 (MVP)
* Daily refresh
* Weekly synthesis
* Monthly report
* Note scoring
* Discord delivery
### Phase 2
* Question dashboard
* Active project weighting
* Stale note detection
### Phase 3
* Knowledge evolution tracking
* Capture-to-insight metrics
* Synthesis note prioritization
---
## Explicitly Avoid (For Now)
Do not introduce unless a clear need emerges:
* Vector databases
* RAG pipelines
* Embedding stores
* Knowledge graph databases
* Multi-agent architectures
* MCP integrations
---
## Success Criteria
The system succeeds if it:
* Regularly resurfaces forgotten knowledge
* Produces useful synthesis and insights
* Highlights unanswered questions
* Prioritizes active work and career goals
* Tracks growth in expertise over time
* Remains simple enough to maintain long term
* Encourages knowledge compounding rather than note accumulation
