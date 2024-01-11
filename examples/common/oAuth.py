import os
import requests

class UtmAdapterOAuth:
    def __init__(self, auth_url):
        self.headers = {'Content-Type': 'application/json'}
        # utm adapter env parameter
        self.client_id = os.getenv('CLIENT_ID')
        self.client_secret = os.getenv('CLIENT_SECRET')
        self.token_url = auth_url
        self.jwt = 'INVALID'

    # Get OAuth token from UTMSP
    def get_auth_token(self):
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials",
            "scope": "blender.write blender.read",
            "audience": 'blender.utm.dev.airoplatform.com'
        }
        response = requests.post(self.token_url, data=data)
        if response.ok:
            token_data = response.json()
            print(token_data)
            token = token_data.get("access_token")
            if token:
                print("Token:", token)
            else:
                print("Token not found in response.")
        else:
            print("Error:", response.status_code)
            print("Response:", response.text)

        return token

