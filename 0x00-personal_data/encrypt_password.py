#!/usr/bin/env python3
"""
 Encrypting passwords
"""

import bcrypt

def hash_password(password: str) -> bytes:
    """
    Hashes the given password using bcrypt with a salt.

    Args:
    password: A string representing the plain-text password.

    Returns:
    A byte string representing the salted, hashed password.
    """
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

