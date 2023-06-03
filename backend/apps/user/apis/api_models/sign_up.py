from flask_restx import fields
from apps.user.apis.namespaces.sign_up_namespace import sign_up_ns


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
                min_length=1,
                max_length=2,
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
