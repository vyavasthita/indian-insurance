from flask.blueprints import Blueprint
from flask import render_template, redirect, url_for
from apps.user.models import User
from apps.user.forms import UserRegistrationForm
from apps.user.dao import user_dao


user_blueprint = Blueprint(name='user', import_name=__name__, template_folder='templates/user')


@user_blueprint.route("/register", methods = ['GET', 'POST'])
def register():
    """
    This is the user registration api endpoint.
    This lets a user sign up with basic details.

    Returns:
        response: Status code and message in Json format
    """
    form = UserRegistrationForm()

    if form.validate_on_submit():
        customer_name = form.customer_name.data
        email_address = form.email_address.data
        insurance_plan_name = form.insurance_plan_name.data
        insured_amount = form.insured_amount.data

        # Update database with new user
        user = user_dao.create_user(
            customer_name, 
            email_address, 
            insurance_plan_name, 
            insured_amount
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