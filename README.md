# Playwright Python Capstone

End-to-end test automation framework built with **Playwright for Python** and **pytest**, covering UI and API automation, data-driven testing, failure diagnostics, HTML reporting, GitHub Actions CI and email notifications.

Repository: [shovandevops/playwright-capstone](https://github.com/shovandevops/playwright-capstone)

---

## 1. Project Objective

Provide a maintainable, modular automation framework that validates web applications repeatably without manual execution. The framework supports:

- Smoke and regression testing
- Read-only validation
- UI automation (Page Object Model)
- API automation (Playwright `APIRequestContext`)
- Data-driven testing from JSON files
- Parallel execution
- Failure diagnostics (screenshots, videos, traces)
- CI execution with automated reporting and email notifications

**Applications under test**

| Type | URL |
|---|---|
| UI | [SauceDemo](https://www.saucedemo.com/) |
| UI | [DemoQA](https://demoqa.com/) |
| UI (multiple windows) | [The Internet – Windows](https://the-internet.herokuapp.com/windows) |
| API | [JSONPlaceholder](https://jsonplaceholder.typicode.com/) / [my-json-server](https://my-json-server.typicode.com/) |

---

## 2. Framework Architecture

The framework is layered so test logic, locators, data, utilities and configuration live in separate modules.

```
 tests/ (business scenarios)
   │
   ├── pages/        Page Objects: locators + page actions (UI)
   ├── api_clients/  Service objects wrapping API endpoints
   │     └── models/ Response models exposing fields via @property
   ├── utils/        Logging, JSON loading, deep JSON compare, sessionStorage helpers
   ├── testdata/     External JSON test data
   └── config/       Environment loading (.env → EnvConfig)

 conftest.py  → shared fixtures (env, logged_in_page, api_context, API clients)
 pytest.ini   → CLI defaults, markers, logging, artifacts, HTML report
```

| Layer | Responsibility |
|---|---|
| **Page Objects** (`pages/`) | Encapsulate locators and actions. SauceDemo and windows pages extend `BasePage` (navigation + logging). Use semantic locators (`get_by_role`, `get_by_placeholder`, `get_by_text`) and explicit waits. |
| **API clients** (`api_clients/`) | Wrap endpoints (`/users`, `/posts`) using a shared `APIRequestContext`. |
| **Models** (`models/`) | `User` model converts JSON into objects and exposes fields via properties. |
| **Fixtures** (`conftest.py`) | Dependency injection for environment config, an authenticated page and API clients, with `yield`-based setup/teardown. |
| **Test data** (`testdata/`) | JSON datasets consumed via `json.load()` and `@pytest.mark.parametrize`. |

---

## 3. Prerequisites

- Python **3.12+** (CI uses 3.13)
- `pip`
- Git
- Internet access (tests target public practice sites)

---

## 4. Installation

```bash
git clone https://github.com/shovandevops/playwright-capstone.git
cd playwright-capstone

python -m venv .venv
```

Activate the virtual environment:

```bash
# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

| Package | Purpose |
|---|---|
| `playwright`, `pytest-playwright` | Browser automation and pytest fixtures (`page`, `browser`, `playwright`) |
| `pytest-html` | HTML test report |
| `pytest-xdist` | Parallel execution (`-n`) |
| `pytest-rerunfailures` | Rerun flaky failures (`--reruns`) |
| `python-dotenv` | Load environment URLs from `.env` |

---

## 5. Playwright Setup

Install the browser binaries:

```bash
playwright install
```

Install only Chromium (with OS dependencies on Linux):

```bash
playwright install --with-deps chromium
```

### Environment configuration

Base URLs are read from `.env` by `config/env.py` and exposed through `EnvConfig` (`config/settings.py`):

```env
SAUCE_DEMO_URL=https://www.saucedemo.com/
DEMO_QA_URL=https://demoqa.com/
JSON_PLACEHOLDER_URL=https://my-json-server.typicode.com/shovandevops/playwright-api-server/
THE_INTERNET_URL=https://the-internet.herokuapp.com/
```

Never store credentials or secrets in `.env` files that are committed. CI secrets live in GitHub Secrets.

---

## 6. Execution Commands

Default options come from `pytest.ini` (Chromium + Firefox, 1 rerun, HTML report, failure artifacts).

```bash
# Run the full suite
pytest

# Smoke tests only
pytest -m smoke

# Smoke or regression tests
pytest -m "smoke or regression"

# Read-only tests
pytest -m readonly

# UI or API suites
pytest tests/ui
pytest tests/api
pytest -m api

# Single browser
pytest --browser chromium

# Watch the browser (headed, slowed down)
pytest tests/ui --headed --slowmo 500

# Single file / single test
pytest tests/ui/test_checkout.py
pytest tests/ui/test_login.py::test_valid_login
```

---

## 7. Markers

Markers are registered in `pytest.ini` and applied either per test or per module with `pytestmark`.

| Marker | Meaning |
|---|---|
| `smoke` | Critical-path tests for quick verification |
| `regression` | Full suite for deep validation |
| `readonly` | Tests that do not modify application data |
| `ui` | Frontend UI tests |
| `api` | Backend API tests |
| `auth` | Login, session and permission tests |

Module-level markers apply to every test in a file:

```python
pytestmark = [pytest.mark.ui, pytest.mark.auth]
```

Combine markers with boolean expressions:

```bash
pytest -m "ui and smoke"
pytest -m "regression and not auth"
```

---

## 8. Parallel Execution

`pytest-xdist` distributes tests across worker processes:

```bash
pytest -n 4
pytest -n auto
pytest -n 4 -m "smoke or regression" --browser chromium
```

Each test gets its own browser context, so tests are independent and safe to run in parallel.

---

## 9. Test Coverage

### UI tests (`tests/ui/`)

| File | Scenarios |
|---|---|
| `test_login.py` | Valid login and navigation; invalid login error; locked-out user error |
| `test_products.py` | Products displayed; product details (3 JSON datasets); sort by name/price (4 datasets) |
| `test_cart.py` | Add product and validate cart count; remove from inventory; remove from cart page |
| `test_checkout.py` | Complete checkout and validate order confirmation (3 JSON datasets) |
| `test_windows.py` | New tab via `page.context.expect_page()`; validates page count, parent/child URLs and child content |
| `test_session_storage.py` | Write, read, save, clear, restore and validate `sessionStorage` |

### API tests (`tests/api/`)

| File | Scenarios |
|---|---|
| `test_posts_api.py` | GET list, GET by id, POST, PUT, DELETE |
| `test_users_api.py` | Search by name (no index assumption) via `User` model; exact JSON comparison; deep JSON comparison with mismatch path (`root.address.city`); POST, PUT, DELETE |

### Wait handling

Tests rely on Playwright auto-waiting plus explicit condition-based waits. `time.sleep()` is never used.

```python
locator.wait_for(state="visible")
page.wait_for_url("**/inventory.html")
page.wait_for_load_state("domcontentloaded")
```

### Session storage vs cookies

`page.context.cookies()` returns only the browser cookie jar (HTTP cookie state sent with requests). `sessionStorage` is a separate, per-tab Web Storage API that lives in the page's JavaScript context and is never part of the cookie jar, so it must be read with `page.evaluate()`:

```python
session_data = page.evaluate("() => Object.fromEntries(Object.entries(sessionStorage))")
```

Captured values are saved to `testdata/session_data.json` (generated at runtime, git-ignored).

---

## 10. Reports, Logs and Failure Artifacts

### HTML report

Generated automatically on every run (configured in `pytest.ini`):

```bash
pytest --html=reports/report.html --self-contained-html
```

Open `reports/report.html` in a browser.

### Logs

Python logging writes to the console and to `logs/automation.log`. Test start/finish, page actions and API calls are logged. Passwords and secrets are never logged.

### Failure artifacts

Written to `test-results/`:

| Artifact | Option | What it gives you |
|---|---|---|
| Screenshot | `--screenshot only-on-failure` | A single image of the page at the end of a failed test |
| Video | `--video retain-on-failure` | A recording of the whole test run, kept only for failed tests |
| Trace | `--tracing retain-on-failure` | A full timeline: DOM snapshots per action, network, console and source. The richest debugging tool |

Open a trace:

```bash
playwright show-trace test-results/<test-folder>/trace.zip
```

---

## 11. CI Workflow (GitHub Actions)

Workflow file: `.github/workflows/playwright.yml`

**Steps**

1. Check out the repository
2. Set up Python
3. Install dependencies from `requirements.txt`
4. Install Playwright browsers and OS dependencies
5. Run `pytest` (generates the HTML report)
6. Upload the HTML report artifact (`pytest-html-report`), always
7. Upload Playwright failure artifacts (`playwright-artifacts` from `test-results/`)
8. Send an email notification with status, repository, workflow, artifact URL and the HTML report attached

**Triggers**

| Trigger | When it runs |
|---|---|
| `push` | Every time commits are pushed to a branch |
| `pull_request` | When a pull request is opened, updated or reopened, so changes are validated before merging |
| `workflow_dispatch` | Manually, from the **Actions** tab ("Run workflow") |

**Email notification secrets**

Configure these under **Settings → Secrets and variables → Actions**. Credentials are never hard-coded in YAML.

| Secret | Purpose |
|---|---|
| `SEND_EMAIL` | Set to `true` to enable the email step |
| `EMAIL_USERNAME` / `EMAIL_PASSWORD` | SMTP credentials |
| `EMAIL_SMTP_SERVER` / `EMAIL_SMTP_PORT` | SMTP host and port (e.g. 587) |
| `EMAIL_TO` | Recipient address |

---

## 12. Project Folder Structure

```
playwright-capstone/
├── .github/workflows/
│   └── playwright.yml        # CI pipeline
├── api_clients/
│   ├── posts_client.py       # /posts endpoint wrapper
│   └── users_client.py       # /users endpoint wrapper
├── config/
│   ├── env.py                # Loads .env
│   └── settings.py           # EnvConfig (base URLs)
├── docs/                     # Assignment and action-item tracker
├── models/
│   └── user_model.py         # User response model
├── pages/
│   ├── base_page.py          # Shared navigation + logging
│   ├── login_page.py
│   ├── products_page.py
│   ├── product_details_page.py
│   ├── cart_page.py
│   ├── checkout_page.py
│   ├── registration_page.py
│   └── windows_page.py
├── scripts/
│   └── send_email.py         # CI email notification
├── testdata/                 # JSON datasets
│   ├── login_data.json
│   ├── products_data.json
│   ├── sort_data.json
│   ├── cart_data.json
│   ├── checkout_data.json
│   └── registration_data.json
├── tests/
│   ├── api/                  # API tests
│   └── ui/                   # UI tests
├── utils/
│   ├── logger.py             # Logging helpers
│   ├── json_utils.py         # JSON test-data loader
│   ├── json_comparator.py    # Deep JSON comparison
│   └── session_storage.py    # sessionStorage helpers
├── logs/                     # automation.log (generated, git-ignored)
├── reports/                  # report.html (generated, git-ignored)
├── screenshots/              # (git-ignored)
├── test-results/             # Playwright artifacts (generated, git-ignored)
├── conftest.py               # Shared fixtures and hooks
├── pytest.ini                # pytest configuration and markers
├── requirements.txt
├── .env                      # Base URLs (no secrets)
└── .gitignore
```

---

## 13. Git Workflow

- `main` is the integration branch.
- Work happens on feature branches (e.g. `feature/api-tests`, `feature/ui-tests`).
- Changes are merged into `main` via pull requests after CI passes.

```bash
git checkout -b feature/my-change
git add .
git commit -m "Describe the change"
git push -u origin feature/my-change
# Open a pull request on GitHub, then merge after review and a green CI run
```
