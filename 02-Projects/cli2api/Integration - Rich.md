---
domain: tool
subdomain: terminal-ui
note_type: technology
source_type: self
status: curated
level: intermediate
tags:
  - cli2api
  - rich
  - integration
  - terminal
  - python
---
# AI Summary
Describes how Rich enhances the cli2api command-line experience by providing formatted output, tables, JSON rendering, progress indicators, live dashboards, improved logging, error presentation, and enhanced help text. The guide explains installation, optional package dependencies, YAML-based configuration, CLI flags, plugin integration, and practical recommendations for when Rich should and should not be used, allowing the CLI surface to remain user-friendly without affecting the API execution model.

---
## What Rich Brings

Rich is a Python library for beautiful CLI output. It provides:
- Tables, trees, and structured data display
- Syntax highlighting and markdown rendering
- Progress bars and spinners
- Colored and styled text
- Live displays for monitoring

For cli2api, Rich enhances the CLI surface that Typer provides.

## Installation

```bash
pip install rich
# Or with the package:
pip install cli2api[rich]
```

## Integration Points

### 1. Formatted Output for Function Results

By default, function return values are printed as plain strings. Rich can format them beautifully:

```python
# rich_output.py
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.json import JSON
from rich.syntax import Syntax

console = Console()

def display_result(result, format="auto"):
    """Display function result using appropriate Rich renderable."""
    if format == "json" or isinstance(result, (dict, list)):
        console.print_json(data=result)
    elif format == "table" and isinstance(result, list) and len(result) > 0:
        display_as_table(result)
    elif isinstance(result, str) and result.startswith("{"):
        # Try to parse as JSON
        try:
            import json
            data = json.loads(result)
            console.print_json(data=data)
        except json.JSONDecodeError:
            console.print(result)
    else:
        console.print(result)

def display_as_table(data):
    """Convert list of dicts to a Rich table."""
    if not data:
        console.print("[dim]No data[/dim]")
        return

    table = Table(show_header=True, header_style="bold magenta")
    # Use keys from first row as columns
    for key in data[0].keys():
        table.add_column(str(key))
    for row in data:
        table.add_row(*[str(v) for v in row.values()])
    console.print(table)
```

### 2. Rich Output Plugin

Make Rich formatting a plugin so it's configurable per route:

```python
# plugins/rich_output.py
class RichOutputPlugin(Plugin):
    def after_response(self, request, response, config):
        if config.get("rich_output"):
            display_result(response, config.get("rich_format", "auto"))
            raise SkipResponse()  # Don't print again
        return response
```

### 3. Progress Bars for Async Jobs

When checking async job status, show a progress bar:

```python
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

def check_task_status(task_id: str):
    """Display task status with Rich progress indicators."""
    result = get_task_result(task_id)

    if result["status"] == "pending":
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            task = progress.add_task(f"Waiting for {task_id}...", total=None)
            while result["status"] == "pending":
                import time
                time.sleep(1)
                result = get_task_result(task_id)

    # Show final result
    if result["status"] == "completed":
        console.print("[bold green]Completed:[/bold green]")
        display_result(result["result"])
    elif result["status"] == "failed":
        console.print(f"[bold red]Failed:[/bold red] {result['error']}")
```

### 4. Task List Display

Show all registered tasks as a Rich table:

```python
def list_tasks():
    """Display all registered functions as a Rich table."""
    table = Table(title="cli2api Tasks", show_header=True)
    table.add_column("Task", style="cyan")
    table.add_column("Path", style="green")
    table.add_column("Method", style="yellow")
    table.add_column("Auth", style="magenta")
    table.add_column("Rate Limit", style="blue")
    table.add_column("Async", style="red")

    for name, config in ROUTES.items():
        table.add_row(
            name,
            config.get("path", "/"),
            config.get("method", "POST"),
            "Yes" if config.get("auth", True) else "No",
            str(config.get("rate_limit", 10)),
            "Yes" if config.get("async_task", False) else "No",
        )

    console.print(table)
```

### 5. Request/Response Logging with Rich

Enhanced logging with syntax highlighting:

```python
# plugins/rich_logging.py
class RichLoggingPlugin(Plugin):
    def before_request(self, request, config, kwargs):
        console.print(f"[dim]{request.method}[/dim] [bold]{request.url}[/bold]")
        if kwargs:
            console.print(Panel(
                JSON(data=kwargs) if isinstance(kwargs, dict) else str(kwargs),
                title="Params",
                border_style="dim",
            ))
        return kwargs

    def after_response(self, request, response, config):
        status_color = "green" if isinstance(response, dict) else "yellow"
        console.print(f"[{status_color}]Response:[/{status_color}]")
        display_result(response)
        return response
```

### 6. Error Display

Pretty error messages:

```python
def display_error(error: Exception):
    """Display an error with Rich formatting."""
    console.print(Panel(
        f"[bold red]{type(error).__name__}[/bold red]\n\n{str(error)}",
        title="Error",
        border_style="red",
    ))
```

### 7. Help Text Enhancement

Rich can render markdown in help text:

```python
# In Typer, use Rich for help:
import typer
from rich.markdown import Markdown

app = typer.Typer(rich_help_panel=True)

@app.command()
def add(a: int, b: int):
    """
    Add two numbers together.

    *Args:*
    - `a`: First number
    - `b`: Second number

    *Returns:* Sum of a and b
    """
    return {"result": a + b}
```

### 8. Live Monitoring Dashboard

For monitoring async jobs in real-time:

```python
from rich.live import Live
from rich.layout import Layout

def monitor_jobs():
    """Live dashboard of running jobs."""
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="body"),
        Layout(name="footer", size=3),
    )

    with Live(layout, refresh_per_second=4) as live:
        while True:
            jobs = get_running_jobs()
            layout["header"].update(Panel("[bold]cli2api Job Monitor[/bold]"))
            layout["body"].update(display_job_table(jobs))
            layout["footer"].update(
                f"[dim]Press Ctrl+C to exit | {len(jobs)} jobs running[/dim]"
            )
            time.sleep(1)
```

## Configuration

Enable Rich output via YAML or CLI flag:

```yaml
defaults:
  rich_output: true
  rich_format: auto  # auto, json, table, text

routes:
  - name: list_users
    rich_format: table  # Force table format for this route
```

Or via CLI flag:

```bash
cli2api --rich list-users
cli2api --format json process-data --x 1 --y 2
```

## Dependencies

Add to pyproject.toml:

```toml
[project.optional-dependencies]
rich = ["rich>=13.0.0"]
```

## When to Use Rich

| Scenario | Use Rich? |
|----------|-----------|
| Interactive terminal usage | Yes |
| Piped output to other tools | No (use plain JSON) |
| CI/CD logs | Optional (Rich detects terminal) |
| API mode (HTTP) | No (irrelevant) |
| Logging to file | No (use structured JSON) |

## Pitfalls

1. **Rich in non-terminal environments** — Rich auto-detects terminals, but piping output may produce escape codes. Use `--no-rich` flag or detect `sys.stdout.isatty()`.
2. **Over-formatting** — Don't add colors/styles to every output. Use Rich for structure (tables, panels), not decoration.
3. **Performance** — Rich rendering is slower than plain print. For high-frequency calls, skip formatting.
4. **JSON consumers** — If output is piped to `jq` or another tool, disable Rich and output raw JSON.
