#!/usr/bin/env python3
"""
PKM Knowledge Refresh System — Daily Refresher
Scans the Obsidian vault, classifies notes, scores them using a
spaced-repetition heuristic, and produces a daily review message.

Phase 1: Daily refresh only (concept + ADR + project + question).
"""

import json
import os
import re
from datetime import date, datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
VAULT_ROOT = Path(__file__).resolve().parent.parent.parent
OUTPUT_DIR = VAULT_ROOT / "00 Daily Review"
STATE_FILE = Path(__file__).resolve().parent / "refresher_state.json"
COOLDOWN_DAYS = 14

# Scoring weights (enhanced formula)
W_DAYS_SINCE = 0.5
W_NOTE_AGE = 0.1
W_LINK_COUNT = 0.1
W_OPEN_QUESTION = 0.15
W_ACTIVE_PROJECT = 0.15

# Skip directories
SKIP_DIRS = {".obsidian", ".git", "00 Daily Review"}

# Frontmatter regex
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
TYPE_RE = re.compile(r"^\s*type\s*:\s*(.+?)\s*$", re.MULTILINE)
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")

# Classification keywords
ADR_KEYWORDS = re.compile(r"\b(ADR|Decision|Trade[- ]off)\b", re.IGNORECASE)
QUESTION_KEYWORDS = re.compile(r"(\?|How to|Guide|FAQ|Interview|Questions?)", re.IGNORECASE)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def parse_frontmatter(text: str) -> dict:
    """Extract YAML frontmatter as a dict. Minimal parser for our needs."""
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    fm = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            fm[key.strip()] = val.strip()
    return fm


def has_frontmatter(text: str) -> bool:
    return text.startswith("---")


def add_type_to_frontmatter(text: str, note_type: str) -> str:
    """Insert type: field into existing frontmatter, or create new frontmatter."""
    match = FRONTMATTER_RE.match(text)
    if match:
        # Insert after the opening --- line
        end_of_open = text.index("---\n") + 4
        return text[:end_of_open] + f"type: {note_type}\n" + text[end_of_open:]
    else:
        return f"---\ntype: {note_type}\n---\n\n{text}"


def count_wikilinks(text: str) -> int:
    return len(WIKILINK_RE.findall(text))


def classify_note(filepath: Path, frontmatter: dict, title: str, fname: str = "") -> str:
    """Determine note type using frontmatter, path, and title heuristics."""
    # Respect existing type
    existing = frontmatter.get("type", "").lower().strip()
    if existing in ("concept", "adr", "project", "question"):
        return existing

    path_str = str(filepath)

    # Skip code/snippet files (e.g. conftest.py, example.py)
    if fname and re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*\.(py|js|ts|sh|sql|yaml|yml|json|toml)$", fname):
        return "skip"

    # Path-based classification
    if "00 Interview Questions" in path_str:
        return "question"
    if "03 Career Vault/Open Questions" in path_str:
        return "question"
    if "00 Projects" in path_str:
        return "project"
    if "01 Curated" in path_str and ADR_KEYWORDS.search(title):
        return "adr"
    if "01 Curated" in path_str:
        return "concept"
    if "02 Reference" in path_str:
        return "concept"
    if "03 Career Vault" in path_str:
        return "concept"

    # Title-based fallback
    if ADR_KEYWORDS.search(title):
        return "adr"
    if QUESTION_KEYWORDS.search(title):
        return "question"

    return "concept"


def days_since(dt_str: str | None) -> int:
    """Days since a YYYY-MM-DD string. Returns 9999 if None/invalid."""
    if not dt_str:
        return 9999
    try:
        past = date.fromisoformat(dt_str)
        return (date.today() - past).days
    except (ValueError, TypeError):
        return 9999


def file_age_days(filepath: Path) -> int:
    mtime = filepath.stat().st_mtime
    return (datetime.now().timestamp() - mtime) / 86400


# ---------------------------------------------------------------------------
# Main logic
# ---------------------------------------------------------------------------
def scan_vault() -> list[dict]:
    """Scan all .md files, classify, and return note metadata."""
    notes = []
    for root, dirs, files in os.walk(VAULT_ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fname in files:
            if not fname.endswith(".md"):
                continue
            fpath = Path(root) / fname
            try:
                content = fpath.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue

            frontmatter = parse_frontmatter(content)
            title = fname[:-3]  # strip .md
            # Try to extract title from first H1 in content
            h1_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
            if h1_match:
                title = h1_match.group(1).strip()

            note_type = classify_note(fpath, frontmatter, title, fname)
            if note_type == "skip":
                continue
            link_count = count_wikilinks(content)

            notes.append({
                "path": fpath,
                "title": title,
                "type": note_type,
                "link_count": link_count,
                "frontmatter": frontmatter,
                "content": content,
                "needs_type_write": "type" not in frontmatter,
            })
    return notes


def write_types_back(notes: list[dict]) -> None:
    """Add type: field to frontmatter of notes that lack it."""
    for note in notes:
        if note["needs_type_write"]:
            new_content = add_type_to_frontmatter(note["content"], note["type"])
            try:
                note["path"].write_text(new_content, encoding="utf-8")
            except OSError as e:
                print(f"  [WARN] Could not write type to {note['path'].name}: {e}")


def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def save_state(state: dict) -> None:
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def score_note(note: dict, state: dict) -> float:
    """Compute priority score for a note."""
    title = note["title"]
    state_entry = state.get(title, {})
    last_surfaced = state_entry.get("last_surfaced")

    ds = days_since(last_surfaced)
    # If in cooldown, return -1 to exclude
    if ds < COOLDOWN_DAYS:
        return -1.0

    age = file_age_days(note["path"])
    links = note["link_count"]
    oq_bonus = 1.0 if note["type"] == "question" else 0.0
    ap_bonus = 1.0 if note["type"] == "project" else 0.0

    return (
        ds * W_DAYS_SINCE
        + age * W_NOTE_AGE
        + links * W_LINK_COUNT
        + oq_bonus * W_OPEN_QUESTION
        + ap_bonus * W_ACTIVE_PROJECT
    )


def extract_summary(content: str, title: str, max_len: int = 200) -> str:
    """Pull a brief summary: first non-frontmatter, non-heading, non-code paragraph."""
    # Strip frontmatter
    match = FRONTMATTER_RE.match(content)
    body = content[match.end():] if match else content

    # Remove code blocks and HTML comments
    body = re.sub(r"```.*?```", "", body, flags=re.DOTALL)
    body = re.sub(r"<!--.*?-->", "", body, flags=re.DOTALL)

    # Find first non-empty, non-heading paragraph
    for block in body.split("\n\n"):
        block = block.strip()
        # Skip empty, headings, horizontal rules, tables-only blocks
        if not block:
            continue
        if block.startswith("#") or block.startswith("---") or block.startswith("***"):
            continue
        # Skip blocks that are only single-line (likely headings or tags)
        lines = [l for l in block.splitlines() if l.strip()]
        if len(lines) == 1 and lines[0].startswith("#"):
            continue
        # Clean up wikilinks for readability
        block_clean = re.sub(r"\[\[([^\]]+)\]\]", r"\1", block)
        # Strip leading blockquote markers
        block_clean = re.sub(r"^>\s?", "", block_clean)
        # Truncate
        if len(block_clean) > max_len:
            block_clean = block_clean[:max_len].rstrip() + "..."
        return block_clean
    return f"*{title}* (no summary available)"


def select_notes(notes: list[dict], state: dict) -> dict:
    """Select highest-scoring note per category. Returns {type: note}."""
    categorized = {"concept": [], "adr": [], "project": [], "question": []}
    for note in notes:
        t = note["type"]
        if t in categorized:
            categorized[t].append(note)

    selections = {}
    for category, pool in categorized.items():
        scored = [(score_note(n, state), n) for n in pool]
        scored = [(s, n) for s, n in scored if s >= 0]  # exclude cooldown
        if scored:
            scored.sort(key=lambda x: x[0], reverse=True)
            selections[category] = scored[0][1]

    return selections


def generate_daily_review(selections: dict, total_notes: int) -> str:
    """Format the daily review message."""
    today = date.today().isoformat()
    lines = [f"# Daily Knowledge Refresh — {today}\n"]

    labels = {
        "concept": "## Concept of the Day",
        "adr": "## Architecture Decision Record",
        "project": "## Project Insight",
        "question": "## Open Question",
    }

    for cat in ("concept", "adr", "project", "question"):
        label = labels[cat]
        note = selections.get(cat)
        if note:
            summary = extract_summary(note["content"], note["title"])
            lines.append(f"{label}\n")
            lines.append(f"**{note['title']}**\n")
            lines.append(f"> {summary}")
            lines.append(f"[[{note['title']}]]\n")
        else:
            lines.append(f"{label}\n")
            lines.append(f"*No {cat} available in pool.*\n")

    lines.append("---")
    lines.append(f"*Surfaced notes: {len(selections)} | Total in pool: {total_notes}*")
    return "\n".join(lines)


def update_state(state: dict, selections: dict) -> dict:
    """Mark selected notes as surfaced today."""
    today = date.today().isoformat()
    for cat, note in selections.items():
        title = note["title"]
        entry = state.get(title, {"surfaced_count": 0})
        entry["last_surfaced"] = today
        entry["surfaced_count"] = entry.get("surfaced_count", 0) + 1
        state[title] = entry
    return state


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def main():
    print("Scanning vault...")
    notes = scan_vault()
    print(f"  Found {len(notes)} markdown files.")

    # Write type classifications back to notes
    write_types_back(notes)
    print("  Classification complete.")

    # Load state and score
    state = load_state()
    selections = select_notes(notes, state)

    print(f"\nSelected notes for today:")
    for cat, note in selections.items():
        print(f"  [{cat}] {note['title']}")

    # Generate output
    OUTPUT_DIR.mkdir(exist_ok=True)
    today = date.today().isoformat()
    output_path = OUTPUT_DIR / f"{today}.md"
    message = generate_daily_review(selections, len(notes))
    output_path.write_text(message, encoding="utf-8")
    print(f"\nDaily review written to: {output_path}")

    # Update state
    state = update_state(state, selections)
    save_state(state)
    print("State saved.")

    # Print the review to stdout for cron job capture
    print("\n" + "=" * 60)
    print(message)


if __name__ == "__main__":
    main()
