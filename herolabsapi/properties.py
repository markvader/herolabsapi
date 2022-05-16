""""Define an API endpoint manager for Properties data & actions."""
from __future__ import annotations

from typing import Awaitable, Callable, Optional

from herolabsapi.const import LIST_PROPERTIES_RESOURCE, FETCH_PROPERTY_SETTINGS_RESOURCE, FETCH_NOTIFICATION_SETTINGS_RESOURCE


class Properties:
    """Define the property manager object.
    Property is the main object, and it may represent a single flat, house, apartment etc.
    It has an owner and all other objects like a sonic, signal, incidents and others
    are either directly or indirectly linked to a property."""

    def __init__(self, async_request: Callable[..., Awaitable]) -> None:
        """Initialize."""
        self._async_request: Callable[..., Awaitable] = async_request

        self._total_properties: Optional[int] = None

        self._property_id: Optional[str] = None
        self._property_name: Optional[str] = None
        self._property_active: Optional[bool] = None
        self._property_address: Optional[str] = None
        self._property_city: Optional[str] = None
        self._property_country: Optional[str] = None
        self._property_lat: Optional[str] = None
        self._property_long: Optional[str] = None
        self._property_postcode: Optional[str] = None
        self._property_uprn: Optional[str] = None

        self._first_property_id: Optional[str] = None
        self._first_property_name: Optional[str] = None
        self._first_property_active: Optional[bool] = None
        self._first_property_address: Optional[str] = None
        self._first_property_city: Optional[str] = None
        self._first_property_country: Optional[str] = None
        self._first_property_lat: Optional[str] = None
        self._first_property_long: Optional[str] = None
        self._first_property_postcode: Optional[str] = None
        self._first_property_uprn: Optional[str] = None

        self._property_notifications_cloud_disconnection: Optional[bool] = None
        self._property_notifications_device_handle_moved: Optional[bool] = None
        self._property_notifications_health_check_failed: Optional[bool] = None
        self._property_notifications_high_volume_threshold_litres: Optional[int] = None
        self._property_notifications_long_flow_notify_delay_mins: Optional[int] = None
        self._property_notifications_low_battery_level: Optional[bool] = None
        self._property_notifications_pressure_test_failed: Optional[bool] = None
        self._property_notifications_pressure_test_skipped: Optional[bool] = None
        self._property_notifications_radio_disconnection: Optional[bool] = None

        self._property_settings_webhook_url: Optional[str] = None
        self._property_settings_webhook_enabled: Optional[bool] = None
        self._property_settings_timezone: Optional[str] = None
        self._property_settings_pressure_tests_schedule: Optional[str] = None
        self._property_settings_pressure_tests_enabled: Optional[bool] = None
        self._property_settings_auto_shut_off: Optional[bool] = None

    async def async_get_total_properties(self) -> str:
        """Return the number of properties."""
        data = await self._async_request("get", LIST_PROPERTIES_RESOURCE)
        self._total_properties = data["total_entries"]
        return f"Total Properties = {self._total_properties}"

    async def async_get_property_details(self) -> dict:
        """Return the list of properties."""
        data = await self._async_request("get", LIST_PROPERTIES_RESOURCE)
        # Should insert additional check here in case the number of sonic device has increased since last polling
        # storing only first property object currently
        if not self._total_properties:
            self._total_properties = data["total_entries"]
            assert self._total_properties
        self._first_property_id = data["data"][0]["id"]
        self._first_property_name = data["data"][0]["name"]
        self._first_property_active = data["data"][0]["active"]
        self._first_property_address = data["data"][0]["address"]
        self._first_property_city = data["data"][0]["city"]
        self._first_property_country = data["data"][0]["country"]
        self._first_property_lat = data["data"][0]["lat"]
        self._first_property_long = data["data"][0]["lng"]
        self._first_property_postcode = data["data"][0]["postcode"]
        self._first_property_uprn = data["data"][0]["uprn"]
        return data

    async def async_get_property_details_by_id(self, property_id: str) -> dict:
        """Return the specified property details."""
        property_id_url = f"{LIST_PROPERTIES_RESOURCE}{property_id}"
        data = await self._async_request("get", property_id_url)
        self._property_id = data["id"]
        self._property_name = data["name"]
        self._property_active = data["active"]
        self._property_address = data["address"]
        self._property_city = data["city"]
        self._property_country = data["country"]
        self._property_lat = data["lat"]
        self._property_long = data["lng"]
        self._property_postcode = data["postcode"]
        self._property_uprn = data["uprn"]
        return data

    async def async_get_property_notification_settings(self, property_id: str) -> dict:
        """Part of the property object is notification settings where a user can configure
        what notifications they would like to receive."""
        property_id_url = f"{FETCH_NOTIFICATION_SETTINGS_RESOURCE}{property_id}/notifications"
        data = await self._async_request("get", property_id_url)
        self._property_notifications_cloud_disconnection = data["cloud_disconnection"]
        self._property_notifications_device_handle_moved = data["device_handle_moved"]
        self._property_notifications_health_check_failed = data["health_check_failed"]
        self._property_notifications_high_volume_threshold_litres = data["high_volume_threshold_litres"]
        self._property_notifications_long_flow_notify_delay_mins = data["long_flow_notification_delay_mins"]
        self._property_notifications_low_battery_level = data["low_battery_level"]
        self._property_notifications_pressure_test_failed = data["pressure_test_failed"]
        self._property_notifications_pressure_test_skipped = data["pressure_test_skipped"]
        self._property_notifications_radio_disconnection = data["radio_disconnection"]
        return data

    async def async_get_property_settings(self, property_id: str) -> dict:
        """Part of the property object is settings where a user can configure timezone, webhook etc."""
        property_id_url = f"{FETCH_PROPERTY_SETTINGS_RESOURCE}{property_id}/settings"
        data = await self._async_request("get", property_id_url)
        self._property_settings_auto_shut_off = data["auto_shut_off"]
        self._property_settings_pressure_tests_enabled = data["pressure_tests_enabled"]
        self._property_settings_pressure_tests_schedule = data["pressure_tests_schedule"]
        self._property_settings_timezone = data["timezone"]
        self._property_settings_webhook_enabled = data["webhook_enabled"]
        self._property_settings_webhook_url = data["webhook_url"]
        return data

    async def async_update_property_details(self, property_id: str, **kwargs) -> None:
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
        property_id_url = f"{LIST_PROPERTIES_RESOURCE}{property_id}"
        data = await self._async_request("put", property_id_url, **kwargs)
        return data
