"""Agent Dispatcher — routes user queries to the appropriate agent persona."""

from __future__ import annotations
from .career_architect import CareerArchitect
from .pkm_curator import PKMCurator
from .data_mentor import DataEngineeringMentor
from .project_reviewer import ProjectReviewer


INTENT_MAP = {
    "career": CareerArchitect,
    "resume": CareerArchitect,
    "interview": CareerArchitect,
    "promotion": CareerArchitect,
    "skill gap": CareerArchitect,
    "job": CareerArchitect,
    "salary": CareerArchitect,
    "linkedin": CareerArchitect,
    "link": PKMCurator,
    "duplicate": PKMCurator,
    "restructure": PKMCurator,
    "metadata": PKMCurator,
    "tag": PKMCurator,
    "organize": PKMCurator,
    "merge": PKMCurator,
    "clean": PKMCurator,
    "quality": PKMCurator,
    "architecture": DataEngineeringMentor,
    "design": DataEngineeringMentor,
    "pattern": DataEngineeringMentor,
    "pipeline": DataEngineeringMentor,
    "database": DataEngineeringMentor,
    "kafka": DataEngineeringMentor,
    "spark": DataEngineeringMentor,
    "data lake": DataEngineeringMentor,
    "etl": DataEngineeringMentor,
    "project": ProjectReviewer,
    "milestone": ProjectReviewer,
    "blocker": ProjectReviewer,
    "progress": ProjectReviewer,
    "goal": ProjectReviewer,
    "next step": ProjectReviewer,
}


class AgentDispatcher:
    """Routes queries to the most appropriate agent."""

    def __init__(self, vault_index: dict, scored_notes: dict, knowledge_graph: object):
        self.agents = {
            "career": CareerArchitect(vault_index, scored_notes, knowledge_graph),
            "pkm": PKMCurator(vault_index, scored_notes, knowledge_graph),
            "mentor": DataEngineeringMentor(vault_index, scored_notes, knowledge_graph),
            "reviewer": ProjectReviewer(vault_index, scored_notes, knowledge_graph),
        }

    def dispatch(self, query: str) -> tuple:
        query_lower = query.lower()
        best_agent = None
        best_score = 0
        for keyword, agent_class in INTENT_MAP.items():
            if keyword in query_lower:
                for name, agent in self.agents.items():
                    if isinstance(agent, agent_class):
                        if len(keyword) > best_score:
                            best_score = len(keyword)
                            best_agent = name
                        break
        if best_agent is None:
            best_agent = "mentor"
        agent = self.agents[best_agent]
        context = agent.build_context(query)
        return agent.get_system_prompt(), context, agent.NAME

    def list_agents(self) -> list:
        return [{"name": a.NAME, "description": a.DESCRIPTION} for a in self.agents.values()]
