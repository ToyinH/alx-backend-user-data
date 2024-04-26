#!/usr/bin/env python3
"""
This module defines a basic Flask app with a single GET route.
"""

from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def welcome():
    """
    Endpoint to return a welcome message as JSON.
    
    Returns:
        dict: A JSON payload with a welcome message.
    """
    return jsonify({"message": "Bienvenue"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
