#!/usr/bin/env python3
"""
Module handling routes for the API.
"""

from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None

if getenv("AUTH_TYPE") == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()

if getenv("AUTH_TYPE") == "auth":
    from api.v1.auth.auth import Auth
    auth = Auth()


@app.before_request
def before_request() -> str:
    """
    Executes before processing a request.
    """
    if auth is None:
        return
    excluded_paths = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/'
    ]
    if auth.require_auth(request.path, excluded_paths):
        if auth.authorization_header(request) is None:
            abort(401)

        # Assigning current user to request
        request.current_user = auth.current_user(request)
        if auth.current_user(request) is None:
            abort(403)


@app.errorhandler(404)
def not_found(error) -> str:
    """
    Handles 404 errors.
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def not_authorized(error) -> str:
    """
    Handles 401 errors.
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def not_allowed(error) -> str:
    """
    Handles 403 errors.
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    """
    Main function to run the application.
    """
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
