---
type: concept
---

#python #packaging #pip #poetry #pyproject-toml

```table-of-contents
```

# Python External Libraries Playbook

## Install from Local Path

In **project B**:

```bash
pip install -e ../project-a
# or
poetry add ../my-local-package
```

`-e` = editable, so changes in project A show up immediately in project B.

For this to work, project A needs a `pyproject.toml` with a proper name:

```toml
[tool.poetry]
name = "my-local-package"
version = "0.1.0"
```

Or in `pyproject.toml` of project B:

```toml
[tool.poetry.dependencies]
my-local-package = { path = "../my-local-package", develop = true }
```

## Build a Wheel and Install

In **project A**:

```bash
poetry build
```

Creates:
- `dist/project_a-0.1.0-py3-none-any.whl`
- `dist/project_a-0.1.0.tar.gz`

In **project B**:

```bash
pip install ../project-a/dist/project_a-0.1.0-py3-none-any.whl
```

## Install from Git

In **project B's** `requirements.txt`:

```
git+https://github.com/your-org/project-a.git@main
```

Or via pip:

```bash
pip install "git+https://github.com/your-org/project-a.git@v0.1.0"
```

Or via [[Poetry]]:

```bash
poetry add git+https://github.com/username/repo.git
```

Poetry projects install fine this way — pip doesn't care if the source used Poetry, as long as `pyproject.toml` is present.

For **private repos**, use SSH:

```bash
pip install "git+ssh://git@github.com/your-org/project-a.git@v0.1.0"
```

Or configure a token:

```bash
pip install "git+https://<token>@github.com/your-org/project-a.git@v0.1.0"
```

## Common Pitfalls

- **Cached wheels**: if the version number hasn't changed but code has, use `--force-reinstall --no-cache-dir` or `poetry cache clear --all pypi -n`
- **Version conflicts**: editable installs don't resolve transitive dependencies. Run `pip install -r requirements.txt` after adding editable packages
- **`pip install` vs `poetry add`**: pip doesn't update `pyproject.toml` or `poetry.lock`. Use `poetry add` for Poetry projects to keep lock file in sync
- **`--no-deps`**: skips dependency resolution. Useful when you know deps are already installed, but can leave the environment broken
- **Editable install breakage**: if the editable package is moved/deleted, the import breaks silently. Reinstall with `pip install -e <path>` after moving

## Related

- [[Poetry]]
- [[pip]]
- [[pyproject.toml]]
- [[Python Packaging]]
- [[Virtual Environments]]
