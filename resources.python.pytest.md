---
id: ce5foouxk3wvlv5uimvrip9
title: Pytest
desc: ''
updated: 1753518058618
created: 1753518052265
---
tags: [master, pytest, testing, python, automation, qa]

---

## 📌 Topic Overview

**Pytest** is the most popular Python testing framework known for its **simple syntax**, **powerful fixtures**, and **rich plugin ecosystem**. It supports **unit, functional, and integration testing** and easily scales from small projects to complex test suites.

> Pytest is the Swiss Army knife of Python testing — simple for beginners but powerful enough for pros.

Its key strengths are **auto-discovery of tests**, **assert rewriting** for readable failures, and flexible **parametrization**.

---

## 🚀 80/20 Roadmap

| Stage | Concept                  | Why It Matters                                                 |
|-------|--------------------------|----------------------------------------------------------------|
| 1️⃣    | Test Discovery & Structure | Write tests pytest recognizes automatically                    |
| 2️⃣    | Assertions & Reporting   | Understand pytest’s assert introspection and failure reports  |
| 3️⃣    | Fixtures                | Reusable setup/teardown with dependency injection             |
| 4️⃣    | Parametrization         | Run tests with multiple input sets                             |
| 5️⃣    | Markers & Skip/xfail    | Selectively run or skip tests                                  |
| 6️⃣    | Plugins & Extensions    | Extend capabilities with community plugins                    |
| 7️⃣    | Integration with CI/CD  | Run tests in pipelines with coverage and reporting            |
| 8️⃣    | Parallel Execution      | Speed up tests with `pytest-xdist`                            |

---

## 🛠️ Practical Tasks

- ✅ Write a simple test function and run it with `pytest`  
- ✅ Use `assert` for validations  
- ✅ Create a fixture to setup a database connection  
- ✅ Parametrize a test for multiple input values  
- ✅ Mark a test as skipped or expected failure (`@pytest.mark.skip`, `@pytest.mark.xfail`)  
- ✅ Generate an HTML report using `pytest-html`  
- ✅ Run tests in parallel with `pytest-xdist`  

---

## 🧾 Cheat Sheets

### ▶️ Basic Test

```python
def test_add():
    assert 1 + 1 == 2
````

Run tests:

```bash
pytest
```

---

### ▶️ Fixture Example

```python
import pytest

@pytest.fixture
def sample_dict():
    return {"key": "value"}

def test_dict(sample_dict):
    assert sample_dict["key"] == "value"
```

---

### ▶️ Parametrization

```python
import pytest

@pytest.mark.parametrize("input,expected", [(2,4), (3,9), (4,16)])
def test_square(input, expected):
    assert input**2 == expected
```

---

### ▶️ Skip & Expected Failure

```python
import pytest

@pytest.mark.skip(reason="Not implemented yet")
def test_feature():
    assert False

@pytest.mark.xfail(reason="Known bug")
def test_bug():
    assert False
```

---

## 🎯 Progressive Challenges

| Level           | Challenge                                             |
| --------------- | ----------------------------------------------------- |
| 🥉 Beginner     | Write tests for a simple function and run pytest      |
| 🥈 Intermediate | Use fixtures to setup complex test data               |
| 🥇 Advanced     | Parametrize tests and add custom markers              |
| 🏆 Expert       | Integrate pytest with CI/CD and run tests in parallel |

---

## 🎙️ Interview Q\&A

* **Q:** How does pytest discover test functions?
* **Q:** What are fixtures and how do they help?
* **Q:** Explain parametrization and why it’s useful.
* **Q:** How can you skip or mark tests as expected failures?
* **Q:** What plugins do you use with pytest?

---

## 🛣️ Next Tech Stack Recommendations

* **pytest-cov** — Coverage reporting
* **pytest-xdist** — Parallel test execution
* **pytest-mock** — Mocking support
* **tox** — Manage multiple test environments
* **Allure / pytest-html** — Rich test reports
* **GitHub Actions / Jenkins** — CI/CD integration
* **Selenium / Playwright** — For UI testing with pytest

---

## 🔍 Mental Model

> “Pytest is your automated proofreader — it runs your code, checks if the outputs are right, and reports exactly what went wrong with human-readable details.”

* ✅ Auto-discovers tests in files/functions named `test_`
* ✅ Fixtures = reusable test scaffolding
* ✅ Parametrization = test data-driven testing
* ✅ Markers = selective test execution
* ✅ Plugins = tailor the tool to your workflow
