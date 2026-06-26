"""Akashic Intelligence Engine — CLI entry point."""

from __future__ import annotations
import argparse, json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))


def run_parser(vault_path):
    from vault_parser import VaultParser
    p = VaultParser(vault_path)
    index = p.build_index()
    data_dir = Path(__file__).parent / "data"
    p.save_index(index, data_dir / "vault_index.json")
    return index


def run_scorer(index):
    from quality_scorer import QualityScorer
    s = QualityScorer(index)
    r = s.score_all()
    s.save_scores(r, Path(__file__).parent / "data" / "quality_scores.json")
    return r


def run_graph(index):
    from knowledge_graph import KnowledgeGraph
    g = KnowledgeGraph(index)
    g.build()
    g.save_graph(Path(__file__).parent / "data" / "knowledge_graph.json")
    return g


def run_recommendations(index, scores, graph):
    from recommendation_engine import RecommendationEngine
    e = RecommendationEngine(index, scores, graph)
    recs = e.get_daily_recommendations()
    e.save_recommendations(recs, Path(__file__).parent / "data" / "daily_recommendations.json")
    return recs


def format_markdown(recs, scores, summary):
    lines = []
    lines.append("# Akashic Intelligence Engine — Daily Report\n")
    lines.append(f"Generated: {__import__('datetime').datetime.now().isoformat()[:19]}\n")
    lines.append("## Daily Recommendations\n")
    for r in recs:
        lines.append(f"### [{r['category']}] {r['title']}")
        lines.append(f"Path: `{r['path']}`")
        lines.append(f"Reason: {r['reason']}\n")
    lines.append("## Knowledge Health\n")
    lines.append(f"- Total notes: {summary['total_nodes']}")
    lines.append(f"- Total links: {summary['total_edges']}")
    lines.append(f"- Orphan notes: {summary['orphan_count']}")
    lines.append(f"- Hub notes: {summary['hub_count']}")
    lines.append(f"- Connected components: {summary['component_count']}\n")
    lines.append("## Top Knowledge (by composite score)\n")
    for s in scores["scored_notes"][:5]:
        lines.append(f"- **{s['title']}**: {s['composite_score']}/100")
    lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Akashic Intelligence Engine")
    parser.add_argument("--vault", type=Path, default=None)
    parser.add_argument("--output", choices=["json", "markdown"], default="markdown")
    parser.add_argument("--mode", default="full", choices=["full", "parse", "score", "graph", "daily", "agents", "agent"])
    parser.add_argument("--query", type=str, default=None)
    args = parser.parse_args()

    if args.vault is None:
        candidates = [
            Path.home() / "Workspace" / "03 knowledge" / "The-Akashic-Records",
            Path(__file__).parent.parent.parent.parent / "The-Akashic-Records",
        ]
        for c in candidates:
            if c.exists():
                args.vault = c
                break

    if not args.vault or not args.vault.exists():
        print("ERROR: Vault not found. Use --vault to specify path.")
        sys.exit(1)

    print(f"Vault: {args.vault}")

    index = None
    scores = None
    graph = None
    recs = None

    if args.mode in ("full", "parse", "score", "graph", "daily"):
        print("Parsing vault...")
        index = run_parser(args.vault)
        print(f"  -> {index['metadata']['total_notes']} notes indexed")

    if args.mode in ("full", "score", "graph", "daily"):
        print("Scoring notes...")
        scores = run_scorer(index)
        print(f"  -> Avg composite: {scores['metadata']['avg_composite']}")

    if args.mode in ("full", "graph", "daily"):
        print("Building knowledge graph...")
        graph = run_graph(index)
        summary = graph.summary()
        print(f"  -> {summary['total_edges']} edges, {summary['orphan_count']} orphans")

    if args.mode in ("full", "daily"):
        print("Generating recommendations...")
        recs = run_recommendations(index, scores, graph)
        print(f"  -> {len(recs)} recommendations")

    if args.mode == "full" and args.output == "markdown":
        report = format_markdown(recs, scores, summary)
        report_path = Path(__file__).parent / "data" / "daily_report.md"
        report_path.write_text(report, encoding="utf-8")
        print(f"\nReport saved to {report_path}")

    if args.mode == "daily":
        if args.output == "json":
            print(json.dumps(recs, indent=2))
        else:
            print(format_markdown(recs, scores, summary))
    elif args.mode == "scores":
        if args.output == "json":
            print(json.dumps(scores, indent=2))
        else:
            for s in scores["scored_notes"][:20]:
                print(f"  {s['composite_score']:5.1f} | {s['title']}")
    elif args.mode == "graph":
        if args.output == "json":
            data_dir = Path(__file__).parent / "data"
            print(json.dumps(json.loads((data_dir / "knowledge_graph.json").read_text()), indent=2))
        else:
            print(f"Nodes: {summary['total_nodes']}, Edges: {summary['total_edges']}")
            print(f"Orphans: {summary['orphan_count']}, Hubs: {summary['hub_count']}")
    elif args.mode == "agents":
        from agents.dispatcher import AgentDispatcher
        d = AgentDispatcher(index, scores, graph)
        for a in d.list_agents():
            print(f"  {a['name']}: {a['description']}")
    elif args.mode == "agent":
        if not args.query:
            print("ERROR: --query required"); sys.exit(1)
        from agents.dispatcher import AgentDispatcher
        d = AgentDispatcher(index, scores, graph)
        prompt, context, name = d.dispatch(args.query)
        print(f"Agent: {name}\n")
        print(context)


if __name__ == "__main__":
    main()
