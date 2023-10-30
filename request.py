import requests

# Set the URL of your Flask server
url = "http://127.0.0.1:5000/predict_congestion"

# Define the data to send in the request
data = {
    "route_id": 1700960,
    "direction_id": 1,
    "future_time": "2023-10-25 23:50:00"
}

# Send the POST request
response = requests.post(url, json=data)

# Extract and print the JSON response
print(response.json())