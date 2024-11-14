#!/usr/bin/env python3
"""
Defines a class Basic_auth that inherits from
class Auth from /api/v1/auth
"""

from typing import Tuple, TypeVar
from api.v1.auth.auth import Auth
from base64 import b64decode
from models.user import User


class BasicAuth(Auth):
    """
    Basic_auth
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        returns the Base64 part of the Authorization header for a
        Basic Authentication
        """
        if authorization_header is None:
            return None
        if type(authorization_header) != str:
            return None
        if not authorization_header.startswith('Basic '):
            return None
        else:
            return authorization_header.split(' ')[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ returns the decoded value of a Base64 string
        base64_authorization_header
        """

        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) != str:
            return None
        try:
            b64decode(base64_authorization_header)
        except ValueError:
            return None

        return b64decode(base64_authorization_header).decode('utf-8')

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """ returns the user email and password from the Base64 decoded value
        decoded_base64_authorization_header
        """

        if decoded_base64_authorization_header is None:
            return None, None
        if type(decoded_base64_authorization_header) != str:
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None

        return tuple(decoded_base64_authorization_header.split(':'))

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """ returns the User instance based on his email and password
        """
        if user_email is None or type(user_email) != str:
            return None
        if user_pwd is None or type(user_pwd) != str:
            return None
        users = User.search({'email': user_email})
        if users is None or users == []:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ current_user
        """
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None
        base64_auth_header = self.extract_base64_authorization_header(
            auth_header)
        if base64_auth_header is None:
            return None
        decoded_base64_auth_header = self.decode_base64_authorization_header(
            base64_auth_header)
        if decoded_base64_auth_header is None:
            return None
        user_email, user_pwd = self.extract_user_credentials(
            decoded_base64_auth_header)
        if user_email is None or user_pwd is None:
            return None
        return self.user_object_from_credentials(user_email, user_pwd)
