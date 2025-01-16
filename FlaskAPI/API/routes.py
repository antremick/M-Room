# File: API/routes.py
import flask
from API import app
from API.db_setup import get_or_create_building, insert_room
from API.model import get_db
import json
from pprint import pprint
@app.route("/import_data", methods=["POST"])
def import_data():
    """
    Expects JSON in the form of a list of objects, e.g.:
    """
    try:
      data = flask.request.get_json(force=True)
      if not data:
        return flask.jsonify({"error": "No JSON payload received"}), 400

      # data should be a list of dictionaries
      for item in data:
          building_name = item["BldDescrShort"]
          room_num = item["FacilityID"]
          meetings = item.get("Meetings", [])

          # 1) Ensure building exists (create if needed)
          building_id = get_or_create_building(building_name)

          # 2) Insert the room
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
    Example response:
    [
      {
        "id": 1,
        "name": "Engineering Building"
      },
      {
        "id": 2,
        "name": "BLAU Hall"
      }
    ]
    """
    conn = get_db()
    rows = conn.execute("SELECT id, name FROM building").fetchall()
    buildings_list = [dict(r) for r in rows]
    
    return flask.jsonify(buildings_list), 200

@app.route("/rooms", methods=["GET"])
def get_rooms():
    """
    Return a list of all rooms with their 'meetings' data as a parsed list.
    Example response:
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
    # Fetch rows. Adjust columns to match your schema.
    # If you want building info, join with the building table.
    rows = conn.execute("""
        SELECT r.id, r.roomNum, r.building_id, r.meetings
        FROM room AS r
        ORDER BY r.id
    """).fetchall()

    # Convert each row to a dict and parse the 'meetings' JSON
    rooms_list = []
    for row in rows:
        row_dict = dict(row)
        # 'meetings' column is stored as TEXT in DB; parse into a Python list
        if row_dict["meetings"]:
            row_dict["meetings"] = json.loads(row_dict["meetings"])
        else:
            row_dict["meetings"] = []
        rooms_list.append(row_dict)

    return flask.jsonify(rooms_list), 200