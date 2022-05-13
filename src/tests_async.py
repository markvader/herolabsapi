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


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    async with ClientSession() as session:
        try:
            client = await Client.async_login(herolabs_email, herolabs_password, session=session)
            # Discover user details
            user_details = await client.user.async_get_user_details()
            _LOGGER.info(user_details)

            sonic_details = await client.sonic.async_get_sonic_details()
            _LOGGER.info(sonic_details)

            # Invalidate user token
            # invalidate_token = await client.invalidate_token()
            # _LOGGER.info(invalidate_token)

            # Update user details
            # update_user_details = await client.user.async_update_user_details(
            # {'last_name': 'TestLastName', 'first_name': 'TestFirstName'})
            # _LOGGER.info(update_user_details)

            # Update user details

            # request_password_reset = await client.user.async_reset_password_request("useremail@emailprovider.com")
            # _LOGGER.info(request_password_reset)

        except HeroLabsError as err:
            _LOGGER.error("There was an error: %s", err)

# asyncio.run(main())
asyncio.get_event_loop().run_until_complete(main())
