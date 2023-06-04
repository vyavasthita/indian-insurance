"""To send email

SENECA GLOBAL CONFIDENTIAL & PROPRIETARY

@file email.py
@author Dilip Kumar Sharma
@copyright Seneca Global
@date 3rd Jun 2023

About; -
--------
    Module for sending email.

Working; -
----------
    This modules sends email to given receipients.
    This module uses 'flask-mail' module to send email.

Uses; -
-------
    This module is used by routes module to send email.

Reference; -
------------
    https://mailtrap.io/blog/flask-email-sending/
"""

from flask_mail import Message
from apps import mail, configuration


def send_email(to: str, subject: str, template: str) -> tuple:
    """To send email

    Args:
        to (str): Receipient of the email
        subject (str): Subject of the email
        template (str): Template/content of the email

    Returns:
        tuple: status, message, result
                status is boolean value indicating success (True) or Failure(False),
                message is a string about the error occurred if any, otherwise None,
                result is the actual response received or None otherwise.
    """
    try:
        msg = Message(
            subject,
            recipients=[to],
            html=template,
            sender=configuration.MAIL_DEFAULT_SENDER
        )
        mail.send(msg)
    except Exception as err:
        print(f"Failed to send email. To {to}, sender {configuration.MAIL_DEFAULT_SENDER}.")
        return False, "Failed to send email.", None
    
    # Success/failure, Message, Result
    return True, None, None