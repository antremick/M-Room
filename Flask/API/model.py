# File: API/model.py
import os
import flask
import psycopg2
import psycopg2.extras
from API import app

def get_db():
    """
    Open a new PostgreSQL database connection if none exists
    for the current Flask request context.
    """
    if 'pg_conn' not in flask.g:
        # Heroku provides DATABASE_URL, e.g. "postgres://user:pass@host:port/dbname"
        db_url = os.environ['DATABASE_URL']  
        
        # Connect using a dict cursor so rows behave somewhat like SQLite row_factory
        conn = psycopg2.connect(db_url, cursor_factory=psycopg2.extras.DictCursor)
        
        # Store in flask.g for this request
        flask.g.pg_conn = conn
    return flask.g.pg_conn

@app.teardown_appcontext
def close_db(exception):
    """
    Close the PostgreSQL connection at the end of each request, if open.
    """
    pg_conn = flask.g.pop('pg_conn', None)
    if pg_conn is not None:
        pg_conn.close()