import json
from flask import request
from flask_restx import Namespace, Resource, fields
from flask import render_template, request, flash, redirect, url_for, jsonify
from werkzeug.exceptions import BadRequest
from apps.user.dao import UserInsuranceDao, BlacklistDao, UserProfileDao, UserDao
from apps import configuration
from apps.user.apis.namespaces import sign_up_ns
from apps.user.apis.api_models.sign_up import *
from utils.password_helper import PasswordGenerator
from utils.token import TokenHelper
from utils.email import send_email


@sign_up_ns.route('/')
@sign_up_ns.expect(sign_up_api_request_model, validate=True)
@sign_up_ns.response(
    code=201,
    description="Sign Up is successful",
)
@sign_up_ns.response(
    code=400,
    description="Validation Error",
    model=sign_up_post_response_model_400,
)
class User(Resource):
    """
    This is the user registration api endpoint.
    This lets a user sign up with basic details.

    Returns:
        response: Status code and message in Json format
    """
    # POST
    def post(self):
        if request.headers.get("Content-Type") != "application/json":
            return {
                "message": "Content-Type not supported!"
            }, 400
        
        request_json = request.get_json()
        
        input_data = None

        content_type = request.headers.get('Content-Type')

        if content_type == 'application/json':
            input_data = json.loads(request.data.decode('utf-8'))
        else:
            return {"Error": 'Content type is not supported.'}
        
        customer_name = input_data['customer_name']
        email_address = input_data['email_address']
        insurance_plan_name = input_data['insurance_plan_name']
        insured_amount = input_data['insured_amount']

        password_generator = PasswordGenerator(configuration.PASSWORD_LENGTH)
        
        password = password_generator.generate_password()

        insurance_info = UserInsuranceDao.add_user_insurance(
            customer_name = customer_name,
            email_address = email_address,
            password = password,
            insurance_plan_name = insurance_plan_name,
            insured_amount = insured_amount
        )

        # User is created, now generate email token for the user
        # token_helper = TokenHelper()
        # token = token_helper.generate_confirmation_token(email=email_address)

        # confirm_url = url_for('user.confirm_user', token=token, _external=True)

        # html_template = render_template('verification.html', confirm_url=confirm_url)

        # subject = "Please verify your email"
        # # send_email(email_address, subject, html_template)

        # flash('Please check your email. A verification email has been sent to you.', 'success')

        return {'Msg': 'Done'}, 200