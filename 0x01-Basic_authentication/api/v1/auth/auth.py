#!usr/bin/env python3
"""
defines a class that is the template for all authentication system
you will implement.
"""


from flask import request
from typing import List, TypeVar
import flask


class Auth:

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ if path is part of the excluded_paths False
        """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True

        if not path.endswith('/'):
            path = path+'/'

        if path in excluded_paths:
            return False
        else:
            return True

    def authorization_header(self, request=None) -> str:
        """ authorization_header
        """
        if request is None:
            return None
        if 'Authorization' not in list(request.headers.keys()):
            return None
        else:
            return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ current_user
        """
        return None
