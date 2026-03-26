import urllib.request
import json

url = "http://localhost:8000/recommend"
data = {
    "research_objective": "Determine crystal structure",
    "sample_type": "Powder",
    "domain": "Materials Science",
    "sensitivity": "High"
}

req = urllib.request.Request(url, method="POST")
req.add_header("Content-Type", "application/json")
data_bytes = json.dumps(data).encode("utf-8")

try:
    response = urllib.request.urlopen(req, data=data_bytes)
    result = json.loads(response.read().decode("utf-8"))
    print(json.dumps(result, indent=2))
except Exception as e:
    print(f"Error: {e}")
