from common.product_config import UTMSPConfigParser
from common.oAuth import UtmAdapterOAuth
from datetime import datetime, timezone
import requests
import json
import os

class utm_adapter_rid:
    def __init__(self, nrid_ep_url):
        self.endpoint_secure_url = nrid_ep_url

    def encode_send_nrid(self, url):
        data = {
	    "observations": [
		{
		    "current_states": [
		        {
		            "timestamp": {
		                "value": "2024-01-10T06:54:33Z",
		                "format": "RFC3339"
		            },
		            "timestamp_accuracy": 0.0,
		            "operational_status": "Undeclared",
		            "position": {
		                "lat": 24.4364146,
		                "lng": 80.613942,
		                "alt": 0.48791500000000004,
		                "accuracy_h": "HAUnknown",
		                "accuracy_v": "VAUnknown",
		                "extrapolated": 1,
		                "pressure_altitude": 0.0
		            },
		            "track": 9085.0,
		            "speed": 0.019999999552965164,
		            "speed_accuracy": "SAUnknown",
		            "vertical_speed": 0.05999999865889549,
		            "height": {
		                "distance": -0.191,
		                "reference": "TakeoffLocation"
		            },
		            "group_radius": 0.0,
		            "group_ceiling": 0.0,
		            "group_floor": 0.0,
		            "group_count": 1,
		            "group_time_start": "2024-01-10T06:54:33Z",
		            "group_time_end": "2024-01-10T06:54:33Z"
		        }
		    ],
		    "flight_details": {
		        "rid_details": {
		            "id": "97d5b889-06f5-4ead-a883-605b294cfca2",
		            "operator_id": "test.123",
		            "operation_description": "Delivery operation, see more details at https://deliveryops.com/operation"
		        },
		        "eu_classification": {
		            "category": "EUCategoryUndefined",
		            "class": "EUClassUndefined"
		        },
		        "uas_id": {
		            "serial_number": "5283920058631409231",
		            "registration_number": "test.123",
		            "utm_id": "5283920058631409231",
		            "specific_session_id": "Unknown"
		        },
		        "operator_location": {
		            "position": {
		                "lng": 80.6139419,
		                "lat": 24.4364145,
		                "accuracy_h": "HAUnknown",
		                "accuracy_v": "VAUnknown"
		            },
		            "altitude": 0,
		            "altitude_type": "Takeoff"
		        },
		        "auth_data": {
		            "format": "string",
		            "data": 0
		        },
		        "serial_number": "5283920058631409231",
		        "registration_number": "test.123"
		    }
		}
	    ]
	}
        # Set the headers including the Authorization header with the token
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        try:
            # Send the Put request with the JSON data and headers
            response = requests.put(url + 'flight_stream/set_telemetry', json=data, headers=headers)
            json_string = json.dumps(data, indent=2)  # 'indent' parameter is optional for pretty formatting
            print(json_string)
            print(url + 'flight_stream/set_telemetry')
            print(headers)
            print(response)
            # Check the response
            if response.ok:
                print("POST request successful!")
                print("Response:", response.status_code)
                print("Response Content:", response.content.decode("utf-8"))
                return 0
            else:
                print("POST request failed!")
                print("Status Code:", response.status_code)
                return 1
        except requests.exceptions.RequestException as e:
            print("An error occurred:", e)
            return 1

if __name__ == "__main__":
    with open("../qgcs-config/product.json", "r") as file:
        json_data = json.load(file)
    parser = UTMSPConfigParser(json_data)
    parser.print_general_info()
    auth_url = parser.data["utmsp_oauth2_data"]["token_url"]

    print(auth_url)
    # Create an instance of UtmAdapterOAuth
    utm_adapter = UtmAdapterOAuth(auth_url=auth_url)

    # get oAuth token
    token = utm_adapter.get_auth_token()

    nrid_ep_url = parser.data["base_url"]

    utm_adapter_rid = utm_adapter_rid(nrid_ep_url)

    status = utm_adapter_rid.encode_send_nrid(nrid_ep_url)

