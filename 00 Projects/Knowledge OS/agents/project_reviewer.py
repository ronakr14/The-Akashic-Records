"""Project Reviewer Agent — reasons over project notes and deliverables."""

from __future__ import annotations


class ProjectReviewer:
    """Agent persona for project-level analysis."""

    NAME = "Project Reviewer"
    DESCRIPTION = "Reviews active projects, suggests milestones, detects blockers, and tracks progress against goals."

    SYSTEM_PROMPT = """You are the Project Reviewer.

Your role:
1. Review active project notes for completeness and progress
2. Identify projects without recent updates (stale)
3. Suggest next milestones based on existing plans
4. Detect knowledge gaps that could block progress

When responding:
- Be direct about what's missing or blocked
- Reference specific project notes by name
- Suggest concrete next steps with file paths
- Flag projects that have no recent activity
"""

    def __init__(self, vault_index: dict, scored_notes: dict, knowledge_graph: object):
        self.vault_index = vault_index
        self.scored_notes = scored_notes
        self.graph = knowledge_graph

    def build_context(self, query: str) -> str:
        query_lower = query.lower()
        project_notes = [n for n in self.vault_index["notes"]
                         if n["note_type"] == "project" or "Projects" in n["path"]]
        if query_lower not in ("all", "review", "status", "projects"):
            project_notes = [n for n in project_notes
                             if any(kw in n["title"].lower() for kw in query_lower.split())]

        lines = [f"## Project Reviewer Context\n\nQuery: {query}\n"]
        for note in project_notes[:10]:
            lines.append(f"### {note['title']}")
            lines.append(f"Path: {note['path']}")
            lines.append(f"Last modified: {note.get('last_modified', 'unknown')}")
            lines.append(f"Tags: {', '.join(note.get('tags', []))}\n")
        return "\n".join(lines)

    def get_system_prompt(self) -> str:
        return self.SYSTEM_PROMPT
