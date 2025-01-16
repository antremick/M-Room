"""Command line testing calls to clasroom APIs"""
import os
from dotenv import load_dotenv
import sys
# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now import api_functions
import api_functions
import api_functions
from pprint import pprint 


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
ROSS_CODE = 'ROSS BUS'
BLAU_CODE = 'BLAU HALL'

# pprint(classrooms)

# classroomID = classrooms[0]["FacilityID"]
# for endpoint in endpoints[1:]:
#     get_data_from_endpoint(endpoint, classroomID)
def without_keys(d, keys):
    """Remove Keys from a dictionary"""
    return {k: d[k] for k in d.keys() - keys}

def with_keys(my_dict, keep):
    """Keep only wanted keys in a dictionary"""
    unwanted = set(my_dict) - set(keep)
    for unwanted_key in unwanted:
        del my_dict[unwanted_key]
    return my_dict



# remove buildingid, campus code, and campus description keys 
blau_rooms = [without_keys(room, ["BuildingID", "CampusCd", "CampusDescr"]) for room in classrooms if room["BldDescrShort"] == BLAU_CODE]
ross_rooms = [without_keys(room, ["BuildingID", "CampusCd", "CampusDescr"])  for room in classrooms if room["BldDescrShort"] == ROSS_CODE]

pprint(blau_rooms)

# dates = {
#     "startDate": "11-15-2023",
#     "endDate": "11-16-2023"
# }

dates = {
    "startDate": "6-1-2024",
    "endDate": "6-7-2024"
}
authHeader = api_functions.generate_token(publicKey, privateKey, "classrooms")
# for room in blau_rooms:
#     classroomID = room["FacilityID"]
#     meetings = api_functions.get_data_from_endpoint(endpoints[4], classroomID, authHeader, dates)
#     # keep only date and meeting time keys from meetings, add to rooms
#     if meetings:
#         room["Meetings"] = [with_keys(meeting, ["MtgDate", "MtgStartTime", "MtgEndTime"]) for meeting in meetings]


for room in blau_rooms:
    classroomID = room["FacilityID"]
    meetings = api_functions.get_data_from_endpoint(endpoints[4], classroomID, authHeader, dates)
    room["Meetings"] = [with_keys(meeting, ["MtgDate", "MtgStartTime", "MtgEndTime"]) for meeting in meetings]

pprint(blau_rooms)

