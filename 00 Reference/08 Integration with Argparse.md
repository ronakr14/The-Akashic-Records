
# Integration with Argparse

> See also: [[07 Integration with Typer]] (recommended alternative) | [[cli2api Feature Roadmap and Enhancements#7. CLI + API Dual Mode]]

## Status: Discouraged

Argparse technically works with cli2api but fights the architecture at every turn. This document explains why and shows how to do it if you absolutely must.

## Why Argparse Doesn't Fit

| Requirement | Typer | Argparse |
|-------------|-------|----------|
| Auto args from function signature | Yes | No — manual definition |
| Type validation | Automatic | Manual per argument |
| Auto help text | Yes | Manual per argument |
| Consistent with FastAPI | Yes | No |
| Async support | Native | Manual |
| Zero duplication | Yes | No — duplicates every param |

With argparse, you must manually redefine every argument that your function already defines:

```python
# Function already declares: a: int, b: int
def add(a: int, b: int):
    return a + b

# Argparse makes you repeat it all:
parser.add_argument("--a", type=int, required=True, help="...")
parser.add_argument("--b", type=int, required=True, help="...")
```

This breaks the core principle: **single source of truth**.

## When Argparse Might Still Make Sense

1. **Zero dependencies** — argparse is in stdlib, no pip install needed
2. **Tiny scripts** — one-off tools that will never grow
3. **Restricted environments** — can't install third-party packages
4. **Existing codebase** — already using argparse extensively

If none of these apply, use Typer instead.

## How to Integrate (If You Must)

### Basic Approach

```python
# cli_argparse.py
import argparse
from registry import ROUTES

def build_parser():
    parser = argparse.ArgumentParser(prog="cli2api")
    subparsers = parser.add_subparsers(dest="command")

    for name, config in ROUTES.items():
        func = config["func"]
        sub = subparsers.add_parser(name)

        # Inspect function signature to build args
        import inspect
        sig = inspect.signature(func)
        for param_name, param in sig.parameters.items():
            kwargs = {}
            if param.default != inspect.Parameter.empty:
                kwargs["default"] = param.default
                kwargs["type"] = param.annotation if param.annotation != inspect.Parameter.empty else str
            else:
                kwargs["required"] = True
                kwargs["type"] = param.annotation if param.annotation != inspect.Parameter.empty else str
            sub.add_argument(f"--{param_name}", **kwargs)

    return parser

def run_cli():
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    config = ROUTES[args.command]
    func = config["func"]

    # Filter out non-function kwargs
    func_params = set(inspect.signature(func).parameters.keys())
    kwargs = {k: v for k, v in vars(args).items() if k in func_params and k != "command"}

    result = func(**kwargs)
    print(result)
```

### Entry Point

```python
# main.py
import sys

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "api":
        # API mode
        from app import app
        import uvicorn
        uvicorn.run(app)
    else:
        # CLI mode
        from cli_argparse import run_cli
        run_cli()
```

### Limitations vs Typer

1. **No auto type coercion** — you must handle type conversion manually
2. **No auto help text** — must write help= for every argument
3. **No validation** — must validate ranges, choices, etc. yourself
4. **No shell completion** — must implement yourself or use argcomplete
5. **No Rich integration** — must manually format output
6. **No async support** — must manage event loop yourself
7. **No shared validation** — API and CLI have separate validation paths

## Migrating from Argparse to Typer

If you have an existing argparse-based CLI:

```python
# Before (argparse)
parser = argparse.ArgumentParser()
parser.add_argument("--a", type=int, required=True)
parser.add_argument("--b", type=int, required=True)
args = parser.add_args()
result = add(args.a, args.b)

# After (Typer)
@app.command()
def add(a: int, b: int):
    return add_func(a, b)
```

The function signature becomes the CLI definition. No manual mapping needed.

## Verdict

Use Typer. Argparse in a cli2api system is like installing manual crank windows in a car that already has power controls — technically possible, completely unnecessary.


```yaml
title: cli2api Integration with Argparse

folder: Projects/cli2api/Integrations

categorical:
  domain:
    value: software-engineering
    reason: Documents integration with an external Python CLI framework.

  subdomain: cli-framework

  note_type:
    value: technology
    reason: Explains how argparse can be integrated into cli2api, its trade-offs, and why it is not the preferred choice.

  source_type:
    value: self
    reason: Self-authored integration and comparison guide.

  status:
    value: curated
    reason: Stable reference documenting an optional integration and migration path.

  level:
    value: intermediate
    reason: Covers registry-based command generation and Python introspection without introducing major architectural concepts.

ratings:
  confidence:
    score: 5
    reason: Self-authored technical documentation.

  completeness:
    score: 5
    reason: Includes rationale, implementation, limitations, migration guidance, and recommendation.

  complexity:
    score: 3
    reason: Focuses on integrating a single CLI framework rather than core framework architecture.

  importance:
    score: 3
    reason: Argparse is intentionally presented as a secondary, discouraged option rather than a primary execution surface.

  career_relevance:
    score: 4
    reason: Demonstrates understanding of Python CLI tooling and architectural trade-offs.

  freshness:
    score: 4
    reason: Still relevant for legacy and dependency-free environments, although Typer is the modern recommendation.

  reusability:
    score: 4
    reason: Useful for projects that require stdlib-only CLI implementations or migration from existing argparse codebases.

  review_priority:
    score: 2
    reason: Expected to change infrequently since it documents a fallback integration.

  connectedness:
    score: 4
    reason: References Typer integration, CLI architecture, execution pipeline, and framework principles.

  actionability:
    score: 4
    reason: Provides complete implementation examples and migration guidance.

  quality_score:
    score: 95
    reason: Well-structured comparison and implementation guide that clearly explains why argparse is a fallback rather than the preferred integration.

custom:
  tags:
    - cli2api
    - argparse
    - cli
    - integration
    - python

ai_summary: >
  Explains how argparse can be integrated into cli2api while highlighting why it is discouraged compared to Typer. The document compares both frameworks against cli2api's design goals, describes situations where argparse remains appropriate, provides a registry-driven implementation example, discusses its limitations, outlines migration to Typer, and reinforces the framework's principle that function signatures should remain the single source of truth for both CLI and API interfaces.
```

I agree with classifying this as **`technology`**. Unlike your Architecture or Design Principles notes, this one is focused on integrating a specific library and evaluating its trade-offs. It naturally belongs alongside `Typer.md`, `Rich.md`, `FastAPI.md`, etc., under an `Integrations/` folder.

```yaml
title: cli2api Integration with Argparse

folder: Projects/cli2api/Integrations

categorical:
  domain:
    value: software-engineering
    reason: Documents integration with an external Python CLI framework.

  subdomain: cli-framework

  note_type:
    value: technology
    reason: Explains how argparse can be integrated into cli2api, its trade-offs, and why it is not the preferred choice.

  source_type:
    value: self
    reason: Self-authored integration and comparison guide.

  status:
    value: curated
    reason: Stable reference documenting an optional integration and migration path.

  level:
    value: intermediate
    reason: Covers registry-based command generation and Python introspection without introducing major architectural concepts.

ratings:
  confidence:
    score: 5
    reason: Self-authored technical documentation.

  completeness:
    score: 5
    reason: Includes rationale, implementation, limitations, migration guidance, and recommendation.

  complexity:
    score: 3
    reason: Focuses on integrating a single CLI framework rather than core framework architecture.

  importance:
    score: 3
    reason: Argparse is intentionally presented as a secondary, discouraged option rather than a primary execution surface.

  career_relevance:
    score: 4
    reason: Demonstrates understanding of Python CLI tooling and architectural trade-offs.

  freshness:
    score: 4
    reason: Still relevant for legacy and dependency-free environments, although Typer is the modern recommendation.

  reusability:
    score: 4
    reason: Useful for projects that require stdlib-only CLI implementations or migration from existing argparse codebases.

  review_priority:
    score: 2
    reason: Expected to change infrequently since it documents a fallback integration.

  connectedness:
    score: 4
    reason: References Typer integration, CLI architecture, execution pipeline, and framework principles.

  actionability:
    score: 4
    reason: Provides complete implementation examples and migration guidance.

  quality_score:
    score: 95
    reason: Well-structured comparison and implementation guide that clearly explains why argparse is a fallback rather than the preferred integration.

custom:
  tags:
    - cli2api
    - argparse
    - cli
    - integration
    - python

ai_summary: >
  Explains how argparse can be integrated into cli2api while highlighting why it is discouraged compared to Typer. The document compares both frameworks against cli2api's design goals, describes situations where argparse remains appropriate, provides a registry-driven implementation example, discusses its limitations, outlines migration to Typer, and reinforces the framework's principle that function signatures should remain the single source of truth for both CLI and API interfaces.
```

I agree with classifying this as **`technology`**. Unlike your Architecture or Design Principles notes, this one is focused on integrating a specific library and evaluating its trade-offs. It naturally belongs alongside `Typer.md`, `Rich.md`, `FastAPI.md`, etc., under an `Integrations/` folder.