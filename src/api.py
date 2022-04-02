# Hero Labs API Python Library - api.py

import logging
import json
from requests import request, Session

from sonic import Sonic

from const import (
    # API Endpoints
    AUTH_RESOURCE,
    USER_RESOURCE,
    REFRESH_TOKEN_RESOURCE,
    SIGN_OUT_RESOURCE,
    UPDATE_USER_RESOURCE,
    RESET_PASSWORD_RESOURCE,
    LIST_PROPERTIES_RESOURCE,
    FETCH_NOTIFICATION_SETTINGS_RESOURCE,
    FETCH_PROPERTY_SETTINGS_RESOURCE,
    LIST_SIGNALS_RESOURCE,
    LIST_SONICS_RESOURCE,
    LIST_INCIDENTS_RESOURCE,
    LIST_TELEMETRY_RESOURCE,
)

_LOGGER = logging.getLogger(__name__)

class Api:

        # Acquiring an access token is a one-step process.
        # Send an authorizing request with your credentials (email & password).
        # All other API endpoint requests must be authenticated with an access token 
        # that is put in the authorization header using the Bearer scheme.
        # A client may have up to 10 active tokens at a time.

    def __init__(self, timeout=10, command_timeout=60, http_session: Session = None):
        self._timeout = timeout
        self._command_timeout = command_timeout
        self._http_session = http_session

    def sign_in(self, email, password):
        response = self._call_api(
            "post", 
            AUTH_RESOURCE,
            params = None,
            headers = {
                'Content-Type': 'application/json'
            },
            json = { 
                'email': email,
                'password':  password
            })
        
        return response

    def _call_api(self, method, url, headers, params, **kwargs):
        payload = kwargs.get("params") or kwargs.get("json")

        if "timeout" not in kwargs:
            kwargs["timeout"] = self._timeout
        
        _LOGGER.debug("Calling %s with payload=%s", url, payload)

        response = self._http_session.request(method, url, headers = headers, params = params, **kwargs) if\
            self._http_session is not None else\
            request(method, url, headers = headers, params = params, **kwargs)

        _LOGGER.debug("API Response received: %s - %s", response.status_code, response.content)

        response.raise_for_status()

        return response

    def get_userDetails(self, token_details, userId):
        #This Api call returns an access token's owner details.
        headers = {
            'Content-Type': 'application/json',
            'Authorization': "Bearer "+token_details
        }
        params = None,
        user_info_url = USER_RESOURCE+userId
        userDetails = self._call_api("get", user_info_url, headers, params).json()
        return userDetails
          