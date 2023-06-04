"""To do validation

SENECA GLOBAL CONFIDENTIAL & PROPRIETARY

@file validation.py
@author Dilip Kumar Sharma
@copyright Seneca Global
@date 4th Jun 2023

About; -
--------
    Module do to general validations.

Working; -
----------
    This module uses email-validator package to validate email format

Uses; -
-------
    This module is used by schema validation for validating email format

Reference; -
------------
    https://pypi.org/project/email-validator/
"""

from email_validator import validate_email, EmailNotValidError


def check_valid_email(email: str) -> bool:
    """To validate

    Args:
        email (str): Email id to be validated

    Returns:
        bool: Valid or invalid email format
    """
    if len(email) > 50:
        return False, "Email too long with '{}' characters. Max '{}' characters are allowed.".format(len(email), 50)

    try:
        # Validating the `email`
        emailObject = validate_email(email)

        # If the `email` is valid
        # it is updated with its normalized form
        email = emailObject.email
    except EmailNotValidError as errorMsg:
        # If `email` is not valid
        # we print a human readable error messages
        return False, str(errorMsg)
    
    return True, email
