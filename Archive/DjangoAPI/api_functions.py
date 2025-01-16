"""Make calls to classroom apis"""
from pprint import pprint
import requests
import json


# Your public and private API keys
def generate_token(public_key, private_key, scope):
    """Generate a Auth Token."""
    # API endpoint and headers
    token_url = 'https://gw.api.it.umich.edu/um/oauth2/token'
    token_headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    # API payload with your credentials and scope
    token_data = {
        'grant_type': 'client_credentials',
        'client_id': public_key,  
        'client_secret': private_key,  
        'scope': scope 
    }
    # Perform the POST request
    response = requests.post(token_url, headers=token_headers, data=token_data)

    # Check if the request was successful
    if response.ok:
        # If response is OK, print the content
        print("Access token Acquired")
        response_dict = response.json()
        access_token = response_dict["access_token"]
        return {"Authorization": f"Bearer {access_token}"}
    else:
        # If the request failed, print the status code and error message
        print(f"Request failed with status code {response.status_code}: {response.text}")


BASE_URL = "https://gw.api.it.umich.edu/um/aa/ClassroomList/v2"
def get_classroom(public_key, private_key):
    """Make a call to the /Classrooms Endpoint"""
    auth_header = generate_token(public_key, private_key, "classrooms")
    response = requests.get(f"{BASE_URL}/Classrooms", headers=auth_header)
    if response.ok:
        content_type = response.headers.get('Content-Type', '')
        print(f"Content-Type: {content_type}")
        print("Classrooms API Call Successfull")
        try:
            data = response.json()  # Parse JSON response
            return data.get("Classrooms", {}).get("Classroom", [])
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            print(response.text)
        return None
    else:
        print(f"Request failed with status code {response.status_code}: {response.text}")

def get_room_info(room_id, public_key, private_key):
    """Make a call to the /Classrooms/{room_id} Endpoint. Prev Auth reqd."""
    auth_header = generate_token(public_key, private_key, "classrooms")
    response = requests.get(f"{BASE_URL}/Classrooms/{room_id}", headers=auth_header)
    if response.ok:
        print("Classroom Info API Call Successfull")
        try:
            data = response.json()  # Parse JSON response
            return data.get("Classrooms", {}).get("Classroom", [])
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            print(response.text)
    else:
        print(f"Request failed with status code {response.status_code}: {response.text}")

def get_data_from_endpoint(endpoint, room_id, auth_header, params):
    """Make an API call to any classroom endpoint"""
    #insert the room_id into the endpoint
    endpoint = endpoint.replace("{RoomID}", room_id)

    # Make the GET request
    response = requests.get(f"{BASE_URL}{endpoint}", headers=auth_header, params=params) 
    # Check if the response is successful
    if response.status_code == 200:
        print(f"Call to {endpoint} successful")
        try:
            data = response.json()  # Parse JSON response
            return data.get("Classrooms", {}).get("Classroom", [])
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            print(response.text)
        if "Classroom" in response_dict["Classrooms"]:
            return response_dict["Classrooms"]["Classroom"]
        else:
            return False
    else:
        # Print an error message for a 401 response
        print(f"{response.status_code} Error from {endpoint}: {response.text}")
        return None  # Return None or an appropriate error message

def without_keys(d, keys):
    """Remove Keys from a dictionary"""
    return {k: d[k] for k in d.keys() - keys}


def with_keys(my_dict, keep):
    """Keep only wanted keys in a dictionary"""
    unwanted = set(my_dict) - set(keep)
    for unwanted_key in unwanted:
        del my_dict[unwanted_key]
    return my_dict