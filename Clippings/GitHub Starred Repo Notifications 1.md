---
title: "GitHub Starred Repo Notifications"
source: "https://chatgpt.com/c/6a09ebb4-1400-83aa-b586-47315a1aa7e3"
author:
published:
created: 2026-05-26
description: "ChatGPT conversation with 18 messages"
tags:
  - "clippings"
---
**ChatGPT said**

Short answer: GitHub doesn’t give you this out of the box. “Stars” are basically bookmarks, not a signal for updates. If you want *summarised notifications*, you’ll need to build a thin automation layer on top. The good news: this is very doable—and honestly a solid little engineering system.

Let me lay out the cleanest architecture instead of hacks.

---

## 🚫 First, reality check

- Starring a repo ≠ subscribing to updates
- GitHub only notifies you if you explicitly **watch** a repo
- Even then, notifications are noisy and not summarised

So yeah, default UX is not aligned with what you want.

---

## 🧠 What you actually want (reframed)

> “Track repos I care about (starred), detect meaningful changes, summarise them, and push notifications.”

That’s a pipeline problem. Think: **data ingestion → filtering → summarisation → delivery**

---

## 🏗️ Recommended Architecture (lean but powerful)

### 1\. Source of truth: your starred repos

Use GitHub API:

- Endpoint: `GET /user/starred`
- Auth via Personal Access Token

Company: GitHub

---

### 2\. Detect changes (delta engine)

For each repo:

- Fetch:
	- commits (`/repos/{owner}/{repo}/commits`)
		- releases (`/releases`)
		- PRs (`/pulls`)
- Store last checked timestamp (Postgres / SQLite)

Only process **new activity since last run** → keeps it idempotent

---

### 3\. Summarisation layer (this is where it gets interesting)

Feed diffs / commit messages into an LLM:

- Cluster commits → reduce noise
- Generate:
	- “What changed”
		- “Why it matters”
		- “Impact level”

You can use:

- OpenAI API
- Or local LLM (since you like local-first setups)

---

### 4\. Notification layer

Pick your poison:

- Telegram bot (cleanest UX)
	- Telegram
- Email digest
- Slack webhook
- Or even Notion/Obsidian sync (since you’re into PKM)

---

### 5\. Scheduler

- Cron job / GitHub Actions / Airflow-lite
- Frequency: every 6–12 hours is enough

---

## ⚙️ Minimal Implementation Stack (your style)

Since you’re a data engineer, I’d go:

- Python (or your PowerShell + Python hybrid)
- Postgres (state tracking)
- Requests / httpx
- Small summarisation service

Optional upgrades:

- Redis → caching
- Celery → parallel processing
- Docker → portability

---

## 🔁 Workflow (end-to-end)

1. Fetch starred repos
2. Loop repos in parallel
3. Pull latest commits/releases
4. Compare with stored state
5. Summarise changes
6. Push notification
7. Update state

---

## 💬 Example notification (Telegram)

```
📦 Repo: apache/airflow

🔄 Updates (last 12h):
- 14 commits merged
- 2 PRs closed

🧠 Summary:
Airflow improved DAG parsing performance and fixed scheduler deadlocks.

⚠️ Impact:
Medium — relevant if you're using dynamic DAGs.

🔗 Link:
https://github.com/apache/airflow
```

---

## 🧩 Alternative (no-code-ish, but weaker)

If you don’t want to build:

- Use GitHub “Watch → Custom → Releases only”
- Pipe emails → Zapier → summarise → Telegram

But honestly? This gets messy fast and loses fidelity.

---

## 🧠 My take (opinionated)

Don’t treat this as a “notification tool.”  
Treat it as a **signal extraction system for code ecosystems**.

If you build it right, you can:

- Rank repos by activity quality
- Detect trends (e.g., “everyone is updating to X API”)
- Feed into your PKM (Obsidian notes auto-generated)

That’s way more valuable than just pings.

---

## 🚀 If you want next step

I can:

- Draft the Python repo structure
- Give you a working MVP script
- Add Telegram bot + summarisation
- Or design it as a production-grade pipeline (parallel, retry, rollback like your previous setup)

Just tell me how far you want to push this.

---

**You said**

I do not want to track any repo. I just want if I starred a GitHub repository, I should get a summary of repo

---

**ChatGPT said**

Got it—you don’t want a monitoring system, you want a **one-time intelligence brief the moment you hit “⭐ Star”**. That’s a very different (and much cleaner) problem.

Here’s the blunt truth first:

👉 **GitHub does not emit any event when you star a repo (for external consumers).**  
So there’s no native webhook, no trigger, nothing you can subscribe to.

Company: GitHub

---

## 🧠 So what’s the workaround?

You fake the “event”.

Instead of reacting *exactly at click time*, you:

- periodically check your starred repos
- detect **newly added ones**
- trigger summarisation **only once per repo**

This gives you the same UX without fighting GitHub’s limitations.

---

## ⚙️ Minimal, clean solution (no overengineering)

### Step 1 — Poll starred repos

API:

```
GET /user/starred
```

Store repo IDs locally (SQLite is enough)

---

### Step 2 — Detect “new star”

Compare:

- current starred list  
	vs
- previously seen list

👉 New repo = trigger summary

---

### Step 3 — Generate summary (this is the core value)

For each new repo, fetch:

- README
- Description
- Topics/tags
- Stars, forks
- Recent commits (optional)

Then summarise into something like:

```
📦 Repo: langchain-ai/langchain

🧠 What it is:
Framework for building LLM-powered applications using composable chains.

⚙️ Key features:
- Prompt chaining
- Tool integration
- Memory modules

📊 Signals:
⭐ 80k stars | High activity

💡 Why it matters:
Widely used for production LLM apps; ecosystem standard.

⚠️ Risk:
Rapidly evolving APIs (breaking changes likely)
```

You can use:

- OpenAI (API)
- or local LLM if you want control

---

### Step 4 — Notify yourself

Best options:

- Telegram → instant + clean
- Email → slower but fine
- Obsidian → auto-create note (this is actually 🔥 for your setup)

---

## 🔁 Execution model

Run every 10–30 minutes:

```
fetch_starred()
diff()
if new_repo:
    summarise()
    notify()
    save_state()
```

That’s it. No need for commit tracking, no noise, no complexity.

---

## 🧠 Opinionated take

This is actually a **high-leverage personal knowledge system**, not just a notifier.

If you push it slightly further, you can:

- auto-tag repos (AI, infra, data engineering, etc.)
- cluster similar repos
- build a “GitHub memory layer”

Basically: your stars stop being a junk drawer.

---

## ⚠️ What NOT to do

- Don’t try browser extensions to hook the click → brittle
- Don’t rely on email notifications → GitHub doesn’t send star-based ones
- Don’t overbuild with queues/workers → totally unnecessary here

---

## 🚀 If you want, I can give you:

- a **dead-simple Python script (~100 lines)** that does all this
- or a **production-grade version** with:
	- retries
		- parallel fetch
		- Telegram bot
		- Obsidian integration

Just say which direction:  
👉 “quick MVP” or “full system”

---

**ChatGPT said**

Short answer: **yes—but with constraints**. n8n can absolutely run this pipeline, but you need to accept one tradeoff:

👉 n8n is great for orchestration, not for heavy intelligence logic  
👉 So you either:

- keep logic inside n8n (simpler, slightly hacky), or
- offload intelligence to a small API (cleaner, more scalable)

I’ll show you a **pure n8n version first**, then where I’d draw the line.

---

## 🧠 What you’re building in n8n

Same pipeline, just visual:

```
Cron → GitHub (starred repos) → Compare (state)
     → IF new repo
         → Fetch repo + README
         → LLM Summary + Tags
         → Embedding
         → Similarity + Novelty (custom code)
         → Obsidian note
         → Email
         → Store state
```

---

## ⚙️ Core Nodes You’ll Use

- n8n → orchestration
- GitHub → API
- OpenAI → summarisation + embeddings
- Email node → notifications
- File node → Obsidian

---

## 🔁 Workflow Breakdown (Node-by-Node)

## 1\. Trigger

**Cron Node**

- Every 15 min

---

## 2\. Fetch Starred Repos

**HTTP Request Node**

```
GET https://api.github.com/user/starred
Authorization: Bearer {{GITHUB_TOKEN}}
```

---

## 3\. Detect New Stars (State Handling)

n8n doesn’t have a real DB unless you wire one.

👉 Use:

- SQLite node (best) OR
- n8n “Data Store” OR
- even a JSON file (MVP)

**Logic Node (Function):**

```javascript
const existing = $json.existing_ids || [];
const current = items.map(i => i.json.id.toString());

const newOnes = items.filter(i => !existing.includes(i.json.id.toString()));

return newOnes;
```

---

## 4\. Loop Through New Repos

Use **Split In Batches Node**

---

## 5\. Fetch Repo Details

Two HTTP nodes:

- `/repos/{owner}/{repo}`
- `/readme`

Decode README:

```javascript
const content = Buffer.from($json.content, 'base64').toString('utf-8');
return [{ content }];
```

---

## 6\. LLM Summary + Tagging

**OpenAI Node**

Prompt:

```
Summarize this GitHub repo.

Return JSON:
{
 "summary": "...",
 "tags": ["", ""],
 "category": "",
 "confidence": 0-1
}

DATA:
{{$json.readme}}
```

---

## 7\. Embeddings

**OpenAI Embeddings Node**

- Input: summary

Store vector in n8n datastore or external DB

---

## ⚠️ Reality Check: Similarity + Novelty in n8n

This is where things get… not pretty.

You’ll need a **Function Node**:

```javascript
function cosine(a, b) {
  let dot = 0, magA = 0, magB = 0;
  for (let i = 0; i < a.length; i++) {
    dot += a[i] * b[i];
    magA += a[i] * a[i];
    magB += b[i] * b[i];
  }
  return dot / (Math.sqrt(magA) * Math.sqrt(magB));
}

const newVec = $json.embedding;
const existing = $json.all_embeddings || [];

let maxSim = 0;
let similar = [];

for (const item of existing) {
  const sim = cosine(newVec, item.embedding);
  if (sim > 0.75) {
    similar.push({ name: item.name, score: sim });
  }
  if (sim > maxSim) maxSim = sim;
}

return [{
  similarity: similar.sort((a,b)=>b.score-a.score).slice(0,5),
  novelty: 1 - maxSim
}];
```

👉 This works… but it’s not elegant.

---

## 8\. Obsidian Note Creation

**Write Binary File Node**

Path:

```bash
/your-vault/{{repo_name}}.md
```

Content template:

```markdown
# {{$json.repo}}

## Summary
{{$json.summary}}

## Tags
{{$json.tags.join(' ')}}

## Similar Repos
{{#each $json.similarity}}
- [[{{this.name}}]] ({{this.score}})
{{/each}}

## Novelty
{{$json.novelty}}
```

---

## 9\. Email Notification

Use **Email Node**

---

## 🧠 My blunt take (important)

n8n version is:

### ✅ Great for:

- orchestration
- quick automation
- visibility

### ❌ Weak for:

- embeddings at scale
- similarity search
- graph logic
- performance

---

## 🧠 Recommended Hybrid (this is what I’d actually do)

Let n8n orchestrate, but outsource intelligence:

```
n8n → calls → your Python API (gh-intel core)
                ↓
         returns:
         - summary
         - tags
         - similarity
         - novelty
```

Why?

- cleaner logic
- reusable outside n8n
- faster iteration
- no JavaScript math hacks

---

## 🚀 If you want next step

I can:

1. **Export a ready-to-import n8n workflow JSON**
2. Build a **hybrid version (n8n + your Python engine)**
3. Add **Telegram + Obsidian bidirectional linking in n8n**
4. Add **vector DB (Qdrant) integration**

---

## 🧠 Final thought

Pure n8n = “automation tool”  
Hybrid system = **“personal intelligence platform”**

You’ve already done the hard thinking—don’t downgrade the architecture just for convenience.

---

If you want the actual n8n JSON workflow, say:  
👉 *“give me n8n workflow export”*

---

**You said**

Suggest a GitHub repository name for this app

---

**ChatGPT said**

You’ve built something more than a utility script—it’s basically a **personal dev intelligence engine**. So the name should reflect *signal extraction + knowledge graph + GitHub context*, not just “star notifier”.

I’ll give you options across styles, with blunt opinions so you don’t pick something forgettable.

---

## 🧠 Strong, brandable (my top picks)

- **RepoSage** → clean, memorable, implies insight
- **StarMind** → stars → intelligence layer (simple, sharp)
- **CodeScry** → “scrying” = seeing hidden patterns (underrated vibe)
- **DevIntel** → boring but powerful, enterprise-ready
- **GraphForge** → emphasizes knowledge graph angle
- **SignalHub** → you’re extracting signal from noise

👉 If you want one name that scales: **RepoSage**

---

## ⚙️ Technical / descriptive (clear but less sexy)

- **gh-intel** (what you already used — solid CLI name)
- **github-intelligence-engine**
- **star2knowledge**
- **repo-insight-engine**
- **github-semantic-index**

👉 These are great for clarity, weak for recall.

---

## 🔬 Data/AI flavored (your background shows here)

- **EmbedHub**
- **VectorVault**
- **RepoVec**
- **SemanticStars**
- **LatentRepos**

👉 Slightly niche, but signals “this isn’t basic automation”

---

## 🧠 PKM / Obsidian aligned

- **RepoBrain**
- **CodeVault**
- **DevSecondBrain**
- **StarGraph**
- **RepoAtlas**

👉 These align well with your Obsidian + PKM direction

---

## 🚀 Opinionated ranking (no fence-sitting)

If I had to pick:

1. **RepoSage** → best balance (brand + meaning)
2. **StarMind** → clean and intuitive
3. **GraphForge** → strong if you lean into graph features
4. **DevIntel** → if you want enterprise vibe
5. **gh-intel** → best CLI/tooling name

---

## 🧠 Naming strategy (quick sanity check)

Avoid:

- “awesome”, “ultimate”, “smart” → noise
- overly long names → nobody types them
- too niche (e.g., “obsidian-star-embedding-engine”)

Aim for:

- 2 words max
- easy to say
- hint of intelligence / insight

---

## 💡 My straight recommendation

👉 Use:

- **RepoSage** (repo name)
- **gh-intel** (CLI command)

That combo is clean, scalable, and actually feels like a product.

---

If you want, I can also:

- check name availability on GitHub
- generate logo ideas / branding
- or suggest a tagline that doesn’t sound cringe

Just say 👍

---

**You said**

I need to do hybrid setup using n8n. Help me with it

---

**ChatGPT said**

Good instinct. A **hybrid setup** is the sweet spot: let **n8n** handle orchestration and notifications, and keep your Python engine (gh-intel) doing the heavy lifting (embeddings, similarity, novelty, linking). You get reliability + maintainability without turning n8n into a math engine.

Let’s wire this cleanly.

---

## 🧠 Architecture (hybrid, production-sane)

```
Cron (n8n)
   ↓
GitHub API (starred repos)
   ↓
Diff (new stars)
   ↓
HTTP → gh-intel service (your Python API)
   ↓
Returns:
  - summary
  - tags (llm + manual)
  - similarity
  - novelty
   ↓
n8n:
  - write Obsidian note
  - send email / Telegram
  - persist state
```

**Why this split works:**

- n8n = scheduling, retries, visibility
- Python = intelligence (vector math, tagging, graph logic)

---

## ⚙️ Step 1 — Wrap your Python into a tiny API

Use **FastAPI**. Keep it lean.

### app.py

```python
from fastapi import FastAPI
from pydantic import BaseModel

from gh_intel.ai.summarizer import summarize
from gh_intel.ai.embeddings import get_embedding
from gh_intel.ai.tagging import llm_tags, merge_tags
from gh_intel.intelligence.similarity import top_similar
from gh_intel.intelligence.novelty import compute_novelty
from gh_intel.db import load_all_embeddings, save_embedding

app = FastAPI()

class RepoInput(BaseModel):
    full_name: str
    description: str = ""
    readme: str = ""

@app.post("/process")
def process_repo(data: RepoInput):
    summary = summarize(
        {"full_name": data.full_name, "description": data.description},
        data.readme
    )

    embedding = get_embedding(summary)
    existing = load_all_embeddings()

    similar = top_similar(embedding, existing)
    novelty = compute_novelty(
        embedding,
        [v["embedding"] for v in existing.values()]
    )

    llm_output = llm_tags(summary)
    tag_data = merge_tags(llm_output, manual_tags=[])

    save_embedding(data.full_name, embedding)

    return {
        "summary": summary,
        "tags": tag_data,
        "similar": similar,
        "novelty": novelty
    }
```

Run it:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

---

## 🔁 Step 2 — n8n Workflow (node-by-node)

## 1\. Cron Trigger

- Every 15 min

---

## 2\. GitHub → Fetch starred repos

HTTP Node:

```
GET https://api.github.com/user/starred
Authorization: Bearer {{GITHUB_TOKEN}}
```

---

## 3\. Detect new stars (state)

Use:

- n8n Data Store OR SQLite

Function Node:

```javascript
const seen = $json.seen || [];
return items.filter(i => !seen.includes(i.json.id.toString()));
```

---

## 4\. Split in batches

- Avoid rate limits

---

## 5\. Fetch repo + README

Two HTTP nodes:

- `/repos/{owner}/{repo}`
- `/readme` (decode base64)

---

## 6\. Call your Python service

HTTP Node:

```
POST http://<your-server>:8000/process
Content-Type: application/json
```

Body:

```json
{
  "full_name": "{{ $json.full_name }}",
  "description": "{{ $json.description }}",
  "readme": "{{ $json.readme }}"
}
```

---

## 7\. Create Obsidian note

Use **Write File Node**

Path:

```bash
/obsidian-vault/{{ $json.full_name.replace('/', '_') }}.md
```

Content:

```markdown
# {{$json.full_name}}

## Summary
{{$json.summary}}

## Tags
LLM: {{$json.tags.llm_tags}}
Manual: {{$json.tags.manual_tags}}

## Similar Repos
{{#each $json.similar}}
- [[{{this[1].replace('/', '_')}}]] ({{this[2].toFixed(2)}})
{{/each}}

## Novelty
{{$json.novelty}}
```

---

## 8\. Email / Telegram

Use:

- Email Node OR
- Telegram Node via Telegram

---

## 9\. Persist state

Store repo IDs → prevents reprocessing

---

## 🧠 Design Decisions (don’t skip)

### 1\. Keep intelligence out of n8n

If you try to do embeddings + similarity inside n8n:

- performance tanks
- logic becomes unreadable
- debugging becomes pain

### 2\. Your API becomes reusable

Same `/process` endpoint can later power:

- CLI
- UI dashboard
- batch processing

### 3\. This scales cleanly

You can later:

- swap SQLite → vector DB
- add caching
- batch embeddings

without touching n8n

---

## 🚀 Optional upgrades (high ROI)

### 1\. Queue layer

If load increases:

- add Redis queue between n8n → API

---

### 2\. Add /similar endpoint

So you can query:

> “show me similar repos to X”

---

### 3\. Store results in JSON for audit

So you don’t recompute unnecessarily

---

## ⚠️ Common mistakes (seen this too often)

- ❌ stuffing all logic into n8n Function nodes
- ❌ not storing embeddings persistently
- ❌ no retry strategy → random failures
- ❌ writing messy Obsidian notes (you’ll stop using it)

---

## 🧠 Final take

This hybrid model gives you:

- orchestration clarity (n8n)
- intelligence power (Python)
- extensibility (API-first design)

You’ve basically built a **personal developer intelligence platform** —not joking.

---

If you want next step, I can:

- export a **ready-to-import n8n workflow JSON**
- dockerize this setup (n8n + API + DB)
- add **Telegram bot with inline actions (tag/edit/reject)**

Just tell me where you want to take it.