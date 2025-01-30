"""Command line testing calls to clasroom APIs"""
import os
from dotenv import load_dotenv
import sys
import json
# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now import api_functions
import api_functions
from pprint import pprint 
import requests

def load_json_data(filename="buildings.json"):
    """Load data from a JSON file
    
    Args:
        filename (str): Path to the JSON file. Defaults to 'buildings.json'
        
    Returns:
        dict: The loaded JSON data
    """
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Create absolute path to the JSON file
    file_path = os.path.join(script_dir, filename)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: {file_path} not found")
        return None
    except json.JSONDecodeError:
        print(f"Error: {file_path} is not valid JSON")
        return None

def main():
    """Main function for importing classrooms and other data"""
    load_dotenv()
    

        
    publicKey = os.getenv("PUBLIC_KEY")
    privateKey = os.getenv("PRIVATE_KEY")

    endpoints = [
        "/Classrooms",
        "/Classrooms/{RoomID}",
        "/Classrooms/{RoomID}/Characteristics",
        "/Classrooms/{RoomID}/Contacts",
        "/Classrooms/{RoomID}/Meetings"
    ]

   
    date = {
        "startDate": api_functions.get_today_date(),
        "endDate": api_functions.get_today_date()
    }

    # Load in Classrooms
    print("Loading in Buildings")
    classrooms = api_functions.get_classroom(publicKey, privateKey)

    with open('data.json', 'w', encoding='utf-8') as json_file:
        json.dump(classrooms, json_file)

        # Load data from JSON file
    # remove buildingid, campus code, and campus description keys 
    classrooms = [api_functions.without_keys(room, ["CampusCd", "CampusDescr"]) for room in classrooms]
    authHeader = api_functions.generate_token(publicKey, privateKey, "classrooms")
   
    data = load_json_data()
    if data is None:
        return
    
    myset = set()
    print("Parsing Classrooms")
    for room in classrooms:
        if room["BuildingID"] in data:
            room["BuildingShort"] = data[room["BuildingID"]]["short_name"]
            room["BuildingName"] = data[room["BuildingID"]]["full_name"]
        # myset.add(room["BldDescrShort"])
        classroomID = room["FacilityID"]
        # Get meetings for each classroom
        meetings = api_functions.get_data_from_endpoint(endpoints[4], classroomID, authHeader, date)
        room["Meetings"] = [api_functions.with_keys(meeting, ["MtgDate", "MtgStartTime", "MtgEndTime"]) for meeting in meetings]

    

    url = "https://mroom-api-c7aef75a74b0.herokuapp.com/import_data"

    # Pass the Python dictionary directly to the function
    print("Pushing to API")
    api_functions.push_to_api(url, classrooms)

if __name__ == "__main__":
    main()