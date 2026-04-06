"""Password Hashing module

SENECA GLOBAL CONFIDENTIAL & PROPRIETARY

@file security.py
@author Dilip Kumar Sharma
@copyright Seneca Global
@date 4th Jun 2023

About; -
--------
    Module for hashing given password

Working; -
----------
    This modules generates and validates password

Uses; -
-------
    This module is used by dao module to generate password hash during user registration.
    This module could also be used to verify password hash during user login.

Reference; -
------------
    TBD
"""

from werkzeug.security import generate_password_hash, check_password_hash


def get_hashed_password(password: str) -> str:
    """Go generate password hash

    Args:
        password (str): Password to be hashed

    Returns:
        str: Generated hashed password
    """
    return generate_password_hash(password=password)

def validate_password_hash(password: str, hashed_password: str) -> str:
    """Check whether or not the password is correct.

    Args:
        password (str): Password to be validated
        hashed_password (str): Hashed password to check against

    Returns:
        str: _description_
    """
    return check_password_hash(hashed_password, password=password)