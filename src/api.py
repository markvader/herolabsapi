# Hero Labs API Python Library

from typing import Any
import asyncio
from requests.auth import HTTPBasicAuth
import requests
import json

from const import (
    # API Endpoints
    AUTH_RESOURCE,
    USER_RESOURCE,
)

from test_credentials import (
    USERNAME,
    PASSWORD,
)

AUTH_TOKEN = "testtoken"
USER_ID = "123456789"

async def sign_in():
        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            # Initially I am pulling credentials from a seperate test_credential file
            'email': USERNAME,
            'password':  PASSWORD,
        }
        url = AUTH_RESOURCE
        
        # Acquiring an access token is a one-step process.
        # You just need to send an authorizing request with your credentials.
        # All requests must be authenticated with an access token put in request 
        # headers under Authorization key using the Bearer scheme.
        # Your client may have up to 10 active tokens at a time.
        result = requests.post(url, headers=headers, json=data)

        #accessing authorisation token
        AUTH_TOKEN = '{}'.format(result.json()['token_details'])
        
        #accessing user id
        USER_ID = '{}'.format(result.json()['user_details']['id'])
        print("Token: "+AUTH_TOKEN)
        print("User ID: "+USER_ID)

   
        #This Api call returns an access token's owner details.
        user_info_api = USER_RESOURCE+USER_ID

        headers2 = {
            'Content-Type': 'application/json',
            'Authorization': "Bearer "+AUTH_TOKEN
        }
        #requsting user info from api
        user_info = requests.get(user_info_api, headers=headers2)

        EMAIL = '{}'.format(user_info.json()['email'])
        print("Email: "+EMAIL)

asyncio.run(sign_in())
