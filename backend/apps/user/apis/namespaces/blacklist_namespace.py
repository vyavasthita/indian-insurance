from flask import render_template
from flask_restx import Resource, fields, Namespace
from apps.user.forms import UserBlacklistForm
from apps.user.dao import BlacklistDao
from utils.insurance_logger import InsuranceLogger
from utils.http_status import HttpStatus


blacklist_ns = Namespace('blacklist', description='Blacklist email related operations')

blacklist_api_request_model = blacklist_ns.model(
    'Blacklist', 
    {
        'email_address': fields.String(
                required=True, 
                description='Email of Customer', 
                example="user@senecaglobal.com", 
                min_length=10,
                max_length=40,
        ),
        'reason': fields.String(
                required=False, 
                description='Reason for blacklisting', 
                example="Duplicate account with same attributes",
                min_length=10,
                max_length=50,
        ),
    },
)

blacklist_post_response_model_400 = blacklist_ns.model(
    "BlacklistPostResponseModel400",
    {
        "message": fields.String(
            required=True,
            description="Response message from API for invalid request",
            example="Input payload validation failed",
        )
    },
)

@blacklist_ns.route('/')
class Blacklist(Resource):
    """
    This is the user registration api endpoint.
    This lets a user sign up with basic details.

    Returns:
        response: Status code and message in Json format
    """
    # POST
    @blacklist_ns.expect(blacklist_api_request_model, validate=True)
    @blacklist_ns.response(
        code=HttpStatus.HTTP_200_OK,
        description="Blacklisting is successful",
    )
    @blacklist_ns.response(
        code=400,
        description="Validation Error",
        model=blacklist_post_response_model_400,
    )
    def post(self):
        """
        This is the blacklisting.
        This page is used by admin.

        Returns:
            response: Status code and message in Json format
        """
        form = UserBlacklistForm()

        if form.validate_on_submit():
            email_address = form.email_address.data
            reason = form.reason.data

            InsuranceLogger.log_info(f"Checking blacklisting for user with email {email_address}.")

            is_success, message, result = BlacklistDao.get_blacklist_by_email(
                                                        email_address = email_address
                                                    )
            if not is_success:
                return {
                            "status": "INTERNAL-SERVER-ERROR",
                            "reason": message
                        }, HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR
            elif result is not None:
                return {
                            "status": "Success",
                            "reason": "Email '{}' is already blacklisted.".format(email_address)
                        }, HttpStatus.HTTP_200_OK
            else:   # black list email
                is_success, message, result = BlacklistDao.add_blacklist(
                                                            email_address = email_address
                )
                if not is_success:
                    return {
                                "status": "INTERNAL-SERVER-ERROR",
                                "reason": message
                            }, HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR
                else:
                    return {
                                "status": "Success",
                                "reason": "Email '{}' is blacklisted successfully.".format(email_address)
                            }, HttpStatus.HTTP_200_OK
                
        return render_template('blacklist.html', form = form)
