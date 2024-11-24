#!/usr/bin/env python3
"""
defines Auth class
"""
from db import DB
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import User


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
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

    def valid_login(self, email: str, password: str) -> bool:
        """
        In this task, you will implement the Auth.valid_login method.
        It should expect email and password required arguments and return a
        boolean.
        Try locating the user by email. If it exists, check the password with
        bcrypt.checkpw.
        If it matches return True. In any other case, return False
        """
        import bcrypt

        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """
        Takes an email string argument and returns the session ID as a
        string.

        The method should find the user corresponding to the email,
        generate a new UUID and store it in the database as the user’s
        session_id, then return the session ID.
        """
        session_id = _generate_uuid()
        try:
            user = self._db.find_user_by(email=email)
            self._db.update_user(user.id, session_id=session_id)
            self._db._session.commit()
            return session_id
        except NoResultFound:
            return session_id

    def get_user_from_session_id(self, session_id: str) -> str:
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

    def destroy_session(self, user_id: int) -> None:
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

    def get_reset_password_token(self, email: str) -> str:
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
            token = _generate_uuid()
            self.db.update_user(user.id, reset_token=token)
            return token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
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


def _hash_password(password: str) -> bytes:
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


def _generate_uuid() -> str:
    """
    In this task you will implement a _generate_uuid function in
    the auth module.
    The function should return a string representation
    of a new UUID. Use the uuid module.

    Note that the method is private to the auth module and should NOT be
    used outside of it.
    """
    import uuid

    return str(uuid.uuid4())
