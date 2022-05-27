"""Run an example script to quickly test."""

import asyncio
import logging
import configparser
from aiohttp import ClientSession

from herolabsapi import Client, HeroLabsError

_LOGGER = logging.getLogger()

config = configparser.ConfigParser()
config.read('config.ini')
herolabs_email = config['DEFAULT']['EMAIL']
herolabs_password = config['DEFAULT']['PASSWORD']
demo_sonic_id = config['DEMO_DATA']['SONIC_ID_SAMPLE']
demo_property_id = config['DEMO_DATA']['PROPERTY_ID_SAMPLE']
demo_signal_id = config['DEMO_DATA']['SIGNAL_ID_SAMPLE']
demo_incident_id = config['DEMO_DATA']['INCIDENT_ID_SAMPLE']


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    async with ClientSession() as session:
        try:
            client = await Client.async_login(herolabs_email, herolabs_password, session=session)

            # USER API CALLS
            # Discover user details
            user_details = await client.user.async_get_user_details()
            _LOGGER.info(user_details)

            # Invalidate User Token
            # invalidate_token = await client.invalidate_token()
            # _LOGGER.info(invalidate_token)

            # # Refresh User Token
            # refresh_token = await client.refresh_token()
            # _LOGGER.info(refresh_token)

            # Update User Details
            # update_user_details = await client.user.async_update_user_details(
            # {'last_name': 'TestLastName', 'first_name': 'TestFirstName'})
            # _LOGGER.info(update_user_details)

            # Request Password Reset Email
            # request_password_reset = await client.user.async_reset_password_request("useremail@emailprovider.com")
            # _LOGGER.info(request_password_reset)

            # Request Password Reset Email
            # request_password_reset = await client.user.async_reset_password_request("useremail@emailprovider.com")
            # _LOGGER.info(request_password_reset)

            # SONIC API CALLS

            # Get Total Sonics Number
            total_sonics = await client.sonic.async_get_total_sonics()
            _LOGGER.info(total_sonics)

            # Get Sonic(s) Device Details
            first_sonic_details = await client.sonic.async_get_sonic_details()
            _LOGGER.info(first_sonic_details)
            #
            # Get Sonic Device Details by Sonic ID
            # sonic_details_by_id = await client.sonic.async_get_sonic_details(demo_sonic_id)
            # _LOGGER.info(sonic_details_by_id)
            #
            # Get Sonic Wi-fi Details
            sonic_wifi_details = await client.sonic.async_get_sonic_wifi()
            _LOGGER.info(sonic_wifi_details)
            #
            # Update Sonic Device Details by Sonic ID
            # update_sonic_details_by_id = await client.sonic.async_update_sonic_by_sonic_id(
            # demo_sonic_id, "Updated Sonic Name")
            # _LOGGER.info(update_sonic_details_by_id)

            # Update First Sonic Device Details
            # update_first_sonic = await client.sonic.async_update_first_sonic("Updated Sonic Name")
            # _LOGGER.info(update_first_sonic)
            #
            # Get Sonic Telemetry by Sonic ID
            # sonic_telemetry_by_id = await client.sonic.async_sonic_telemetry_by_id(demo_sonic_id)
            # _LOGGER.info(sonic_telemetry_by_id)
            #
            # Get First Sonic Telemetry
            first_sonic_telemetry = await client.sonic.async_first_sonic_telemetry()
            _LOGGER.info(first_sonic_telemetry)

            # Control Sonic Valve by ID
            # valve_control = await client.sonic.async_sonic_valve_control_by_id(demo_sonic_id, "close")
            # valve_control = await client.sonic.async_sonic_valve_control_by_id(demo_sonic_id, "open")
            # _LOGGER.info(valve_control)

            # Control First Sonic Valve
            # valve_control = await client.sonic.async_first_sonic_valve_control("close")
            # # valve_control = await client.sonic.async_first_sonic_valve_control("open")
            # _LOGGER.info(valve_control)

            # PROPERTY API CALLS
            # Get Total Properties Number
            total_properties = await client.property.async_get_total_properties()
            _LOGGER.info(total_properties)

            # Get Property/Properties Details
            # first_property_details = await client.property.async_get_property_details()
            # _LOGGER.info(first_property_details)
            #
            # Get Property Details by Property ID
            # property_details_by_id = await client.property.async_get_property_details_by_id(demo_property_id)
            # _LOGGER.info(property_details_by_id)

            # Get Property Notification Settings by Property ID
            # property_notification_settings_by_id = \
            #     await client.property.async_get_property_notification_settings(demo_property_id)
            # _LOGGER.info(property_notification_settings_by_id)

            # Get Property Settings by Property ID
            # property_settings_by_id = await client.property.async_get_property_settings(demo_property_id)
            # _LOGGER.info(property_settings_by_id)

            # Update Property Details by Property ID
            # update_property_settings = await client.property.async_update_property_details(
            #         demo_property_id,
            #         json={'city': "NewDemoCityNameValue",
            #               'name': "NewDemoPropertyNameValue"})
            # _LOGGER.info(update_property_settings)

            # SIGNAL API CALLS

            # Get Total Signals Number
            total_signals = await client.signal.async_get_total_signals()
            _LOGGER.info(total_signals)

            # Get Signals(s) Device Details
            first_signal_details = await client.signal.async_get_signal_details()
            _LOGGER.info(first_signal_details)
            #
            # Get Signal Device Details by Signal ID
            signal_details_by_id = await client.signal.async_get_signal_details(demo_signal_id)
            _LOGGER.info(signal_details_by_id)

            # Update Signal Device Name by Signal ID
            update_signal_name = await client.signal.async_update_signal_details(demo_signal_id, "Updated SignalName")
            _LOGGER.info(update_signal_name)

            # INCIDENTS API CALLS
            # Get Incidents
            incidents = await client.incidents.async_get_incidents()
            _LOGGER.info(incidents)

            # Get Incident by ID
            incident_details_by_id = await client.incidents.async_get_incident_details(demo_incident_id)
            _LOGGER.info(incident_details_by_id)

            # Get Incident by Property ID
            incident_details_by_property = await client.incidents.async_get_incidents_by_property(demo_property_id)
            _LOGGER.info(incident_details_by_property)

            # Action an incident
            dismiss_incident_by_id = await client.incidents.async_action_incident(demo_incident_id, "dismiss")
            _LOGGER.info(dismiss_incident_by_id)
            # reopen_incident_by_id = await client.incidents.async_action_incident(demo_incident_id, "reopen")
            # _LOGGER.info(reopen_incident_by_id)

        except HeroLabsError as err:
            _LOGGER.error("There was an error: %s", err)

# asyncio.run(main())
asyncio.get_event_loop().run_until_complete(main())
