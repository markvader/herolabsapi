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
    client = await Client.async_login(herolabs_email, herolabs_password, session=session)

    # USER API CALLS
    # Get User Account Information:
    user_info = await client.user.async_get_user_details()
    print(user_info)

    # SONIC DEVICE API CALLS
    # Get Sonic Devices Information
    sonic_data = await client.sonic.async_get_sonic_details()
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
    print(incidents)

    # Get Open Incidents
    open_incidents = await client.incidents.async_get_open_incidents()
    print(open_incidents)

    # Get Incident Details
    incident_details = await client.incidents.async_get_incident_details(demo_incident_id)
    print(incident_details)

    # Get Incidents by Property ID
    property_incidents = await client.incidents.async_get_incidents_by_property(demo_property_id)
    print(property_incidents)

    # Get Open Incidents by Property ID
    property_open_incidents = await client.incidents.async_get_open_incidents_by_property(demo_property_id)
    print("open incidents for a property", property_open_incidents)

    # Action an Incident
    # close_incident = await client.incidents.async_close_incident(demo_incident_id)
    # print(close_incident)
    # reopen_incident = await client.incidents.async_close_incident(demo_incident_id)


# There are additional api endpoints that can be explored and called, I will put example code in the examples folder


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    