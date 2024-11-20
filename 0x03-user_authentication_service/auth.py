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
        add a new user:
        if user with that email already exist:
        raise Value error with a message
        if not, add the user and return it
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
        generate a uuid
        """
        import uuid
        return str(uuid.UUID())


def _hash_password(password: str):
    """
    hashes a password
    """
    import bcrypt

    hashed = bcrypt.hashpw(bytes(password, encoding='utf-8'),
                           bcrypt.gensalt(12))
    return hashed
