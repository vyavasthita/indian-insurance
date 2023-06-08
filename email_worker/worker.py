"""To send email

SENECA GLOBAL CONFIDENTIAL & PROPRIETARY

@file email.py
@author Dilip Kumar Sharma
@copyright Seneca Global
@date 7th Jun 2023

About; -
--------
    Module for sending email.

Working; -
----------
    This module sends email to given receipients.
    This module uses 'flask-mail' module to send email.

Uses; -
-------
    This module is used by routes module to send email.

Reference; -
------------
    https://mailtrap.io/blog/flask-email-sending/
"""

import os
from celery import Celery


CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL'),
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND')


app = Celery('email', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)


@app.task(name='email.send')
def send_email(sender: str, to: str, subject: str, template: str) -> tuple:
    """To send email

    Args:
        sender (str): Sender of the email
        to (str): Receipient of the email
        subject (str): Subject of the email
        template (str): Template/content of the email

    Returns:
        tuple: status, message, result
                status is boolean value indicating success (True) or Failure(False),
                message is a string about the error occurred if any, otherwise None,
                result is the actual response received or None otherwise.
    """
    print("Sending Email...")
    print(f"Sender {sender}, Receiver {to}, Subject {subject}")
    print("*******************************************************")
    
    # Success/failure, Message, Result
    return True, None, None
