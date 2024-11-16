#!/usr/bin/env python3
"""
new view for Session Authentication
"""

from flask import request, jsonify, abort
from models.user import User
from api.v1.views import Blueprint

app_views = Blueprint('app_views', __name__)


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """ POST /auth_session/login
    """

    email = request.form.get('email')
    password = request.form.get('password')

    if email is None or email == "":
        return jsonify({"error": "email missing"}), 400
    if password is None or password == "":
        return jsonify({"error": "password missing"}), 400

    users = User.search({'email': email})

    if users == [] or users is None:
        return jsonify({"error": "no user found for this email"}), 404

    for user in users:
        if not user.is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401
        if user.email == email:
            from api.v1.app import auth
            import os
            session_id = auth.create_session(user.id)
            response = jsonify(user.to_json())
            session_name = os.getenv('SESSION_NAME')
            response.set_cookie(session_name, session_id)
            return response


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def logout():
    """ DELETE /auth_session/logout
    """
    from api.v1.app import auth
    if auth.destroy_session(request) is False:
        abort(403)
    return jsonify({}), 200
