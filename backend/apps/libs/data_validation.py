import json
from flask import request


def validate_customer_name(customer_name):
    max_spaces_allowed = 2

    if customer_name.count(" ") > max_spaces_allowed:
        return False, "Max '{}' spaces are allowed.".format(max_spaces_allowed)
    
    return True, None

def validate_insurance_plan_name(insurance_plan_name):
    if len(insurance_plan_name) > 200:
        return False, "Max length should be '{}'.".format(200)

    return True, None

def is_insured_amount_valid_inr(insured_amount):
    return True, None # TBD

def validate_insured_amount(insured_amount):
    if insured_amount > 5000000:
        return False, "Max value should be '{}'.".format(5000000)
    
    return is_insured_amount_valid_inr(insured_amount)

def validate_data(func):
    def wrapper(*args, **kwargs):
        input_data = json.loads(request.data.decode('utf-8'))
        
        valid, message = validate_customer_name(input_data['customer_name'])

        if not valid:
            return {
                        "status": "VALIDATION-ERROR",
                        "reason": "Invalid Data in 'customer_name' attribute. {}".format(message)
                    }, 400
        
        valid, message = validate_insurance_plan_name(input_data['insurance_plan_name'])

        if not valid:
            return {
                        "status": "VALIDATION-ERROR",
                        "reason": "Invalid Data. {}".format(message)
                    }, 400
        
        valid, message = validate_insured_amount(input_data['insured_amount'])

        if not valid:
            return {
                        "status": "VALIDATION-ERROR",
                        "reason": "Invalid Data. {}".format(message)
                    }, 400

        return func(*args, **kwargs)
    return wrapper