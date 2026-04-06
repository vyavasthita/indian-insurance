# indian-insurance
Backend for Indian Insurance Company
This has been implemented using Flask.

# Python Version
3.10.6

# Testing Platform

1. OS - Ubuntu 22.04
2. Docker Compose version v2.17.3
3. Docker version 23.0.6

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
- celery
- redis
- flask-restx

# Webserver
gunicorn
Gunicorn configuration is found under apps/config/gunicorn_conf.py

# Sending email
Ref: https://mailtrap.io/blog/flask-email-sending/ and gmail.

Note: Along with sending email, email template is also stored locally as a file.

Verification email file -> ./backend/verification_email.txt
Email email file -> ./backend/welcome_email.txt

# Celery Worker
celery -A wsgi.celery worker --pool=solo --loglevel=info

# Source Code Folder Structure

```bash
|-- LICENSE
|-- Makefile
|-- README.md
|-- backend
|   |-- Dockerfile
|   |-- apps
|   |   |-- __init__.py
|   |   |-- config
|   |   |   |-- config.py
|   |   |   |-- gunicorn_conf.py
|   |   |   `-- logging.conf
|   |   |-- templates
|   |   |   `-- base.html
|   |   `-- user
|   |       |-- dao.py
|   |       |-- data_validation.py
|   |       |-- errors.py
|   |       |-- forms.py
|   |       |-- models.py
|   |       |-- routes.py
|   |       |-- schema_validation.py
|   |       `-- templates
|   |           `-- user
|   |               |-- blacklist.html
|   |               |-- home.html
|   |               |-- register.html
|   |               |-- verification.html
|   |               `-- welcome.html
|   |-- entrypoint.sh
|   |-- migrations
|   |   |-- README
|   |   |-- alembic.ini
|   |   |-- env.py
|   |   |-- script.py.mako
|   |   `-- versions
|   |       |-- 2326888c8dad_.py
|   |       |-- 61cd9afb9169_recreating_migrations_due_to_sqlite_.py
|   |       `-- 6a275c9c288c_update_userprofile_model.py
|   |-- requirements.txt
|   |-- tests
|   |   |-- __init__.py
|   |   |-- conftest.py
|   |   |-- functional
|   |   |   `-- __init__.py
|   |   |-- pytest.ini
|   |   |-- sample_test_schema
|   |   |   |-- invalid_json.csv
|   |   |   `-- not_supported_content_types.csv
|   |   `-- unit
|   |       |-- __init__.py
|   |       `-- user
|   |           |-- __init__.py
|   |           `-- test_post.py
|   |-- utils
|   |   |-- __init__.py
|   |   |-- email.py
|   |   |-- http_status.py
|   |   |-- insurance_logger.py
|   |   |-- password_helper.py
|   |   |-- security.py
|   |   |-- token.py
|   |   `-- validation.py
|   `-- wsgi.py
|-- database
|   `-- init.sql
`-- docker-compose.yaml
```

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

# Best Practices followed
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
21. Sending Email is done by using background tasks using Celery, RabbitMQ, Redis.
22. Different configurations for differnent environments like Dev, test, QA, Production.
23. API documentation using swagger

# Extras Done
1. App is deployed live on https://indian-insurance.onrender.com/api/user/register
2. A blacklist api endpoint is provided. See below. 

# Validations Done
01. Not a Json Format
02. Invalid Json Format
03. Extra attribute is passed in request.
04. Required attribute is not passed in request.
05. Customer Name attribute has more than 2 spaces.
06. Customer Name attribute's is greator than 50 characters.
07. Email address is in invalid format.
08. Email attribute's is greator than 50 characters.
09. Insurance plan name is more than 200 characters.
10. Insured Amount is more than 50000
11. Data type validation for json body
12. Blacklisted email
13. Duplicated email during registration are validated.

# Testing
- This app is tested on Ubuntu 22.04 LTS.
- Automated unit tests have been written using pytest.
- Automated Unit test coverage is 42%.

# HTTP Status code used
- HTTP_200_OK = 200
- HTTP_201_CREATED = 201
- HTTP_400_BAD_REQUEST = 400
- HTTP_404_NOT_FOUND = 404
- HTTP_422_UNPROCESSABLE_ENTITY = 422
- HTTP_500_INTERNAL_SERVER_ERROR = 500

## How to Test

1. Clone the repo
2. Checkout branch 'development'
3. Go to root directory 'indian-insurance'.

I have used 'www.gmail.com' with some tweaks to emails.

# Webserver
gunicorn
Gunicorn configuration is found under apps/config/gunicorn_conf.py

# Assumption Made
'Content-Type' header value must be 'application/json' otherwise exception will be raised.
# Validations Done
1. Invalid POST request
    Request -> Invalid Json
    Response -> 400 Status Code with error message
