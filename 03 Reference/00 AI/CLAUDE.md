# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
This repository is an Obsidian vault for personal knowledge management (The Akashic Records). It contains notes, prompts, references, and system documentation organized in a hierarchical folder structure.

## Common Commands
- **Open vault**: Launch Obsidian and open this folder as a vault.
- **Search notes**: Use Obsidian's quick switcher (Ctrl+O) or global search (Ctrl+Shift+F).
- **Create new note**: Use Obsidian's "New note" button or copy a template from `00 Tag System.md` frontmatter.
- **Edit notes**: Directly edit `.md` files with any text editor; changes sync with Obsidian.
- **No build/lint/test**: This vault contains only markdown files; no compilation or testing required.

## Vault Structure
- `00 Tag System.md` – Defines tag taxonomy and usage rules.
- `02 Areas - Ongoing/` – Active work areas (projects, career, personal).
- `03 Knowledge - Curated/` – Curated knowledge notes on various topics.
- `04 Resources - Reference/` – Reference materials and cheatsheets.
- `05 Output/` – Generated content (blogs, drafts, series).
- `06 Systems/` – System configurations and process documentation.
- `07 Prompts/` – Collections of prompts for LLMs, automation, etc.
- `Attachments/` – Images, PDFs, and other media attached to notes.
- `.obsidian/` – Obsidian configuration and plugin data.
- `.smart-env/` – Smart environment metadata (likely for plugin integrations).
- `Tool Summaries.md` – Comparative notes on various tools and alternatives.

## Naming Conventions
- **MOCs (Maps of Content)**: `00 [Name] MOC.md`
- **Process documents**: `01 [Name] Process.md`
- **Prompt collections**: `[Topic] Prompts.md`
- **Daily notes**: `YYYY-MM-DD.md`
- **Frontmatter** (optional): Includes title, tags, created, updated dates.

## Tag System
See `00 Tag System.md` for detailed rules. Key points:
- Max 5 tags per note.
- Always include a `#type` tag (e.g., `#type/note`, `#type/process`).
- Use `#status/wip` for incomplete notes.
- `#area` optional; only for cross‑area notes.
- `#tool` only when note is about the tool itself.

## Working with Claude Code
- Read/search files using Glob, Grep, Read tools.
- Edit notes via Edit or Write tools (preserve frontmatter if present).
- Apply tag updates by editing frontmatter or inline tags.
- Create new notes by writing a new `.md` file with appropriate frontmatter.
- Respect existing conventions; when in doubt, consult `00 Tag System.md`.

## Notes
- This vault is primarily for personal knowledge; avoid committing large binary files.
- Keep commit messages descriptive; see existing commits for style.
- Plugin configurations live in `.obsidian/plugins/`; do not modify unless adding/removing plugins.
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview
This is an Obsidian vault for personal knowledge base (The Akashic Records). It contains markdown notes on various topics, primarily focused on data engineering, AI, and software development.

## Common Commands
There are no build, lint, or test commands as this is a knowledge base vault, not a software project.
- To view or edit notes: Use any markdown editor or the Obsidian app.
- To search notes: Use Obsidian's built-in search or `grep` from the command line.
- To sync with Obsidian: Use the Obsidian app with this vault folder.

## Vault Structure
- Notes are stored as `.md` files in the root and subdirectories.
- The `.obsidian` directory contains Obsidian configuration and installed plugins.
- Organization is primarily through folders and tags (managed by Obsidian).
- See `.gitignore` for ignored files (e.g., build artifacts, IDE directories).

## Development Notes
This repository does not contain source code requiring compilation or testing.
If contributing notes, follow existing markdown conventions and ensure proper file naming.

2
## 📌 Topic Overview

**Claude** is:

* An advanced **large language model AI assistant** by Anthropic.
* Built with a focus on:

  * **Safety-first AI**: minimizing hallucinations, biased outputs.
  * **User intent alignment**: better understanding and following instructions.
* Accessible via API or integrated in chat platforms.
* Suitable for:

  * Content generation
  * Code assistance
  * Research summarization
  * Complex reasoning tasks

**Why Master Claude?**

* Next-level safe and reliable AI collaboration.
* Enables building AI-powered apps with enhanced trust.
* Offers API integration similar to OpenAI but with unique strengths in ethics.

---

## ⚡ 80/20 Roadmap

| Stage  | Focus Area                                       | Why?                                                    |
| ------ | ------------------------------------------------ | ------------------------------------------------------- |
| **1**  | Understanding Claude’s API & Pricing             | Efficient usage and cost control.                       |
| **2**  | Prompt engineering & best practices              | Maximize response quality and alignment.                |
| **3**  | Conversational AI design                         | Build flows that leverage Claude’s dialogue strengths.  |
| **4**  | Handling safety & moderation filters             | Avoid triggering AI guardrails.                         |
| **5**  | Integrating Claude in products (chatbots, tools) | Practical deployment.                                   |
| **6**  | Advanced multi-turn context management           | Maintain session state and memory.                      |
| **7**  | Fine-tuning / customization options              | Tailor Claude for domain-specific tasks (if available). |
| **8**  | Benchmarking vs other LLMs                       | Understand strengths and tradeoffs.                     |
| **9**  | Ethical AI considerations                        | Ensure responsible use.                                 |
| **10** | Monitoring and feedback loops                    | Continuously improve prompt quality and usage.          |

---

## 🚀 Practical Tasks

| Task                                                              | Description |
| ----------------------------------------------------------------- | ----------- |
| 🔥 Set up API keys and basic Claude API call.                     |             |
| 🔥 Design prompts to generate well-structured outputs.            |             |
| 🔥 Build a conversational chatbot with multi-turn context.        |             |
| 🔥 Implement content filtering to respect safety guidelines.      |             |
| 🔥 Integrate Claude with Slack or web app via API.                |             |
| 🔥 Create summarization tools for long documents.                 |             |
| 🔥 Build a code helper that suggests fixes or generates snippets. |             |
| 🔥 Log interactions for audit and improvement.                    |             |
| 🔥 Experiment with prompt templates to improve accuracy.          |             |
| 🔥 Compare Claude responses to GPT and optimize usage.            |             |

---

## 🧾 Cheat Sheets

* **Basic API call (Python)**:

```python
import requests

url = "https://api.anthropic.com/v1/complete"
headers = {
    "x-api-key": "YOUR_API_KEY",
    "Content-Type": "application/json",
}
data = {
    "model": "claude-v1",
    "prompt": "Human: What is quantum computing?\n\nAssistant:",
    "max_tokens_to_sample": 300,
    "stop_sequences": ["\n\nHuman:"]
}
response = requests.post(url, headers=headers, json=data)
print(response.json()["completion"])
```

* **Prompt structure tips**:

  * Use clear “Human:” and “Assistant:” roles.
  * Provide explicit instructions.
  * Use “stop\_sequences” to avoid run-on text.
  * Break down complex tasks step-by-step.

---

## 🎯 Progressive Challenges

| Level           | Challenge                                                                 |
| --------------- | ------------------------------------------------------------------------- |
| 🥉 Easy         | Generate FAQ answers from static data.                                    |
| 🥈 Intermediate | Build a multi-turn customer support chatbot.                              |
| 🥇 Expert       | Implement a domain-specific assistant with prompt chaining.               |
| 🏆 Black Belt   | Create a Claude-powered code review assistant integrated into GitHub PRs. |

---

## 🎙️ Interview Q\&A

* **Q:** What differentiates Claude from OpenAI’s GPT models?
* **Q:** How does Claude’s safety-first design affect prompt engineering?
* **Q:** What strategies improve multi-turn conversational context in Claude?
* **Q:** How do you handle rate limits and usage costs efficiently?
* **Q:** Explain how to integrate Claude in existing chat apps.

---

## 🛣️ Next Tech Stack Recommendation

After Claude mastery:

* **LangChain** — Build agentic AI workflows incorporating Claude.
* **Vector DBs (Chroma, Pinecone)** — For retrieval-augmented generation.
* **Ollama / Local LLMs** — Hybrid cloud/local AI strategies.
* **Monitoring tools (Prometheus, Grafana)** — Track AI usage & performance.
* **Ethics frameworks** — For responsible AI development.

---

## 🎩 Pro Ops Tips

* Always prefix prompts with explicit roles (Human/Assistant) for clarity.
* Use system-level instructions to guide Claude’s tone and behavior.
* Cache frequent responses to reduce API calls and costs.
* Log and review flagged outputs to refine prompts.
* Regularly test Claude’s responses on edge cases and adversarial inputs.

---

## ⚔️ Tactical Philosophy

**Claude isn’t just a chatbot; it’s your ethical AI co-pilot designed for trustworthy, aligned intelligence.**

Mastering Claude means mastering **safe, reliable, and effective AI integration**.

---
