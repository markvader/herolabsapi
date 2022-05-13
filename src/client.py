import asyncio
import logging

from aiohttp import BasicAuth, ClientSession, ClientTimeout
from aiohttp.client_exceptions import ClientError, ContentTypeError
from typing import Any, TypedDict, cast, Optional
from errors import InvalidCredentialsError, raise_client_error
from const import BASE_RESOURCE, AUTH_RESOURCE, REFRESH_TOKEN_RESOURCE, SIGN_OUT_RESOURCE
from user import User
from datetime import datetime, timedelta

LOGGER = logging.getLogger(__package__)

DEFAULT_RETRIES = 3
DEFAULT_RETRY_DELAY = 1
DEFAULT_TIMEOUT = 10


class Client:

    def __init__(
        self,
        *,
        session: ClientSession | None = None,
        logger: logging.Logger = LOGGER,
        request_retry_delay: int = DEFAULT_RETRY_DELAY,
        request_retries: int = DEFAULT_RETRIES,
    ) -> None:
        """Initialize.
        Note This is not intended to be instantiated directly; users should use the async_login class method instead.
        """
        self._logger = logger
        self._request_retries = request_retries
        self._request_retry_delay = request_retry_delay
        self._session = session

        # Intended to be populated by async_authenticate():
        self._token: str | None = None
        self._token_expiration: Optional[datetime] = None
        self._token_renewal_time: Optional[datetime] = None
        self._user_id: str | None = None

        # Intended to be populated by async_login():
        self._password: str | None = None
        self._email: str | None = None

        # These endpoints will get instantiated post-authentication:
        self.user: Optional[User] = None
        # self._property_id: Optional[str] = None
        # self._incident_id: Optional[str] = None
        #
        # self._sonic_total_sonics: Optional[int] = None
        # self._signal_total_signals: Optional[int] = None

        # self._sonic_id: Optional[str] = None
        # self._signal_id: Optional[str] = None

        # self._sonic_name: Optional[str] = None
        # self._sonic_status: Optional[str] = None
        # self._sonic_valve_state: Optional[str] = None

    @classmethod
    async def async_login(
        cls,
        email: str,
        password: str,
        *,
        session: ClientSession | None = None,
        logger: logging.Logger = LOGGER,
        request_retry_delay: int = DEFAULT_RETRY_DELAY,
        request_retries: int = DEFAULT_RETRIES,
    ) -> "Client":
        """Get a fully initialized API client."""
        # print("Logging In...")
        client = cls(
            session=session,
            logger=logger,
            request_retry_delay=request_retry_delay,
            request_retries=request_retries,
        )
        client._email = email
        client._password = password
        # print("Passing login data to async method")
        await client.async_authenticate()
        # print("async_authenticate has returned")
        return client

    async def _async_request(
        self, method: str, endpoint: str, **kwargs: dict[str, Any]
    ) -> dict[str, Any] | list[dict[str, Any]]:
        """Make an API request."""
        url = f"{BASE_RESOURCE}/{endpoint}"

        kwargs.setdefault("headers", {'Content-Type': 'application/json'})

        use_running_session = self._session and not self._session.closed
        if use_running_session:
            session = self._session
        else:
            session = ClientSession(timeout=ClientTimeout(total=DEFAULT_TIMEOUT))

        assert session

        data: dict[str, Any] | list[dict[str, Any]] = {}
        retry = 0

        while retry < self._request_retries:
            if self._token:
                kwargs["headers"]["Authorization"] = f"Bearer {self._token}"
            async with session.request(method, url, **kwargs) as resp:
                try:
                    data = await resp.json()
                except ContentTypeError:
                    # A ContentTypeError is assumed to be a credentials issue (since the
                    # API returns NGINX's default BasicAuth HTML upon 403):
                    if endpoint == AUTH_RESOURCE:
                        # If we are seeing this error upon login, we assume the
                        # email/password are bad:
                        raise InvalidCredentialsError("Invalid credentials") from None

                    # ...otherwise, we assume the token has expired, so we make a few
                    # attempts to refresh it and retry the original request:
                    retry += 1
                    self._logger.debug(
                        "Token failed; re-authenticating and trying again (attempt %s of %s)",
                        retry,
                        self._request_retries,
                    )
                    await self.async_authenticate()
                    await asyncio.sleep(self._request_retry_delay)
                    continue

                try:
                    resp.raise_for_status()
                except ClientError as err:
                    assert isinstance(data, dict)
                    raise_client_error(endpoint, data, err)

                break
        else:
            # We only end up here if we continue to have credential issues after
            # several retries:
            raise InvalidCredentialsError("Invalid credentials") from None

        if not use_running_session:
            await session.close()

        self._logger.debug("Received data for /%s: %s", endpoint, data)
        return data

    async def async_authenticate(self) -> None:
        """Retrieve and store a new access token (together with the user id).
        Acquiring an access token is a one-step process.
        Send an authorizing request with your credentials (email & password).
        All other API endpoint requests must be authenticated with an access token
        that is put in the authorization header using the Bearer scheme.
        A client may have up to 10 active tokens at a time.
        The default expiration duration should be two weeks (emails exchanged with hero labs developer)
        At my request they will add the token expiry time to the API response"""

        # Invalidate any stored token before calling for new token:
        self._token = None
        # self._token_expiration = None
        # self._token_renewal_time = None
        token_resp = cast(
            str,
            await self._async_request(
                "post", AUTH_RESOURCE,
                headers={'Content-Type': 'application/json'},
                json={'email': self._email, 'password': self._password}
            ),
        )
        self._token = token_resp["token_details"]
        # self._token_expiration = datetime.now() + timedelta(days=10)  # I am expiring the token after 10 days
        # self._token_renewal_time = self._auth_token_expiration - timedelta(days=3)  # token refreshes after 7 days

        if not self._user_id:
            self._user_id = token_resp["user_details"]["id"]
            assert self._user_id
            # print("user id retrieved: " + self._user_id)
            self.user = User(self._async_request, self._user_id)

    async def invalidate_token(self) -> None:
        """Invalidate current token."""
        data = await self._async_request("delete", SIGN_OUT_RESOURCE)
        return data

    async def refresh_token(self) -> None:
        """Refresh current token."""
        data = await self._async_request("put", REFRESH_TOKEN_RESOURCE)
        return data
