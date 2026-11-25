from http.server import SimpleHTTPRequestHandler, HTTPServer
from pathlib import Path
import json
import requests
from requester import Requester

query_node = Requester("https://mini.chammas.tech:8006/api2/json")
HTML_FILE = Path() / "index.html"

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/resources":
            # Automatically serve HTML, JS, CSS with super method
            return super().do_GET()

        try:
            # Get resources
            response = query_node.get_resources()
            response.raise_for_status() # Will raise exception
            result = response.json()

            # Only retrieve allowed data types
            result["data"] = filter_resources(result["data"]) 

        except requests.RequestException as error:
            self.send_error(502, f"Request error: {error}")
            return

        # Convert request to json string
        body = json.dumps(result).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

def filter_key(resource):
    vmid = resource.get("vmid") or 0
    node = resource.get("node") or ""
    return vmid, node

def filter_resources(resources):
    allowed_types = ["node", "qemu", "lxc"]
    filtered = []

    for resource in resources:
        if resource.get("type") in allowed_types:
            filtered.append(resource)

    filtered.sort(key=filter_key)
    return filtered

if __name__ == "__main__":
    print("Server running at http://127.0.0.1:8000")
    HTTPServer(("127.0.0.1", 8000), Handler).serve_forever()