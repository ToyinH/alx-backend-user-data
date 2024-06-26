#!/usr/bin/env python3
"""
auth module
"""
from bcrypt import hashpw, gensalt, checkpw
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing import Union


def _hash_password(password: str) -> bytes:
    """
    Hash a password using bcrypt

    Args:
        password (str): The password to hash

    Returns:
        bytes: Salted hash of the input password
    """

    salted = gensalt()

    hashed_input_password = hashpw(password.encode('utf-8'), salted)

    return hashed_input_password


def _generate_uuid() -> str:
    """
    The function that return a string representation of a new UUID.
    """
    return str(uuid4())


class Auth:
    """
    Auth class to interact with the authentication database.
    """

    def _init_(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user

        Args:
            email (str): Email of the user
            password (str): Password of the user

        Returns:
            User: The newly registered User object

        Raises:
            ValueError: If a user already exists with the provided email
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Login validation
        """
        try:
            user = self._db.find_user_by(email=email)

            hashed_password = user.hashed_password

            pass_check = checkpw(password.encode('utf-8'), hashed_password)

            return pass_check
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """
        The Method that create a session with the user email
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            pass

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """
        Get User from session ID method

        Args:
            session_id (str): Session ID of the user

        Returns:
            User:
                The corresponding User object if session ID is valid
        """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        This method updates the corresponding user’s session ID to None

        Args:
            user_id (int): User ID of the user

        Returns:
            None
        """
        self._db.update_user(user_id, session_id=None)
