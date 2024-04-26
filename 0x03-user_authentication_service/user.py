#!/usr/bin/env python3
"""
This module defines the SQLAlchemy model for the User table.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    """
    SQLAlchemy model representing the User table.

    Attributes:
        id (int): The integer primary key.
        email (str): A non-nullable string representing the email address of the user.
        hashed_password (str): A non-nullable string representing the hashed password of the user.
        session_id (str): A nullable string representing the session ID of the user.
        reset_token (str): A nullable string representing the reset token of the user.
    """

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    session_id = Column(String, nullable=True)
    reset_token = Column(String, nullable=True)
