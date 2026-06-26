"""Data Engineering Mentor Agent — reasons over technical concepts."""

from __future__ import annotations


class DataEngineeringMentor:
    """Agent persona for data engineering discussions."""

    NAME = "Data Engineering Mentor"
    DESCRIPTION = "Discusses architecture, design patterns, and best practices using your vault knowledge as reference material."

    SYSTEM_PROMPT = """You are the Data Engineering Mentor.

Your role:
1. Discuss data engineering concepts using the user's own knowledge as foundation
2. Reference specific notes the user has written to ground discussions
3. Identify where the user's knowledge is strong vs. thin
4. Suggest design approaches based on patterns in the vault

When responding:
- Ground discussions in the user's own notes using [[Title]]
- Cite quality scores to explain depth of knowledge
- Be technical and precise — the user values depth over hand-holding
"""

    def __init__(self, vault_index: dict, scored_notes: dict, knowledge_graph: object):
        self.vault_index = vault_index
        self.scored_notes = scored_notes
        self.graph = knowledge_graph

    def build_context(self, query: str) -> str:
        query_lower = query.lower()
        relevant = []
        for note in self.vault_index["notes"]:
            if note["note_type"] not in ("concept", "curated", "reference"):
                continue
            score = 0
            if any(kw in note["title"].lower() for kw in query_lower.split()):
                score += 5
            if any(kw in " ".join(note.get("tags", [])) for kw in query_lower.split()):
                score += 3
            if score > 0:
                relevant.append((score, note))
        relevant.sort(key=lambda x: x[0], reverse=True)

        lines = [f"## Data Engineering Mentor Context\n\nQuery: {query}\n"]
        for _, note in relevant[:8]:
            neighbors = self.graph.get_neighbors(note["title"])
            lines.append(f"### {note['title']} ({note['note_type']})")
            lines.append(f"Tags: {', '.join(note.get('tags', []))}")
            lines.append(f"Code: {note.get('has_code_examples', False)} | Matrix: {note.get('has_decision_matrix', False)}")
            lines.append(f"Connected to: {', '.join(neighbors[:5]) if neighbors else 'None'}\n")
        return "\n".join(lines)

    def get_system_prompt(self) -> str:
        return self.SYSTEM_PROMPT
