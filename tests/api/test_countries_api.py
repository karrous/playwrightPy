"""Sample API tests for country and capital lookups."""

import pytest

from utils.country_api import CountryApiClient


@pytest.mark.parametrize(
    ("country", "expected_capital"),
    [("Canada", "Ottawa"), ("Japan", "Tokyo")],
)
def test_country_api_returns_expected_capital(country: str, expected_capital: str) -> None:
    response, country_data = CountryApiClient().get_country(country)

    assert response.status_code == 200
    assert country_data["capital"] == expected_capital


def test_country_api_returns_requested_country() -> None:
    _, country_data = CountryApiClient().get_country("France")

    assert country_data["name"] == "France"
    assert country_data["capital"] == "Paris"
