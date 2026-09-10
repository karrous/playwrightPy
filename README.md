# Playwright Python Test Framework

This project is a lean, company-ready starting point for UI and API automation. It uses Python, pytest, Playwright, and requests. The framework is environment-driven so the same test code can run locally, in staging, or in CI.

## Prerequisites

- Python 3.10 or newer
- Git

## Setup

From the project root, create and activate the virtual environment:

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
playwright install chromium
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
playwright install chromium
```

For linting and local development checks, install the development dependencies:

```powershell
pip install -r requirements-dev.txt
```

## Run the tests

The virtual environment must be active:

```bash
pytest
```

Run headed Chromium locally:

```powershell
pytest --headed --browser chromium
```

Run only one test group when needed:

```bash
pytest tests/ui
pytest tests/api
```

Tests run on Chromium headlessly by default. The `--headed` option opens a browser window. Test categories are available through markers:

```powershell
pytest -m smoke
pytest -m ui
pytest -m api
pytest -m regression
```

Check code quality with Ruff:

```powershell
ruff check .
```

## Environment configuration

Each environment (`local`, `dev`, `qa`, `prod`) is a named profile in
[`config/settings.py`](config/settings.py) with its own base URL, API base URL,
and timeout. Select one with `TEST_ENV`; `local` is the default and targets the
public sample sites so the bundled tests run with no setup.

> Replace the `example.com` placeholder hosts in `config/settings.py` with your
> real Dev / QA / Prod endpoints before running against them.

### Run each environment

Windows PowerShell:

```powershell
$env:TEST_ENV = "dev";  pytest
$env:TEST_ENV = "qa";   pytest
$env:TEST_ENV = "prod"; pytest -m smoke   # smoke only against production
Remove-Item Env:TEST_ENV                  # back to the local default
```

macOS/Linux (scoped to the single command):

```bash
TEST_ENV=dev  pytest
TEST_ENV=qa   pytest
TEST_ENV=prod pytest -m smoke
```

### Per-field overrides

`PYTEST_BASE_URL`, `COUNTRY_API_BASE_URL`, and `API_TIMEOUT_SECONDS` override the
selected profile's values one field at a time — useful for an ephemeral
deployment URL without editing source:

```powershell
$env:TEST_ENV = "qa"
$env:PYTEST_BASE_URL = "https://pr-1234.qa.example.com"
pytest -m ui
```

An unknown `TEST_ENV` fails fast (`TEST_ENV must be one of: dev, local, prod, qa`).
See `.env.example` for the supported variables. The project does not load `.env`
files automatically, which keeps CI configuration explicit and avoids an
unnecessary runtime dependency.

The API client is created once per test session and is available through the `country_api` fixture. Replace it with a company-specific service client as the project grows.

The API examples use the public, keyless [countries.dev API](https://countries.dev/docs) and validate capitals for Canada, Japan, and France. Its base URL can be overridden with `COUNTRY_API_BASE_URL` for a test environment or mock service.

## Continuous integration

GitHub Actions runs on pushes and pull requests targeting `main`. The workflow has independent jobs for:

- Ruff code-quality checks
- API tests
- UI tests on Chromium

The UI job collects JUnit results, screenshots, videos, and Playwright traces when failures occur. CI remains headless; headed mode is intended for local debugging.

To target a specific environment from a CI job, set `TEST_ENV` (and any
overrides) in that job's `env:` block, for example:

```yaml
    env:
      TEST_ENV: qa
```

## Optional AI tooling

Playwright MCP and Playwright Test Agents are optional developer tools. They are not required by this framework or its CI workflow. Teams may use them to explore an application or draft test ideas, but the reviewed Python tests under `tests/` remain the source of truth.
