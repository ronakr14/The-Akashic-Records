"""PKM Curator Agent — reasons over vault structure and note quality."""

from __future__ import annotations


class PKMCurator:
    """Agent persona for personal knowledge management."""

    NAME = "PKM Curator"
    DESCRIPTION = "Maintains vault health — detects duplicates, suggests links, improves metadata, and recommends structural improvements."

    SYSTEM_PROMPT = """You are the PKM Curator.

Your role:
1. Detect duplicate or overlapping notes that should be merged
2. Suggest missing links between related notes
3. Identify notes lacking tags, table-of-contents, or related sections
4. Recommend vault restructuring when patterns emerge
5. Prioritize notes that need quality improvement

When responding:
- Be specific — name the exact files to change
- Provide the rationale for each change
- Prioritize high-impact improvements over cosmetic ones
- Suggest concrete wikilinks to add
"""

    def __init__(self, vault_index: dict, scored_notes: dict, knowledge_graph: object):
        self.vault_index = vault_index
        self.scored_notes = scored_notes
        self.graph = knowledge_graph

    def build_context(self, query: str) -> str:
        orphans = self.graph.get_orphan_nodes()
        low_conn = [s for s in self.scored_notes["scored_notes"] if s["dimensions"]["connectedness"] < 30]
        untagged = [n for n in self.vault_index["notes"] if not n.get("tags")]
        missing = self.graph.get_missing_links()[:10]

        lines = [f"## PKM Curator Context\n\nQuery: {query}\n"]

        if orphans:
            lines.append(f"### Orphan Notes ({len(orphans)})\n")
            for o in orphans[:10]:
                lines.append(f"- {o}")

        if low_conn:
            lines.append(f"\n### Low Connectedness ({len(low_conn)} notes)\n")
            for n in low_conn[:10]:
                lines.append(f"- {n['title']} (connectedness: {n['dimensions']['connectedness']})")

        if untagged:
            lines.append(f"\n### Untagged Notes ({len(untagged)} notes)\n")
            for n in untagged[:10]:
                lines.append(f"- {n['title']} ({n['path']})")

        if missing:
            lines.append(f"\n### Suggested Missing Links\n")
            for m in missing[:5]:
                lines.append(f"- [[{m['note_a']}]] <-> [[{m['note_b']}]] (shared: {m['shared_tag']})")

        return "\n".join(lines)

    def get_system_prompt(self) -> str:
        return self.SYSTEM_PROMPT
