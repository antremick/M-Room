# API/__init__.py
import flask

app = flask.Flask(__name__)     # The central Flask app

# Load configuration if needed:
# app.config['SECRET_KEY'] = 'replace_with_real_secret'

import API.model           # So model.py can hook up 'get_db()'
import API.routes             # So routes.py can register routes