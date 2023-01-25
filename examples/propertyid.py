"""find property id reference."""

import asyncio
from aiohttp import ClientSession
from herolabsapi import Client

herolabs_email = "INSERT_EMAIL_ADDRESS_HERE"  # Keep the quotation marks
herolabs_password = "INSERT_PASSWORD_HERE"  # Keep the quotation marks


async def main() -> None:
    async with ClientSession() as session:
        client = await Client.async_login(herolabs_email, herolabs_password, session=session)

        # Get Property Information
        all_property_info = await client.property.async_get_all_property_details()
        # this is only returning 1st property
        print("Property ID:", all_property_info["data"][0]["id"])


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
