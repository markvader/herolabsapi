"""Define an API endpoint manager for Signals data & actions."""
from __future__ import annotations

from datetime import datetime
from typing import Awaitable, Callable, Optional

from herolabsapi import SIGNALS_RESOURCE, PROPERTIES_RESOURCE


class Signals:
    """Define the signal manager object.
    A signal object is a representation of a Signal device (sometimes called hub)
     that communicates with Wi-Fi and Sonic (a valve installed on a pipe)."""

    def __init__(self, async_request: Callable[..., Awaitable]) -> None:
        """Initialize."""
        self._async_request: Callable[..., Awaitable] = async_request

        self._total_signals: Optional[int] = None
        self._signal_id: Optional[str] = None
        self._signal_boot_timestamp: Optional[int] = None
        self._signal_boot_datetime = None
        self._signal_cloud_connection: Optional[str] = None
        self._signal_modem_boot_timestamp: Optional[int] = None
        self._signal_modem_boot_datetime = None
        self._signal_modem_version: Optional[str] = None
        self._signal_name: Optional[str] = None
        self._signal_serial_no: Optional[str] = None
        self._signal_version: Optional[str] = None
        self._signal_wifi_rssi: Optional[int] = None

        self._first_signal_id: Optional[str] = None
        self._first_signal_boot_timestamp: Optional[int] = None
        self._first_signal_boot_datetime = None
        self._first_signal_cloud_connection: Optional[str] = None
        self._first_signal_modem_boot_timestamp: Optional[int] = None
        self._first_signal_modem_boot_datetime = None
        self._first_signal_modem_version: Optional[str] = None
        self._first_signal_name: Optional[str] = None
        self._first_signal_serial_no: Optional[str] = None
        self._first_signal_version: Optional[str] = None
        self._first_signal_wifi_rssi: Optional[int] = None

    async def async_get_total_signals(self) -> str:
        """Return the number of signals."""
        data = await self._async_request("get", SIGNALS_RESOURCE)
        self._total_signals = data["total_entries"]
        return f"Total Signal Devices = {self._total_signals}"

    async def async_get_signal_details(self) -> dict:
        """Return the list of Signal devices."""
        data = await self._async_request("get", SIGNALS_RESOURCE)
        # Should insert additional check here in case the number of signal device has increased since last polling
        # storing only first signal object currently
        if not self._total_signals:
            self._total_signals = data["total_entries"]
            assert self._total_signals
        self._first_signal_id = data["data"][0]["id"]
        self._first_signal_boot_timestamp = data["data"][0]["boot_time"]
        self._first_signal_boot_datetime = datetime.fromtimestamp(self._first_signal_boot_timestamp)
        self._first_signal_cloud_connection = data["data"][0]["cloud_connection"]
        self._first_signal_modem_boot_timestamp = data["data"][0]["modem_boot_time"]
        self._first_signal_modem_boot_datetime = datetime.fromtimestamp(self._first_signal_modem_boot_timestamp)
        self._first_signal_modem_version = data["data"][0]["modem_version"]
        self._first_signal_name = data["data"][0]["name"]
        self._first_signal_serial_no = data["data"][0]["serial_no"]
        self._first_signal_version = data["data"][0]["version"]
        self._first_signal_wifi_rssi = data["data"][0]["wifi_rssi"]
        return data

    async def async_get_signal_details_by_id(self, signal_id: str) -> dict:
        """this sends a request to get the details of a specified signal device"""
        signal_id_url = f"{SIGNALS_RESOURCE}{signal_id}"
        data = await self._async_request("get", signal_id_url)
        self._signal_id = data["id"]
        self._signal_boot_timestamp = data["boot_time"]
        self._signal_boot_datetime = datetime.fromtimestamp(self._signal_boot_timestamp)
        self._signal_cloud_connection = data["cloud_connection"]
        self._signal_modem_boot_timestamp = data["modem_boot_time"]
        self._signal_modem_boot_datetime = datetime.fromtimestamp(self._signal_modem_boot_timestamp)
        self._signal_modem_version = data["modem_version"]
        self._signal_name = data["name"]
        self._signal_serial_no = data["serial_no"]
        self._signal_version = data["version"]
        self._signal_wifi_rssi = data["wifi_rssi"]
        print(type(self._signal_boot_datetime))
        return data

    async def async_get_signal_details_by_property_id(self, property_id: str) -> dict:
        """this sends a request to get the details of signal devices registered to a specified property"""
        property_signals_url = f"{PROPERTIES_RESOURCE}{property_id}/signals"
        data = await self._async_request("get", property_signals_url)
        self._signal_id = data["id"]
        self._signal_boot_timestamp = data["boot_time"]
        self._signal_boot_datetime = datetime.fromtimestamp(self._signal_boot_timestamp)
        self._signal_cloud_connection = data["cloud_connection"]
        self._signal_modem_boot_timestamp = data["modem_boot_time"]
        self._signal_modem_boot_datetime = datetime.fromtimestamp(self._signal_modem_boot_timestamp)
        self._signal_modem_version = data["modem_version"]
        self._signal_name = data["name"]
        self._signal_serial_no = data["serial_no"]
        self._signal_version = data["version"]
        self._signal_wifi_rssi = data["wifi_rssi"]
        return data

    async def async_update_signal_details(self, signal_id: str, signal_name: str) -> dict:
        """this sends a request to update the name of the specified signal device
        name is the only value that can be updated at this endpoint"""
        signal_id_url = f"{SIGNALS_RESOURCE}{signal_id}"
        data = await self._async_request("put", signal_id_url, json={"name": f"{signal_name}"})
        self._signal_name = data["name"]
        return data
