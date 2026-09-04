"""Sample API tests for country and capital lookups."""

import pytest

from utils.country_api import CountryApiClient


@pytest.mark.parametrize(
    ("country", "expected_capital"),
    [("Canada", "Ottawa"), ("Japan", "Tokyo")],
)
@pytest.mark.api
@pytest.mark.smoke
def test_country_api_returns_expected_capital(
    country_api: CountryApiClient,
    country: str,
    expected_capital: str,
) -> None:
    response, country_data = country_api.get_country(country)

    assert response.status_code == 200
    assert country_data["capital"] == expected_capital


@pytest.mark.api
@pytest.mark.regression
def test_country_api_returns_requested_country(country_api: CountryApiClient) -> None:
    _, country_data = country_api.get_country("France")

    assert country_data["name"] == "France"
    assert country_data["capital"] == "Paris"
