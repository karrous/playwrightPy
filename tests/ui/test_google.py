"""Smoke tests for the Google homepage."""

import re

from playwright.sync_api import Page, expect


GOOGLE_URL = "https://www.google.com/ncr"


def test_google_homepage_url(page: Page) -> None:
    response = page.goto(GOOGLE_URL, wait_until="domcontentloaded")

    assert response is not None
    assert response.ok, f"Google returned HTTP {response.status}"
    assert page.url.startswith("https://www.google.com"), page.url


def test_google_homepage_title(page: Page) -> None:
    page.goto(GOOGLE_URL, wait_until="domcontentloaded")

    expect(page).to_have_title(re.compile("Google", re.IGNORECASE))

