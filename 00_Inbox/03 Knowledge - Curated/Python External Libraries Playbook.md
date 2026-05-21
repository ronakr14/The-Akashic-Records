```table-of-contents
```
# 1. Install from local path
In **project B**: 
	`pip install -e ../project-a`
(`-e` = editable, so changes in project A show up immediately)
But for this to work, project A needs a `pyproject.toml` with a proper `[tool.poetry] name` set.

# 2. Build a wheel with Poetry and pip install it
In **project A**:
	`poetry build`
This creates:
	`dist/project_a-0.1.0-py3-none-any.whl
	`dist/project_a-0.1.0.tar.gz`
In **project B**:
	`pip install ../project-a/dist/project_a-0.1.0-py3-none-any.whl`

# 3. Install directly from Git (if you push A to GitHub/GitLab)

In **project B’s requirements.txt**:
	`git+https://github.com/your-org/project-a.git@main`
or in pip:
	`pip install "git+https://github.com/your-org/project-a.git@v0.1.0"`
  
Poetry projects install just fine this way — pip doesn’t care if the source used Poetry, as long as `pyproject.toml` is present.
# 4. Use a private package index (advanced / enterprise-y)

* Publish project A to a private PyPI (e.g., Nexus, Artifactory, or even `poetry publish --repository custom`).
* Then in **project B**:
	`pip install project-a`
