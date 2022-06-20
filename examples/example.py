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


async def main() -> None:
    """Create the aiohttp session and run the example."""
    async with ClientSession() as session:
        client = await Client.async_login(herolabs_email, herolabs_password, session=session)

        # USER API CALLS
        # Get User Account Information:
        user_info = await client.user.async_get_user_details()
        print(user_info)

        # SONIC DEVICE API CALLS
        # Get Sonic Devices Information
        sonic_data = await client.sonic.async_get_all_sonic_details()
        first_device_id = sonic_data["data"][0]["id"]

        # Get Sonic Device Information
        device_info = await client.sonic.async_get_sonic_details(first_device_id)
        print(device_info)
        print("Valve State:", device_info["valve_state"])

        # Get Device Telemetry Data
        device_telemetry = await client.sonic.async_sonic_telemetry_by_id(first_device_id)
        print(device_telemetry)
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
        # await client.sonic.async_update_sonic_name(first_device_id, "New Sonic Name")

        # Change Valve State
        # Open the shutoff valve
        # await client.sonic.async_open_sonic_valve(first_device_id)
        # Close the shutoff valve
        # await client.sonic.async_close_sonic_valve(first_device_id)

        # INCIDENTS API CALLS
        # Get Incidents
        incidents = await client.incidents.async_get_incidents()
        print("all incidents:", incidents)

        # Get Open Incidents
        open_incidents = await client.incidents.async_get_open_incidents()
        print("open incidents:", open_incidents)

        # Get Incident Details
        incident_details = await client.incidents.async_get_incident_details(demo_incident_id)
        print("details of specific incident:", incident_details)

        # Get Incidents by Property ID
        property_incidents = await client.incidents.async_get_incidents_by_property(demo_property_id)
        print("all incidents for a property:", property_incidents)

        # Get Open Incidents by Property ID
        property_open_incidents = await client.incidents.async_get_open_incidents_by_property(demo_property_id)
        print("open incidents for a property:", property_open_incidents)

        # Get Property Information
        all_property_info = await client.property.async_get_all_property_details()
        print(all_property_info)

        # Get Property Information
        property_info = await client.property.async_get_property_details(demo_property_id)
        print(property_info)

        # Get Property Setting
        property_settings = await client.property.async_get_property_settings(demo_property_id)
        print(property_settings)

        # Get Property notification settings
        property_notification_settings = await client.property.async_get_property_notification_settings(demo_property_id)
        print(property_notification_settings)

        # Update Property notification settings
        # await client.property.async_update_property_notifications(demo_property_id,
        #                                                           json={'high_volume_threshold_litres': 75,
        #                                                                 'long_flow_notification_delay_mins': 120,
        #                                                                 'health_check_failed': True}
        #                                                           )

        # Update Property settings
        await client.property.async_update_property_settings(demo_property_id,
                                                             json={'auto_shut_off': True,
                                                                   'pressure_tests_enabled': True}
                                                             )

        # Action an Incident
        # close_incident = await client.incidents.async_close_incident(demo_incident_id)
        # print(close_incident)
        # reopen_incident = await client.incidents.async_close_incident(demo_incident_id)

        # There are additional api endpoints that can be explored and called (properties, signals, user),
        # I will put example code in the examples folder


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    