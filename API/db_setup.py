# File: API/db_setup.py
import os
import json
from API.model import get_db
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv, find_dotenv

def find_env():
    env_path = find_dotenv()
    print(f"Loading .env from: {env_path}")
    load_dotenv(env_path)


def get_table_names():
    """
    Helper function to get environment-specific table names
    """
    # Find and load the .env file

    find_env()
    # Get and print the environment for debugging
    env = os.getenv('ENV')
    print(f"Current ENV value: {env}")
    
    # Default to 'prod' if ENV is not set
    if not env:
        print("Warning: ENV not set, defaulting to 'prod'")
        env = 'prod'
    
    table_names = (f"building_{env}", f"room_{env}")
    print(f"Using table names: {table_names}")
    
    return table_names

def create_tables():
    """
    Create Building and Room tables if they don't already exist (PostgreSQL style).
    Uses environment variable TABLE_ENV to determine table names.
    """
    print("getting table names")
    building_table, room_table = get_table_names()

    conn = get_db()
    with conn.cursor() as cursor:
        # building table
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {building_table} (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                short_name VARCHAR(255) NOT NULL
            )
        """)

        # room table 
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {room_table} (
                id SERIAL PRIMARY KEY,
                roomNum VARCHAR(255) NOT NULL UNIQUE,
                building_id INT NOT NULL,
                meetings TEXT,
                FOREIGN KEY (building_id) REFERENCES {building_table}(id) ON DELETE CASCADE
            )
        """)

    conn.commit()


def insert_building(name, short_name):
    """
    Insert a new Building record in Postgres and return its generated ID.
    """
    if not isinstance(short_name, str):
        raise TypeError("short_name must be a string")

    if len(short_name) > 255:
        raise ValueError("short_name exceeds the maximum length of 255 characters")
    
    building_table, _ = get_table_names()
    conn = get_db()
    with conn.cursor() as cursor:
        sql = f"INSERT INTO {building_table} (name, short_name) VALUES (%s, %s) RETURNING id"
        cursor.execute(sql, (name, short_name))
        row = cursor.fetchone()
    conn.commit()
    return row["id"]

def get_or_create_building(name, short_name):
    """
    Returns the ID of the building with `name`.
    If it doesn't exist, creates it.
    """
    building_table, _ = get_table_names()
    conn = get_db()
    with conn.cursor() as cursor:
        sql = f"SELECT id FROM {building_table} WHERE name = %s"
        cursor.execute(sql, (name,))
        row = cursor.fetchone()

        if row is not None:
            return row[0]
        else:
            return insert_building(name, short_name)

def insert_room(room_num, building_id, meetings=None):
    """
    Insert a new Room record in Postgres, returning its generated ID.
    'meetings' is stored as JSON in TEXT column.
    """
    meetings_json = json.dumps(meetings) if meetings else "[]"
    
    _, room_table = get_table_names()
    conn = get_db()
    with conn.cursor() as cursor:
        sql = f"""
            INSERT INTO {room_table} (roomNum, building_id, meetings)
            VALUES (%s, %s, %s)
            RETURNING id
        """
        cursor.execute(sql, (room_num, building_id, meetings_json))
        row = cursor.fetchone()
    conn.commit()
    return row["id"]

