# AI Summary
00 Prompts. Reusable LLM prompt templates. Pick by goal, not by file name

```table-of-contents
```

# 00 Prompts

Reusable LLM prompt templates. Pick by goal, not by file name.

## Quick-pick

| I want to… | Use this |
|---|---|
| Tailor my resume to a JD | [[Resume — Optimization]] |
| Get my CV past ATS filters | [[ATS — Hard Mode]] |
| Write a cover letter | [[Cover Letter]] |
| Prep for an interview loop | [[Interview — Prep]] |
| Audit / rewrite my LinkedIn | [[LinkedIn — Profile Audit]] |
| Rewrite my GitHub profile README | [[Profile — README Rewrite]] |
| Deep-analyze a repo before adopting it | [[Repo — Deep Analysis]] |
| Decide whether a tool is worth 30 sec of my time | [[Quick Summary]] |
| Get a deep architectural breakdown of a tool | [[Deep Dive]] |
| Wrap a session with full handoff | [[End of Session — Handoff]] |
| Update today's daily note from a session | [[Daily Note — Update]] |
| Extract session corrections into a feedback.md | [[Feedback — Extract]] |

## Folders

- **[[Career]]** — resume, cover letter, interview prep, ATS hard-mode, LinkedIn.
- **[[GitHub]]** — own-profile rewrite, third-party repo analysis.
- **[[Tools]]** — quick 1-liner triage + deep architectural breakdown (paired).
- **[[Session]]** — end-of-session handoff, daily note, feedback extraction.
- **[[_archive]]** — output artifacts (not prompts). Reference only.

## Conventions

- Every file has YAML frontmatter (`description`, `use_when`, `inputs`, `outputs`, `related`, `tags`).
- `Related:` block at the bottom links to nearby prompts.
- Multi-word names use em-dash (`Topic — Subtopic.md`), per repo convention.
- Prompts are templates — paste the `[paste]` slots with your own content.

## Adding a new prompt

1. Pick the right subfolder. If none fits, propose one in your next session.
2. Copy an existing file as a template — keep the frontmatter + `Related:` block.
3. Use `[[Wikilink]]`-style Obsidian cross-references, never plain markdown links.
4. Update this README's quick-pick table.
