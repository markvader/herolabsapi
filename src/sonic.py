# code to be refactored - sonic

"""Define an API endpoint manager for Sonic data & actions."""
from __future__ import annotations

import json
from typing import Awaitable, Callable
from const import USER_RESOURCE


class Sonic:
    """Define the sonic manager object."""

    def __init__(self, async_request: Callable[..., Awaitable], sonic_id: str) -> None:
        """Initialize."""
        self._async_request = async_request
        self._sonic_id: str = sonic_id

    async def async_get_user_details(self) -> dict:
        """Return the user details."""
        user_details_url = f"{USER_RESOURCE}{self._sonic_id}"
        data = await self._async_request("get", user_details_url)
        return data

    async def async_update_user_details(self, user_updates_payload: str) -> None:
        """Update the user details."""
        update_user_details_url = f"{USER_RESOURCE}{self._sonic_id}"
        # For multiple changes use comma separation dictionary {'last_name': 'testLastName', 'language': 'en'}
        #     # These are passed as arguments in the function.
        #     # The updatable options are "email", "first_name", "last_name", "phone" (e.g "+447712345678")
        #     # & "language" (passed as a language value i.e "en", "pl")
        data = await self._async_request("put", update_user_details_url, data=json.dumps(user_updates_payload))
        return data






    #
    # def _retrieve_sonics(self) -> None:
    #     self._check_token()
    #     """this sends a request to get a list of sonic devices token"""
    #     response = requests.get(
    #         const.LIST_SONICS_RESOURCE,
    #         headers=self._authenticated_headers()
    #     )
    #     response_data = response.json()
    #     print("retrieve_sonics: ", response.text)
    #     self._sonic_total_sonics = response_data["total_entries"]
    #     # For now, I am only storing the first sonic device
    #     self._sonic_id = response_data["data"][0]["id"]
    #     self._sonic_auto_shutoff_enabled = response_data["data"][0]["auto_shut_off_enabled"]
    #     self._sonic_auto_shutoff_time_limit = response_data["data"][0]["auto_shut_off_time_limit"]
    #     self._sonic_auto_shutoff_volume_limit = response_data["data"][0]["auto_shut_off_volume_limit"]
    #     self._sonic_battery_level = response_data["data"][0]["battery"]
    #     self._sonic_name = response_data["data"][0]["name"]
    #     self._sonic_radio_connection = response_data["data"][0]["radio_connection"]
    #     self._sonic_radio_rssi = response_data["data"][0]["radio_rssi"]
    #     self._sonic_serial_no = response_data["data"][0]["serial_no"]
    #     self._sonic_status = response_data["data"][0]["status"]
    #     self._sonic_valve_state = response_data["data"][0]["valve_state"]
    #
    # def _retrieve_sonics_wifi(self) -> None:
    #     self._check_token()
    #     """this sends a request to get a list of sonic wifi"""
    #     sonic_wifi_url = const.LIST_SONICS_WIFI_RESOURCE
    #     response = requests.get(
    #         sonic_wifi_url,
    #         headers=self._authenticated_headers()
    #     )
    #     print("retrieve sonics wifi: ", response.text)
    #
    # def _retrieve_sonic_by_id(self, sonic_id: str) -> None:
    #     """this sends a request to get the details of a specified sonic device"""
    #     self._check_token()
    #     sonic_id_url = const.LIST_SONICS_RESOURCE + "/" + sonic_id
    #     response = requests.get(
    #         sonic_id_url,
    #         headers=self._authenticated_headers()
    #     )
    #     print("retrieve sonic data by id: ", response.text)

    #
    # def _sonic_telemetry(self):
    #     self._retrieve_sonics()
    #     """A telemetry object contains the latest telemetry details from a Sonic
    #      such as pressure, temperature etc."""
    #     sonic_telemetry_url = const.LIST_TELEMETRY_RESOURCE + self._sonic_id + "/telemetry"
    #     response = requests.get(
    #         sonic_telemetry_url,
    #         headers=self._authenticated_headers(),
    #     )
    #     response_data = response.json()
    #     self._telemetry_probe_time_timestamp = response_data["probed_at"]
    #     self._telemetry_probe_time_datetime = datetime.fromtimestamp(self._telemetry_probe_time_timestamp)
    #     self._telemetry_pressure = response_data["pressure"]  # pressure is reported as millibar e.g 4914 = 4.914 bar
    #     self._telemetry_water_flow = response_data["water_flow"]
    #     self._telemetry_water_temp = response_data["water_temp"]
    #     print("sonic_telemetry: ", response.text)


    # def _sonics_by_signal_id(self, signal_id: str) -> None:
    #     """this sends a request to get the signals of a specified property"""
    #     self._check_token()
    #     sonics_signals_url = const.LIST_SIGNALS_RESOURCE + "/" + signal_id + "/sonics"
    #     response = requests.get(
    #         sonics_signals_url,
    #         headers=self._authenticated_headers(),
    #     )
    #     print("sonics by specified signal id: ", response.text)
    #

    # def _sonic_valve(self, valve_action: str):
    #     self._retrieve_sonics()
    #     """A telemetry object contains the latest telemetry details from a Sonic
    #      such as pressure, temperature etc."""
    #     sonic_valve_url = const.SONIC_VALVE_RESOURCE + self._sonic_id + "/valve"
    #     response = requests.put(
    #         sonic_valve_url,
    #         headers=self._authenticated_headers(),
    #         json={
    #             "action": f"{valve_action}",  # options are open or close
    #         }
    #     )
    #     print("sonic_valve status_code: ", str(response.status_code), ", valve will now ", valve_action
    #           + response.text)

    #
    # def _update_sonic(self, sonic_id: str, sonic_name: str) -> None:
    #     self._check_token()
    #     """this sends a request to updated the name of the specified sonic device.
    #     Name is the only value that can be updated at this endpoint"""
    #     update_sonic_address = const.LIST_SONICS_RESOURCE + "/" + sonic_id
    #     response = requests.put(
    #         update_sonic_address,
    #         headers=self._authenticated_headers(),
    #         json={
    #             "name": f"{sonic_name}",
    #         }
    #     )
    #     print("Sonic Name Updated: ", response.text)
