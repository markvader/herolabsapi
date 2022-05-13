# code to be refactored - signals

#
# def _retrieve_signals(self) -> None:
#     self._check_token()
#     """A signal object is a representation of a Signal device (sometimes called hub)
#      that communicates with Wi-Fi and Sonic (a valve installed on a pipe)."""
#     response = requests.get(
#         const.LIST_SIGNALS_RESOURCE,
#         headers=self._authenticated_headers()
#     )
#     response_data = response.json()
#     print("retrieve_signals: ", response.text)
#     self._signal_total_signals = response_data["total_entries"]
#     # For now, I am only storing the first signal device
#     self._signal_id = response_data["data"][0]["id"]
#     self._signal_boot_time_timestamp = response_data["data"][0]["boot_time"]
#     self._signal_boot_time_datetime = datetime.fromtimestamp(self._signal_boot_time_timestamp)
#     self._signal_cloud_connection = response_data["data"][0]["cloud_connection"]
#     # self._signal_modem_boot_time_timestamp = response_data["data"][0]["modem_boot_time"]
#     # # _signal_modem_boot_time_timestamp returns 0 value
#     # self._signal_modem_boot_time_datetime = datetime.fromtimestamp(self._signal_modem_boot_time_timestamp)
#     self._signal_modem_version = response_data["data"][0]["modem_version"]
#     self._signal_name = response_data["data"][0]["name"]
#     self._signal_serial_no = response_data["data"][0]["serial_no"]
#     self._signal_version = response_data["data"][0]["version"]
#     self._signal_wifi_rssi = response_data["data"][0]["wifi_rssi"]
#
# def _retrieve_signal_by_id(self, signal_id: str) -> None:
#     """this sends a request to get the details of a specified signal device"""
#     self._check_token()
#     signal_id_url = const.LIST_SIGNALS_RESOURCE + "/" + signal_id
#     response = requests.get(
#         signal_id_url,
#         headers=self._authenticated_headers()
#     )
#     print("retrieve signal data by id: ", response.text)


# def _signals_by_property_id(self, property_id: str) -> None:
#     """this sends a request to get the signals of a specified property"""
#     self._check_token()
#     property_signals_url = const.FETCH_PROPERTY_SETTINGS_RESOURCE + property_id + "/signals"
#     response = requests.get(
#         property_signals_url,
#         headers=self._authenticated_headers(),
#     )
#     print("signals by specified property id: ", response.text)

#
# def _update_signal(self, signal_id: str, signal_name: str) -> None:
#     self._check_token()
#     """this sends a request to updated the name of the specified signal device
#     name is the only value that can be updated at this endpoint"""
#     update_signal_address = const.LIST_SIGNALS_RESOURCE + "/" + signal_id
#     response = requests.put(
#         update_signal_address,
#         headers=self._authenticated_headers(),
#         json={
#             "name": f"{signal_name}",
#         }
#     )
#     print("Signal Name Updated: ", response.text)
