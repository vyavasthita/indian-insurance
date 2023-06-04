"""User blueprint for API requests.

SENECA GLOBAL CONFIDENTIAL & PROPRIETARY

@file routes.py
@author Dilip Kumar Sharma
@copyright Seneca Global
@date 2nd Jun 2023

About; -
--------
    Blueprint for api requests.

Working; -
----------
    All api requests for user are received by this module.

Uses; -
-------
    API requests are handled by this module.

Reference; -
------------
    TBD
"""

import json
import os
from functools import wraps
from flask.blueprints import Blueprint
from flask import render_template, request, jsonify, redirect, url_for
from apps.user.dao import UserInsuranceDao, BlacklistDao, UserProfileDao, UserDao
from apps import configuration, db
from apps.user.schema_validation import validate_schema
from apps.user.data_validation import validate_data
from utils.password_helper import PasswordGenerator
from utils.token import TokenHelper
from utils.email import send_email
from utils.http_status import HttpStatus
from utils.insurance_logger import InsuranceLogger


user_blueprint = Blueprint(name='user', import_name=__name__, 
                           template_folder='templates/user',
                           url_prefix='/user'
                )

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

@user_blueprint.route("/home", methods = ['GET'])
def home():
    """
    This is the user home.
    This page is shown when user opens the url first.

    Returns:
        response: Status code and message in Json format
    """
    return render_template('home.html')

@user_blueprint.route("/register", methods = ['POST'])
@validate_schema
@validate_data
@check_blacklisting
@is_already_registered
def register():
    """
    This is the user registration api endpoint.
    This lets a user sign up with basic details.

    Returns:
        response: Status code and message in Json format
    """
    input_data = json.loads(request.data.decode('utf-8'))
    
    customer_name = input_data['customer_name']
    email_address = input_data['email_address']
    insurance_plan_name = input_data['insurance_plan_name']
    insured_amount = input_data['insured_amount']

    InsuranceLogger.log_debug(
        f"Received user registration with Customer Name {customer_name}, Email Address {email_address}, Insurance Plan Name {insurance_plan_name}, Insured Amount {insured_amount}."
    )

    InsuranceLogger.log_info(f"Verifying if customer with email id {email_address} is already registered.")

    # Customer has passed all validations, now proceed with customer
    InsuranceLogger.log_info(f"Generating random password.")

    password_generator = PasswordGenerator(configuration.PASSWORD_LENGTH)
    is_success, message, password = password_generator.generate_password()

    if not is_success:
        return {
                    "status": "INTERNAL-SERVER-ERROR",
                    "reason": message
                }, HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR
    
    is_success, message, user_insurance = UserInsuranceDao.add_user_insurance(
        customer_name = customer_name,
        email_address = email_address,
        password = password,
        insurance_plan_name = insurance_plan_name,
        insured_amount = insured_amount
    )

    if not is_success:
        return {
                    "status": "INTERNAL-SERVER-ERROR",
                    "reason": message
                }, HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR
    
    # User is created, now generate email token for the user
    token_helper = TokenHelper()

    InsuranceLogger.log_info(f"Generating confirmation token.")
    is_success, message, token = token_helper.generate_confirmation_token(email=email_address)

    if not is_success:
        return {
                    "status": "INTERNAL-SERVER-ERROR",
                    "reason": message
                }, HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR
    
    confirm_url = url_for('user.confirm_user', token=token, _external=True)

    html_template = render_template(
            'verification.html', 
            customer_name = customer_name, 
            email_address = email_address,
            password = password,
            confirm_url=confirm_url
        )

    subject = "Please verify your email"

    InsuranceLogger.log_info(f"Sending email to {email_address}.")

    is_success, message, result = send_email(email_address, subject, html_template)

    if not is_success:
        return {
                    "status": "INTERNAL-SERVER-ERROR",
                    "reason": message
                }, HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR
    
    # Also write mail template to text file temporarily, this should be removed later
    file_path = os.path.abspath(os.path.dirname(__name__))
    file_name = os.path.join(file_path, 'verification_email.txt')

    InsuranceLogger.log_debug(f"Writing verification email template to file {file_name}.")
    with open(file=file_name, mode='w') as f:
        f.write(html_template)

    new_user = dict()

    new_user['Customer Name'] = user_insurance.user.customer_name
    new_user['Email Address'] = email_address
    new_user['Insurance Plan'] = user_insurance.insurance_plan.insurance_plan_name
    new_user['Insurance Amount'] = user_insurance.insured_amount

    InsuranceLogger.log_debug(
        f"Returning response for newly registered user. {new_user}"
    )

    return jsonify(new_user), HttpStatus.HTTP_201_CREATED
    
    # return {
    #             "status": "Success",
    #             "reason": "Thanks for the registration. You will soon receive a verification email on your email '{}'. Please verify the email to activate your account.".format(email_address)
    #         }, HttpStatus.HTTP_201_CREATED

@user_blueprint.route('/confirm/<token>')
def confirm_user(token):
    token_helper = TokenHelper()

    InsuranceLogger.log_info(
        f"validating the confirmation token."
    )

    is_success, message, email = token_helper.validate_token(token)

    if not is_success:
        return {
                    "status": "VERIFICATION-EXPIRED",
                    "reason": message
                }, HttpStatus.HTTP_404_NOT_FOUND
    
    InsuranceLogger.log_info(
        f"Token is valid and not expired. Decoded email is {email}."
    )

    """
    Token is valid and not expired. And we have retreived the decoded email
    """
    # Find the user using his email id from User DB table

    InsuranceLogger.log_info(f"Searching user with email id {email} in User DB table.")
    is_success, message, user = UserDao.get_user_by_email(email_address=email)

    if not is_success:
        return {
                    "status": "INTERNAL-SERVER-ERROR",
                    "reason": message
                }, HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR
    elif user is None:
        InsuranceLogger.log_error(f"User with Email {email} is not found.")
        return {
                    "status": "INVALID-USER",
                    "reason": "User with Email '{}' is not found.".format(email)
                }, HttpStatus.HTTP_404_NOT_FOUND
    
    InsuranceLogger.log_info(f"User with email {email} is found in User DB table, now update user activation status.")
    # User is found in User DB table, now update user activation status
    
    InsuranceLogger.log_info(f"Checking if User with email {email} is already activated.")

    if user.userprofiles.activated:
        # As user is already activated, so no need to update database, just return the status to user
        InsuranceLogger.log_info(f"User with email id {email} is already activated.")
        return {
                    "status": "ALREADY-ACTIVATED",
                    "reason": "User with Email '{}' is already activated.".format(email)
                }, HttpStatus.HTTP_200_OK

    # Now we need to update activation status of given user in database
    is_success, message, result = UserDao.update_profile_by_activation(
        user=user, 
        activated=True
    )

    if not is_success:
        InsuranceLogger.log_error(f"Failed to update activation status for user with {email}.")
        return {
                    "status": "INTERNAL-SERVER-ERROR",
                    "reason": "Activation for email id '{}' failed due to server error.".format(email)
                }, HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR
    
    InsuranceLogger.log_info(f"Activation status for user with {email} is successfully done.")

    # Now we need to send Welcome email post successful registration

    html_template = render_template('welcome.html', customer_name=user.customer_name)

    subject = "Welcome to Indian Insurance"

    is_success, message, result = send_email(email, subject, html_template)

    if not is_success:
        return {
                    "status": "INTERNAL-SERVER-ERROR",
                    "reason": message
                }, HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR
    
    InsuranceLogger.log_info(f"Registration for user with {email} is successfully done. Welcome email is sent to user.")

    # Also write mail template to text file temporarily, this should be removed later
    file_path = os.path.abspath(os.path.dirname(__name__))
    file_name = os.path.join(file_path, 'welcome_email.txt')

    InsuranceLogger.log_debug(f"Writing welcome email template to file {file_name}.")

    with open(file=file_name, mode='w') as f:
        f.write(html_template)

    return {
                "status": "Success",
                "reason": "Thanks for the registration. You will soon receive a welcome email on your email '{}'.".format(email)
            }, HttpStatus.HTTP_200_OK

