# File: API/routes.py
import flask
from API import app
from API.db_setup import get_or_create_building, insert_room, create_tables
from API.model import get_db
import json
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
from jwt import encode, decode  # More specific import
from functools import wraps
import datetime
from flask import request, jsonify
import os
from datetime import UTC

# Use an environment variable for the secret key in production
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-this')

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

        # Load the JSON dictionary from a local file (if you truly want this in production) (why is this in here)
        with open('scripts/buildings.json', 'r', encoding='utf-8') as json_file:
            building_data = json.load(json_file)

        # data should be a list of dictionaries
        # data should be a list of dictionaries
        for item in data:
            if item["BuildingID"] in building_data:
                full_name = building_data[item["BuildingID"]]["full_name"]
                short_name = building_data[item["BuildingID"]]["short_name"]
            else:
                full_name = item["BldDescrShort"]
                short_name = ""

            room_num = item["FacilityID"]
            meetings = item.get("Meetings", [])
            
            print(f"full_name: {full_name}, short_name: {short_name}")
            # Ensure building exists
            building_id = get_or_create_building(full_name, short_name)

            # Insert the room
            insert_room(room_num, building_id, meetings)

        return flask.jsonify({"message": "Data imported successfully"}), 200

    except KeyError as e:
        return flask.jsonify({"error": f"Missing key: {str(e)}"}), 400
    except (json.JSONDecodeError, IOError) as e:
        return flask.jsonify({"error": str(e)}), 500
    except psycopg2.Error as e:
        return flask.jsonify({"error": "Database error: " + str(e)}), 500

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
        cursor.execute("SELECT id, name, short_name FROM building ORDER BY id")
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
    return flask.jsonify(rooms_list), 200

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            data = decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            conn = get_db()
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM users WHERE id = %s", (data['user_id'],))
                current_user = cur.fetchone()
        except:
            return jsonify({'message': 'Token is invalid'}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated

@app.route("/auth/register", methods=["POST"])
def register():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Missing required fields'}), 400
    
    hashed_password = generate_password_hash(data['password'])
    
    conn = get_db()
    with conn.cursor() as cur:
        try:
            cur.execute(
                "INSERT INTO users (email, password_hash) VALUES (%s, %s) RETURNING id",
                (data['email'], hashed_password)
            )
            user_id = cur.fetchone()[0]
            conn.commit()
            
            token = encode({
                'user_id': user_id,
                'exp': datetime.datetime.now(UTC) + datetime.timedelta(days=7)
            }, app.config['SECRET_KEY'])
            
            return jsonify({
                'token': token,
                'email': data['email']
            }), 201
        except Exception as e:
            conn.rollback()
            return jsonify({'message': 'Email already exists'}), 400

@app.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Missing required fields'}), 400
    
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM users WHERE email = %s", (data['email'],))
        user = cur.fetchone()
        
        if user and check_password_hash(user['password_hash'], data['password']):
            token = encode({
                'user_id': user['id'],
                'exp': datetime.datetime.now(UTC) + datetime.timedelta(days=7)
            }, app.config['SECRET_KEY'])
            
            return jsonify({
                'token': token,
                'email': user['email']
            })
            
        return jsonify({'message': 'Invalid credentials'}), 401

# Favorites endpoints
@app.route("/favorites/buildings", methods=["GET", "POST"])
@token_required
def favorite_buildings(current_user):
    conn = get_db()
    
    if request.method == "POST":
        data = request.get_json()
        building_id = data.get('building_id')
        
        with conn.cursor() as cur:
            try:
                cur.execute(
                    "INSERT INTO favorite_buildings (user_id, building_id) VALUES (%s, %s)",
                    (current_user['id'], building_id)
                )
                conn.commit()
                return jsonify({'message': 'Building favorited'}), 201
            except Exception as e:
                conn.rollback()
                return jsonify({'message': 'Building already favorited'}), 400
    
    # GET request
    with conn.cursor() as cur:
        cur.execute("""
            SELECT b.* FROM building b
            JOIN favorite_buildings fb ON b.id = fb.building_id
            WHERE fb.user_id = %s
        """, (current_user['id'],))
        favorites = cur.fetchall()
        return jsonify([dict(row) for row in favorites])

@app.route("/favorites/buildings/<int:building_id>", methods=["DELETE"])
@token_required
def unfavorite_building(current_user, building_id):
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute(
            "DELETE FROM favorite_buildings WHERE user_id = %s AND building_id = %s",
            (current_user['id'], building_id)
        )
        conn.commit()
        return jsonify({'message': 'Building unfavorited'}), 200

# Similar endpoints for favorite rooms
@app.route("/favorites/rooms", methods=["GET", "POST"])
@token_required
def favorite_rooms(current_user):
    conn = get_db()
    
    if request.method == "POST":
        data = request.get_json()
        room_id = data.get('room_id')
        
        with conn.cursor() as cur:
            try:
                cur.execute(
                    "INSERT INTO favorite_rooms (user_id, room_id) VALUES (%s, %s)",
                    (current_user['id'], room_id)
                )
                conn.commit()
                return jsonify({'message': 'Room favorited'}), 201
            except Exception as e:
                conn.rollback()
                return jsonify({'message': 'Room already favorited'}), 400
    
    # GET request
    with conn.cursor() as cur:
        cur.execute("""
            SELECT r.* FROM room r
            JOIN favorite_rooms fr ON r.id = fr.room_id
            WHERE fr.user_id = %s
        """, (current_user['id'],))
        favorites = cur.fetchall()
        return jsonify([dict(row) for row in favorites])

@app.route("/favorites/rooms/<int:room_id>", methods=["DELETE"])
@token_required
def unfavorite_room(current_user, room_id):
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute(
            "DELETE FROM favorite_rooms WHERE user_id = %s AND room_id = %s",
            (current_user['id'], room_id)
        )
        conn.commit()
        return jsonify({'message': 'Room unfavorited'}), 200