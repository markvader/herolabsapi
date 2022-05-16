# code to be refactored - sonic

"""Define an API endpoint manager for Sonic data & actions."""
from __future__ import annotations

import asyncio
import json
from datetime import datetime
from typing import Awaitable, Callable, Optional
from const import LIST_SONICS_RESOURCE, LIST_SONICS_WIFI_RESOURCE, LIST_TELEMETRY_RESOURCE


class Sonic:
    """Define the sonic manager object."""

    def __init__(self, async_request: Callable[..., Awaitable]) -> None:
        """Initialize."""
        self._async_request: Callable[..., Awaitable] = async_request

        self._sonic_total_sonics: Optional[int] = None
        self._first_sonic_id: Optional[str] = None

        self._sonic_name: Optional[str] = None
        self._sonic_status: Optional[str] = None
        self._sonic_valve_state: Optional[str] = None
        self._sonic_auto_shutoff_enabled: Optional[bool] = None
        self._sonic_auto_shutoff_time_limit: Optional[int] = None
        self._sonic_auto_shutoff_volume_limit: Optional[int] = None
        self._sonic_battery_level: Optional[str] = None
        self._sonic_radio_connection: Optional[str] = None
        self._sonic_radio_rssi: Optional[int] = None
        self._sonic_serial_no: Optional[str] = None

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

        self._sonic_telemetry_probe_time_timestamp: Optional[int] = None
        self._sonic_telemetry_probe_time_datetime: Optional[datetime] = None
        self._sonic_telemetry_pressure: Optional[int] = None
        self._sonic_telemetry_water_flow: Optional[float] = None
        self._sonic_telemetry_water_temp: Optional[float] = None

        self._first_sonic_telemetry_probe_time_timestamp: Optional[int] = None
        self._first_sonic_telemetry_probe_time_datetime: Optional[datetime] = None
        self._first_sonic_telemetry_pressure: Optional[int] = None
        self._first_sonic_telemetry_water_flow: Optional[float] = None
        self._first_sonic_telemetry_water_temp: Optional[float] = None

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
        """Should return the sonic wi-fi info, valid response received but no device data returned."""
        data = await self._async_request("get", LIST_SONICS_WIFI_RESOURCE)
        return data

    async def async_get_sonic_by_sonic_id(self, sonic_id: str) -> dict:
        """this sends a request to get the details of a specified sonic device"""
        sonic_id_url = f"{LIST_SONICS_RESOURCE}{sonic_id}"
        data = await self._async_request("get", sonic_id_url)
        if not self._sonic_name:
            self._sonic_name = data["name"]
            assert self._sonic_name
        if self._sonic_status is not None:
            self._sonic_status = data["status"]
            assert self._sonic_status
        # if not self._sonic_valve_state:
        #     self._sonic_valve_state = data["valve_state"]
        #     assert self._sonic_valve_state
        self._sonic_valve_state = data["valve_state"]
        self._sonic_auto_shutoff_enabled = data["auto_shut_off_enabled"]
        self._sonic_auto_shutoff_time_limit = data["auto_shut_off_time_limit"]
        self._sonic_auto_shutoff_volume_limit = data["auto_shut_off_volume_limit"]
        self._sonic_battery_level = data["battery"]
        self._sonic_radio_connection = data["radio_connection"]
        self._sonic_radio_rssi = data["radio_rssi"]
        if self._sonic_serial_no is not None:
            self._sonic_serial_no = data["serial_no"]
            assert self._sonic_serial_no
        return data

    async def async_update_sonic_by_sonic_id(self, sonic_id: str, sonic_name: str) -> None:
        """Update the sonic device. Name is the only value that can be updated at this endpoint"""
        sonic_id_url = f"{LIST_SONICS_RESOURCE}{sonic_id}"
        data = await self._async_request("put", sonic_id_url, json={"name": f"{sonic_name}"})
        return data

    async def async_update_first_sonic(self, sonic_name: str) -> None:
        """Update the first sonic device. Name is the only value that can be updated at this endpoint"""
        if not self._first_sonic_id:
            await self.async_get_sonic_details()
        sonic_id_url = f"{LIST_SONICS_RESOURCE}{self._first_sonic_id}"
        data = await self._async_request("put", sonic_id_url, json={"name": f"{sonic_name}"})
        return data

    async def async_sonic_telemetry_by_id(self, sonic_id: str) -> dict:
        """A telemetry object contains the latest telemetry details from a Sonic such as pressure, temperature etc."""
        sonic_id_url = f"{LIST_TELEMETRY_RESOURCE}{sonic_id}/telemetry"
        data = await self._async_request("get", sonic_id_url)
        self._sonic_telemetry_probe_time_timestamp = data["probed_at"]
        self._sonic_telemetry_probe_time_datetime = datetime.fromtimestamp(self._sonic_telemetry_probe_time_timestamp)
        self._sonic_telemetry_pressure = data["pressure"]  # pressure is reported as millibar e.g 4914 = 4.914 bar
        self._sonic_telemetry_water_flow = data["water_flow"]
        self._sonic_telemetry_water_temp = data["water_temp"]
        return data

    async def async_first_sonic_telemetry(self) -> dict:
        """A telemetry object contains the latest telemetry details from a Sonic such as pressure, temperature etc."""
        sonic_id_url = f"{LIST_TELEMETRY_RESOURCE}{self._first_sonic_id}/telemetry"
        data = await self._async_request("get", sonic_id_url)
        self._first_sonic_telemetry_probe_time_timestamp = data["probed_at"]
        self._first_sonic_telemetry_probe_time_datetime = \
            datetime.fromtimestamp(self._first_sonic_telemetry_probe_time_timestamp)
        self._first_sonic_telemetry_pressure = data["pressure"]  # pressure is reported as millibar e.g 4914 = 4.914 bar
        self._first_sonic_telemetry_water_flow = data["water_flow"]
        self._first_sonic_telemetry_water_temp = data["water_temp"]
        return data

    async def async_sonic_valve_control_by_id(self, sonic_id: str, valve_action: str) -> None:
        """Open / Close Valve by calling a specified sonic_id. valve_action options are "open" or "close" """
        sonic_id_url = f"{LIST_TELEMETRY_RESOURCE}{sonic_id}/valve"
        await self._async_request("put", sonic_id_url, json={"action": f"{valve_action}"})
        # Valve action endpoint does function but does not return any json response, so we must catch
        # it to avoid it raising an alternative ContentTypeError (it does return a valid 200 status code),
        # see ContentTypeError in Client._async_request function.
        # Currently I am repeating a check for current status to watch as it opens or closes
        # but will amend in the future to another cleaner loop.
        await asyncio.sleep(10)  # wait x seconds and then get sonic status and display it
        await self.async_get_sonic_by_sonic_id(sonic_id)  # get updated data on sonic status
        print(datetime.now(), " valve state is now: " + self._sonic_valve_state)
        await asyncio.sleep(10)  # wait x seconds and then get sonic status and display it
        await self.async_get_sonic_by_sonic_id(sonic_id)  # get updated data on sonic status
        print(datetime.now(), " valve state is now: " + self._sonic_valve_state)
        await asyncio.sleep(10)  # wait x seconds and then get sonic status and display it
        await self.async_get_sonic_by_sonic_id(sonic_id)  # get updated data on sonic status
        print(datetime.now(), " valve state is now: " + self._sonic_valve_state)
        await asyncio.sleep(10)  # wait x seconds and then get sonic status and display it
        await self.async_get_sonic_by_sonic_id(sonic_id)  # get updated data on sonic status
        print(datetime.now(), " valve state is now: " + self._sonic_valve_state)
        await asyncio.sleep(10)  # wait x seconds and then get sonic status and display it
        await self.async_get_sonic_by_sonic_id(sonic_id)  # get updated data on sonic status
        print(datetime.now(), " valve state is now: " + self._sonic_valve_state)
        await asyncio.sleep(10)  # wait x seconds and then get sonic status and display it
        await self.async_get_sonic_by_sonic_id(sonic_id)  # get updated data on sonic status
        print(datetime.now(), " valve state is now: " + self._sonic_valve_state)
        await asyncio.sleep(10)  # wait x seconds and then get sonic status and display it
        await self.async_get_sonic_by_sonic_id(sonic_id)  # get updated data on sonic status
        print(datetime.now(), " valve state is now: " + self._sonic_valve_state)
        await asyncio.sleep(10)  # wait x seconds and then get sonic status and display it
        await self.async_get_sonic_by_sonic_id(sonic_id)  # get updated data on sonic status
        print(datetime.now(), " valve state is now: " + self._sonic_valve_state)
        return

    async def async_first_sonic_valve_control(self, valve_action: str) -> None:
        """Open / Close First Listed Sonic Valve. valve_action options are "open" or "close" """
        sonic_id_url = f"{LIST_TELEMETRY_RESOURCE}{self._first_sonic_id}/valve"
        await self._async_request("put", sonic_id_url, json={"action": f"{valve_action}"})
        # Valve action endpoint does function but does not return any json response, so we must catch
        # it to avoid it raising an alternative ContentTypeError (it does return a valid 200 status code),
        # see ContentTypeError in Client._async_request function.
        # Currently, I am repeating a check for current status to watch as it opens or closes
        # but will amend in the future to another cleaner loop.
        await asyncio.sleep(10)  # wait x seconds and then get sonic status and display it
        await self.async_get_sonic_by_sonic_id(self._first_sonic_id)  # get updated data on sonic status
        print(datetime.now(), " valve state is now: " + self._sonic_valve_state)
        await asyncio.sleep(10)  # wait x seconds and then get sonic status and display it
        await self.async_get_sonic_by_sonic_id(self._first_sonic_id)  # get updated data on sonic status
        print(datetime.now(), " valve state is now: " + self._sonic_valve_state)
        await asyncio.sleep(10)  # wait x seconds and then get sonic status and display it
        await self.async_get_sonic_by_sonic_id(self._first_sonic_id)  # get updated data on sonic status
        print(datetime.now(), " valve state is now: " + self._sonic_valve_state)
        await asyncio.sleep(10)  # wait x seconds and then get sonic status and display it
        await self.async_get_sonic_by_sonic_id(self._first_sonic_id)  # get updated data on sonic status
        print(datetime.now(), " valve state is now: " + self._sonic_valve_state)
        await asyncio.sleep(10)  # wait x seconds and then get sonic status and display it
        await self.async_get_sonic_by_sonic_id(self._first_sonic_id)  # get updated data on sonic status
        print(datetime.now(), " valve state is now: " + self._sonic_valve_state)
        await asyncio.sleep(10)  # wait x seconds and then get sonic status and display it
        await self.async_get_sonic_by_sonic_id(self._first_sonic_id)  # get updated data on sonic status
        print(datetime.now(), " valve state is now: " + self._sonic_valve_state)
        await asyncio.sleep(10)  # wait x seconds and then get sonic status and display it
        await self.async_get_sonic_by_sonic_id(self._first_sonic_id)  # get updated data on sonic status
        print(datetime.now(), " valve state is now: " + self._sonic_valve_state)
        await asyncio.sleep(10)  # wait x seconds and then get sonic status and display it
        await self.async_get_sonic_by_sonic_id(self._first_sonic_id)  # get updated data on sonic status
        print(datetime.now(), " valve state is now: " + self._sonic_valve_state)
        return
