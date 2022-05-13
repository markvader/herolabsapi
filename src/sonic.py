# code to be refactored - sonic

"""Define an API endpoint manager for Sonic data & actions."""
from __future__ import annotations

import json
from typing import Awaitable, Callable, Optional
from const import LIST_SONICS_RESOURCE, LIST_SONICS_WIFI_RESOURCE


class Sonic:
    """Define the sonic manager object."""

    def __init__(self, async_request: Callable[..., Awaitable]) -> None:
        """Initialize."""
        self._async_request: Callable[..., Awaitable] = async_request

        self._sonic_total_sonics: Optional[int] = None
        self._first_sonic_id: Optional[str] = None

        self._first_sonic_name: Optional[str] = None
        self._first_sonic_status: Optional[str] = None
        self._first_sonic_valve_state: Optional[str] = None
        self._first_sonic_auto_shutoff_enabled: Optional[bool] = None
        self._first_sonic_auto_shutoff_time_limit: Optional[int] = None
        self._first_sonic_auto_shutoff_volume_limit: Optional[int] = None
        self._first_sonic_battery_level: Optional[str] = None
        self._first_sonic_radio_connection: Optional[str] = None
        self._first_sonic_radio_rssi: Optional[int] = None
        self._first_sonic_serial_no: Optional[str] = None

    async def async_get_sonic_details(self) -> dict:
        """Return the list of sonic devices."""
        data = await self._async_request("get", LIST_SONICS_RESOURCE)
        # Should insert additional check here in case the number of sonic device has increased since last polling
        if not self._sonic_total_sonics:
            self._sonic_total_sonics = data["total_entries"]
            assert self._sonic_total_sonics
        if not self._first_sonic_id:
            self._first_sonic_id = data["data"][0]["id"]
            assert self._first_sonic_id
        if not self._first_sonic_name:
            self._first_sonic_name = data["data"][0]["name"]
            assert self._first_sonic_name
        if self._first_sonic_status is not None:
            self._first_sonic_status = data["data"][0]["status"]
            assert self._first_sonic_status
        if not self._first_sonic_valve_state:
            self._first_sonic_valve_state = data["data"][0]["valve_state"]
            assert self._first_sonic_valve_state
            self._first_sonic_auto_shutoff_enabled = data["data"][0]["auto_shut_off_enabled"]
            self._first_sonic_auto_shutoff_time_limit = data["data"][0]["auto_shut_off_time_limit"]
            self._first_sonic_auto_shutoff_volume_limit = data["data"][0]["auto_shut_off_volume_limit"]
            self._first_sonic_battery_level = data["data"][0]["battery"]
            self._first_sonic_radio_connection = data["data"][0]["radio_connection"]
            self._first_sonic_radio_rssi = data["data"][0]["radio_rssi"]
            self._first_sonic_serial_no = data["data"][0]["serial_no"]
        return data

    async def async_get_sonic_wifi(self) -> dict:
        """Should return the sonic wifi info, valid response received but no device data returned."""
        data = await self._async_request("get", LIST_SONICS_WIFI_RESOURCE)
        return data


    # async def async_update_user_details(self, user_updates_payload: str) -> None:
    #     """Update the user details."""
    #     update_user_details_url = f"{USER_RESOURCE}{self._sonic_id}"
    #     data = await self._async_request("put", update_user_details_url, data=json.dumps(user_updates_payload))
    #     return data

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
