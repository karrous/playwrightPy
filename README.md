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

`pytest.ini` contains a safe default base URL for the Google example. Override it without changing source code:

### Windows PowerShell

```powershell
$env:TEST_ENV = "staging"
$env:PYTEST_BASE_URL = "https://staging.example.com"
$env:COUNTRY_API_BASE_URL = "https://api.example.com"
$env:API_TIMEOUT_SECONDS = "15"
pytest -m ui
```

### macOS/Linux

```bash
export TEST_ENV=staging
export PYTEST_BASE_URL=https://staging.example.com
export COUNTRY_API_BASE_URL=https://api.example.com
export API_TIMEOUT_SECONDS=15
pytest -m ui
```

See `.env.example` for the supported variables. The project does not load `.env` files automatically, which keeps CI configuration explicit and avoids adding an unnecessary runtime dependency.

The API client is created once per test session and is available through the `country_api` fixture. Replace it with a company-specific service client as the project grows.

The API examples use the public, keyless [countries.dev API](https://countries.dev/docs) and validate capitals for Canada, Japan, and France. Its base URL can be overridden with `COUNTRY_API_BASE_URL` for a test environment or mock service.

## Continuous integration

GitHub Actions runs on pushes and pull requests targeting `main`. The workflow has independent jobs for:

- Ruff code-quality checks
- API tests
- UI tests on Chromium

The UI job collects JUnit results, screenshots, videos, and Playwright traces when failures occur. CI remains headless; headed mode is intended for local debugging.

## Optional AI tooling

Playwright MCP and Playwright Test Agents are optional developer tools. They are not required by this framework or its CI workflow. Teams may use them to explore an application or draft test ideas, but the reviewed Python tests under `tests/` remain the source of truth.
