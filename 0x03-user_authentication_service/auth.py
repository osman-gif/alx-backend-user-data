#!/usr/bin/env python3
"""
defines Auth class
"""
from db import DB
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email, password):
        """
        A method that take mandatory email and password string arguments
        and return a User object.

        If a user already exist with the passed email, raise a ValueError
        with the message User <user's email> already exists.
        If not, hash the password with _hash_password, save the user to
        the database using self._db and return the User object.
        """

        user = None
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError("User {email} already exists")

        except NoResultFound:
            hpwd = _hash_password(password)
            self._db.add_user(email, hpwd)
            return user

    def valid_login(self, email, password):
        """
        checks if user exist, if true check if
        password and user hashed password are
        identical, if so retun true else retun
        false
        """
        import bcrypt
        try:
            user = self._db.find_user_by(email=email)
            user = bcrypt.checkpw(password=password,
                                  hashed_password=user.hashed_password)
            if user is True:
                return True
            else:
                return False

        except NoResultFound:
            return False

    def _generate_uuid(self):
        """
        return a string representation of a new UUID. Use the uuid module.
        """
        import uuid

        return repr(uuid.uuid4())

    def create_session(self, email):
        """
        Takes an email string argument and returns the session ID as a
        string.

        The method should find the user corresponding to the email,
        generate a new UUID and store it in the database as the user’s
        session_id, then return the session ID.
        """
        try:
            user = self.find_user_by(email=email)
            session_id = self._generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id):
        """
        A method taht takes a single session_id string argument and
        returns the corresponding User or None.

        If the session ID is None or no user is found, return None.
        Otherwise return the corresponding user.
        """
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id):
        """
        The method takes a single user_id integer argument and returns None.

        The method updates the corresponding user’s session ID to None.
        """
        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user_id, session_id=None)
        except NoResultFound:
            return None
        return None

    def get_reset_password_token(self, email):
        """
        function to respond to the POST /reset_password route.
        The request is expected to contain form data with the "email" field.

        If the email is not registered, respond with a 403 status code.
        Otherwise, generate a token and respond with a 200 HTTP status and
        the following JSON payload:
        {"email": "<user email>", "reset_token": "<reset token>"}

        """
        try:
            user = self._db.find_user_by(email=email)
            token = self._generate_uuid()
            self.db.update_user(user.id, reset_token=token)
            return token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token, password):
        """
        method. It takes reset_token string argument and a password string
        argument and returns None.
        Use the reset_token to find the corresponding user. If it does not
        exist, raise a ValueError exception.
        Otherwise, hash the password and update the user’s hashed_password
        field with the new hashed password and the reset_token field to None.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashpwd = _hash_password(password=password)
            self._db.update_user(user.id, hashed_password=hashpwd,
                                 reset_token=None)
        except NoResultFound:
            raise ValueError


def _hash_password(password: str):
    """
    A method that takes in a password string arguments
    and returns bytes.

    The returned bytes is a salted hash of the input password, hashed with
    bcrypt.hashpw.
    """
    import bcrypt

    hashed = bcrypt.hashpw(bytes(password, encoding='utf-8'),
                           bcrypt.gensalt(12))
    return hashed
