# HeroLabsAPI: a Python3, asyncio-friendly library for Sonic Smart Valves
Written by [@markvader](https://www.github.com/markvader)

`herolabsapi` is a Python 3, `asyncio`-friendly library for interacting with
[Sonic by Hero Labs](https://www.watergate.ai/).

## Manufacturer Documentation
[Hero Labs API Documentation](https://docs.watergate.ai/)

[Hero Labs API Swagger UI](https://iot-core.watergate.ai/ape/v1/swaggerui/)

A list of gathered API endpoints and their functions can be found [here](https://github.com/markvader/herolabsapi/blob/master/api_endpoints.md)
# Installation

```
pip install herolabsapi
```


# Usage & Examples

See examples/example.py for full example code

```python
import asyncio
from datetime import datetime

from herolabsapi import Client

async def main() -> None:

    client = await Client.async_login("<EMAIL>", "<PASSWORD>")
    
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

    # Action an Incident
    # close_incident = await client.incidents.async_close_incident(demo_incident_id)
    # print(close_incident)
    # reopen_incident = await client.incidents.async_close_incident(demo_incident_id)

    # There are additional api endpoints that can be explored and called (properties, signals, user),
    # example code is in the examples folder.
    

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
```

By default, the library creates a new connection to Sonic Device with each coroutine. If you are
calling a large number of coroutines (or merely want to squeeze out every second of
runtime savings possible), an
[`aiohttp`](https://github.com/aio-libs/aiohttp) `ClientSession` can be used for connection
pooling:

```python
import asyncio

from aiohttp import ClientSession
from datetime import datetime

from herolabsapi import Client

async def main() -> None:
    """Create the aiohttp session and run the example."""
    async with ClientSession() as session:
        client = await Client.async_login("<EMAIL>", "<PASSWORD>", session=session)
    
        # USER API CALLS
        # Get User Account Information:
        user_info = await client.user.async_get_user_details()

        #additional example code same as above and example folder

```


