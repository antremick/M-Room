"""Load Data from Blau Rooms Into Django"""
"""Load Data from Blau Rooms Into Django"""
import os
import sys
from dotenv import load_dotenv
from pprint import pprint

import django

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now import api_functions
import api_functions
# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "API.settings")
django.setup()

# Import models and other dependencies
from projectApp.models import Building, Room


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

classrooms = api_functions.get_classroom(publicKey, privateKey)
BLAU_CODE = 'BLAU HALL'
blau_rooms = [api_functions.without_keys(room, ["BuildingID", "CampusCd", "CampusDescr"]) for room in classrooms if room["BldDescrShort"] == BLAU_CODE]


dates = {
    "startDate": "6-1-2024",
    "endDate": "6-7-2024"
}

authHeader = api_functions.generate_token(publicKey, privateKey, "classrooms")


for room in blau_rooms:
    classroomID = room["FacilityID"]
    meetings = api_functions.get_data_from_endpoint(endpoints[4], classroomID, authHeader, dates)
    room["Meetings"] = [api_functions.with_keys(meeting, ["MtgDate", "MtgStartTime", "MtgEndTime"]) for meeting in meetings]

for room in blau_rooms:
    building_name = room["BldDescrShort"]
    room_number = room["FacilityID"]
    meetings = room["Meetings"]

    building, created = Building.objects.get_or_create(name=building_name)
    Room.objects.create(room_number=room_number, building=building, meetings=meetings)

print("Buildings and Rooms have been populated successfully.")