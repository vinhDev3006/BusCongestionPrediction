import requests
import json
import pprint

# Define the URL of your Flask server
server_url = "http://127.0.0.1:5000"  # Change this to your server's URL

# Define the input parameters
data = {
    "route_id": 300025,
    "direction_id": 0,
    "future_time": "2023-10-25 23:50:00"
}

# Make a POST request to the /predict route
response = requests.post(f"{server_url}/predict", json=data)

if response.status_code == 200:
    result = response.json()
    # Format the JSON response with an indentation of 4 spaces
    pprint.pprint(result, compact=True)
else:
    print(f"Error: {response.status_code} - {response.text}")