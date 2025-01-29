# File: API/routes.py
import flask
from API import app
from API.db_setup import get_or_create_building, insert_room, create_tables
from API.model import get_db
import json

@app.route("/")
def index():
    return "Hello from Zappa + Flask + Postgres!"

@app.route("/import_data", methods=["POST"])
def import_data():
    """
    Expects JSON in the form of a list of objects.
    Example input: [...data...]
    """
    ### This is jank fix it
    create_tables()
    
    conn = get_db()
    try:
        # 1) Clear existing rows in each table (use a cursor)
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM room")
            cursor.execute("DELETE FROM building")
        conn.commit()

        data = flask.request.get_json(force=True)
        if not data:
            return flask.jsonify({"error": "No JSON payload received"}), 400

        # Load the JSON dictionary from a local file (if you truly want this in production)
        with open('scripts/buildings.json', 'r') as json_file:
            building_data = json.load(json_file)

        # data should be a list of dictionaries
        for item in data:
            if item["BuildingID"] in building_data:
                building_name = building_data[item["BuildingID"]]
            else:
                building_name = item["BldDescrShort"]
            room_num = item["FacilityID"]
            meetings = item.get("Meetings", [])

            # Ensure building exists
            building_id = get_or_create_building(building_name)

            # Insert the room
            insert_room(room_num, building_id, meetings)

        return flask.jsonify({"message": "Data imported successfully"}), 200

    except KeyError as e:
        return flask.jsonify({"error": f"Missing key: {str(e)}"}), 400
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500

@app.route("/buildings", methods=["GET"])
def get_buildings():
    """
    Returns a list of buildings in JSON format.
    Example:
    [
      { "id": 1, "name": "Engineering Building" },
      { "id": 2, "name": "BLAU Hall" }
    ]
    """
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute("SELECT id, name FROM building ORDER BY id")
        rows = cursor.fetchall()

    # rows is a list of dicts if you used DictCursor
    buildings_list = [dict(row) for row in rows]
    return flask.jsonify(buildings_list), 200

@app.route("/rooms", methods=["GET"])
def get_rooms():
    """
    Return a list of all rooms with their 'meetings' data as a parsed list.
    Example:
    [
      {
        "id": 1,
        "roomNum": "BLAU0560",
        "building_id": 5,
        "meetings": [
          {
            "MtgDate": "06-02-2024",
            "MtgStartTime": "09:30 AM",
            "MtgEndTime": "06:00 PM"
          },
          ...
        ]
      },
      ...
    ]
    """
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT r.id, r.roomNum, r.building_id, r.meetings
            FROM room AS r
            ORDER BY r.id
        """)
        rows = cursor.fetchall()

    # Convert 'meetings' from a JSON string to a Python list
    rooms_list = []
    for row in rows:
        row_dict = dict(row)
        if row_dict["meetings"]:
            row_dict["meetings"] = json.loads(row_dict["meetings"])
        else:
            row_dict["meetings"] = []
        rooms_list.append(row_dict)

    return flask.jsonify(rooms_list), 200