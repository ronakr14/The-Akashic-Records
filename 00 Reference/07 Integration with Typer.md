```table-of-contents
```

# Integration with Typer

> See also: [[04 Enhancements Included#7. CLI + API Dual Mode]] | [[09 Integration with Rich]] | [[10 Examples of Use]]

## Why Typer?

Typer is the recommended CLI framework for cli2api because it shares the same mental model as FastAPI:

| Concept | FastAPI | Typer |
|---------|---------|-------|
| Interface definition | Function signature | Function signature |
| Validation | Type hints | Type hints |
| Auto docs | /docs (Swagger) | --help |
| Async support | Native | Supported |

Both derive behavior from the same function signature. This means zero duplication between API and CLI.

## Basic Integration

### Step 1 — Register CLI Commands from Registry

```python
# cli_app.py
import typer
from registry import ROUTES

app = typer.Typer()

def register_cli():
    for config in ROUTES.values():
        func = config["func"]
        app.command(name=config["name"])(func)
```

That's it. Every registered function becomes a CLI command.

### Step 2 — Wire into App

```python
# main.py
import typer
from cli_app import app as cli_app
from app import create_app

# FastAPI app
fastapi_app = create_app()

# Typer app (for CLI usage)
# Run: python main.py add --a 1 --b 2
```

### Step 3 — Entry Point

```python
# main.py
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] != "api":
        # CLI mode
        sys.argv = sys.argv[1:]  # Remove 'api' if present
        cli_app()
    else:
        # API mode
        import uvicorn
        uvicorn.run(fastapi_app)
```

Or use pyproject.toml scripts:

```toml
[project.scripts]
cli2api = "cli2api.cli:app"
```

## How It Works

Given:

```python
@expose
def add(a: int, b: int):
    return {"result": a + b}
```

With YAML:

```yaml
routes:
  - name: add
    path: /add
    method: POST
```

You get:

```bash
# API
POST /add?a=1&b=2
-> {"result": 3}

# CLI
cli2api add --a 1 --b 2
-> {"result": 3}
```

Same function. Same validation. Same behavior.

## Typer Advantages for cli2api

1. **Zero duplication** — CLI args derived from function signature automatically
2. **Auto help** — `cli2api add --help` shows args, types, defaults
3. **Type safety** — Typer validates types before calling function
4. **Composable** — Easy to add subcommands, groups, shell completion
5. **Consistent with FastAPI** — same type hint system, same validation rules

## Advanced: CLI with Plugins

By default, CLI mode skips API-specific plugins (auth, rate limit). But you can configure:

```python
# cli_app.py
def register_cli():
    for config in ROUTES.values():
        func = config["func"]

        @app.command(name=config["name"])
        def cli_wrapper(**kwargs):
            # Optionally apply some plugins in CLI mode
            # e.g., logging yes, auth no, rate limit no
            if config.get("cli_logging"):
                logger.info(f"CLI call: {config['name']} | {kwargs}")
            return func(**kwargs)
```

## Advanced: --async Flag in CLI

Trigger async job from CLI:

```python
@app.command(name="run-async")
def run_async(task_name: str, **kwargs):
    """Run a task asynchronously via Celery."""
    if task_name not in TASKS:
        print(f"Unknown task: {task_name}")
        return
    result = TASKS[task_name].delay(**kwargs)
    print(f"Task queued: {result.id}")
    print(f"Check status: cli2api status {result.id}")
```

## Advanced: Unified Execution Pipeline

For true consistency across surfaces:

```python
# execution.py
def execute(config, **kwargs):
    """Unified execution pipeline used by CLI, API, and Celery."""
    # Before plugins
    kwargs = run_plugins("before", config.get("plugins", []), kwargs)

    # Execute
    result = config["func"](**kwargs)

    # After plugins
    result = run_plugins("after", config.get("plugins", []), result)

    return result
```

Then:

```python
# API calls execute(config, **kwargs)
# CLI calls execute(config, **kwargs)
# Celery calls execute(config, **kwargs)
```

Same pipeline. Same plugin behavior. Guaranteed consistency.

## Subcommands

For larger CLI tools, group commands:

```python
# cli_app.py
app = typer.Typer()

data_app = typer.Typer()
app.add_typer(data_app, name="data")

report_app = typer.Typer()
app.add_typer(report_app, name="report")

# Result:
# cli2api data process --x 1 --y 2
# cli2api report generate --user-id 42
```

## Shell Completion

Typer supports shell completion out of the box:

```bash
# Bash
cli2api --install-completion

# Shows in help
cli2api --help
```

## Error Handling

Typer handles:
- Invalid types: `Error: Invalid value for '--a': 'abc' is not a valid integer`
- Missing required args: `Error: Missing option '--a'.`
- Help: `cli2api add --help`

All automatic from the function signature.
