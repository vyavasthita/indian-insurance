from flask.blueprints import Blueprint
from flask import render_template
from apps.user.models import User


user_blueprint = Blueprint(name='user', import_name=__name__, template_folder='templates/user')


@user_blueprint.route("/register", methods = ['GET', 'POST'])
def register():
    """
    This is the user registration api endpoint.
    This lets a user sign up with basic details.

    Returns:
        response: Status code and message in Json format
    """
    return render_template('register.html')
