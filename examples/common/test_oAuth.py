import os
from oAuth import UtmAdapterOAuth
from product_config import UTMSPConfigParser
def main():
    with open("../../qgcs-config/product.json", "r") as file:
        json_data = file.read()
    parser = UTMSPConfigParser(json_data)
    auth_url = parser.data["utmsp_oauth2_data"]["token_url"]
    auth_url = os.getenv('AUTH_URL')

    print(auth_url)
    # Create an instance of UtmAdapterOAuth
    utm_adapter = UtmAdapterOAuth(auth_url=auth_url)

    # Call the get_auth_token method
    token = utm_adapter.get_auth_token()

    # Print the obtained token
    print("Obtained Token:", token)

if __name__ == "__main__":
    main()

