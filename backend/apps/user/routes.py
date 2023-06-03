import json
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


user_blueprint = Blueprint(name='user', import_name=__name__, 
                           template_folder='templates/user',
                           url_prefix='/user'
                )

def check_blacklisting(func):
    def wrapper(*args, **kwargs):
        input_data = json.loads(request.data.decode('utf-8'))

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

    # Customer has passed all validations, now proceed with customer
    password_generator = PasswordGenerator(configuration.PASSWORD_LENGTH)
    password = password_generator.generate_password()

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
    is_success, message, token = token_helper.generate_confirmation_token(email=email_address)

    if not is_success:
        return {
                    "status": "INTERNAL-SERVER-ERROR",
                    "reason": message
                }, HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR
    
    confirm_url = url_for('user.confirm_user', token=token, _external=True)

    html_template = render_template('verification.html', confirm_url=confirm_url)

    subject = "Please verify your email"
    is_success, message, result = send_email(email_address, subject, html_template)

    if not is_success:
        return {
                    "status": "INTERNAL-SERVER-ERROR",
                    "reason": message
                }, HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR
    
    return {
                "status": "Success",
                "reason": "Thanks for the registration. You will soon receive a verification email on your email '{}'. Please verify the email to activate your account.".format(email_address)
            }, HttpStatus.HTTP_201_CREATED

@user_blueprint.route('/confirm/<token>')
def confirm_user(token):
    token_helper = TokenHelper()

    is_success, message, email = token_helper.validate_token(token)

    if not is_success:
        return {
                    "status": "VERIFICATION-EXPIRED",
                    "reason": message
                }, HttpStatus.HTTP_404_NOT_FOUND

    """
    Token is valid and not expired. And we have retreived the decoded email
    """
    # Find the user using his email id from User DB table
    print(f"Searching user with email id {email} in User DB table.")
    is_success, message, user = UserDao.get_user_by_email(email_address=email)

    if not is_success:
        return {
                    "status": "INTERNAL-SERVER-ERROR",
                    "reason": message
                }, HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR
    elif user is None:
        print(r"User with Email {email} is not found.")
        return {
                    "status": "INVALID-USER",
                    "reason": "User with Email '{}' is not found.".format(email)
                }, HttpStatus.HTTP_404_NOT_FOUND
    
    # User is found in User DB table
    # Now search User in UserProfile DB table by passing FK user
    is_success, message, user_profile = UserProfileDao.get_profile_by_user(user=user)

    if not is_success:
        return {
                    "status": "INTERNAL-SERVER-ERROR",
                    "reason": message
                }, HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR
    elif user_profile is None:
        print(r"User with Email {email} is not found.")
        return {
                    "status": "INVALID-USER",
                    "reason": "User with Email '{}' is not found.".format(email)
                }, HttpStatus.HTTP_404_NOT_FOUND
    
    print("User", user.id)
    print("Customer Profile id", user_profile.id)
    print("Customer Profile", user_profile.customerprofile)
    print("Customer Is activated", user_profile.activated, type(user_profile.activated))
    print("********************************************")
    
    if user_profile.activated:
        print(f"User with email id {email} is already activated.")
        return {
                    "status": "ALREADY-ACTIVATED",
                    "reason": "User with Email '{}' is already activated.".format(email)
                }, HttpStatus.HTTP_200_OK
    
    else:
        is_success, message, result = UserProfileDao.update_profile_by_activation(
            user_profile=user_profile, 
            activated=True
        )
        print('Email is successfully verified. Thanks!')


    return redirect(url_for('user.post_verification'))

@user_blueprint.route("/post_registration", methods = ['GET'])
def post_registration():
    """
    This is the post user registration api endpoint.
    Post successfull registration, user is redirected to this page.

    Returns:
        response: Status code and message in Json format
    """
    return render_template('post_registration.html')

@user_blueprint.route("/post_verification", methods = ['GET'])
def post_verification():
    """
    This is the post user verification api endpoint.
    Post successfull verification, user is redirected to this page.

    Returns:
        response: Status code and message in Json format
    """
    return render_template('post_verification.html')

