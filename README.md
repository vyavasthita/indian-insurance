# indian-insurance
Backend for Indian Insurance Company
This has been implemented using Flask.

# Python Version
3.10.6

# Webserver
gunicorn
Gunicorn configuration is found under apps/config/gunicorn_conf.py

# Sending email
Ref: https://mailtrap.io/blog/flask-email-sending/

# Assumptions
- I have supported 'content-type' with 'application/json' only.
- Blacklisted emails are manually inserted into Blacklist DB table.
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

# Highligts
- Gunicorn production web server is used.
- Python Logging is done for Console and File.
- Unit tests implemented. Coverage is 42%.
- Password is randomly generated and hashed before inserting into database.
- Functions and method type annotations is written wherever possible.
- Docstrings added.
- While inserting data to multiple tables during sign up, sqlalchemy transaction is used. So either all records are inserted or none.
- Email verification expiration time is configurable.
- Comments were added wherever possible.
- If any exception occurred while connecting to DB then 500 status code with message will be returned to client.
- I have added some HTML pages with Flask-Form package. Though it was not necessory, i just added for testing purpose.
- I have used SqlAlchemy DB session transaction using context manager to do rollback when
multiple commits happen and if one or more fails.
- All import statements are declared in order. 
    Also similiar modules are imported in order.
    Python core -> flask -> flask third party -> application modules

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
- Automated Unit test coverage is 43%.

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
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_400_BAD_REQUEST = 400
HTTP_404_NOT_FOUND = 404
HTTP_422_UNPROCESSABLE_ENTITY = 422
HTTP_500_INTERNAL_SERVER_ERROR = 500

# Improvements Required, To Do
Some improvements are required, these are intentionlly not done due to time constraints.

1. Sending email takes little time, this requires debugging.
    Or we need to use some background task using Celery/RQ.

2. Use supervisor if required to restart the app automatically post some error in application.

3. API documentation using swagger

4. Serialization - I did not use any serialization library like marshmallow. I just used simple python dict with flask jsonify().

5. - CORS for all domain is enable. Later we need to make it configurable for particular domains.

6. Different configurations for differnent environments like Dev, test, QA, Production.

7. Separate requirements.txt file for different environments or use of poetry.

8. Some of the responses sent to client are more of a developer use. While client should only see generic message.

9. Unit test coverage

# Pending
Some of the endpoints should be accessed once user is signed up, this is not yet done

# Note
Initially I have created flask form for sign up for testing purpose.
Relevant code and html still part of code. This could be deleted later.
