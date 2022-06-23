"""Script to quickly test."""

import asyncio
import configparser
from aiohttp import ClientSession
from datetime import datetime

from herolabsapi import Client

config = configparser.ConfigParser()
config.read('config.ini')
herolabs_email = config['DEFAULT']['EMAIL']
herolabs_password = config['DEFAULT']['PASSWORD']
demo_property_id = config['DEMO_DATA']['PROPERTY_ID_SAMPLE']
demo_incident_id = config['DEMO_DATA']['INCIDENT_ID_SAMPLE']
demo_signal_id = config['DEMO_DATA']['SIGNAL_ID_SAMPLE']


async def main() -> None:
    """Create the aiohttp session and run the example."""
    async with ClientSession() as session:
        client = await Client.async_login(herolabs_email, herolabs_password, session=session)

        # USER API CALLS
        # Get User Account Information:
        user_info = await client.user.async_get_user_details()
        user_id = user_info["id"]
        print("user_info", user_info)

        # Update User Details
        # The key/values pairs that can be updated are:
        # email (string) - User email
        # first_name (string) - User first name
        # last_name (string) - User last name
        # phone (string) - (e.g "+447712345678")
        # language (string) - (passed as a language code (ISO 639-1 standard) i.e "en", "pl")
        updated_user_info = await client.user.async_update_user_details({'first_name': "new first name",
                                                                         'last_name': "new last name"})
        print("updated_user_info:", updated_user_info)

        # Request Password Reset
        await client.user.async_reset_password_request("emailaddress@test.com")

        ######################################################################

        # SONIC DEVICE API CALLS
        # Get Sonic Devices Information
        sonic_data = await client.sonic.async_get_all_sonic_details()
        print("all sonic data:", sonic_data)
        first_device_id = sonic_data["data"][0]["id"]
        # second_device_id = sonic_data["data"][1]["id"]

        # Get Sonic Device Information
        device_info = await client.sonic.async_get_sonic_details(first_device_id)
        print("device_info: ", device_info)
        print("Valve State of ", device_info["name"], ":", device_info["valve_state"])

        # Get 2nd Sonic Device Information
        # second_device_info = await client.sonic.async_get_sonic_details(second_device_id)
        # print("second_device_info: ", second_device_info)
        # print(second_device_info["name"], "Valve State:", device_info["valve_state"])

        # Get Device Telemetry Data
        device_telemetry = await client.sonic.async_sonic_telemetry_by_id(first_device_id)
        print("device_telemetry:", device_telemetry)
        print("Water Pressure:", device_telemetry["pressure"])
        print("Water Flow:", device_telemetry["water_flow"])
        print("Water Temperature:", device_telemetry["water_temp"])
        # Convert timestamp to readable datetime format
        timestamp = device_telemetry["probed_at"]
        datetime_telemetry = datetime.fromtimestamp(timestamp).strftime('%H:%M:%S %d-%m-%y')
        print("Telemetry timestamp:", datetime_telemetry)

        # Get Total Sonic Devices number
        total_sonics = await client.sonic.async_get_total_sonics()
        print("Total Sonic Devices:", total_sonics)

        # Rename Sonic Device
        await client.sonic.async_update_sonic_name(first_device_id, "New Sonic Name")

        # Change Valve State
        # Open the shutoff valve
        await client.sonic.async_open_sonic_valve(first_device_id)

        # Close the shutoff valve
        await client.sonic.async_close_sonic_valve(first_device_id)

        ######################################################################

        # INCIDENTS API CALLS
        # Get Incidents
        incidents = await client.incidents.async_get_incidents()
        print("all incidents:", incidents)

        # Get Open Incidents
        open_incidents = await client.incidents.async_get_open_incidents()
        print("open incidents:", open_incidents)
        # Count open incidents
        open_incident_count = len([ele for ele in open_incidents if isinstance(ele, dict)])
        print("open_incident_count:", open_incident_count)
        # print latest incident if one exists
        if open_incident_count > 0:
            latest_incident = open_incidents[0]["id"]
        else:
            latest_incident = None
        print("latest_incident:", latest_incident)

        # Get Incident Details
        incident_details = await client.incidents.async_get_incident_details(demo_incident_id)
        print("details of specific incident:", incident_details)

        # Get Incidents by Property ID
        property_incidents = await client.incidents.async_get_incidents_by_property(demo_property_id)
        print("all incidents for a property:", property_incidents)

        # Get Open Incidents by Property ID
        property_open_incidents = await client.incidents.async_get_open_incidents_by_property(demo_property_id)
        print("open incidents for a property:", property_open_incidents)
        # Count open incidents
        open_incident_count = len([ele for ele in property_open_incidents if isinstance(ele, dict)])
        print("open_incident_count:", open_incident_count)
        # print latest incident if one exists
        if open_incident_count > 0:
            latest_incident = property_open_incidents[0]["id"]
        else:
            latest_incident = None
        print("latest incident at property:", latest_incident)

        # Action an Incident
        close_incident = await client.incidents.async_close_incident(demo_incident_id)
        print(close_incident)

        reopen_incident = await client.incidents.async_close_incident(demo_incident_id)
        print(reopen_incident)
        ######################################################################
        # PROPERTY API CALLS
        # Get Property Information
        all_property_info = await client.property.async_get_all_property_details()
        print("all_property_info:", all_property_info)

        # Get Property Information
        first_property_id = all_property_info["data"][0]["id"]
        property_info = await client.property.async_get_property_details(first_property_id)
        print("first_property_info:", property_info)

        # Get Property Setting
        property_settings = await client.property.async_get_property_settings(first_property_id)
        print("first_property_settings:", property_settings)

        # Get Property notification settings
        property_notification_settings = await client.property.async_get_property_notification_settings(first_property_id)
        print("first_property_notification_settings:", property_notification_settings)

        # Update Property
        # The key/values pairs that can be updated are:
        # active	(boolean) - Whether the property is active or not
        # address (string) - Property address
        # city (string) - Property city
        # country (string) - Property country
        # lat	(number) - Property latitude
        # lng	(number) - Property longitude
        # name (string) - Property name
        # postcode (string) - Property postcode
        # uprn (string) - Property uprn
        await client.property.async_update_property_details(first_property_id, {'name': "Kornelia", 'city': "Słupsk"})

        # Update Property notification settings
        # The key/values pairs that can be updated are:
        # high_volume_threshold_litres (int) - valve of int must be one of:
        # [25, 50, 75, 100, 150, 200, 250, 300, 400, 500, 600, 800, 1000]
        # long_flow_notification_delay_mins (int) - valve of int must be one of:
        # [15, 30, 60, 120, 180, 240, 300, 360]
        # cloud_disconnection (bool)
        # device_handle_moved (bool),
        # health_check_failed (bool)
        # low_battery_level (bool)
        # pressure_test_failed (bool)
        # pressure_test_skipped (bool)
        # radio_disconnection (bool)
        await client.property.async_update_property_notifications(first_property_id,
                                                                  {'high_volume_threshold_litres': 300,
                                                                   'long_flow_notification_delay_mins': 60,
                                                                   'health_check_failed': True})

        # Update Property settings
        # The key/values pairs that can be updated are:
        # auto_shut_off (bool) - Automatic shut off
        # pressure_tests_enabled (bool) - Enable or disable the pressure test
        # pressure_tests_schedule (string) - Time in a day when the pressure test runs.
        # The format is HH:MM:SS in 24h clock.
        # timezone (string) - Property timezone e.g."Europe/London"
        # webhook_enabled (bool)
        # webhook_url (string)
        await client.property.async_update_property_settings(first_property_id, {'auto_shut_off': True,
                                                                                 'pressure_tests_enabled': True})

        ######################################################################

        # SIGNAL DEVICE API CALLS
        # Get Signal Devices Information
        signal_data = await client.signal.async_get_all_signal_details()
        print("all signal data:", signal_data)
        first_signal_device_id = signal_data["data"][0]["id"]
        # second_signal_device_id = signal_data["data"][1]["id"]

        # Get Signal Device Information
        signal_device_info = await client.signal.async_get_signal_details(first_signal_device_id)
        print("signal device info:", signal_device_info)
        print("Signal Device Name:", signal_device_info["name"])

        # Rename Signal Device
        # name is the only value that can be updated at this endpoint
        await client.signal.async_update_signal_details(first_signal_device_id, "New Signal Name")

        # Get 2nd Signal Device Information
        # second_signal_device_info = await client.sonic.async_get_sonic_details(second_signal_device_id)
        # print("signal device info:", second_signal_device_info)
        # print("Second Signal Device Name:", second_signal_device_info["name"])

        # Get Total Signal Devices number
        total_signals = await client.signal.async_get_total_signals()
        print("Total Signal Devices:", total_signals)

        # get the details of signal devices registered to a specified property
        signal_devices_at_demo_property = await client.signal.async_get_signal_details_by_property_id(demo_property_id)
        print("signal devices at demo property:", signal_devices_at_demo_property)
        print("There are", signal_devices_at_demo_property["total_entries"], "signal devices at demo property")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    