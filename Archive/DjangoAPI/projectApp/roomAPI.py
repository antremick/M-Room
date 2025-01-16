import os
from dotenv import load_dotenv
import api_functions
from pprint import pprint 
from .serializers import RoomSerializer, BuildingSerializer




load_dotenv()

publicKey = os.getenv("PUBLIC_KEY")
privateKey = os.getenv("PRIVATE_KEY")

authHeader = api_functions.generate_token(publicKey, privateKey, "classrooms")

dates = {
            "startDate": "12-07-2023",
            "endDate": "12-08-2023" }

classrooms = api_functions.get_data_from_endpoint("/Classrooms", 0, authHeader, dates)

if classrooms:
    for room in classrooms:
        RoomNum = room["FacilityID"]
        Building = room["BldDescrShort"]
        Meetings = []

        meetings = api_functions.get_data_from_endpoint("/Classrooms/{RoomID}/Meetings", RoomNum, authHeader, dates)
        if meetings:
            for meeting in meetings:
                start = meeting["MtgStartTime"]
                end = meeting["MtgEndTime"]


                ############## Tweak this to just make it times 
                # digits = [0,0,0,0,0,0,0,0,0,0]
                # #First digit
                #     # Start AM/PM
                # #Digits 2 - 5 
                #     #Start time

                # if start[-2:] == "PM":
                #     digits[0] = 1
                # digits[1:3] = start[0:2]
                # digits[3:5] = start[3:5]
                # if end[-2:] == "PM":
                #     digits[5] = 1
                # digits[6:8] = end[0:2]
                # digits[8:] = end[3:5]

                #convert digits array to int
                Meetings.append(int(''.join(map(str, digits))))

        room_data = {"RoomNum":  RoomNum,
                    "Building": Building,
                    "Meetings": Meetings }

        building_data = {"Building": Building}
        serializer = BuildingSerializer(data=building_data)

        room_data = {"RoomNum":  RoomNum,
                    "Building": Building,
                    "Meetings": Meetings }
        serializer = RoomSerializer(data=room_data)

        if serializer.is_valid():
            serializer.save()
        else:
            print("An error occurred: ", serializer.errors)