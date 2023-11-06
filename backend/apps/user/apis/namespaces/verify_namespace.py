import json
import os
from celery.result import AsyncResult
from flask import render_template, request, jsonify, url_for
from flask_restx import Resource, Namespace, fields
from apps.user.dao import UserInsuranceDao, UserDao
from apps import configuration
from apps.user.schema_validation import validate_schema
from apps.user.data_validation import validate_data
from apps import celery
from utils.password_helper import PasswordGenerator
from utils.token import TokenHelper
from utils.email import send_email
from utils.http_status import HttpStatus
from utils.insurance_logger import InsuranceLogger


verify_ns = Namespace('verify', description='Verification related operations')

verify_api_request_model = verify_ns.model(
    'Verify Registration', 
    {
        'customer_name': fields.String(
                required=True, 
                description='Name of Customer', 
                example="Customer 1",
                min_length=3,
                max_length=40,
        ),
        'email_address': fields.String(
                required=True, 
                description='Email of Customer', 
                example="user@senecaglobal.com", 
                min_length=10,
                max_length=40,
        ),
        'insurance_plan_name': fields.String(
                required=True, 
                description='Insurance Plan Name', 
                example="Family",
                min_length=4,
                max_length=20,
        ),
        'insured_amount': fields.Integer(
                required=True, 
                description='Insured Amount', 
                example=300000,
                max=5000000,
        ),
    },
)

verify_post_response_model_400 = verify_ns.model(
    "VerifyPostResponseModel400",
    {
        "message": fields.String(
            required=True,
            description="Response message from API for invalid request",
            example="Input payload validation failed",
        )
    },
)

verify_post_response_model_400 = verify_ns.model(
    "VerifyPostResponseModel400",
    {
        "message": fields.String(
            required=True,
            description="Response message from API for invalid request",
            example="Input payload validation failed",
        )
    },
)

@verify_ns.route('/')
class Verify(Resource):
    """
    This is the user registration api endpoint.
    This lets a user sign up with basic details.

    Returns:
        response: Status code and message in Json format
    """
    # GET
    @verify_ns.response(
        code=HttpStatus.HTTP_200_OK,
        description="Sign Up is successful",
    )
    @verify_ns.response(
        code=HttpStatus.HTTP_400_BAD_REQUEST,
        description="Validation Error",
        model=verify_post_response_model_400,
    )
    def get(self, token):
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

        celery.send_task('email.send', (configuration.MAIL_DEFAULT_SENDER, email, subject, html_template))
        
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