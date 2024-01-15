from common.product_config import UTMSPConfigParser
from common.oAuth import UtmAdapterOAuth
from datetime import datetime, timezone
import requests
import json
import os

class utm_adapter_flight_auth:
    def __init__(self, nrid_ep_url):
        self.endpoint_secure_url = nrid_ep_url

    def encode_send_fp(self, url):
        data = {
	    "submitted_by": "user@example.com",
	    "type_of_operation": 1,
	    "originating_party": "Flight 1023",
	    "start_datetime": "2024-1-15T13:44:11.000000Z",
	    "end_datetime": "2024-1-15T14:43:11.000000Z",
	    "flight_declaration_geo_json": {
		"type": "FeatureCollection",
		"features": [
		    {
		        "type": "Feature",
		        "properties": {
		            "min_altitude": {
		                "meters": 66,
		                "datum": "agl"
		            },
		            "max_altitude": {
		                "meters": 0,
		                "datum": "agl"
		            }
		        },
		        "geometry": {
		            "type": "Polygon",
		            "coordinates": [
		                [
		                    [
		                        24.435641654195084,
		                        80.6140664952805
		                    ],
		                    [
		                        24.436081507305897,
		                        80.61735940416605
		                    ],
		                    [
		                        24.437729526553444,
		                        80.61799223127974
		                    ],
		                    [
		                        24.437729784425326,
		                        80.61799142104064
		                    ],
		                    [
		                        24.43784823234804,
		                        80.61802572135264
		                    ],
		                    [
		                        24.43797010689046,
		                        80.61803924666822
		                    ],
		                    [
		                        24.438092407129542,
		                        80.61803166394009
		                    ],
		                    [
		                        24.43821212157601,
		                        80.61800315985488
		                    ],
		                    [
		                        24.438326302544223,
		                        80.61795443632911
		                    ],
		                    [
		                        24.43843213847049,
		                        80.61788669306276
		                    ],
		                    [
		                        24.438527023398954,
		                        80.61780159808171
		                    ],
		                    [
		                        24.438608620933607,
		                        80.61770124676775
		                    ],
		                    [
		                        24.43867492190831,
		                        80.61758811009258
		                    ],
		                    [
		                        24.438724293822478,
		                        80.61746497384303
		                    ],
		                    [
		                        24.438755520968375,
		                        80.61733487005216
		                    ],
		                    [
		                        24.438767834469566,
		                        80.61720100228172
		                    ],
		                    [
		                        24.43876093112382,
		                        80.61706666690066
		                    ],
		                    [
		                        24.438734980888395,
		                        80.61693517150343
		                    ],
		                    [
		                        24.43869062277939,
		                        80.61680975411485
		                    ],
		                    [
		                        24.43862894895779,
		                        80.61669350282403
		                    ],
		                    [
		                        24.438551478075603,
		                        80.61658928020881
		                    ],
		                    [
		                        24.438460117654582,
		                        80.61649965255071
		                    ],
		                    [
		                        24.438357117286884,
		                        80.61642682670009
		                    ],
		                    [
		                        24.438245013145742,
		                        80.6163725959509
		                    ],
		                    [
		                        24.438245271016566,
		                        80.6163717857118
		                    ],
		                    [
		                        24.437490437172958,
		                        80.61608193290334
		                    ],
		                    [
		                        24.43718794106442,
		                        80.61381730471953
		                    ],
		                    [
		                        24.437187167933672,
		                        80.61381742927267
		                    ],
		                    [
		                        24.43715993165442,
		                        80.61368624804686
		                    ],
		                    [
		                        24.437114347809132,
		                        80.61356136176096
		                    ],
		                    [
		                        24.437051538808483,
		                        80.61344584563415
		                    ],
		                    [
		                        24.436973051183774,
		                        80.61334254401169
		                    ],
		                    [
		                        24.4368808175421,
		                        80.61325400043802
		                    ],
		                    [
		                        24.436777108952608,
		                        80.61318239530857
		                    ],
		                    [
		                        24.436664479000946,
		                        80.61312949174413
		                    ],
		                    [
		                        24.43654570104057,
		                        80.61309659226202
		                    ],
		                    [
		                        24.436423699748044,
		                        80.61308450717286
		                    ],
		                    [
		                        24.43630147922692,
		                        80.61309353384547
		                    ],
		                    [
		                        24.436182048897514,
		                        80.61312345012902
		                    ],
		                    [
		                        24.43606834954846,
		                        80.61317351942967
		                    ],
		                    [
		                        24.435963180916627,
		                        80.61324250872809
		                    ],
		                    [
		                        24.435869132553492,
		                        80.61332871939663
		                    ],
		                    [
		                        24.435788520321715,
		                        80.6134300285974
		                    ],
		                    [
		                        24.435723329172884,
		                        80.61354394183513
		                    ],
		                    [
		                        24.43567516432242,
		                        80.61366765401795
		                    ],
		                    [
		                        24.435645211831343,
		                        80.61379811909876
		                    ],
		                    [
		                        24.435634209180545,
		                        80.61393212457841
		                    ],
		                    [
		                        24.435642427335306,
		                        80.61406637072736
		                    ],
		                    [
		                        24.435641654195084,
		                        80.6140664952805
		                    ]
		                ]
		            ]
		        }
		    }
		]
	    }
	}
        # Set the headers including the Authorization header with the token
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        try:
            # Send the Put request with the JSON data and headers
            response = requests.put(url + 'flight_declaration_ops/set_flight_declaration', json=data, headers=headers)
            json_string = json.dumps(data, indent=2)  # 'indent' parameter is optional for pretty formatting
            print(json_string)
            print(url + 'flight_declaration_ops/set_flight_declaration')
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
    auth_url = parser.data["utmsp_oauth2_data"]["token_url"]

    # Create an instance of UtmAdapterOAuth
    utm_adapter = UtmAdapterOAuth(auth_url=auth_url)

    # get oAuth token
    token = utm_adapter.get_auth_token()

    fp_ep_url = parser.data["base_url"]

    utm_adapter_flight_auth = utm_adapter_flight_auth(fp_ep_url)

    status = utm_adapter_flight_auth.encode_send_fp(fp_ep_url)

