#!/usr/bin/env python3
"""
This module defines a basic Flask app with a single GET route.
"""

from flask import Flask, request, jsonify
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/')
def welcome():
    """
    Endpoint to return a welcome message as JSON.

    Returns:
        dict: A JSON payload with a welcome message.
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def register_user():
    """
    Endpoint to register a user.

    Expects form data fields: "email" and "password".

    Returns:
        dict: A JSON payload indicating success
        or failure of user registration.
    """
    try:
        email = request.form.get('email')
        password = request.form.get('password')

        if AUTH.register_user(email, password):
            return jsonify({"email": email, "message": "user created"}), 200
        else:
            return jsonify({"message": "email already registered"}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 400


@app.route('/sessions', methods=['DELETE'])
def logout():
    """
    The end-point to logout an authenticated user
    """
    session_id = request.cookies.get("session_id")

    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)

    AUTH.destroy_session(user.id)

    return redirect('/')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
