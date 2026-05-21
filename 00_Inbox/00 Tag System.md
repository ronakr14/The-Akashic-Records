# Obsidian Tag System — The Akashic Records

## Philosophy
Tags = cross-reference system, not folders. Minimal, flat, purposeful.

## Tag Taxonomy

### #status
Purpose: Track note lifecycle
Values: #status/active #status/wip #status/archived #status/done

### #area
Purpose: Broad life/work category
Values: #area/projects #area/knowledge #area/career #area/personal

### #type
Purpose: Note format/function
Values: #type/note #type/prompt #type/process #type/reference #type/moc

### #tool
Purpose: Tools explicitly studied or configured
Values: (e.g., #tool/claude #tool/obsidian #tool/airflow)

### #concept
Purpose: Technical concept captured
Values: #concept/data-engineering #concept/llm #concept/rag #concept/sql

---

## Usage Rules

1. Max 5 tags per note
2. Always include #type tag
3. Use #status/wip for incomplete notes
4. #tool only when note is about the tool itself
5. #area optional — only if note spans categories

---

## Tag Assignment Examples

| Note | Tags |
|------|------|
| Career/job search prompts | #type/prompt #area/career #status/active |
| SPARQ Process (ConcertAI) | #type/process #area/projects #status/wip |
| Software Engineer Playbook | #type/reference #concept/data-engineering #status/done |
| Blog draft (ETL Monkey) | #type/note #area/knowledge #status/done |
| MOC for blog series | #type/moc #area/knowledge |

---

## Filename Conventions

- MOCs: `00 [Name] MOC.md`
- Process docs: `01 SPARQ Process.md`
- Prompts: `[Topic] Prompts.md`
- Daily notes: `YYYY-MM-DD.md`

Frontmatter template:
```yaml
---
title: Note Title
tags: [#type/note, #area/knowledge, #status/active]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```