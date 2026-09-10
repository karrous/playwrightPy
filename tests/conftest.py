"""Shared fixtures for UI and API tests."""

from collections.abc import Generator

import pytest

from config.settings import Settings
from utils.country_api import CountryApiClient

_SETTINGS_KEY = pytest.StashKey[Settings]()


def pytest_addoption(parser: pytest.Parser) -> None:
    group = parser.getgroup("environment", "Test environment / language")
    group.addoption(
        "--env",
        action="store",
        default=None,
        help="Target environment: local | dev | qa | prod (overrides TEST_ENV).",
    )
    group.addoption(
        "--language",
        action="store",
        default=None,
        help="Language: a short code (fr, de, ...) or BCP-47 tag (fr-FR); overrides TEST_LANGUAGE.",
    )


def pytest_configure(config: pytest.Config) -> None:
    """Resolve settings from CLI options (falling back to env vars) once per run."""
    try:
        resolved = Settings.from_environment(
            env_name=config.getoption("--env"),
            language=config.getoption("--language"),
        )
    except ValueError as error:
        raise pytest.UsageError(str(error)) from error
    config.stash[_SETTINGS_KEY] = resolved
    config.option.base_url = resolved.base_url


def pytest_report_header(config: pytest.Config) -> str:
    s = config.stash[_SETTINGS_KEY]
    return (
        f"environment: {s.environment} | locale: {s.locale} | "
        f"base_url: {s.base_url} | api_base_url: {s.api_base_url}"
    )


@pytest.fixture(scope="session")
def test_settings(request: pytest.FixtureRequest) -> Settings:
    return request.config.stash[_SETTINGS_KEY]


@pytest.fixture(scope="session")
def base_url(test_settings: Settings) -> str:
    """Selected environment's UI URL, used by pytest-base-url and Playwright."""
    return test_settings.base_url


@pytest.fixture
def browser_context_args(browser_context_args: dict, test_settings: Settings) -> dict:
    """Run the browser in the selected language (Accept-Language, navigator.language)."""
    return {**browser_context_args, "locale": test_settings.locale}


@pytest.fixture(scope="session")
def country_api(test_settings: Settings) -> Generator[CountryApiClient, None, None]:
    client = CountryApiClient(
        base_url=test_settings.api_base_url,
        timeout=test_settings.api_timeout_seconds,
        locale=test_settings.locale,
    )
    yield client
    client.close()
