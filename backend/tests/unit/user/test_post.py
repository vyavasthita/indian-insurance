import os
import json
import csv
import pytest

test_schema_dir = "tests/sample_test_schema"
not_supported_json_file_name = os.path.join(test_schema_dir, "not_supported_content_types.csv")
invalid_json_file_name = os.path.join(test_schema_dir, "invalid_json.csv")

def read_test_data_from_csv(file_name):
    with open(file_name, newline="") as csvfile:
        data = csv.reader(csvfile, delimiter=",")
        next(data)  # skip header row

        return [[row[0], int(row[1])] for row in data if row]

def test_index(app, client):
    response = client.get('/user/home')
    assert response.status_code == 200

def json_of_request(json_dict):
    return json.dumps(json_dict)

def json_of_response(response):
    """Decode json from response"""
    return json.loads(response.data.decode('utf8'))

@pytest.mark.schema_validation
@pytest.mark.parametrize("content_type, expected_status_code", read_test_data_from_csv(not_supported_json_file_name))
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
@pytest.mark.parametrize("payload, expected_status_code", read_test_data_from_csv(invalid_json_file_name))
def test_invalid_json_payload(client, payload, expected_status_code):
    url = '/user/register'

    mimetype = 'application/json'

    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    
    response = client.post(url, data=payload, headers=headers)

    assert response.status_code == expected_status_code

    assert json_of_response(response) == { 
                "status": "VALIDATION-ERROR", 
                "reason": "Invalid Json Format"
            }