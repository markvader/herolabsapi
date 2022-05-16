""""Define an API endpoint manager for Incidents data & actions."""
from __future__ import annotations

from datetime import datetime
from typing import Awaitable, Callable, Optional
from const import LIST_INCIDENTS_RESOURCE, LIST_PROPERTIES_RESOURCE


class Incidents:
    """Define the incident manager object.
    An incident is created whenever the hero labs platform detects leakage, disconnection, low battery etc."""

    def __init__(self, async_request: Callable[..., Awaitable]) -> None:
        """Initialize."""
        self._async_request: Callable[..., Awaitable] = async_request

        self._total_incidents: Optional[int] = None
        self._incidents_id: Optional[str] = None
        self._incidents_detected_at: Optional[str] = None
        self._incidents_open: Optional[bool] = None
        self._incidents_possible_actions: Optional[list] = None
        self._incidents_severity: Optional[str] = None
        self._incidents_sonic_id: Optional[str] = None
        self._incidents_state: Optional[str] = None
        self._incidents_type: Optional[str] = None

        self._first_incidents_id: Optional[str] = None
        self._first_incidents_detected_at: Optional[str] = None
        self._first_incidents_open: Optional[bool] = None
        self._first_incidents_possible_actions: Optional[list] = None
        self._first_incidents_severity: Optional[str] = None
        self._first_incidents_sonic_id: Optional[str] = None
        self._first_incidents_state: Optional[str] = None
        self._first_incidents_type: Optional[str] = None

    async def async_get_incidents(self) -> dict:
        """Return the list of Incidents."""
        data = await self._async_request("get", LIST_INCIDENTS_RESOURCE)
        # Currently, I am only recording the latest event, I will likely use the feed to build full history
        # Could also filter open/live incidents
        self._total_incidents = data["total_entries"]
        self._first_incidents_id = data["data"][0]["id"]
        self._first_incidents_open = data["data"][0]["open"]
        self._first_incidents_severity = data["data"][0]["severity"]
        self._first_incidents_detected_at = data["data"][0]["detected_at"]
        self._first_incidents_possible_actions = data["data"][0]["possible_actions"]
        self._first_incidents_state = data["data"][0]["state"]
        self._first_incidents_type = data["data"][0]["type"]
        self._first_incidents_sonic_id = data["data"][0]["sonic_id"]
        return data

    async def async_get_incident_details(self, incident_id) -> dict:
        """Return the details on specified incident. (leakage detection, disconnection, low battery etc.)"""
        incident_id_url = f"{LIST_INCIDENTS_RESOURCE}{incident_id}"
        data = await self._async_request("get", incident_id_url)
        self._incidents_id = data["id"]
        self._incidents_detected_at = data["detected_at"]
        self._incidents_open = data["open"]
        self._incidents_possible_actions = data["possible_actions"]
        self._incidents_severity = data["severity"]
        self._incidents_sonic_id = data["sonic_id"]
        self._incidents_state = data["state"]
        self._incidents_type = data["type"]
        return data

    async def async_get_incidents_by_property(self, property_id) -> dict:
        """Return the details of incidents on a specified property.
        (leakage detection, disconnection, low battery etc.)"""
        incident_id_url = f"{LIST_PROPERTIES_RESOURCE}{property_id}/incidents"
        data = await self._async_request("get", incident_id_url)
        self._total_incidents = data["total_entries"]
        self._first_incidents_id = data["data"][0]["id"]
        self._first_incidents_open = data["data"][0]["open"]
        self._first_incidents_severity = data["data"][0]["severity"]
        self._first_incidents_detected_at = data["data"][0]["detected_at"]
        self._first_incidents_possible_actions = data["data"][0]["possible_actions"]
        self._first_incidents_state = data["data"][0]["state"]
        self._first_incidents_type = data["data"][0]["type"]
        self._first_incidents_sonic_id = data["data"][0]["sonic_id"]
        return data

    async def async_action_incident(self, incident_id: str, incident_action: str) -> str:
        """Transitioning an incident to a different state. incident_action options are "dismiss" or "reopen" """
        incident_id_url = f"{LIST_INCIDENTS_RESOURCE}{incident_id}/action"
        await self._async_request("put", incident_id_url, json={"action": f"{incident_action}"})
        return f"Incident has been {incident_action}ed"
