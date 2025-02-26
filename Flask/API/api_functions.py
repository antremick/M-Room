"""Make calls to classroom apis"""
from pprint import pprint
import requests
import json
from datetime import date 
import base64
import sys

# Your public and private API keys
def generate_token(public_key, private_key, scope):
    """Generate an OAuth token for API access"""
    token_url = "https://gw.api.it.umich.edu/um/oauth2/token"
    token_data = {
        "grant_type": "client_credentials",
        "scope": scope
    }
    token_headers = {
        "Authorization": f"Basic {base64.b64encode(f'{public_key}:{private_key}'.encode()).decode()}"
    }
    
    try:
        response = requests.post(token_url, headers=token_headers, data=token_data, timeout=30)
        response.raise_for_status()
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    except requests.exceptions.ConnectionError:
        print("\nERROR: Cannot connect to UMich API.")
        print("Make sure you are:")
        print("1. Connected to the internet")
        print("2. On the UMich network or VPN")
        print("3. Have valid API credentials in your .env file")
        sys.exit(1)
    except Exception as e:
        print(f"\nError generating token: {str(e)}")
        sys.exit(1)


BASE_URL = "https://gw.api.it.umich.edu/um/aa/ClassroomList/v2"
def get_classroom(public_key, private_key):
    """Make a call to the /Classrooms Endpoint with pagination support"""
    auth_header = generate_token(public_key, private_key, "classrooms")
    all_classrooms = []
    next_url = f"{BASE_URL}/Classrooms"

    while next_url:
        print(f"Fetching: {next_url}")
        response = requests.get(next_url, headers=auth_header)
        
        if response.ok:
            try:
                data = response.json()
                classrooms = data.get("Classrooms", {}).get("Classroom", [])
                if classrooms:
                    all_classrooms.extend(classrooms)
                
                # Parse Link header for pagination
                link_header = response.headers.get('Link', '')
                print("Link header:", link_header)  # Debug print
                
                # Parse all links in the header
                links = {}
                if link_header:
                    parts = link_header.split(',')
                    for part in parts:
                        section = part.split(';')
                        url = section[0].strip('<> ')
                        rel = section[1].split('=')[1].strip('"')
                        links[rel] = url
                
                next_url = links.get('next')
                print("Next URL:", next_url)  # Debug print
                
                print(f"Retrieved {len(classrooms)} classrooms. Total so far: {len(all_classrooms)}")
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON: {e}")
                print(response.text)
                break
        else:
            print(f"Request failed with status code {response.status_code}: {response.text}")
            break


        
    return all_classrooms

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

def get_data_from_endpoint(endpoint, room_id, auth_header, params, base_url=None):
    """Make an API call to any endpoint"""
    # Use provided base_url or default to classroom API
    if base_url is None:
        base_url = "https://gw.api.it.umich.edu/um/aa/ClassroomList/v2"
        
    #insert the room_id into the endpoint
    endpoint = endpoint.replace("{RoomID}", room_id)

    # Make the GET request
    response = requests.get(f"{base_url}{endpoint}", headers=auth_header, params=params) 
    # Check if the response is successful
    if response.status_code == 200:
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
    """Keep only wanted keys in a dictionary
    
    Args:
        my_dict (dict): Dictionary to filter
        keep (list): List of keys to keep
        
    Returns:
        dict: New dictionary with only the specified keys
    """
    if not isinstance(my_dict, dict):
        return my_dict
    

    filtered_dict = {}
    for key in keep:
        if key in my_dict:
            filtered_dict[key] = my_dict[key]
    return filtered_dict

def push_to_api(url, payload):
        """Send JSON payload to API specified at URL"""
        try:

            headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
            }
            # Post the data as JSON (directly pass the dictionary, no need for json.dumps)
            response = requests.post(url, json=payload, headers=headers)
            
            # Check if the request was successful
            if response.status_code == 200 or response.status_code == 201:
                print("Push request sent successfully!")
                # Print response if needed
                print("Response:", response.json())
            else:
                print(f"Error: Received status code {response.status_code}")
                print("Details:", response.text)
        except requests.exceptions.RequestException as e:
            print("Request failed:", e)

def get_today_date():
    """
    Returns today's date as a string in 'MM-DD-YYYY' format.
    """
    today = date.today()
    formatted_date = today.strftime("%-m-%-d-%Y")  # For Unix-based systems
    # If you're on Windows, use the following line instead:
    # formatted_date = today.strftime("%#m-%#d-%Y")
    return formatted_date
