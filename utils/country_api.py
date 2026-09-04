"""Client for the public countries.dev API used by the sample tests."""

import os
from typing import Any

import requests


class CountryApiClient:
    """Small API client that keeps endpoint and timeout details out of tests."""

    def __init__(self, base_url: str | None = None, timeout: float = 10) -> None:
        self.base_url = (base_url or os.getenv("COUNTRY_API_BASE_URL", "https://countries.dev")).rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

    def get_country(self, country: str) -> tuple[requests.Response, dict[str, Any]]:
        response = self.session.get(
            f"{self.base_url}/name/{country}",
            params={"fields": "name,capital"},
            timeout=self.timeout,
        )
        response.raise_for_status()
        payload = response.json()
        if not isinstance(payload, list) or not payload or not isinstance(payload[0], dict):
            raise ValueError(f"Unexpected country API response for {country!r}")
        return response, payload[0]

    def close(self) -> None:
        """Release the underlying HTTP connection pool."""
        self.session.close()
