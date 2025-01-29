# File: API/db_test.py
import logging
from . import app
from API.db_setup_prod import get_db  # or wherever get_db() is defined

def test_db_connection():
    """
    Attempt to connect to the database by acquiring a connection
    within a Flask app context and running a simple query.
    """
    try:
        with app.app_context():
            conn = get_db()
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
            logging.info(f"DB connection test query returned: {result}")
        return True
    except Exception as e:
        logging.error(f"DB connection failed: {e}", exc_info=True)
        return False

if __name__ == "__main__":
    if test_db_connection():
        print("Database connection is OK!")
    else:
        print("Database connection failed!")