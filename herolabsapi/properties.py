""""Define an API endpoint manager for Properties data & actions."""
from __future__ import annotations

import json
from typing import Awaitable, Callable

from herolabsapi import PROPERTIES_RESOURCE


class Properties:
    """Define the property manager object.
    Property is the main object, and it may represent a single flat, house, apartment etc.
    It has an owner and all other objects like a sonic, signal, incidents and others
    are either directly or indirectly linked to a property."""

    def __init__(self, async_request: Callable[..., Awaitable]) -> None:
        """Initialize."""
        self._async_request: Callable[..., Awaitable] = async_request

    async def async_get_total_properties(self) -> str:
        """Return the number of properties."""
        data = await self._async_request("get", PROPERTIES_RESOURCE)
        return data["total_entries"]

    async def async_get_all_property_details(self) -> dict:
        """Return the list of properties."""
        return await self._async_request("get", PROPERTIES_RESOURCE)

    async def async_get_property_details(self, property_id: str) -> dict:
        """Return the specified property details."""
        property_id_url = f"{PROPERTIES_RESOURCE}{property_id}"
        return await self._async_request("get", property_id_url)

    async def async_get_property_notification_settings(self, property_id: str) -> dict:
        """Part of the property object is notification settings where a user can configure
        what notifications they would like to receive."""
        property_id_url = f"{PROPERTIES_RESOURCE}{property_id}/notifications"
        return await self._async_request("get", property_id_url)

    async def async_get_property_settings(self, property_id: str) -> dict:
        """Part of the property object is settings where a user can configure timezone, webhook etc."""
        property_id_url = f"{PROPERTIES_RESOURCE}{property_id}/settings"
        return await self._async_request("get", property_id_url)

    async def async_update_property_details(self, property_id: str, property_updates_payload: dict) -> None:
        """The key/values pairs that can be updated are:
        active	(boolean) - Whether the property is active or not
        address (string) - Property address
        city (string) - Property city
        country (string) - Property country
        lat	(number) - Property latitude
        lng	(number) - Property longitude
        name (string) - Property name
        postcode (string) - Property postcode
        uprn (string) - Property uprn"""
        property_id_url = f"{PROPERTIES_RESOURCE}{property_id}"
        return await self._async_request("put", property_id_url, data=json.dumps(property_updates_payload))

    async def async_update_property_notifications(self, property_id: str,
                                                  property_notification_updates_payload: dict) -> None:
        """The key/values pairs that can be updated are:
        high_volume_threshold_litres (int) - valve of int must be one of:
        [25, 50, 75, 100, 150, 200, 250, 300, 400, 500, 600, 800, 1000]
        long_flow_notification_delay_mins (int) - valve of int must be one of:
        [15, 30, 60, 120, 180, 240, 300, 360]
        cloud_disconnection (bool)
        device_handle_moved (bool),
        health_check_failed (bool)
        low_battery_level (bool)
        pressure_test_failed (bool)
        pressure_test_skipped (bool)
        radio_disconnection (bool)"""
        property_id_url = f"{PROPERTIES_RESOURCE}{property_id}/notifications"
        return await self._async_request("put", property_id_url, data=json.dumps(property_notification_updates_payload))

    async def async_update_property_settings(self, property_id: str, property_settings_updates_payload: dict) -> None:
        """The key/values pairs that can be updated are:
        auto_shut_off (bool) - Automatic shut off
        pressure_tests_enabled (bool) - Enable or disable the pressure test
        pressure_tests_schedule (string) - Time in a day when the pressure test runs. The format is HH:MM:SS in 24h clock.
        timezone (string) - Property timezone e.g."Europe/London"
        webhook_enabled (bool)
        webhook_url (string)"""
        property_id_url = f"{PROPERTIES_RESOURCE}{property_id}/settings"
        return await self._async_request("put", property_id_url, data=json.dumps(property_settings_updates_payload))
