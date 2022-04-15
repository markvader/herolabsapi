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
        self._property_id: Optional[str] = None
        self._incident_id: Optional[str] = None

        self._sonic_total_sonics: Optional[int] = None
        self._sonic_id: Optional[str] = None
        self._sonic_auto_shutoff_enabled: Optional[bool] = None
        self._sonic_auto_shutoff_time_limit: Optional[int] = None
        self._sonic_auto_shutoff_volume_limit: Optional[int] = None
        self._sonic_battery_level: Optional[str] = None
        self._sonic_name: Optional[str] = None
        self._sonic_radio_connection: Optional[str] = None
        self._sonic_radio_rssi: Optional[int] = None
        self._sonic_serial_no: Optional[str] = None
        self._sonic_status: Optional[str] = None
        self._sonic_valve_state: Optional[str] = None

        self._signal_total_signals: Optional[int] = None
        self._signal_id: Optional[str] = None
        self._signal_boot_time: Optional[int] = None
        self._signal_cloud_connection: Optional[str] = None
        self._signal_modem_boot_time: Optional[int] = None
        self._signal_modem_version: Optional[str] = None
        self._signal_name: Optional[str] = None
        self._signal_serial_no: Optional[str] = None
        self._signal_version: Optional[str] = None
        self._signal_wifi_rssi: Optional[int] = None

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
        print(response.text)

    def _user_details(self):
        user_details_url = USER_RESOURCE + self._user_id
        response = requests.get(
            user_details_url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self._auth_token}"
            }
        )
        data = response.json()

        print(response.text)
        return data

    def _retrieve_sonics(self) -> None:
        """this sends a request to get a list of sonic devices token"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._auth_token}"
        }
        response = requests.get(LIST_SONICS_RESOURCE, headers=headers)
        response_data = response.json()
        print(response_data)
        self._sonic_total_sonics = response_data["total_entries"] #need to do something if total sonics > 1
        self._sonic_id = response_data["data"][0]["id"]
        self._sonic_auto_shutoff_enabled = response_data["data"][0]["auto_shut_off_enabled"]
        self._sonic_auto_shutoff_time_limit = response_data["data"][0]["auto_shut_off_time_limit"]
        self._sonic_auto_shutoff_volume_limit = response_data["data"][0]["auto_shut_off_volume_limit"]
        self._sonic_battery_level = response_data["data"][0]["battery"]
        self._sonic_name = response_data["data"][0]["name"]
        self._sonic_radio_connection = response_data["data"][0]["radio_connection"]
        self._sonic_radio_rssi = response_data["data"][0]["radio_rssi"]
        self._sonic_serial_no = response_data["data"][0]["serial_no"]
        self._sonic_status = response_data["data"][0]["status"]
        self._sonic_valve_state = response_data["data"][0]["valve_state"]
        # print(self._sonic_total_sonics)
        # print(self._sonic_id)
        # print(self._sonic_auto_shutoff_enabled)
        # print(self._sonic_auto_shutoff_time_limit)
        # print(self._sonic_auto_shutoff_volume_limit)
        # print(self._sonic_battery_level)
        # print(self._sonic_name)
        # print(self._sonic_radio_connection)
        # print(self._sonic_radio_rssi)
        # print(self._sonic_serial_no)
        # print(self._sonic_status)
        # print(self._sonic_valve_state)

    def _retrieve_signals(self) -> None:
        """A signal object is a representation of a Signal device (sometimes called hub)
         that communicates with WiFi and Sonic (a valve installed on a pipe)."""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._auth_token}"
        }
        response = requests.get(LIST_SIGNALS_RESOURCE, headers=headers)
        response_data = response.json()
        print(response_data)
        self._signal_total_signals = response_data["total_entries"] #need to do something if total signals > 1
        self._signal_id = response_data["data"][0]["id"]
        self._signal_boot_time = response_data["data"][0]["boot_time"]
        self._signal_cloud_connection = response_data["data"][0]["cloud_connection"]
        self._signal_modem_boot_time = response_data["data"][0]["modem_boot_time"]
        self._signal_modem_version = response_data["data"][0]["modem_version"]
        self._signal_name = response_data["data"][0]["name"]
        self._signal_serial_no = response_data["data"][0]["serial_no"]
        self._signal_version = response_data["data"][0]["version"]
        self._signal_wifi_rssi = response_data["data"][0]["wifi_rssi"]
        # print(self._signal_total_signals)
        # print(self._signal_id)
        # print(self._signal_boot_time)
        # print(self._signal_cloud_connection)
        # print(self._signal_modem_boot_time)
        # print(self._signal_modem_version)
        # print(self._signal_name)
        # print(self._signal_serial_no)
        # print(self._signal_version)
        # print(self._signal_wifi_rssi)
