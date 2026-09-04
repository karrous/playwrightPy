"""Smoke tests for the Google homepage."""

import re

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.ui
@pytest.mark.smoke
def test_google_homepage_url(page: Page, base_url: str) -> None:
    response = page.goto("/ncr", wait_until="domcontentloaded")

    assert response is not None
    assert response.ok, f"Google returned HTTP {response.status}"
    assert page.url.startswith(base_url), page.url


@pytest.mark.ui
@pytest.mark.smoke
def test_google_homepage_title(page: Page) -> None:
    page.goto("/ncr", wait_until="domcontentloaded")

    expect(page).to_have_title(re.compile("Google", re.IGNORECASE))
