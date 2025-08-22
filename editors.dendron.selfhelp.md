---
id: lok36ccnd2x0gcta4fezjb1
title: Selfhelp
desc: ''
updated: 1753022175534
created: 1753021939511
---

#tag.pkm.dendron.quicknotes

Alright, you're diving into **Dendron**—the *VS Code-powered brain extension*—and you want the express lane. Perfect. Dendron isn’t your average note app; it’s a **hierarchical, markdown-first, dev-friendly PKM system** that behaves more like a knowledge graph crossed with a file system. Most people get lost in features. You're going to dominate the **20% of Dendron that gives 80% of its value**—fast.

---

## 🚀 Dendron in Record Time: The Ruthlessly Efficient Mastery Plan

---

### 🎯 Phase 0: What’s the *Point* of Dendron?

> Think like a dev, not a diarist.

* 🌲 **Hierarchies** = Namespaces (not folders)
* ⚙️ **CLI + Commands** = Fast note creation, linking, publishing
* 🧠 **Second brain** = One vault, all domains, organized by schema
* 💥 **Speed over structure**: Don't organize before you write—Dendron **organizes as you write**.

---

### 🛠️ Phase 1: Setup That Doesn’t Suck (30 Minutes Max)

**Install Dendron the Right Way:**

1. Install **VS Code**
2. Install **Dendron extension**
3. Open Command Palette → `>Dendron: Initialize Workspace`
4. Choose **"Create Single Vault Workspace"**

Done. That’s it. Skip multi-vaults unless you *love* complexity.

---

### 🔥 Phase 2: The 5 Moves of Dendron Mastery (Core 20%)

#### ✅ 1. `Ctrl+L` – *Lookup Notes, Fast*

* Type `project.devops.pipeline`, and boom—it creates or opens that note.
* This is your **note creation, search, and edit** all in one.
* Use dot notation like a namespace:
  `tech.linux.commands.top` → creates structured hierarchy instantly.

#### ✅ 2. Use the **Dendron CLI**

```bash
npx dendron-cli doctor
npx dendron-cli publish export
npx dendron-cli seed add github:username/repo
```

* Get health checks, export to static site, or pull in “seed notes” (like starter kits).

#### ✅ 3. Master the **Daily Journal Flow**

Use `> Dendron: Create Daily Note`

* Automatically creates `daily.2025.05.17` (or whatever date)
* Set a hotkey for journaling. (Yes, automate it.)
* Use templates to auto-fill headers/tasks.

#### ✅ 4. Use **Note References & Links**

* `[[project.devops.pipeline]]` – link to another note
* `![[note.image.png]]` – embed images/diagrams
* `[[^block-id]]` – block reference = Dendron sorcery

> **Every link is an atomic relationship**—this builds your brain graph.

#### ✅ 5. Planting vs Linking (🌱 vs 🔗)

* **Plant a note**: `project.ai.models.transformers`
* **Link existing**: just use `[[ ]]`
* Don't pre-structure—**plant as you go**. Structure will emerge.

---

### 🧩 Phase 3: Templates + Task System (1 Day)

* Create a `.vscode/templates` folder.
* Add `project.md`, `daily.md`, `meeting.md`, `journal.md`
* Then set hotkeys or command palette access for template use.

Templates = **pre-fab scaffolding for your thoughts**.

```markdown
# {{title}}

## Context
- 

## Key Points

## Links
- [[related.note]]
```

---

### 🧠 Phase 4: Hierarchies = Taxonomy That Works *For You*

Skip folders. Just **use dot notation**:

* `project.client.acme`
* `project.client.acme.meeting.2025-05-17`
* `project.client.acme.requirements`
* `project.client.acme.deployments.pipeline`

This becomes **auto-tagging + self-organizing**.

**Use `Dendron: View Hierarchy` to see the tree.**

---

### 🌍 Phase 5: Publish Your Notes as a Site (Optional but Sexy)

```bash
npx dendron-cli publish export
```

* Outputs your vault to a static site.
* Add a `netlify.toml` or push to GitHub Pages for full public PKM glory.
* Bonus: Add `custom.css` and theme your brain.

---

### 🛡️ Bonus Pro Moves (When You're Ready to Show Off)

| Move                  | What It Does                                       |
| --------------------- | -------------------------------------------------- |
| `dendron.yml` config  | Full vault control (publishing, schemas)           |
| `schema.json`         | Define types of notes (like Templater on steroids) |
| Seeding Notes         | Pull in other people's vaults as modules           |
| Graph View            | Visualizes linked notes like a neural net          |
| `Ctrl+Shift+P` macros | Power command execution via command palette        |

---

### 📈 The 20% Recap

| Feature           | Result                                 |
| ----------------- | -------------------------------------- |
| Lookup Notes      | 10x speed in navigating + creating     |
| Hierarchical Tags | Context-rich note structure            |
| Templates         | Instant scaffolding                    |
| Daily Notes       | Workflow logging + journaling          |
| Graph Linking     | Contextual thought networks            |
| CLI + Publishing  | Portability + public knowledge sharing |

---
