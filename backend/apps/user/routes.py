from flask.blueprints import Blueprint
from flask import render_template, redirect, url_for
from apps.user.forms import UserRegistrationForm
from apps.user.dao import InsuranceDBDao


user_blueprint = Blueprint(name='user', import_name=__name__, 
                           template_folder='templates/user',
                           url_prefix='/user'
                )


@user_blueprint.route("/home", methods = ['GET'])
def home():
    """
    This is the user home.
    This page is shown when user opens the url first.

    Returns:
        response: Status code and message in Json format
    """
    return render_template('home.html')

@user_blueprint.route("/register", methods = ['GET', 'POST'])
def register():
    """
    This is the user registration api endpoint.
    This lets a user sign up with basic details.

    Returns:
        response: Status code and message in Json format
    """
    form = UserRegistrationForm()
    password = "something" # to be randomly generated

    if form.validate_on_submit():
        customer_name = form.customer_name.data
        email_address = form.email_address.data
        insurance_plan_name = form.insurance_plan_name.data
        insured_amount = form.insured_amount.data

        insurance_info = InsuranceDBDao.add_user_insurance(
            customer_name = customer_name,
            email_address = email_address,
            password = password,
            insurance_plan_name = insurance_plan_name,
            insured_amount = insured_amount            
        )

        return redirect(url_for('user.post_registration'))

    return render_template('register.html', form = form)

@user_blueprint.route("/post_registration", methods = ['GET'])
def post_registration():
    """
    This is the post user registration api endpoint.
    Post successfull registration, use is redirected to this page.

    Returns:
        response: Status code and message in Json format
    """
    return render_template('post_registration.html')