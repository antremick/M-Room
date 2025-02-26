# File: run.py
from API import app
from API.db_setup import create_tables

if __name__ == "__main__":
    # Manually push an app context
    with app.app_context():
        create_tables()  # Runs ONCE, before the server starts

    app.run(debug=True)