import os
from pprint import pprint
from django.core.management.base import BaseCommand
from django.db import connection
from api_functions import generate_token, get_data_from_endpoint
from projectApp.models import Building, Room
from projectApp.serializers import BuildingSerializer, RoomSerializer


def call_api_and_ingest():
    """
    Call the external API, fetch data, and save it to the Django models.
    """
    # Load environment variables
    public_key = os.getenv("PUBLIC_KEY")
    private_key = os.getenv("PRIVATE_KEY")

    if not public_key or not private_key:
        print("Error: PUBLIC_KEY and PRIVATE_KEY must be set in the environment.")
        return

    # Generate API token
    auth_header = generate_token(public_key, private_key, "classrooms")

    # Specify date range for API query
    dates = {"startDate": "12-07-2023", "endDate": "12-08-2023"}

    # Fetch classroom data from the API
    classrooms = get_data_from_endpoint("/Classrooms", 0, auth_header, dates)

    if classrooms:
        print("Ingesting data into Django models...")
        for room in classrooms:
            room_num = room["FacilityID"]
            building_name = room["BldDescrShort"]
            meetings = []

            # Fetch meeting times for the room
            room_meetings = get_data_from_endpoint(
                f"/Classrooms/{room_num}/Meetings", room_num, auth_header, dates
            )
            if room_meetings:
                for meeting in room_meetings:
                    start = meeting["MtgStartTime"]
                    end = meeting["MtgEndTime"]
                    meetings.append({"start": start, "end": end})

            # Save Building data
            building_data = {"name": building_name}
            building_serializer = BuildingSerializer(data=building_data)
            if building_serializer.is_valid():
                building_instance, _ = Building.objects.get_or_create(
                    name=building_name
                )
            else:
                print("Error in Building Serializer:", building_serializer.errors)
                continue

            # Save Room data
            room_data = {
                "roomNum": room_num,
                "building": building_instance.id,
                "meetings": meetings,
            }
            room_serializer = RoomSerializer(data=room_data)
            if room_serializer.is_valid():
                room_serializer.save()
            else:
                print("Error in Room Serializer:", room_serializer.errors)
                continue

        print("Data ingestion completed successfully.")
    else:
        print("No classrooms data fetched from the API.")


def query_data_with_sql():
    """
    Use raw SQL to verify data ingestion.
    """
    print("\nFetching data using raw SQL...\n")
    with connection.cursor() as cursor:
        # Query Building data
        cursor.execute("SELECT * FROM projectApp_building;")
        buildings = cursor.fetchall()
        print("Buildings:")
        pprint(buildings)

        # Query Room data
        cursor.execute("SELECT * FROM projectApp_room;")
        rooms = cursor.fetchall()
        print("\nRooms:")
        pprint(rooms)


class Command(BaseCommand):
    help = "Ingest data from an external API into the Django database and verify the ingestion with raw SQL queries."

    def handle(self, *args, **kwargs):
        # Step 1: Call the API and ingest data
        call_api_and_ingest()

        # Step 2: Query the ingested data using raw SQL
        query_data_with_sql()