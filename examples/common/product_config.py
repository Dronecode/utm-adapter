import json

class UTMSPConfigParser:
    parsed_data = None

    def __init__(self, json_data):
        self.data = json_data
        UTMSPConfigParser.parsed_data = self.data

    def print_general_info(self):
        print("UTMSP Name:", self.data["utmsp_name"])
        print("Base URL:", self.data["base_url"])
        print("OAuth Token URL:", self.data["utmsp_oauth2_data"]["token_url"])

    def print_available_services(self):
        for service in self.data["available_services"]:
            service_name = list(service.keys())[0]
            capabilities = service[service_name]["capabilities"]
            print(f"\nService: {service_name}")
            print("Capabilities:", capabilities)

    def main(self):
        self.print_general_info()
        self.print_available_services()

if __name__ == "__main__":
    with open("../../qgcs-config/product.json", "r") as file:
        json_data = json.load(file)
    parser = UTMSPConfigParser(json_data)
    parser.main()

