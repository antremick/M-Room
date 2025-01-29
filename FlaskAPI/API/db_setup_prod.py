# File: API/db_setup_prod.py
import json
import os
from dotenv import load_dotenv
import pymysql
import flask

def get_db():
    """Connect to DB"""
    load_dotenv()
    if 'mysql_db' not in flask.g:
        conn = pymysql.connect(
            host = os.environ.get("DB_HOST"),
            user = os.environ.get("DB_USERNAME"),
            password = os.environ.get("DB_PASSWORD"),
            db = os.environ.get("DB_NAME"),
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor
        )
        flask.g.mysql_db = conn
    return flask.g.mysql_db


def create_tables():
    """
    Create Building and Room tables if they don't already exist (MySQL style).
    """
    conn = get_db()
    with conn.cursor() as cursor:
        # Building table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS building (
                id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(255) NOT NULL
            ) ENGINE=InnoDB;
        """)

        # Room table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS room (
                id INT PRIMARY KEY AUTO_INCREMENT,
                roomNum VARCHAR(255) NOT NULL UNIQUE,
                building_id INT NOT NULL,
                meetings TEXT,
                FOREIGN KEY (building_id) REFERENCES building(id)
                    ON DELETE CASCADE
            ) ENGINE=InnoDB;
        """)
    conn.commit()


def insert_building(name):
    """
    Insert a new Building record and return its auto-increment ID.
    """
    conn = get_db()
    with conn.cursor() as cursor:
        sql = "INSERT INTO building (name) VALUES (%s)"
        cursor.execute(sql, (name,))
        conn.commit()
        return cursor.lastrowid


def get_or_create_building(name):
    """
    Returns the ID of the building with `name`.
    If not found, creates it.
    """
    conn = get_db()
    with conn.cursor() as cursor:
        sql = "SELECT id FROM building WHERE name = %s"
        cursor.execute(sql, (name,))
        row = cursor.fetchone()

        if row is not None:
            # Building already exists
            return row["id"]
        else:
            # Need to create new building
            return insert_building(name)


def insert_room(room_num, building_id, meetings=None):
    """
    Insert a new Room record.
    'meetings' should be a Python list of dicts, which we store as JSON in MySQL.
    """
    meetings_json = json.dumps(meetings) if meetings else "[]"
    conn = get_db()
    with conn.cursor() as cursor:
        sql = """
            INSERT INTO room (roomNum, building_id, meetings)
            VALUES (%s, %s, %s)
        """
        cursor.execute(sql, (room_num, building_id, meetings_json))
        conn.commit()
        return cursor.lastrowid