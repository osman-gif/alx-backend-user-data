#!/usr/bin/env python3
"""
Creates a Flask app that has a single GET route ("/")
"""

import flask
from flask import jsonify, make_response, abort, request, redirect, Response
from auth import Auth
from sqlalchemy.orm.exc import NoResultFound

AUTH = Auth()

app = flask.Flask(__name__)


@app.route('/')
def home():
    """
    defines a route to display a message to users
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users():
    """
    end-point to register a user. Define a users function that implements
    the POST /users route.
    """
    password = request.form.get('password')
    email = request.form.get('email')

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": "{email}", "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """
    A function to respond to the POST /sessions route.
    The request is expected to contain form data with "email" and a
    "password" fields.
    If the login information is incorrect, use flask.abort to respond
    with a 401 HTTP status.
    Otherwise, create a new session for the user, store it the session
    ID as a cookie with key "session_id" on the response and return a
    JSON payload of the form
    {"email": "<user email>", "message": "logged in"}

    """
    email = request.form.get('email')
    password = request.form('password')

    valid_user = AUTH.valid_login(email=email, password=password)
    if valid_user:
        session_id = AUTH.create_session(email=email)
        if session_id is not None:
            response = make_response()
            response.set_cookie('session_id', session_id)
            return jsonify(
                {"email": "{email}", "message": "logged in"}), response
    else:
        return abort(401)


@app.route('/session', methods=['DELETE'])
def logout():
    """
     function to respond to the DELETE /sessions route.
     The request is expected to contain the session ID as a cookie with key
     "session_id".
     Find the user with the requested session ID. If the user exists destroy
     the session and redirect the user to GET /.

     If the user does not exist,
     respond with a 403 HTTP status.
    """

    session_id = request.cookies.get('session_id')
    try:
        user = AUTH._db.find_user_by(session_id=session_id)
        if user is not None:
            AUTH.destroy_session(user.id)
            redirect('/')
    except NoResultFound:
        return Response.status_code(403)


@app.route('/profile')
def profile():
    """
    function to respond to the GET /profile route.
    The request is expected to contain a session_id cookie. Use it to find
    the user. If the user exist, respond with a 200 HTTP status and the
    following JSON payload:
    {"email": "<user email>"}

    If the session ID is invalid or the user does not exist, respond with
    a 403 HTTP status.
    """

    session_id = request.cookies.get('session_id')
    try:
        user = AUTH._db.find_user_by(session_id=session_id)
        return jsonify({"email": "{user.email}"}), 200
    except NoResultFound:
        return 403


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    email = request.form.get('email')
    try:
        user = AUTH._db.find_user_by(email=email)
        token = AUTH.get_reset_password_token(email=email)
        return jsonify({"email": "{email}", "reset_token": "{token}"}), 400
    except NoResultFound:
        return 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
