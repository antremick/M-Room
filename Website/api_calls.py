"""Make calls to clasroom APIs"""
import os
from dotenv import load_dotenv
import api_functions


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
# pprint(classrooms)

# classroomID = classrooms[0]["FacilityID"]
# for endpoint in endpoints[1:]:
#     get_data_from_endpoint(endpoint, classroomID)

dates = {
    "startDate": "11-15-2023",
    "endDate": "11-16-2023"
}
authHeader = api_functions.generate_token(publicKey, privateKey, "classrooms")
for room in classrooms:
    classroomID = room["FacilityID"]
    api_functions.get_data_from_endpoint(endpoints[4], classroomID, authHeader, dates)
