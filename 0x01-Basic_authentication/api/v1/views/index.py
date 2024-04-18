#!/usr/bin/env python3
"""
Module of Index views containing API endpoint views.
"""
from flask import jsonify, abort
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """
    Retrieve the status of the API.

    Returns:
        str: A JSON response containing the status of the API.
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """
    Retrieve statistics about the objects in the system.

    Returns:
        str: A JSON response containing the number of each object type.
    """
    from models.user import User
    stats = {}
    stats['users'] = User.count()
    return jsonify(stats)


@app_views.route('/unauthorized', methods=['GET'], strict_slashes=False)
def not_authorized() -> str:
    """
    Handle unauthorized access.

    Returns:
        str: An error message indicating unauthorized access.
    """
    abort(401)


@app_views.route('/forbidden', methods=['GET'], strict_slashes=False)
def not_allowed() -> str:
    """
    Handle forbidden access.

    Returns:
        str: An error message indicating forbidden access.
    """
    abort(403)
