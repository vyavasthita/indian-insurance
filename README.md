# indian-insurance
Backend for Indian Insurance Company
This has been implemented using Flask.

# Python Version
3.10.6

# Testing Platform

1. OS - Ubuntu 22.04
2. Docker Compose version v2.17.3
3. Docker version 23.0.6

# Webserver
gunicorn
Gunicorn configuration is found under apps/config/gunicorn_conf.py

# Sending email
Ref: https://mailtrap.io/blog/flask-email-sending/

# Assumptions
- I have supported 'content-type' with 'application/json' only.
- Registration mail like is valid for configurable number of seconds.
- For blacklisted emails, we are sending https status code 422 with message
  saying "Email Validation Failed. You are not allowed to create an account with us."
- Insurance Plan is NOT pre populated in DB, So user can use any new name for it. Also
  insurance plan name is not unique in DB.
- Validation for Indian Currency is not done because any insurance amount is valid amount
  due to denominations of Rs 1 & 2. 

# DB Schema
1. User
    id, integer, PK
    customer_name, string(40), not null
    customer_name, string(40), not null
    email_address, string(60), indexed, unique, not null
    password, string(100), unique, not null

2. User
    id, integer, PK
    activated, bool, not null, default=False
    
    FK - User.id

3. InsurancePlan
    id, integer, PK
    insurance_plan_name, string(200), not null
    
4. Insurance
    id, integer, PK
    insured_amount, integer, not null
    
    FK - User.id, InsurancePlan.id

5. Blacklist
    id, integer, PK
    email_address, string(60), indexed, unique, not null
    reason, string(100), null

## Best Practices followed
01. Production web server gunicorn
02. Normalized DB Schema
03. Python Logging - Console and File
04. Hashing of generated password
05. Use of exception handling
06. Proper HTTP status codes
07. Doc string added for all modules and methods
08. Type annotations are added for all methods.
09. Docker with docker compose used. Both Sqlite and production db mysql is used.
10. Use of environment variables.
11. Unit tests with coverage report
12. Detailed README file.
13. Proper git commit messages. Every commit is done post completing a functionality.
14. Pep8 naming convention for modules, classes, methods, functions and variables.
15. Comments added wherever required.
16. Use of sqlalchemy transaction for rollback if failure.
17. Use of Makefile to each in using the application.
18. Manual steps are minimal while testing the app.
19. Proper directory and file structure of source code.
20. Import statements are in order.
    - Python core -> flask -> flask third party -> application modules

    Also related modules are imported in order.

# Extras Done
1. App is deployed live on https://indian-insurance.onrender.com/api/user/register
2. An blacklist url is provided 

# Validations Done
1. Not a Json Format
2. Invalid Json Format
3. Extra attribute is passed in request.
4. Required attribute is not passed in request.
5. Customer Name attribute has more than 2 spaces.
6. Customer Name attribute's is greator than 50 characters.
7. Email address is in invalid format.
8. Email attribute's is greator than 50 characters.
9. Insurance plan name is more than 200 characters.
10. Insured Amount is more than 50000
11. Data type validation for json body
12. Blacklisted email
13. Duplicated email during registration are validated.

# Testing
- This app is tested on Ubuntu 22.04 LTS.
- Automated unit tests have been written using pytest.
- Automated Unit test coverage is 42%.

# Python Packages Used
- flask
- flask-sqlalchemy
- flask-migrate
- flask-wtf
- flask-mail
- gunicorn
- flask-cors
- pytest
- pytest-cov
- email-validator
- python-dotenv

# HTTP Status code used
- HTTP_200_OK = 200
- HTTP_201_CREATED = 201
- HTTP_400_BAD_REQUEST = 400
- HTTP_404_NOT_FOUND = 404
- HTTP_422_UNPROCESSABLE_ENTITY = 422
- HTTP_500_INTERNAL_SERVER_ERROR = 500

# Improvements Required, To Do
Some improvements are required, these are intentionly not done due to time constraints.

1. Sending email takes little time, this requires debugging.
    Or we need to use some background task using Celery/RQ.

2. Use supervisor if required to restart the app automatically post some error in application.

3. API documentation using swagger

4. Serialization - I did not use any serialization library like marshmallow. I just used simple python dict with flask jsonify().

5. CORS for all domain is enable. Later we need to make it configurable for particular domains.

6. Different configurations for differnent environments like Dev, test, QA, Production.

7. Separate requirements.txt file for different environments or use poetry.

8. Some of the responses sent to client are more of a developer use. While client should only see generic message.

9. More automated unit tests need to be written specially for db crud operations and also by using mocking.

10. Unit test coverage should improve.

11. Use custome error handlers for invalid endpoints (404, 500 status codes)

# Pending
Some of the endpoints should be accessed once user is signed up, this is not yet done

## How to Test

1. Clone the repo
2. Checkout branch 'development'
3. Go to root directory 'indian-insurance'.

I have used 'www.gmail.com' with some tweaks to emails.

# Blacklisting if email

I have created an API endpoint for marking emails as blacklisted. 
This is to avoid manual addition of email in database.

Go to browser and hit url -> <domain>/api/user/blacklist

Type: POST

content-type: multipart/form-data

URL: <domain>/api/user/blacklist

Json Payload:

{
  "email_address": "<Email>",
  "reason": ""
}

# Option 1 (Live environment without any configuration)
This application is deployed to 'https://render.com/'.

1. Use Postman or any other client for API testing
    - For customer registration use the following Payload for Post request.

    Type: POST

    URL: https://indian-insurance.onrender.com/api/user/register

    Json Payload:

    {
        "customer_name": "<Customer Name>",
        "email_address": "<Email>",
        "insurance_plan_name": "<Insurance Plan Name>",
        "insured_amount": <Insurance Amount>
    }

2. My Email Credentials are deployed to above environment.
   Hence you will receive email while using the above live environment.

# Option 2 (Without Docker and With Sqlite DB)

Use a Ubuntu OS

1. Create Virtual Environment
    - python3 -m venv venv

2. Activate Virtual Environment
    - source venv/bin/activate

3. Go to directory 
    - cd backend

4. To use sqlite, export following environment variable
    - export FLASK_ENV=development

5. Create .env file
    - in the same backend directory, create a env file
    - touch .env
    - Copy the contents in .env file shared via email

6. Install Packages
    - pip install -r requirements.txt

7. Run The Flask App
    ./entrypoint.sh

8. Use Postman or any other client for API testing
    - For customer registration use the following Payload for Post request.

    Type: POST

    URL: http://127.0.0.1:5000/api/user/register

    Json Payload:

    {
        "customer_name": "<Customer Name>",
        "email_address": "<Email>",
        "insurance_plan_name": "<Insurance Plan Name>",
        "insured_amount": <Insurance Amount>
    }

9. To Run unit tests
    - pytest -v

10. To Run unit tests coverage
    - pytest --cov

11. We need to update backend/.env file with email credentials we are going to use.
    MAIL_USERNAME=<Your email>
    MAIL_PASSWORD=<app password>

    Here if we use normal password, gmail will not athorize it. Google has completely blocke this.
    Now we need to use 'app password'. Refere below page for this.

    https://myaccount.google.com/lesssecureapps

# Option 3 (With Docker and With MySql DB)

Prerequisites; -

Docker and Docker compose must be installed.

1. Go to directory 
    - cd backend

2. Create .env file
    - in the same backend directory, create a env file
    - touch .env
    - Copy the contents in .env file shared via email

3. Go back to root directory 'indian-insurance'
    cd ..

4. Run following command 
    - make run

    This will start 3 docker containers.
    a) Flask App
    b) MySql DB
    c) Phpmyadmin

5. Use Postman or any other client for API testing
    - For customer registration use the following Payload for Post request.

    Type: POST

    URL: http://127.0.0.1:5000/api/user/register

    Json Payload:
    
    {
        "customer_name": "<Customer Name>",
        "email_address": "<Email>",
        "insurance_plan_name": "<Insurance Plan Name>",
        "insured_amount": <Insurance Amount>
    }

6. To access MySql db, use phpmyadmin.
    URL: http://127.0.0.1:8080

    database: indianinsurance

7. To Run unit tests
    - docker exec backend pytest -v

8. To Run unit tests coverage
    - docker exec backend pytest --cov

9. To stop the containers
    - make stop

10. We need to update backend/.env file with email credentials we are going to use.

    MAIL_USERNAME=<Your email>
    MAIL_PASSWORD=<app password>

    Here if we use normal password, gmail will not athorize it. Google has completely blocke this.
    Now we need to use 'app password'. Refere below page for this.

    https://myaccount.google.com/lesssecureapps
