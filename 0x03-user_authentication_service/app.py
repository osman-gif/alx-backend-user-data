#!/usr/bin/env python3
"""
Creates a Flask app that has a single GET route ("/")
"""

import flask
from flask import jsonify
from auth import Auth


AUTH = Auth()

app = flask.Flask(__name__)


@app.route('/')
def home():
    """
    defines a route to display a message to users
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users(email, password):
    """
    defines a route to reqister users
    """
    try:
        AUTH.register_user(email, password)
        return jsonify({"email":"{email}", "message": "user created"})
    except ValueError:
        return jsonify({"message":"email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
