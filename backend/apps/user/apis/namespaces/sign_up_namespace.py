import json
import os
from celery.result import AsyncResult
from flask import render_template, request, jsonify, url_for
from flask_restx import Resource, Namespace, fields
from apps.user.dao import UserInsuranceDao
from apps import configuration
from apps.user.schema_validation import validate_schema
from apps.user.data_validation import validate_data, check_blacklisting, is_already_registered
from apps import celery
from utils.password_helper import PasswordGenerator
from utils.token import TokenHelper
from utils.email import send_email
from utils.http_status import HttpStatus
from utils.insurance_logger import InsuranceLogger




sign_up_ns = Namespace('register', description='Sign Up related operations')

sign_up_api_request_model = sign_up_ns.model(
    'Sign Up', 
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

sign_up_post_response_model_400 = sign_up_ns.model(
    "SignUpPostResponseModel400",
    {
        "message": fields.String(
            required=True,
            description="Response message from API for invalid request",
            example="Input payload validation failed",
        )
    },
)

@sign_up_ns.route('/')
class User(Resource):
    """
    This is the user registration api endpoint.
    This lets a user sign up with basic details.

    Returns:
        response: Status code and message in Json format
    """
    # POST
    
    @sign_up_ns.expect(sign_up_api_request_model, validate=True)
    @sign_up_ns.response(
        code=HttpStatus.HTTP_201_CREATED,
        description="Sign Up is successful",
    )
    @sign_up_ns.response(
        code=HttpStatus.HTTP_400_BAD_REQUEST,
        description="Validation Error",
        model=sign_up_post_response_model_400,
    )
    @validate_schema
    @validate_data
    @check_blacklisting
    @is_already_registered
    def post(self):
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
        
        confirm_url = url_for('user.verify', token=token, _external=True)

        html_template = render_template(
                'verification.html', 
                customer_name = customer_name, 
                email_address = email_address,
                password = password,
                confirm_url=confirm_url
            )

        subject = "Please verify your email"

        InsuranceLogger.log_info(f"Sending email to {email_address}.")

        celery.send_task('email.send', (configuration.MAIL_DEFAULT_SENDER, email_address, subject, html_template))

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
