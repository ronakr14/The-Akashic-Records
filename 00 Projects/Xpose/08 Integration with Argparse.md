---
tags:
  - cli2api
  - project
  - integration
  - cli
  - argparse
related:
  - "[[01 Goal]]"
  - "[[04 Enhancements Included#7. CLI + API Dual Mode]]"
  - "[[07 Integration with Typer]]"
  - "[[09 Integration with Rich]]"
---

# Integration with Argparse

> See also: [[07 Integration with Typer]] (recommended alternative) | [[04 Enhancements Included#7. CLI + API Dual Mode]]

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
