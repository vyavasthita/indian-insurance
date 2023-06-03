import json
from flask import request
from werkzeug.exceptions import BadRequest
from utils.http_status import HttpStatus


def is_content_type_json():
    content_type = request.headers.get('Content-Type')
    return content_type == 'application/json', content_type

def is_valid_json():
    try:
        request.json
    except BadRequest:
        return False
    
    return True
    
def validate_data_type():
    input_data = json.loads(request.data.decode('utf-8'))

    expected_attributes = {
        'customer_name' : str, 'email_address': str, 'insurance_plan_name': str, 'insured_amount': int
    }

    for attribute, value in input_data.items():
        if type(value) != expected_attributes[attribute]:
            return False, "Data type of attribute '{}' should be {}.".format(attribute, expected_attributes[attribute])

    return True, None

def is_expected_schema():
    expected_attributes = ['customer_name', 'email_address', 
                           'insurance_plan_name', 'insured_amount']

    actual_attributes = json.loads(request.data.decode('utf-8')).keys()

    for attribute in expected_attributes:
        if attribute not in actual_attributes:
            return False, "'{}' is a required attribute.".format(attribute)

    for attribute in actual_attributes:
        if attribute not in expected_attributes:
            return False, "Attribute '{}' is not expected.".format(attribute)

    return validate_data_type()

def validate_schema(func):
    def wrapper(*args, **kwargs):
        is_json, content_type = is_content_type_json()

        if not is_json:
            return { 
                        "status": "VALIDATION-ERROR", 
                        "reason": "content-type {} is not supported. Expected content type is 'application/json'".format(content_type)
                    }, HttpStatus.HTTP_400_BAD_REQUEST
        elif not is_valid_json():
            return {
                        "status": "VALIDATION-ERROR",
                        "reason": "Invalid Json Format"
                    }, HttpStatus.HTTP_400_BAD_REQUEST
        else:
            valid, message = is_expected_schema()
            if not valid:
                return {
                            "status": "VALIDATION-ERROR",
                            "reason": "Invalid Schema. {}".format(message)
                        }, HttpStatus.HTTP_400_BAD_REQUEST
        return func(*args, **kwargs)
    return wrapper