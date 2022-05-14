import asyncio
import logging
from aiohttp import ClientSession
import configparser
from client import Client
from errors import HeroLabsError

_LOGGER = logging.getLogger()

config = configparser.ConfigParser()
config.read('config.ini')
herolabs_email = config['DEFAULT']['EMAIL']
herolabs_password = config['DEFAULT']['PASSWORD']
demo_sonic_id = config['DEMO_DATA']['SONIC_ID_SAMPLE']


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    async with ClientSession() as session:
        try:
            client = await Client.async_login(herolabs_email, herolabs_password, session=session)
            # Discover user details
            # user_details = await client.user.async_get_user_details()
            # _LOGGER.info(user_details)

            # Get Sonic(s) Device Details
            sonic_details = await client.sonic.async_get_sonic_details()
            _LOGGER.info(sonic_details)
            #
            # Get Sonic Wi-fi Details
            # sonic_wifi_details = await client.sonic.async_get_sonic_wifi()
            # _LOGGER.info(sonic_wifi_details)
            #
            # Get Sonic Device Details by Sonic ID
            sonic_details_by_id = await client.sonic.async_get_sonic_by_sonic_id(demo_sonic_id)
            _LOGGER.info(sonic_details_by_id)
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
            # first_sonic_telemetry = await client.sonic.async_first_sonic_telemetry()
            # _LOGGER.info(first_sonic_telemetry)

            # Invalidate User Token
            # invalidate_token = await client.invalidate_token()
            # _LOGGER.info(invalidate_token)

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

            # Control Sonic Valve by ID
            # valve_control = await client.sonic.async_sonic_valve_control_by_id(demo_sonic_id, "close")
            valve_control = await client.sonic.async_sonic_valve_control_by_id(demo_sonic_id, "open")
            _LOGGER.info(valve_control)

        except HeroLabsError as err:
            _LOGGER.error("There was an error: %s", err)

# asyncio.run(main())
asyncio.get_event_loop().run_until_complete(main())
