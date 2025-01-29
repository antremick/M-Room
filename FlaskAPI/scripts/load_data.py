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


    with open('data.json', 'w') as json_file:
        json.dump(classrooms, json_file)
    # remove buildingid, campus code, and campus description keys 
    classrooms = [api_functions.without_keys(room, ["CampusCd", "CampusDescr"]) for room in classrooms]
    authHeader = api_functions.generate_token(publicKey, privateKey, "classrooms")
   
    myset = set()
    print("Parsing Classrooms")
    for room in classrooms:
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