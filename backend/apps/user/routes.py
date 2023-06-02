from flask.blueprints import Blueprint
from flask import render_template, request, jsonify

from apps.user.dao import InsuranceDBDao, BlacklistDao
from utils.password_helper import PasswordGenerator
from apps import configuration
import json


user_blueprint = Blueprint(name='user', import_name=__name__, 
                           template_folder='templates/user',
                           url_prefix='/user'
                )


def check_blacklisting(func):
    def wrapper(*args, **kwargs):
        input_data = json.loads(request.data.decode('utf-8'))

        if BlacklistDao.get_blacklist_by_email(email_address = input_data['email_address']):
            return {'Error': 'You are not allowed to create an account with us.'}, 422
        
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

    insurance_info = InsuranceDBDao.add_user_insurance(
        customer_name = customer_name,
        email_address = email_address,
        password = password,
        insurance_plan_name = insurance_plan_name,
        insured_amount = insured_amount            
    )

    return jsonify({'msg': 'some value'})

@user_blueprint.route("/post_registration", methods = ['GET'])
def post_registration():
    """
    This is the post user registration api endpoint.
    Post successfull registration, use is redirected to this page.

    Returns:
        response: Status code and message in Json format
    """
    return render_template('post_registration.html')