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


def _hash_password(password: str):
    """
    hashes a password
    """
    import bcrypt

    hashed = bcrypt.hashpw(bytes(password, encoding='utf-8'),
                           bcrypt.gensalt(12))
    return hashed
