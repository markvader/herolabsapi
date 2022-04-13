# Hero Labs API Python Library - api.py

import requests
from datetime import datetime
import json
from typing import Optional
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


class Api:

        # Acquiring an access token is a one-step process.
        # Send an authorizing request with your credentials (email & password).
        # All other API endpoint requests must be authenticated with an access token 
        # that is put in the authorization header using the Bearer scheme.
        # A client may have up to 10 active tokens at a time.
        
    def __init__(self, herolabs_email: str, herolabs_password: str):
        """
        param (str) herolabs_email = the herolabs user email
        param (str) herolabs_password = the herolabs user password
        """
        self._herolabs_email: str = herolabs_email
        self._herolabs_password: str = herolabs_password
        self._user_id: Optional[str] = None
        self._auth_token: Optional[str] = None
        self._auth_token_expiration: Optional[datetime] = None

    def _retrieve_token(self) -> None:
        """this sends a request to get an auth token"""
        headers = {
            'Content-Type': 'application/json',
        }
        json_data = {
            'email': self._herolabs_email,
            'password': self._herolabs_password,
        }
        response = requests.post(AUTH_RESOURCE, headers=headers, json=json_data)
        response_data = response.json()
        self._auth_token = response_data["token_details"]
        self._user_id = response_data["user_details"]["id"]
        
        # print(response.text)

    def _user_details(self) -> None:
        user_details_url = USER_RESOURCE + self._user_id
        response = requests.get(
            user_details_url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self._auth_token}"
            }
        )
        data = response.json()
        print("user_id json response: "+response.text)
