# File: API/db_setup.py
import json
from API.model import get_db


def create_tables():
    """
    Create Building and Room tables if they don't already exist.
    """
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS building (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS room (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roomNum TEXT NOT NULL UNIQUE,
            building_id INTEGER NOT NULL,
            meetings TEXT,
            FOREIGN KEY(building_id) REFERENCES building(id) ON DELETE CASCADE
        )
    """)
    conn.commit()

def insert_building(name):
    """
    Insert a new Building record.
    Returns the newly created building's ID.
    """
    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO building (name) VALUES (?)",
        (name,)
    )
    conn.commit()
    return cursor.lastrowid

def get_or_create_building(name):
    """
    Returns the ID of the building with `name`.
    If it doesn't exist, creates it.
    """
    conn = get_db()
    row = conn.execute(
        "SELECT id FROM building WHERE name = ?",
        (name,)
    ).fetchone()

    if row is not None:
        # Building already exists
        return row["id"]
    else:
        # Need to create new building
        return insert_building(name)

def insert_room(room_num, building_id, meetings=None):
    """
    Insert a new Room record.
    'meetings' should be a Python list of dicts.
    """
    conn = get_db()
    meetings_json = json.dumps(meetings) if meetings else "[]"
    cursor = conn.execute(
        "INSERT INTO room (roomNum, building_id, meetings) VALUES (?, ?, ?)",
        (room_num, building_id, meetings_json)
    )
    conn.commit()
    return cursor.lastrowid