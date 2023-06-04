"""Password generator helper

SENECA GLOBAL CONFIDENTIAL & PROPRIETARY

@file password_helper.py
@author Dilip Kumar Sharma
@copyright Seneca Global
@date 2nd Jun 2023

About; -
--------
    Module for generating random password.

Working; -
----------
    This modules uses random module to generate password.

Uses; -
-------
    This module is used by routes module to generate password for user registration.

Reference; -
------------
    TBD
"""

import random
import string


class PasswordGenerator:
    def __init__(self, length: int) -> None:
        self._length = length
        self._lower = string.ascii_lowercase
        self._upper = string.ascii_uppercase
        self._num = string.digits
        self._symbols = string.punctuation

    def generate_password(self) -> str:
        """Generates random password

        Returns:
            str: Generated password
        """
        all = self._lower + self._upper + self._num + self._symbols

        return "".join(random.sample(all, self._length))



