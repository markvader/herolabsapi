"""Define package exceptions."""
from __future__ import annotations

from typing import Any


class HeroLabsError(Exception):
    """Define a base exception."""

    pass


class InvalidCredentialsError(HeroLabsError):
    """Define an error related to invalid credentials (Error 401 - Unauthorized)."""

    pass


class ServiceUnavailableError(HeroLabsError):
    """Define an error related to the service being unavailable (Error 503 - Service Unavailable)."""

    pass


class TooManyRequestsError(HeroLabsError):
    """Define an error related to too many requests (Error 429 - Too Many Requests)."""

    pass


class InvalidScopeError(HeroLabsError):
    """Define an error related to requesting a resource for which we aren't scope."""

    pass


class RequestError(HeroLabsError):
    """Define an error related to a bad HTTP request."""

    pass


ERROR_MESSAGE_TO_EXCEPTION_MAP = {
    "Invalid scope": InvalidScopeError,
}


def raise_client_error(endpoint: str, data: dict[str, Any], err: Exception) -> None:
    """Wrap an aiohttp.exceptions.ClientError in the correct exception type."""
    if "message" in data:
        msg = data["message"]
    else:
        msg = data["error"]

    try:
        [exception] = [v for k, v in ERROR_MESSAGE_TO_EXCEPTION_MAP.items() if k in msg]
    except ValueError:
        exception = RequestError

    raise exception(f"Error while requesting /{endpoint}: {msg}") from err
