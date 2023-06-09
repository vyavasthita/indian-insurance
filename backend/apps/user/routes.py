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
from flask.blueprints import Blueprint
from flask_restx import Api
from apps.user.apis.namespaces.blacklist_namespace import blacklist_ns
from apps.user.apis.namespaces.sign_up_namespace import sign_up_ns
from apps.user.apis.namespaces.verify_namespace import verify_ns

user_blueprint = Blueprint(name='api', import_name=__name__, 
                           template_folder='templates/user',
                           url_prefix='/api/user'
                )

api = Api(
            user_blueprint,
            title='Indian Insurance',
            version='1.0',
            description='Sign Up page for Indian Insurance'
        )

api.add_namespace(sign_up_ns)
api.add_namespace(blacklist_ns)
api.add_namespace(verify_ns)
