---
id: 7x38mctftdinvnxhgm5k5j6
title: Playwright
desc: ''
updated: 1753518199899
created: 1753518189570
---
tags: [master, playwright, testing, automation, e2e, browser-testing, devtools]

---

## 📌 Topic Overview

**Playwright** is a **modern, fast, and reliable end-to-end testing framework** for web applications developed by Microsoft. It supports **cross-browser automation** (Chromium, Firefox, WebKit), multiple languages (JavaScript, Python, C#, Java), and comes with **built-in parallelization**, **headless mode**, and **network mocking**.

> It’s like Selenium’s smarter, faster cousin — but built for the modern web with automatic waiting, multi-tab support, and better debugging tools.

Unlike Cypress, Playwright can test **multiple tabs, iframes, and real mobile devices**, and it can run **without requiring a DOM**, making it a true full-stack web automation toolkit.

---

## 🚀 80/20 Roadmap

| Stage | Focus Area                  | Why It Matters                                                  |
|-------|-----------------------------|-----------------------------------------------------------------|
| 1️⃣    | Core Concepts               | Understand how Playwright differs from Selenium & Cypress       |
| 2️⃣    | Browser Contexts            | Isolated sessions, multi-user testing                           |
| 3️⃣    | Selectors & Locators        | Best practices to interact with DOM elements                    |
| 4️⃣    | Auto-waiting & Assertions   | Stable, flake-free test execution                               |
| 5️⃣    | Parallelism & Test Suites   | Fast, scalable CI/CD test runs                                  |
| 6️⃣    | Network Mocking             | Offline testing and API simulation                              |
| 7️⃣    | Visual & Trace Debugging    | Time-travel debugging, video/screenshots                        |

---

## 🛠️ Practical Tasks

- ✅ Install Playwright and set up a basic test project  
- ✅ Write login flow test with retries and auto-wait  
- ✅ Record and replay trace sessions to debug flaky tests  
- ✅ Configure test projects with multiple browsers  
- ✅ Mock API responses to test error states  
- ✅ Integrate with GitHub Actions for CI automation  
- ✅ Run Playwright in Docker or headless mode in CI/CD  

---

## 🧾 Cheat Sheets

### ▶️ Install & Setup (JavaScript)

```bash
npm init playwright@latest
# or for Python:
pip install playwright
playwright install
````

### ▶️ Sample Test (JS)

```javascript
import { test, expect } from '@playwright/test';

test('basic login test', async ({ page }) => {
  await page.goto('https://example.com/login');
  await page.fill('#username', 'admin');
  await page.fill('#password', 'secret');
  await page.click('button[type="submit"]');
  await expect(page).toHaveURL(/dashboard/);
});
```

### ▶️ Record Trace

```bash
npx playwright test --trace on
npx playwright show-trace trace.zip
```

### ▶️ Mock API Response

```javascript
await page.route('**/api/data', route => {
  route.fulfill({
    status: 200,
    contentType: 'application/json',
    body: JSON.stringify({ message: 'Hello from mock!' }),
  });
});
```

---

## 🎯 Progressive Challenges

| Level           | Challenge                                                 |
| --------------- | --------------------------------------------------------- |
| 🥉 Beginner     | Write a test that opens a page and checks for a heading   |
| 🥈 Intermediate | Write a login + dashboard flow with trace & screenshot    |
| 🥇 Advanced     | Create test suites across Chrome, Firefox, and WebKit     |
| 🏆 Expert       | Integrate Playwright with GitHub Actions + mock API layer |

---

## 🎙️ Interview Q\&A

* **Q:** What makes Playwright different from Selenium?
* **Q:** How does Playwright handle automatic waits?
* **Q:** How do you isolate browser sessions in Playwright?
* **Q:** How can you test APIs using Playwright?
* **Q:** What strategies reduce test flakiness in Playwright automation?

---

## 🛣️ Next Tech Stack Recommendations

* **GitHub Actions / GitLab CI** — CI integration
* **Allure Reports** — Reporting for test runs
* **Docker + Playwright** — Containerized test environments
* **Percy / Applitools** — Visual diff testing
* **TestRail / Xray** — Test case management
* **Codegen / Trace Viewer** — Low-code automation and debugging

---

## 🔍 Mental Model

> "Playwright is not just a browser automation tool. It’s a **developer-first, test-friendly, and CI/CD-native** platform for making sure your app behaves exactly as expected — on **every browser, every device, every time**."

* ✅ Fast and reliable by design
* ✅ Built-in retries, selectors, and waits reduce flakiness
* ✅ Cross-browser support without needing third-party tools
* ✅ Robust enough for complex UIs, APIs, and visual workflows
