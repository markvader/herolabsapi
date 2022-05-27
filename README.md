# HeroLabsAPI: a Python3, asyncio-friendly library for Sonic Smart Valves
Written by [@markvader](https://www.github.com/markvader)

`herolabsapi` is a Python 3, `asyncio`-friendly library for interacting with
[Sonic by Hero Labs](https://www.hero-labs.com/).

##Manufacturer Documentation
[Hero Labs API Documentation](https://docs.hero-labs.com/)

[Hero Labs API Swagger UI](https://iot-core.hero-labs.com/ape/v1/swaggerui/)

# Installation

```
pip install herolabsapi
```


# Usage & Examples

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
    await client.sonic.async_update_sonic_name(first_device_id, "New Sonic Name")

    # Change Valve State
    # Open the shutoff valve
    await client.sonic.async_open_sonic_valve(first_device_id)
    # Close the shutoff valve
    await client.sonic.async_close_sonic_valve(first_device_id)

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
    close_incident = await client.incidents.async_close_incident(demo_incident_id)
    # print(close_incident)
    reopen_incident = await client.incidents.async_close_incident(demo_incident_id)

# There are additional api endpoints that can be explored and called, I will put example code in the examples folder


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

        #additional example code same as above

```


## API Endpoints

| Method                | Endpoint                                            | Description                                    |
|:----------------------|:----------------------------------------------------|:-----------------------------------------------|
| **Incidents**         ||
| GET                   | /ape​/v1​/incidents                                 | Get all accessible incidents                   |
| GET                   | /ape​/v1​/incidents​/{id}                           | Get an incident                                |
| PUT                   | ​/ape​/v1​/incidents​/{incident_id}​/action         | Transitioning an incident to a different state |
| GET                   | /ape​/v1​/properties​/{property_id}​/incidents      | Get all incidents for a property               |
| **Properties**        ||
| GET                   | /ape​/v1​/properties                                | Get all accessible property                    |
| GET                   | /ape​/v1​/properties​/{id}                          | Get a property                                 |
| PATCH                 | /ape​/v1​/properties​/{id}                          | Update a property                              |
| PUT                   | ​/ape​/v1​/properties​/{id}                         | Update a property                              |
| GET                   | /ape​/v1​/properties​/{property_id}​/incidents      | Get all incidents for a property               |
| GET                   | /ape​/v1​/properties​/{property_id}​/notifications  | Get a property notification settings           |
| PUT                   | ​/ape​/v1​/properties​/{property_id}​/notifications | Update a property notification settings        |
| GET                   | /ape​/v1​/properties​/{property_id}​/settings       | Get a property settings                        |
| PUT                   | ​/ape​/v1​/properties​/{property_id}​/settings      | Update a property settings                     |
| GET                   | /ape​/v1​/properties​/{property_id}​/signals        | Get all signals for a property                 |
| **Property settings** ||
| GET                   | /ape​/v1​/properties​/{property_id}​/notifications  | Get a property notification settings           |
| PUT                   | ​/ape​/v1​/properties​/{property_id}​/notifications | Update a property notification settings        |
| GET                   | /ape​/v1​/properties​/{property_id}​/settings       | Get a property settings                        |
| PUT                   | ​/ape​/v1​/properties​/{property_id}​/settings      | Update a property settings                     |
| **Signals**           ||
| GET                   | /ape​/v1​/properties​/{property_id}​/signals        | Get all signals for a property                 |
| GET                   | /ape​/v1​/signals                                   | Get all accessible signals                     |
| GET                   | /ape​/v1​/signals​/{id}                             | Get a signal                                   |
| PATCH                 | /ape​/v1​/signals​/{id}                             | Update a signal                                |
| PUT                   | ​/ape​/v1​/signals​/{id}                            | Update a signal                                |
| GET                   | /ape​/v1​/signals​/{signal_id}​/sonics              | Get all sonics for a signal                    |
| **Sonics**            ||
| GET                   | /ape​/v1​/signals​/{signal_id}​/sonics              | Get all sonics for a signal                    |
| GET                   | /ape​/v1​/sonics                                    | Get all accessible sonics                      |
| GET                   | /ape​/v1​/sonics​/{id}                              | Get a sonic                                    |
| PATCH                 | /ape​/v1​/sonics​/{id}                              | Update a sonic                                 |
| PUT                   | ​/ape​/v1​/sonics​/{id}                             | Update a sonic                                 |
| PUT                   | ​/ape​/v1​/sonics​/{sonic_id}​/valve                | Open or close a sonic valve                    |
| PUT                   | ​/ape​/v1​/sonics_wifi​/{sonic_id}​/valve           | Open or close a sonic valve                    |
| **Telemetry details** ||
| GET                   | /ape​/v1​/sonics​/{sonic_id}​/telemetry             | Getting the latest telemetry details           |
| GET                   | /ape​/v1​/sonics_wifi​/{sonic_id}​/telemetry        | Getting the latest telemetry details           |
| **SonicsWifi**        ||
| PUT                   | ​/ape​/v1​/sonics​/{sonic_id}​/valve                | Open or close a sonic valve                    |
| GET                   | /ape​/v1​/sonics_wifi                               | Get all accessible sonic wifis                 |
| GET                   | /ape​/v1​/sonics_wifi​/{id}                         | Get a sonic wifi                               |
| PATCH                 | /ape​/v1​/sonics_wifi​/{id}                         | Update a sonic wifi                            |
| PUT                   | /ape​/v1​/sonics_wifi​/{id}                         | Update a sonic wifi                            |
| PUT                   | /ape​/v1​/sonics_wifi​/{sonic_id}​/valve            | Open or close a sonic valve                    |
