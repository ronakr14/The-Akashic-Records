"""Career Architect Agent — reasons over vault knowledge for career decisions."""

from __future__ import annotations


class CareerArchitect:
    """Agent persona for career-related guidance."""

    NAME = "Career Architect"
    DESCRIPTION = "Analyzes your knowledge vault to identify career gaps, track interview readiness, and recommend skill development paths."

    SYSTEM_PROMPT = """You are the Career Architect.

Your role:
1. Analyze the user's knowledge coverage across data engineering domains
2. Identify gaps between current knowledge and career goals
3. Recommend which interview topics to prioritize based on note quality
4. Track ADRs and lessons as evidence of engineering maturity

When responding:
- Reference specific notes by title using [[Title]] format
- Cite quality scores to justify recommendations
- Prioritize actionable next steps over generic advice
- Be direct — the user wants actionable intelligence, not encouragement
"""

    def __init__(self, vault_index: dict, scored_notes: dict, knowledge_graph: object):
        self.vault_index = vault_index
        self.scored_notes = scored_notes
        self.graph = knowledge_graph

    def build_context(self, query: str) -> str:
        query_lower = query.lower()
        relevant = []
        for note in self.vault_index["notes"]:
            score = 0
            if any(kw in note["title"].lower() for kw in query_lower.split()):
                score += 3
            if any(kw in " ".join(note.get("tags", [])) for kw in query_lower.split()):
                score += 2
            if score > 0:
                neighbors = self.graph.get_neighbors(note["title"])
                relevant.append((score, note, neighbors))
        relevant.sort(key=lambda x: x[0], reverse=True)

        lines = [f"## Career Architect Context\n\nQuery: {query}\n"]
        for _, note, neighbors in relevant[:8]:
            lines.append(f"### {note['title']} ({note['note_type']})")
            lines.append(f"Tags: {', '.join(note.get('tags', []))}")
            lines.append(f"Links: {len(note.get('outgoing_links', []))} out, {len(note.get('incoming_links', []))} in")
            lines.append(f"Connected to: {', '.join(neighbors[:5]) if neighbors else 'None'}\n")
        return "\n".join(lines)

    def get_system_prompt(self) -> str:
        return self.SYSTEM_PROMPT
