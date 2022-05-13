# code to be refactored - properties








    #
    # def _retrieve_properties(self) -> None:
    #     self._check_token()
    #     """Property is the main object, and it may represent a single flat, house, apartment etc.
    #     It has an owner and all other objects like a sonic, signal, incidents and others
    #     are either directly or indirectly linked to a property."""
    #     response = requests.get(
    #         const.LIST_PROPERTIES_RESOURCE,
    #         headers=self._authenticated_headers(),
    #     )
    #     response_data = response.json()
    #     print("retrieve_properties: ", response.text)
    #     self._properties_total_properties = response_data["total_entries"]
    #     # For now, I am only storing the first property
    #     self._property_id = response_data["data"][0]["id"]
    #     self._property_name = response_data["data"][0]["name"]
    #     self._property_active = response_data["data"][0]["active"]
    #     self._property_address = response_data["data"][0]["address"]
    #     self._property_city = response_data["data"][0]["city"]
    #     self._property_country = response_data["data"][0]["country"]
    #     self._property_lat = response_data["data"][0]["lat"]
    #     self._property_long = response_data["data"][0]["lng"]
    #     self._property_postcode = response_data["data"][0]["postcode"]
    #     self._property_uprn = response_data["data"][0]["uprn"]
    #
    # def _retrieve_property_by_id(self, property_id: str) -> None:
    #     """this sends a request to get the details of a specified property"""
    #     self._check_token()
    #     property_id_url = const.LIST_PROPERTIES_RESOURCE + "/" + property_id
    #     response = requests.get(
    #         property_id_url,
    #         headers=self._authenticated_headers()
    #     )
    #     print("retrieve property by id: ", response.text)
    #
    # def _property_notification_settings(self) -> None:
    #     self._retrieve_properties()
    #     """Part of the property object is notification settings where a user can configure
    #      what notifications they would like to receive."""
    #     property_notification_settings_url = const.FETCH_NOTIFICATION_SETTINGS_RESOURCE + self._property_id + "/notifications"
    #     response = requests.get(
    #         property_notification_settings_url,
    #         headers=self._authenticated_headers(),
    #     )
    #     response_data = response.json()
    #     self._property_notifications_cloud_disconnection = response_data["cloud_disconnection"]
    #     self._property_notifications_device_handle_moved = response_data["device_handle_moved"]
    #     self._property_notifications_health_check_failed = response_data["health_check_failed"]
    #     self._property_notifications_high_volume_threshold_litres = response_data["high_volume_threshold_litres"]
    #     self._property_notifications_long_flow_notify_delay_mins = response_data["long_flow_notification_delay_mins"]
    #     self._property_notifications_low_battery_level = response_data["low_battery_level"]
    #     self._property_notifications_pressure_test_failed = response_data["pressure_test_failed"]
    #     self._property_notifications_pressure_test_skipped = response_data["pressure_test_skipped"]
    #     self._property_notifications_radio_disconnection = response_data["radio_disconnection"]
    #     print("property_notifications: ", response.text)
    #
    # def _property_notification_settings_by_property_id(self, property_id: str) -> None:
    #     """this sends a request to get the notification settings of a specified property"""
    #     self._check_token()
    #     property_notification_settings_url = const.FETCH_NOTIFICATION_SETTINGS_RESOURCE + property_id + "/notifications"
    #     response = requests.get(
    #         property_notification_settings_url,
    #         headers=self._authenticated_headers(),
    #     )
    #     print("property notification settings by specified property id: ", response.text)
    #
    # def _property_settings(self) -> None:
    #     self._retrieve_properties()
    #     """Part of the property object is settings where a user can configure timezone, webhook etc."""
    #     property_settings_url = const.FETCH_PROPERTY_SETTINGS_RESOURCE + self._property_id + "/settings"
    #     response = requests.get(
    #         property_settings_url,
    #         headers=self._authenticated_headers()
    #     )
    #     response_data = response.json()
    #     self._property_settings_auto_shut_off = response_data["auto_shut_off"]
    #     self._property_settings_pressure_tests_enabled = response_data["pressure_tests_enabled"]
    #     self._property_settings_pressure_tests_schedule = response_data["pressure_tests_schedule"]
    #     self._property_settings_timezone = response_data["timezone"]
    #     self._property_settings_webhook_enabled = response_data["webhook_enabled"]
    #     self._property_settings_webhook_url = response_data["webhook_url"]
    #     print("property_settings: ", response.text)
    #
    # def _property_settings_by_property_id(self, property_id: str) -> None:
    #     """this sends a request to get the settings of a specified property"""
    #     self._check_token()
    #     property_settings_url = const.FETCH_PROPERTY_SETTINGS_RESOURCE + property_id + "/settings"
    #     response = requests.get(
    #         property_settings_url,
    #         headers=self._authenticated_headers(),
    #     )
    #     print("property settings by specified property id: ", response.text)

    #
    # def _update_property(self, property_id: str, **kwargs) -> None:
    #     self._check_token()
    #     """The key/values pairs that can be updated are:
    #     active	(boolean) - Whether the property is active or not
    #     address (string) - Property address
    #     city (string) - Property city
    #     country (string) - Property country
    #     lat	(number) - Property latitude
    #     lng	(number) - Property longitude
    #     name (string) - Property name
    #     postcode (string) - Property postcode
    #     uprn (string) - Property uprn"""
    #     update_property_address = const.LIST_PROPERTIES_RESOURCE + "/" + property_id
    #     response = requests.put(
    #         update_property_address,
    #         headers=self._authenticated_headers(),
    #         **kwargs
    #     )
    #     print("Property Details Updated: ", response.text)
