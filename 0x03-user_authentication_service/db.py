#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str):
        """
        method, which has two required string arguments: email and
        hashed_password, and returns a User object.
        The method should save the user to the database
        """
        from user import User
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs):
        """
        This method takes in arbitrary keyword arguments and returns the
        first row found in the users table as filtered by the method’s input
        arguments. No validation of input arguments required at this point.
        """

        from user import User

        user = None
        keys = list(kwargs.keys())
        user_dict_keys = list(User.__dict__.keys())

        for key in keys:
            if key not in user_dict_keys:
                raise InvalidRequestError

        user = self._session.query(User).filter_by(**kwargs).first()

        if user is None:
            raise NoResultFound

        return user

    def update_user(self, user_id, **kwargs):
        """
        method that takes as argument a required user_id integer and arbitrary
        keyword arguments, and returns None.
        The method will use find_user_by to locate the user to update, then
        will update the user’s attributes as passed in the method’s arguments
        then commit changes to the database.

        If an argument that does not correspond to a user attribute is passed,
        raise a ValueError.
        """

        from user import User

        user = self.find_user_by(id=user_id)

        self._session.query(User).filter_by(id=user.id).update(kwargs)

        return None
