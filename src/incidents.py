# code to be refactored - incidents
#
# def _retrieve_incidents(self) -> None:
#     """An incident is created whenever the hero labs platform
#      detects leakage, disconnection, low battery etc."""
#     self._check_token()
#     response = requests.get(
#         const.LIST_INCIDENTS_RESOURCE,
#         headers=self._authenticated_headers()
#     )
#     response_data = response.json()
#     print("retrieve_incidents: ", response.text)
#     self._incidents_total_incidents = response_data["total_entries"]
#     # Currently, I am only recording the latest event, I will likely use the feed to build full history
#     # Could also filter open/live incidents
#     self._incidents_id = response_data["data"][0]["id"]
#     self._incidents_detected_at = response_data["data"][0]["detected_at"]
#     self._incidents_open = response_data["data"][0]["open"]
#     self._incidents_possible_actions = response_data["data"][0]["possible_actions"]
#     self._incidents_severity = response_data["data"][0]["severity"]
#     self._incidents_state = response_data["data"][0]["state"]
#     self._incidents_type = response_data["data"][0]["type"]
#
# def _retrieve_incident_by_id(self, incident_id: str) -> None:
#     """this sends a request to get the details of a specified incident
#     (leakage detection, disconnection, low battery etc.)"""
#     self._check_token()
#     incident_id_url = const.LIST_INCIDENTS_RESOURCE + "/" + incident_id
#     response = requests.get(
#         incident_id_url,
#         headers=self._authenticated_headers()
#     )
#     print("retrieve incident by id: ", response.text)


# def _incidents_by_property_id(self, property_id: str) -> None:
#     """this sends a request to get the incidents of a specified property"""
#     self._check_token()
#     property_incidents_url = const.FETCH_PROPERTY_SETTINGS_RESOURCE + property_id + "/incidents"
#     response = requests.get(
#         property_incidents_url,
#         headers=self._authenticated_headers(),
#     )
#     print("Incidents by specified property id: ", response.text)
#

#
# def _action_incident(self, incident_id: str, incident_action: str) -> None:
#     """Transitioning an incident to a different state"""
#     self._check_token()
#     incident_id_url = const.LIST_INCIDENTS_RESOURCE + "/" + incident_id + "/action"
#     response = requests.put(
#         incident_id_url,
#         headers=self._authenticated_headers(),
#         json={
#             "action": f"{incident_action}",  # options are "dismiss" or "reopen"
#         }
#     )
#     print("Incident " + incident_action + " completed: " + response.text)
