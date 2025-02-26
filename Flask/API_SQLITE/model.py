# API/model.py
import sqlite3
import flask
import pathlib
from API import app

# Path to your actual SQLite DB file
# You could also store this in app.config if you prefer
DB_FILENAME = pathlib.Path(__file__).resolve().parent / "API.sqlite3"

def get_db():
    """Open a new database connection if none exists for the current context."""
    if 'sqlite_db' not in flask.g:
        # Connect to the DB file; you can set additional flags/PRAGMA as needed
        flask.g.sqlite_db = sqlite3.connect(DB_FILENAME)
        # Return rows as dictionaries (optional):
        flask.g.sqlite_db.row_factory = sqlite3.Row
    return flask.g.sqlite_db

@app.teardown_appcontext
def close_db(exception):
    """Close the database at the end of each request."""
    db = flask.g.pop('sqlite_db', None)
    if db is not None:
        db.close()