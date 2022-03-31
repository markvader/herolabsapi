# herolabsapi
Python Library for the Hero Labs API

Work In Progress -  Started 31st March 2022

[Hero Labs API Documentation](https://docs.hero-labs.com/)

[Hero Labs API Swagger UI](https://iot-core.hero-labs.com/ape/v1/swaggerui/)


## Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| Incidents||
| --- | --- | --- |
|GET|/ape​/v1​/incidents|Get all accessible incidents|
|GET|/ape​/v1​/incidents​/{id}|Get an incident|
|PUT|​/ape​/v1​/incidents​/{incident_id}​/action|Transitioning an incident to a different state|
|GET|/ape​/v1​/properties​/{property_id}​/incidents|Get all incidents for a property|
|||			
|Properties||
| --- | --- | --- |
|GET|/ape​/v1​/properties|Get all accessible property|
|GET|/ape​/v1​/properties​/{id}|Get a property|
|PATCH|/ape​/v1​/properties​/{id}|Update a property|
|PUT|​/ape​/v1​/properties​/{id}|Update a property|
|GET|/ape​/v1​/properties​/{property_id}​/incidents|Get all incidents for a property|
|GET|/ape​/v1​/properties​/{property_id}​/notifications|Get a property notification settings|
|PUT|​/ape​/v1​/properties​/{property_id}​/notifications|Update a property notification settings|
|GET|/ape​/v1​/properties​/{property_id}​/settings|Get a property settings|
|PUT|​/ape​/v1​/properties​/{property_id}​/settings|Update a property settings|
|GET|/ape​/v1​/properties​/{property_id}​/signals|Get all signals for a property|
|||
|Property settings||
| --- | --- | --- |
|GET|/ape​/v1​/properties​/{property_id}​/notifications|Get a property notification settings|
|PUT|​/ape​/v1​/properties​/{property_id}​/notifications|Update a property notification settings|
|GET|/ape​/v1​/properties​/{property_id}​/settings|Get a property settings|
|PUT|​/ape​/v1​/properties​/{property_id}​/settings|Update a property settings|
|||
|Signals||
| --- | --- | --- |
|GET|/ape​/v1​/properties​/{property_id}​/signals|Get all signals for a property|
|GET|/ape​/v1​/signals|Get all accessible signals|
|GET|/ape​/v1​/signals​/{id}|Get a signal|
|PATCH|/ape​/v1​/signals​/{id}|Update a signal|
|PUT|​/ape​/v1​/signals​/{id}|Update a signal|
|GET|/ape​/v1​/signals​/{signal_id}​/sonics|Get all sonics for a signal|
|||
|Sonics||
| --- | --- | --- |
|GET|/ape​/v1​/signals​/{signal_id}​/sonics|Get all sonics for a signal|
|GET|/ape​/v1​/sonics|Get all accessible sonics|
|GET|/ape​/v1​/sonics​/{id}|Get a sonic|
|PATCH|/ape​/v1​/sonics​/{id}|Update a sonic|
|PUT|​/ape​/v1​/sonics​/{id}|Update a sonic|
|PUT|​/ape​/v1​/sonics​/{sonic_id}​/valve|Open or close a sonic valve|
|PUT|​/ape​/v1​/sonics_wifi​/{sonic_id}​/valve|Open or close a sonic valve|
|||			
|Telemetry details||
| --- | --- | --- |
|GET|/ape​/v1​/sonics​/{sonic_id}​/telemetry|Getting the latest telemetry details|
|GET|/ape​/v1​/sonics_wifi​/{sonic_id}​/telemetry|Getting the latest telemetry details|
|||
|SonicsWifi||
| --- | --- | --- |
|PUT|​/ape​/v1​/sonics​/{sonic_id}​/valve|Open or close a sonic valve|
|GET|/ape​/v1​/sonics_wifi|Get all accessible sonic wifis|
|GET|/ape​/v1​/sonics_wifi​/{id}|Get a sonic wifi|
|PATCH|/ape​/v1​/sonics_wifi​/{id}|Update a sonic|
|PUT|/ape​/v1​/sonics_wifi​/{id}|Update a sonic|
|PUT|/ape​/v1​/sonics_wifi​/{sonic_id}​/valve|Open or close a sonic valve|
