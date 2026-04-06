"""Data Validation for endpoints.

SENECA GLOBAL CONFIDENTIAL & PROPRIETARY

@file data_validation.py
@author Dilip Kumar Sharma
@copyright Seneca Global
@date 3rd Jun 2023

About; -
--------
    Data validation done for POST request.

Working; -
----------
    This module checks all parameter passed to post request and raises response and status
    code when payload is invalid.

Uses; -
-------
    This module is used as decorator by POST request endpoint.

Reference; -
------------
    TBD
"""

import json
from functools import wraps
from flask import request
from apps.user.dao import UserDao, UserInsuranceDao, BlacklistDao
from utils.http_status import HttpStatus
from utils.validation import check_valid_email
from utils.insurance_logger import InsuranceLogger


def validate_customer_name(customer_name: str) -> tuple:
    """Validate customer name

    Args:
        customer_name (str): Name of customer received in request

    Returns:
        tuple: bool for success/failure and message if any
    """
    max_spaces_allowed = 2 # To Do : Read from configuration
    space_count = customer_name.count(" ")

    if space_count > max_spaces_allowed:
        return False, "'{}' Spaces found. Max '{}' spaces are allowed.".format(space_count, max_spaces_allowed)
    
    if len(customer_name) > 50:
        return False, "Customer Name too long with '{}' characters. Max '{}' characters are allowed.".format(len(customer_name), 50)

    return True, None

def validate_insurance_plan_name(insurance_plan_name: str) -> tuple:
    """Validate insurance plan name

    Args:
        insurance_plan_name (str): Name of insurance plan received in request

    Returns:
        tuple: bool for success/failure and message if any
    """
    if len(insurance_plan_name) > 200:  # To Do : Read from configuration
        return False, "Max length should be '{}'.".format(200)

    return True, None

def is_insured_amount_valid_inr(insured_amount: int) -> tuple:
    """Validate insurance amount is valid INR

    Args:
        insured_amount (int): Insurance amount received in request

    Returns:
        tuple: bool for success/failure and message if any
    """
    return True, None # TBD

def validate_insured_amount(insured_amount: int) -> tuple:
    """Validate insurance amount is not beyond a limit.

    Args:
        insured_amount (int): Insurance amount received in request

    Returns:
        tuple: bool for success/failure and message if any
    """
    if insured_amount > 5000000:    # To Do : Read from configuration
        return False, "Max value should be '{}'.".format(5000000)
    
    return is_insured_amount_valid_inr(insured_amount)

def validate_data(func):
    """Validate data in api request.

    Args:
        func (_type_): A function object
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        input_data = json.loads(request.data.decode('utf-8'))
        
        valid, message = validate_customer_name(input_data['customer_name'])

        if not valid:
            return {
                        "status": "VALIDATION-ERROR",
                        "reason": "Invalid Data in 'customer_name' attribute. {}".format(message)
                    }, HttpStatus.HTTP_400_BAD_REQUEST
        
        InsuranceLogger.log_info(f"Validating email {input_data['email_address']}")

        valid, message = check_valid_email(input_data['email_address'])

        if not valid:
            InsuranceLogger.log_info(f"Invalid Email Address. {message}")

            return {
                        "status": "VALIDATION-ERROR",
                        "reason": "Invalid Email Address. {}".format(message)
                    }, HttpStatus.HTTP_400_BAD_REQUEST
        
        valid, message = validate_insurance_plan_name(input_data['insurance_plan_name'])

        if not valid:
            return {
                        "status": "VALIDATION-ERROR",
                        "reason": "Invalid Data. {}".format(message)
                    }, HttpStatus.HTTP_400_BAD_REQUEST
        
        valid, message = validate_insured_amount(input_data['insured_amount'])

        if not valid:
            return {
                        "status": "VALIDATION-ERROR",
                        "reason": "Invalid Data. {}".format(message)
                    }, HttpStatus.HTTP_400_BAD_REQUEST

        return func(*args, **kwargs)
    return wrapper


def check_blacklisting(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        input_data = json.loads(request.data.decode('utf-8'))

        InsuranceLogger.log_info(f"Checking blacklisting for user with email {input_data['email_address']}.")

        is_success, message, result = BlacklistDao.get_blacklist_by_email(
                                                    email_address = input_data['email_address']
                                                )
        if not is_success:
            return {
                        "status": "INTERNAL-SERVER-ERROR",
                        "reason": message
                    }, HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR
        elif result is not None:
            return {
                        "status": "VALIDATION-ERROR",
                        "reason": "Email Validation Failed. You are not allowed to create an account with us."
                    }, HttpStatus.HTTP_422_UNPROCESSABLE_ENTITY
        
        return func(*args, **kwargs)
    return wrapper

def is_already_registered(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        input_data = json.loads(request.data.decode('utf-8'))
        
        email_address = input_data['email_address']

        is_success, message, user = UserDao.get_user_by_email(email_address=email_address)

        if not is_success:
            return {
                        "status": "INTERNAL-SERVER-ERROR",
                        "reason": message
                    }, HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR
        elif user is not None:
            InsuranceLogger.log_info(f"User with Email {email_address} is already registered.")
            return {
                        "status": "VALIDATION-ERROR",
                        "reason": "User with Email '{}' is already registered.".format(email_address)
                    }, HttpStatus.HTTP_400_BAD_REQUEST

        return func(*args, **kwargs)
    
    return wrapper