"""Environment-driven settings shared by UI and API tests."""

import os
from dataclasses import dataclass


def _as_float(value: str, name: str) -> float:
    try:
        return float(value)
    except ValueError as error:
        raise ValueError(f"{name} must be a number, got {value!r}") from error


@dataclass(frozen=True)
class Settings:
    """Runtime settings with safe defaults for the sample tests."""

    environment: str
    base_url: str
    api_base_url: str
    api_timeout_seconds: float

    @classmethod
    def from_environment(cls) -> "Settings":
        return cls(
            environment=os.getenv("TEST_ENV", "local"),
            base_url=os.getenv("PYTEST_BASE_URL", "https://www.google.com").rstrip("/"),
            api_base_url=os.getenv("COUNTRY_API_BASE_URL", "https://countries.dev").rstrip("/"),
            api_timeout_seconds=_as_float(os.getenv("API_TIMEOUT_SECONDS", "10"), "API_TIMEOUT_SECONDS"),
        )


settings = Settings.from_environment()

