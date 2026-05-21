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