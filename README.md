# Playwright Python Test Framework

This project contains UI smoke tests built with Playwright and pytest, plus API tests built with `requests`.

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

## Run the tests

The virtual environment must be active:

```bash
pytest
```

Run only one test group when needed:

```bash
pytest tests/ui
pytest tests/api
```

The UI tests run Chromium headlessly by default. To see the browser, use `pytest --headed`.

The API examples use the public, keyless [countries.dev API](https://countries.dev/docs) and validate capitals for Canada, Japan, and France. Its base URL can be overridden with `COUNTRY_API_BASE_URL` for a test environment or mock service.

## Continuous integration

GitHub Actions runs on pushes and pull requests targeting `main`. The workflow creates `.venv`, installs dependencies and Chromium, then runs the complete pytest suite.
