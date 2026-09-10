"""Shared fixtures for UI and API tests."""

from collections.abc import Generator

import pytest

from config.settings import Settings, settings
from utils.country_api import CountryApiClient


def pytest_configure(config: pytest.Config) -> None:
    """Feed the selected environment's URL to pytest-base-url."""
    config.option.base_url = settings.base_url


def pytest_report_header() -> str:
    return (
        f"environment: {settings.environment} "
        f"(base_url={settings.base_url}, api_base_url={settings.api_base_url})"
    )


@pytest.fixture(scope="session")
def test_settings() -> Settings:
    return settings


@pytest.fixture(scope="session")
def base_url(test_settings: Settings) -> str:
    """Selected environment's UI URL, used by pytest-base-url and Playwright."""
    return test_settings.base_url


@pytest.fixture(scope="session")
def country_api(test_settings: Settings) -> Generator[CountryApiClient, None, None]:
    client = CountryApiClient(
        base_url=test_settings.api_base_url,
        timeout=test_settings.api_timeout_seconds,
    )
    yield client
    client.close()
