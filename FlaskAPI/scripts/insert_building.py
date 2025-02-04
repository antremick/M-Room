import requests
import json

# Test data following the format from test_import.sh
test_data = [{
    "BldDescrShort": "Test Building",
    "shortname": "TEST",
    "BuildingID": "TEST101",
    "FacilityID": "TEST101",
    "Meetings": [
        {
            "MtgDate": "06-02-2024",
            "MtgStartTime": "10:00 AM",
            "MtgEndTime": "11:00 AM"
        }
    ]
}]

# API endpoint from test_import.sh
url = "https://mroom-api-c7aef75a74b0.herokuapp.com/import_data"

# Make the POST request
try:
    response = requests.post(
        url,
        json=test_data,
        headers={"Content-Type": "application/json"},
        timeout=10
    )
    
    print(f"Status Code: {response.status_code}")
    print("Response Text:", response.text)
    
    if response.ok:
        print("JSON Response:")
        print(json.dumps(response.json(), indent=2))
    
except requests.exceptions.RequestException as e:
    print(f"Error making request: {e}")