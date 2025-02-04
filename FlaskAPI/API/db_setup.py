# File: API/db_setup.py
import json
from API.model import get_db

def create_tables():
    """
    Create Building and Room tables if they don't already exist (PostgreSQL style).
    """
    conn = get_db()
    with conn.cursor() as cursor:
        # building table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS building (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                short_name VARCHAR(255) NOT NULL
            )
        """)

        # room table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS room (
                id SERIAL PRIMARY KEY,
                roomNum VARCHAR(255) NOT NULL UNIQUE,
                building_id INT NOT NULL,
                meetings TEXT,
                FOREIGN KEY (building_id) REFERENCES building(id) ON DELETE CASCADE
            )
        """)
    conn.commit()

def insert_building(name, short_name):
    """
    Insert a new Building record in Postgres and return its generated ID.
    """
    if not isinstance(short_name, str):
        raise TypeError("short_name must be a string")

    # Ensure short_name is within the 255 character limit
    if len(short_name) > 255:
        raise ValueError("short_name exceeds the maximum length of 255 characters")
    
    conn = get_db()
    with conn.cursor() as cursor:
        # Use RETURNING id to get the auto-generated primary key
        sql = "INSERT INTO building (name, short_name) VALUES (%s, %s) RETURNING id"
        cursor.execute(sql, (name, short_name))
        row = cursor.fetchone()
    conn.commit()
    return row["id"]  # if using a DictCursor, else row[0]

def get_or_create_building(name, short_name):
    """
    Returns the ID of the building with `name`.
    If it doesn't exist, creates it.
    """
    conn = get_db()
    with conn.cursor() as cursor:
        # Try to find an existing record
        sql = "SELECT id FROM building WHERE name = %s"
        cursor.execute(sql, (name,))  # Make sure to pass name as a tuple
        row = cursor.fetchone()

        if row is not None:
            # Building already exists
            return row[0]  # Access the first (and only) element in the tuple
        else:
            # Need to create new building
            return insert_building(name, short_name)

def insert_room(room_num, building_id, meetings=None):
    """
    Insert a new Room record in Postgres, returning its generated ID.
    'meetings' is stored as JSON in TEXT column.
    """
    meetings_json = json.dumps(meetings) if meetings else "[]"

    conn = get_db()
    with conn.cursor() as cursor:
        sql = """
            INSERT INTO room (roomNum, building_id, meetings)
            VALUES (%s, %s, %s)
            RETURNING id
        """
        cursor.execute(sql, (room_num, building_id, meetings_json))
        row = cursor.fetchone()
    conn.commit()
    return row["id"]