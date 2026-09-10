"""Environment-driven settings shared by UI and API tests.

Selection order:

1. ``TEST_ENV`` picks a named environment below (default: ``local``).
2. ``PYTEST_BASE_URL``, ``COUNTRY_API_BASE_URL`` and ``API_TIMEOUT_SECONDS``
   override individual fields of the selected environment when set.

This keeps CI explicit: a job sets ``TEST_ENV=qa`` and nothing else, or
overrides a single URL for an ephemeral deployment.
"""

import math
import os
from dataclasses import dataclass


def _as_float(value: str, name: str) -> float:
    try:
        number = float(value)
    except ValueError as error:
        raise ValueError(f"{name} must be a number, got {value!r}") from error
    if not math.isfinite(number) or number <= 0:
        raise ValueError(f"{name} must be a positive, finite number, got {value!r}")
    return number


@dataclass(frozen=True)
class EnvironmentProfile:
    """Default endpoints for one environment."""

    base_url: str
    api_base_url: str
    api_timeout_seconds: float = 10.0


# Named environments. Replace the placeholder hosts with the real ones for
# your application. "local" keeps the public sample targets so the bundled
# example tests run with no configuration.
ENVIRONMENTS: dict[str, EnvironmentProfile] = {
    "local": EnvironmentProfile(
        base_url="https://www.google.com",
        api_base_url="https://countries.dev",
    ),
    "dev": EnvironmentProfile(
        base_url="https://dev.example.com",
        api_base_url="https://api.dev.example.com",
    ),
    "qa": EnvironmentProfile(
        base_url="https://qa.example.com",
        api_base_url="https://api.qa.example.com",
    ),
    "prod": EnvironmentProfile(
        base_url="https://www.example.com",
        api_base_url="https://api.example.com",
        api_timeout_seconds=15.0,
    ),
}


@dataclass(frozen=True)
class Settings:
    """Resolved runtime settings for the selected environment."""

    environment: str
    base_url: str
    api_base_url: str
    api_timeout_seconds: float

    @classmethod
    def from_environment(cls) -> "Settings":
        name = os.getenv("TEST_ENV", "local").strip().lower()
        try:
            profile = ENVIRONMENTS[name]
        except KeyError:
            valid = ", ".join(sorted(ENVIRONMENTS))
            raise ValueError(f"TEST_ENV must be one of: {valid}; got {name!r}") from None

        timeout_override = os.getenv("API_TIMEOUT_SECONDS")

        return cls(
            environment=name,
            base_url=os.getenv("PYTEST_BASE_URL", profile.base_url).rstrip("/"),
            api_base_url=os.getenv("COUNTRY_API_BASE_URL", profile.api_base_url).rstrip("/"),
            api_timeout_seconds=(
                _as_float(timeout_override, "API_TIMEOUT_SECONDS")
                if timeout_override is not None
                else profile.api_timeout_seconds
            ),
        )


settings = Settings.from_environment()
