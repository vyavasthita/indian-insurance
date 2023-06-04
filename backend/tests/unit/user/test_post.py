import json
import pytest


def not_supported_content_types():
    for ct in [("text/html", 400), ("multipart/form-data", 400), ("x-www-form-urlencoded", 400)]:
        yield ct

def invalid_jsons():
    data = [
        (
        '{ "customer_name": Customer 1", "email_address": "user1@gmail.com", "insurance_plan_name": "Abc", "insured_amount": 300000}', 
        400
        ), 
        (
        '{ "customer_name": "Customer 1", "email_address": "user1@gmail.com" "insurance_plan_name": "Abc", "insured_amount": 300000}', 
        400
        ), 
    ]

    for j in data:
        yield j

def test_index(app, client):
    response = client.get('/user/home')
    assert response.status_code == 200

def json_of_request(json_dict):
    return json.dumps(json_dict)

def json_of_response(response):
    """Decode json from response"""
    return json.loads(response.data.decode('utf8'))

@pytest.mark.schema_validation
@pytest.mark.parametrize("content_type, expected_status_code", not_supported_content_types())
def test_content_type_not_json(client, content_type, expected_status_code):
    url = '/user/register'

    mimetype = content_type
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    data = {
            "customer_name":"Customer 1",
            "email_address": "customer1@gmail.com",
            "insurance_plan_name": "Family",
            "insured_amount": 300000
        }
    
    response = client.post(url, data=json_of_request(data), headers=headers)

    assert response.status_code == expected_status_code

    assert json_of_response(response) == { 
                "status": "VALIDATION-ERROR", 
                "reason": "content-type {} is not supported. Expected content type is 'application/json'".format(content_type)
            }

@pytest.mark.schema_validation
@pytest.mark.parametrize("payload, expected_status_code", invalid_jsons())
def test_invalid_json_payload(client, payload, expected_status_code):
    url = '/user/register'

    mimetype = 'application/json'

    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    
    response = client.post(url, data=payload, headers=headers)

    assert response.status_code == expected_status_code