import json
from flask.blueprints import Blueprint
from flask import render_template, request, jsonify, flash, redirect, url_for
from apps.user.dao import UserInsuranceDao, BlacklistDao, UserProfileDao, UserDao
from apps import configuration
from utils.password_helper import PasswordGenerator
from utils.token import TokenHelper
from utils.email import send_email


user_blueprint = Blueprint(name='user', import_name=__name__, 
                           template_folder='templates/user',
                           url_prefix='/user'
                )


def check_blacklisting(func):
    def wrapper(*args, **kwargs):
        input_data = json.loads(request.data.decode('utf-8'))

        if BlacklistDao.get_blacklist_by_email(email_address = input_data['email_address']):
            return {'VALIDATION-ERROR': 'Email Validation Failed. You are not allowed to create an account with us.'}, 422
        
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
@check_blacklisting
def register():
    """
    This is the user registration api endpoint.
    This lets a user sign up with basic details.

    Returns:
        response: Status code and message in Json format
    """
    print("Register method is called...")
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
    token_helper = TokenHelper()
    token = token_helper.generate_confirmation_token(email=email_address)

    confirm_url = url_for('user.confirm_user', token=token, _external=True)

    html_template = render_template('verification.html', confirm_url=confirm_url)

    subject = "Please verify your email"
    print(f"token {token}")
    send_email(email_address, subject, html_template)

    flash('Please check your email. A verification email has been sent to you.', 'success')

    return jsonify({'msg': 'some value'})

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

@user_blueprint.route('/confirm/<token>')
def confirm_user(token):
    token_helper = TokenHelper()
    email = None

    try:
        email = token_helper.validate_token(token)
    except:
        print(f"Email confirmation link is invalid or has expired.")
        flash('Email confirmation link is invalid or has expired.', 'danger')
        return {'Error': 'Email confirmation link is invalid or has expired'}, 404
        # To Do: Send response here
    """
    Token is valid and not expired. And we have retreived the decoded email
    """
    # Find the user using his email id from User DB table
    user = UserDao.get_user_by_email(email_address=email)

    if user:
        print(f"User found is {user}")
        # Now search User in UserProfile DB table by passing FK user
        user_profile = UserProfileDao.get_profile_by_user(user=user)

        if user_profile.activated:
            print(f"User with email id {email} is already activated.")
            flash('Given email ID is already verified.', 'success')
        else:
            UserProfileDao.update_profile_by_activation(
                user_profile=user_profile, 
                activated=True
            )
            
            flash('Email is successfully verified. Thanks!', 'success')
    else:
        print(f"Account with {email} not found")
        flash(f"Account with {email} not found", "danger")

    return redirect(url_for('user.post_verification'))