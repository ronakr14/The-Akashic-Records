"""Vault Parser — extracts structured metadata from an Obsidian vault."""

from __future__ import annotations
import json, re
from datetime import datetime, timezone
from pathlib import Path

SKIP_DIRS = {".git", ".obsidian", ".hermes", "__pycache__", "node_modules"}
SKIP_FILES = {"CLAUDE.md", "Catalog.md", "README.md", "Storage Tracker.md"}

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
TAG_INLINE_RE = re.compile(r"#([a-zA-Z][\w-]*)")
WIKILINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)
CODE_BLOCK_RE = re.compile(r"```[\w]*\n.*?```", re.DOTALL)
TAG_LINE_RE = re.compile(r"^(#[a-zA-Z][\w-]*\s+)+#[a-zA-Z][\w-]*$")
DECISION_MATRIX_RE = re.compile(r"When to Use|Decision Matrix|When to Choose", re.IGNORECASE)
INTERVIEW_QA_RE = re.compile(r"\*\*Q\d+:", re.IGNORECASE)
RELATED_RE = re.compile(r"## Related|## See Also", re.IGNORECASE)


def _classify_note_type(path, content):
    """Classify a note's type based on path and content."""
    path_str = str(path).lower()
    if "career vault/adrs" in path_str:
        return "adr"
    if "career vault/open questions" in path_str:
        return "question"
    if "career vault" in path_str:
        return "concept"
    if "interview questions" in path_str:
        return "interview"
    if "prompts" in path_str:
        return "prompt"
    if "00 projects" in path_str:
        return "project"
    if "02 reference" in path_str:
        return "reference"
    if "01 curated" in path_str:
        return "curated"
    # Content-based fallback
    sections = content.split("\n---")
    if len(sections) >= 2:
        fm_text = sections[1] if content.startswith("---") else ""
        if "type: adr" in fm_text:
            return "adr"
        if "type: project" in fm_text:
            return "project"
        if "type: concept" in fm_text:
            return "concept"
    return "unknown"


def _extract_frontmatter(content):
    """Extract simple YAML frontmatter as dict."""
    match = FRONTMATTER_RE.match(content)
    if not match:
        return {}
    fm_text = match.group(1)
    result = {}
    current_key = None
    for line in fm_text.split("\n"):
        if line.startswith(" ") or line.startswith("\t"):
            if current_key and line.strip().startswith("- "):
                result[current_key].append(line.strip()[2:].strip())
            continue
        if ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if val:
                result[key] = val
            else:
                result[key] = []
                current_key = key
    return result


def _extract_tags(content, frontmatter):
    """Extract tags from frontmatter or inline tag line."""
    tags = []
    if "tags" in frontmatter:
        fm_tags = frontmatter["tags"]
        if isinstance(fm_tags, list):
            tags.extend(fm_tags)
        elif isinstance(fm_tags, str):
            tags.extend(TAG_INLINE_RE.findall(fm_tags))
    for line in content.split("\n")[:10]:
        if TAG_LINE_RE.match(line.strip()):
            tags.extend(TAG_INLINE_RE.findall(line))
    seen = set()
    unique = []
    for t in tags:
        t_clean = t.lower().strip()
        if t_clean and t_clean not in seen:
            seen.add(t_clean)
            unique.append(t_clean)
    return unique


def _extract_headings(content):
    return [{"level": len(m.group(1)), "text": m.group(2).strip()}
            for m in HEADING_RE.finditer(content)]


def _extract_wikilinks(content):
    seen = set()
    links = []
    for m in WIKILINK_RE.finditer(content):
        target = m.group(1).strip()
        if target not in seen:
            seen.add(target)
            links.append(target)
    return links


def _has_code_examples(content):
    return bool(CODE_BLOCK_RE.search(content))


def _has_decision_matrix(content):
    return bool(DECISION_MATRIX_RE.search(content))


def _has_interview_qa(content):
    return bool(INTERVIEW_QA_RE.search(content))


def _has_related_section(content):
    return bool(RELATED_RE.search(content))


class VaultParser:
    def __init__(self, vault_path):
        self.vault_path = Path(vault_path)

    def _should_skip(self, path):
        for part in path.relative_to(self.vault_path).parts:
            if part in SKIP_DIRS:
                return True
        if path.name in SKIP_FILES:
            return True
        return False

    def _parse_note(self, path):
        try:
            content = path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            return None

        frontmatter = _extract_frontmatter(content)
        body = FRONTMATTER_RE.sub("", content, count=1) if frontmatter else content
        stat = path.stat()
        note_type = _classify_note_type(path, content)

        return {
            "path": str(path.relative_to(self.vault_path)),
            "title": path.stem,
            "note_type": note_type,
            "tags": _extract_tags(content, frontmatter),
            "word_count": len(body.split()),
            "heading_count": len(_extract_headings(body)),
            "link_count": 0,
            "outgoing_links": _extract_wikilinks(body),
            "incoming_links": [],
            "has_code_examples": CODE_BLOCK_RE.search(body) is not None,
            "has_decision_matrix": DECISION_MATRIX_RE.search(body) is not None,
            "has_interview_qa": INTERVIEW_QA_RE.search(body) is not None,
            "has_related_section": RELATED_RE.search(body) is not None,
            "file_size_bytes": stat.st_size,
            "last_modified": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
            "created_at": datetime.fromtimestamp(stat.st_ctime, tz=timezone.utc).isoformat(),
        }

    def build_index(self):
        notes = []
        title_to_path = {}
        for md_file in sorted(self.vault_path.rglob("*.md")):
            if self._should_skip(md_file):
                continue
            note = self._parse_note(md_file)
            if note:
                notes.append(note)
                title_to_path[note["title"]] = note["path"]

        # Compute incoming links
        for note in notes:
            for target in note["outgoing_links"]:
                if target in title_to_path:
                    for other in notes:
                        if other["title"] == target:
                            other["incoming_links"].append(note["title"])
                            break

        for note in notes:
            note["link_count"] = len(note["outgoing_links"])

        return {
            "notes": notes,
            "metadata": {
                "vault_root": str(self.vault_path),
                "built_at": datetime.now(tz=timezone.utc).isoformat(),
                "total_notes": len(notes),
                "version": "1.0",
            },
        }

    def save_index(self, index, output_path):
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8")

    def load_index(self, index_path):
        return json.loads(index_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    vault = Path(__file__).parent.parent.parent.parent
    parser = VaultParser(vault)
    index = parser.build_index()
    output = Path(__file__).parent / "data" / "vault_index.json"
    parser.save_index(index, output)
    print(f"Index built: {index['metadata']['total_notes']} notes -> {output}")
