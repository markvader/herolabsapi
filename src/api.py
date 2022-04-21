import requests
from datetime import datetime, timedelta
import json
from typing import Optional
from const import (
    # API Endpoints
    AUTH_RESOURCE,
    USER_RESOURCE,
    LIST_SONICS_RESOURCE,
    LIST_SIGNALS_RESOURCE,
    LIST_INCIDENTS_RESOURCE,
    LIST_TELEMETRY_RESOURCE,
    LIST_PROPERTIES_RESOURCE,
    FETCH_NOTIFICATION_SETTINGS_RESOURCE,
    FETCH_PROPERTY_SETTINGS_RESOURCE,
    SONIC_VALVE_RESOURCE,
    REFRESH_TOKEN_RESOURCE,
    SIGN_OUT_RESOURCE,
    UPDATE_USER_RESOURCE,
    RESET_PASSWORD_RESOURCE,
)


class Api:

    def __init__(self, herolabs_email: str, herolabs_password: str):
        """
        param (str) herolabs_email = the herolabs user email
        param (str) herolabs_password = the herolabs user password
        """
        self._herolabs_email: str = herolabs_email
        self._herolabs_password: str = herolabs_password

        self._auth_token: Optional[str] = None
        self._auth_token_expiration: Optional[datetime] = None
        self._token_renewal_time: Optional[datetime] = None

        self._user_id: Optional[str] = None
        self._property_id: Optional[str] = None
        self._incident_id: Optional[str] = None

        self._sonic_total_sonics: Optional[int] = None
        self._signal_total_signals: Optional[int] = None

        self._sonic_id: Optional[str] = None
        self._signal_id: Optional[str] = None

        # self._sonic_name: Optional[str] = None
        # self._sonic_status: Optional[str] = None
        # self._sonic_valve_state: Optional[str] = None

    def _retrieve_token(self) -> None:
        """this sends a request to get an auth token
        Acquiring an access token is a one-step process.
        Send an authorizing request with your credentials (email & password).
        All other API endpoint requests must be authenticated with an access token
        that is put in the authorization header using the Bearer scheme.
        A client may have up to 10 active tokens at a time.
        The default expiration duration should be two weeks (emails exchanged with hero labs developer)
        At my request they will add the token expiry time to the API response"""
        response = requests.post(
            AUTH_RESOURCE,
            headers={
                'Content-Type': 'application/json',
            },
            json={
                'email': self._herolabs_email,
                'password': self._herolabs_password,
            }
        )
        response_data = response.json()
        self._auth_token = response_data["token_details"]
        self._user_id = response_data["user_details"]["id"]
        self._user_email = response_data["user_details"]["email"]
        self._auth_token_expiration = datetime.now() + timedelta(days=10)  # I am expiring the token after 10 days
        self._token_renewal_time = self._auth_token_expiration - timedelta(days=2)  # token refreshes after 8 days
        print("retrieve token data: ", response.text)

    def _check_token(self):
        """Check token expiry time."""
        # if no token exists, get one
        if self._auth_token is None:
            # print("no token, - acquiring now")
            self._retrieve_token()
            # print("token acquired, new expiry time: ", self._auth_token_expiration)
            return
        if datetime.now() < self._token_renewal_time:
            # print("token date valid")
            # print(self._auth_token_expiration)
            return
        if self._token_renewal_time <= datetime.now() < self._auth_token_expiration:
            # print("token expiring soon, requesting updated token")
            self._refresh_token()
            # print("new token expiry time: ", self._auth_token_expiration)
            return
        else:
            # print("no valid or in-date token")
            self._retrieve_token()
            # print("token acquired")
            # print("new token expiry time: ", self._auth_token_expiration)
            return

    def _authenticated_headers(self):
        """Returns a dict header for use within subsequent api calls"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._auth_token}"
        }
        return headers

    def _refresh_token(self):
        """Refresh access token"""
        response = requests.put(
            REFRESH_TOKEN_RESOURCE,
            headers=self._authenticated_headers(),
        )
        response_data = response.json()
        self._auth_token = response_data["token_details"]
        self._auth_token_expiration = datetime.now() + timedelta(days=10)  # I am expiring the token after 10 days
        self._token_renewal_time = self._auth_token_expiration - timedelta(days=2)  # token refreshes after 8 days
        print("Refresh Token: ", response.text)

    def _invalidate_token(self):
        """Refresh access token"""
        response = requests.delete(
            SIGN_OUT_RESOURCE,
            headers=self._authenticated_headers(),
        )
        self._auth_token: Optional[str] = None
        self._auth_token_expiration: Optional[str] = None
        self._token_renewal_time: Optional[str] = None
        print("invalidate_token status_code: ", str(response.status_code), "Token Invalidated. ", response.text)

    def _user_details(self):
        self._check_token()
        """Returns an access token's owner details."""
        user_details_url = USER_RESOURCE + self._user_id
        response = requests.get(
            user_details_url,
            headers=self._authenticated_headers(),
        )
        print("user_details: ", str(response.text))

    def _update_user_details(self, user_updates_payload) -> None:
        """Updates an access token's owner details."""
        self._check_token()
        update_user_details_url = UPDATE_USER_RESOURCE + self._user_id
        # For multiple changes use comma separation dictionary {'last_name': 'testLastName', 'language': 'en'}
        # These are passed as arguments in the function.
        # The updatable options are "email", "first_name", "last_name", "phone" (e.g "+447712345678")
        # & "language" (passed as a language value i.e "en", "pl")
        response = requests.put(
            update_user_details_url,
            headers=self._authenticated_headers(),
            data=json.dumps(user_updates_payload)
        )
        print("status_code: ", str(response.status_code), " updated_user_details: ", response.text)

    def _retrieve_sonics(self) -> None:
        self._check_token()
        """this sends a request to get a list of sonic devices token"""
        response = requests.get(
            LIST_SONICS_RESOURCE,
            headers=self._authenticated_headers()
        )
        response_data = response.json()
        print("retrieve_sonics: ", response.text)
        self._sonic_total_sonics = response_data["total_entries"]
        # For now, I am only storing the first sonic device
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

    def _retrieve_signals(self) -> None:
        self._check_token()
        """A signal object is a representation of a Signal device (sometimes called hub)
         that communicates with Wi-Fi and Sonic (a valve installed on a pipe)."""
        response = requests.get(
            LIST_SIGNALS_RESOURCE,
            headers=self._authenticated_headers()
        )
        response_data = response.json()
        print("retrieve_signals: ", response.text)
        self._signal_total_signals = response_data["total_entries"]
        # For now, I am only storing the first signal device
        self._signal_id = response_data["data"][0]["id"]
        self._signal_boot_time = response_data["data"][0]["boot_time"]
        self._signal_cloud_connection = response_data["data"][0]["cloud_connection"]
        self._signal_modem_boot_time = response_data["data"][0]["modem_boot_time"]
        self._signal_modem_version = response_data["data"][0]["modem_version"]
        self._signal_name = response_data["data"][0]["name"]
        self._signal_serial_no = response_data["data"][0]["serial_no"]
        self._signal_version = response_data["data"][0]["version"]
        self._signal_wifi_rssi = response_data["data"][0]["wifi_rssi"]

    def _retrieve_incidents(self) -> None:
        self._check_token()
        """An incident is created whenever the hero labs platform
         detects leakage, disconnection, low battery etc."""
        response = requests.get(
            LIST_INCIDENTS_RESOURCE,
            headers=self._authenticated_headers()
        )
        response_data = response.json()
        print("retrieve_incidents: ", response.text)
        self._incidents_total_incidents = response_data["total_entries"]
        # Currently, I am only recording the latest event, I will likely use the feed to build full history
        # Could also filter open/live incidents
        self._incidents_id = response_data["data"][0]["id"]
        self._incidents_detected_at = response_data["data"][0]["detected_at"]
        self._incidents_open = response_data["data"][0]["open"]
        self._incidents_possible_actions = response_data["data"][0]["possible_actions"]
        self._incidents_severity = response_data["data"][0]["severity"]
        self._incidents_state = response_data["data"][0]["state"]
        self._incidents_type = response_data["data"][0]["type"]

    def _sonic_telemetry(self):
        self._retrieve_sonics()
        """A telemetry object contains the latest telemetry details from a Sonic
         such as pressure, temperature etc."""
        sonic_telemetry_url = LIST_TELEMETRY_RESOURCE + self._sonic_id + "/telemetry"
        response = requests.get(
            sonic_telemetry_url,
            headers=self._authenticated_headers(),
        )
        response_data = response.json()
        self._telemetry_probe_time = response_data["probed_at"]
        self._telemetry_pressure = response_data["pressure"]  # pressure is reported as millibar e.g 4914 = 4.914 bar
        self._telemetry_water_flow = response_data["water_flow"]
        self._telemetry_water_temp = response_data["water_temp"]
        print("sonic_telemetry: ", response.text)

    def _retrieve_properties(self) -> None:
        self._check_token()
        """Property is the main object, and it may represent a single flat, house, apartment etc.
        It has an owner and all other objects like a sonic, signal, incidents and others
        are either directly or indirectly linked to a property."""
        response = requests.get(
            LIST_PROPERTIES_RESOURCE,
            headers=self._authenticated_headers(),
        )
        response_data = response.json()
        print("retrieve_properties: ", response.text)
        self._properties_total_properties = response_data["total_entries"]
        # For now, I am only storing the first property
        self._property_id = response_data["data"][0]["id"]
        self._property_name = response_data["data"][0]["name"]
        self._property_active = response_data["data"][0]["active"]
        self._property_address = response_data["data"][0]["address"]
        self._property_city = response_data["data"][0]["city"]
        self._property_country = response_data["data"][0]["country"]
        self._property_lat = response_data["data"][0]["lat"]
        self._property_long = response_data["data"][0]["lng"]
        self._property_postcode = response_data["data"][0]["postcode"]
        self._property_uprn = response_data["data"][0]["uprn"]

    def _property_notification_settings(self) -> None:
        self._retrieve_properties()
        """Part of the property object is notification settings where a user can configure
         what notifications they would like to receive."""
        property_notification_settings_url = FETCH_NOTIFICATION_SETTINGS_RESOURCE + self._property_id + "/notifications"
        response = requests.get(
            property_notification_settings_url,
            headers=self._authenticated_headers(),
        )
        response_data = response.json()
        self._property_notifications_cloud_disconnection = response_data["cloud_disconnection"]
        self._property_notifications_device_handle_moved = response_data["device_handle_moved"]
        self._property_notifications_health_check_failed = response_data["health_check_failed"]
        self._property_notifications_high_volume_threshold_litres = response_data["high_volume_threshold_litres"]
        self._property_notifications_long_flow_notify_delay_mins = response_data["long_flow_notification_delay_mins"]
        self._property_notifications_low_battery_level = response_data["low_battery_level"]
        self._property_notifications_pressure_test_failed = response_data["pressure_test_failed"]
        self._property_notifications_pressure_test_skipped = response_data["pressure_test_skipped"]
        self._property_notifications_radio_disconnection = response_data["radio_disconnection"]
        print("property_notifications: ", response.text)

    def _property_settings(self) -> None:
        self._retrieve_properties()
        """Part of the property object is settings where a user can configure timezone, webhook etc."""
        property_settings_url = FETCH_PROPERTY_SETTINGS_RESOURCE + self._property_id + "/settings"
        response = requests.get(
            property_settings_url,
            headers=self._authenticated_headers()
        )
        response_data = response.json()
        self._property_settings_auto_shut_off = response_data["auto_shut_off"]
        self._property_settings_pressure_tests_enabled = response_data["pressure_tests_enabled"]
        self._property_settings_pressure_tests_schedule = response_data["pressure_tests_schedule"]
        self._property_settings_timezone = response_data["timezone"]
        self._property_settings_webhook_enabled = response_data["webhook_enabled"]
        self._property_settings_webhook_url = response_data["webhook_url"]
        print("property_settings: ", response.text)

    def _sonic_valve(self, valve_action: str):
        self._retrieve_sonics()
        """A telemetry object contains the latest telemetry details from a Sonic
         such as pressure, temperature etc."""
        sonic_valve_url = SONIC_VALVE_RESOURCE + self._sonic_id + "/valve"
        response = requests.put(
            sonic_valve_url,
            headers=self._authenticated_headers(),
            json={
                "action": f"{valve_action}",  # options are open or close
            }
        )
        print("sonic_valve status_code: ", str(response.status_code), ", valve will now ", valve_action
              + response.text)

    def _reset_password_request(self, user_email: str):
        self._check_token()
        """Requests reset password email with further instructions. The endpoint returns always
        http status 204 regardless of email existence."""
        response = requests.post(
            RESET_PASSWORD_RESOURCE,
            headers=self._authenticated_headers(),
            json={
                "email": f"{user_email}",  # options are open or close
            }
        )
        print("reset_password_request status_code: ", str(response.status_code), response.text)
