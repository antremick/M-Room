"""Command line testing calls to classroom APIs"""


import os
from dotenv import load_dotenv
import sys
import json
import re
# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import api_functions
import requests
import argparse

class DataLoader:
    """Class for handling classroom data loading and processing"""
    
    def __init__(self, dev_mode=False):
        """Initialize DataLoader with default endpoints and API URL"""
        self.endpoints = [
            "/Classrooms",
            "/Classrooms/{RoomID}",
            "/Classrooms/{RoomID}/Characteristics",
            "/Classrooms/{RoomID}/Contacts",
            "/Classrooms/{RoomID}/Meetings"
        ]
        
        # Development mode buildings (common buildings at UMich)
        self.dev_buildings = ['CCCB', 'UMMA', 'UNION', 'CHEM', 'MASON']
        self.dev_mode = dev_mode
        
        load_dotenv()
        if os.getenv('ENV') == "staging":
            self.api_url = os.getenv('API_STAGING') + "/import_data"
        else: 
            self.api_url = os.getenv('API_PROD') + "/import_data"
        self.rooms_key, self.rooms_secret = self._get_api_credentials("ROOMS")
        self.buildings_key, self.buildings_secret = self._get_api_credentials("BUILDINGS")
        self.auth_header = None
        self.building_data = None
        self.buildings_auth = None
        self.short_long = {}
        
    def _get_api_credentials(self, key_name):
        """Get API credentials from environment variables"""
        load_dotenv()
        return os.getenv(f"{key_name}_KEY"), os.getenv(f"{key_name}_SECRET")

    # def load_json_data(self, filename="buildings_import.json"):
    #     """Load data from a JSON file
        
    #     Args:
    #         filename (str): Path to the JSON file. Defaults to 'buildings.json'
            
    #     Returns:
    #         dict: The loaded JSON data
    #     """
    #     script_dir = os.path.dirname(os.path.abspath(__file__))
    #     file_path = os.path.join(script_dir, filename)
        
    #     try:
    #         with open(file_path, 'r', encoding='utf-8') as file:
    #             return json.load(file)
    #     except FileNotFoundError:
    #         print(f"Error: {file_path} not found")
    #         return None
    #     except json.JSONDecodeError:
    #         print(f"Error: {file_path} is not valid JSON")
    #         return None

    def _get_meetings_for_room(self, room_id, date):
        """Get meetings for a specific room
        
        Args:
            room_id (str): Room identifier
            date (dict): Date range for meetings
            
        Returns:
            list: List of meetings or empty list if error
        """
        meetings = api_functions.get_data_from_endpoint(self.endpoints[4], room_id, self.auth_header, date)
        
        # Get trailing digits by iterating from end until we hit a non-digit
        if not meetings:
            meetings = []
        
        room_num = ''
        for char in reversed(room_id):
            if not char.isdigit():
                break
            room_num = char + room_num
            
        for meeting in meetings:
            meeting["FacilityID"] = room_num
        
        
        return [api_functions.with_keys(meeting, ["MtgDate", "MtgStartTime", "MtgEndTime"]) for meeting in meetings]

    def buildings_api_call(self, room):
        """Add building information to room data
        
        Args:
            room (dict): Room data
        """
        # First try to get building info from local JSON file
     
            # If not in local file, fetch from Buildings API
        if room["BldDescrShort"] in self.short_long:
            room["long_name"] = self.short_long[room["BldDescrShort"]]
        else:
            try:
                # Generate new token with buildings scope
                if not hasattr(self, 'buildings_auth'):
                    self.buildings_auth = api_functions.generate_token(
                        self.buildings_key,
                        self.buildings_secret,
                        "buildings"
                    )
                buildings_auth = self.buildings_auth
                # Make API call to get building info
                response = requests.get(
                    f"https://gw.api.it.umich.edu/um/bf/Buildings/v2/BuildingInfoByShortName/{room['BldDescrShort']}", 
                    headers=buildings_auth,
                    timeout=30
                )
                
                if response.ok:
                    building_data = response.json()
                    if "ListOfBldgs" in building_data:
                        room["long_name"] = building_data["ListOfBldgs"]["Buildings"][0]["BuildingLongDescription"]
                        self.short_long[room["BldDescrShort"]] = room["long_name"]
                else:
                    print(f"Failed to get building info for ID {room['BuildingID']}: {response.status_code}")
                    print(f"Error response: {response.text}")
                    
            except Exception as e:
                print(f"Error fetching building data for ID {room['BuildingID']}: {str(e)}")

    def process_classrooms(self, classrooms, date):
        """Process classroom data with meetings and building information"""
        if self.dev_mode:
            # Filter classrooms to only include dev buildings using BldDescrShort
            classrooms = [room for room in classrooms 
                         if room.get("BldDescrShort") in self.dev_buildings]
            print(f"\nDEV MODE: Processing {len(classrooms)} classrooms from {len(self.dev_buildings)} buildings")
            
            # Debug print to see what we're getting
            building_counts = {}
            for room in classrooms:
                bldg = room.get("BldDescrShort")
                building_counts[bldg] = building_counts.get(bldg, 0) + 1
        else:
            print(f"\nProcessing {len(classrooms)} classrooms..")
        
        for room in classrooms:
            # Extract short name by removing trailing numbers
            room["short_name"] = ''.join(c for c in room["FacilityID"] if not c.isdigit())
            
            self.buildings_api_call(room)
            room["Meetings"] = self._get_meetings_for_room(room["FacilityID"], date)
        
        print(f"\nFinished processing {len(classrooms)} classrooms")
        return classrooms

    def run(self):
        """Main execution method for loading and processing classroom data"""
        date = {
            "startDate": api_functions.get_today_date(),
            "endDate": api_functions.get_today_date()
        }

        print("Loading in Buildings")
        classrooms = api_functions.get_classroom(self.rooms_key, self.rooms_secret)
            # Extract building ID by removing trailing numbers

        print("Generating Rooms Token")
        self.auth_header = api_functions.generate_token(
            self.rooms_key, self.rooms_secret, "classrooms"
        )

        print("Generating Buildings Token")
        self.buildings_auth = api_functions.generate_token(
            self.buildings_key, self.buildings_secret, "buildings"
        )
       
        print("Parsing Classrooms")
        classrooms = self.process_classrooms(classrooms, date)

        print("Pushing to API")
        api_functions.push_to_api(self.api_url, classrooms)

def main():
    """Main function to initialize and run the DataLoader"""
    parser = argparse.ArgumentParser(description='Load classroom data')
    parser.add_argument('--dev', action='store_true', 
                       help='Run in development mode with limited buildings')
    args = parser.parse_args()
    
    if args.dev:
        print("Running in development mode with limited buildings")
    
    loader = DataLoader(dev_mode=args.dev)
    loader.run()

if __name__ == "__main__":
    main()