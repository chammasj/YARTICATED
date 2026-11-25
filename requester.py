import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
USERNAME = os.getenv("USERNAME")
API_TOKEN = os.getenv("API_TOKEN")

if not USERNAME or USERNAME.count("@") != 1 or USERNAME.count("!") != 1:
    raise Exception("No valid USERNAME found. Format: USERNAME={USERNAME}@{REALM}!{TOKEN_ID}")

if not API_TOKEN:
    raise Exception("No API_TOKEN found. Is your .env file missing?")

class Requester:
    # Endpoint may be any cluster node
    def __init__(self, address):
        if address.startswith("http:"):
            raise Exception("Endpoint base URL may not use HTTP.")

        self.address = address
        self.headers={"Authorization": f"PVEAPIToken={USERNAME}={API_TOKEN}"}
    
    def set_endpoint(self, address):
        self.endpoint = address.strip()
    
    def get_resources(self):
        return self.__request("/cluster/resources")

    def __request(self, path):
        return requests.get(
            self.address+path,
            headers=self.headers,
            timeout=15,
        )


### TODO: REMOVE
def main():
    node_mini = Requester("https://mini.chammas.tech:8006/api2/json")

    resources = node_mini.get_resources()   
    print(json.dumps(resources.json(), indent=2))

if __name__ == "__main__":
    main()
### /REMOVE