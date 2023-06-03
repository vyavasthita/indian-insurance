# indian-insurance
Backend for Indian Insurance Company

# Python Version
3.10.8

# Python Packages Used
flask
flask-sqlalchemy
flask-migrate
flask-wtf
flask-mail
gunicorn

# HTTP Status code used
422 : If customer email address is blacklisted

# Done
Functions and method type annotations is written wherever possible.
Docstrings added.
While inserting data to multiple tables during sign up, sqlalchemy transaction is used. So either all records are inserted or none.
Email verification expiration time is configurable.
Comments were added wherever possible.
If any exception occurred while connecting to DB then 500 status code with message will be returned to client.

# Pending
Some of the endpoints should be accessed once user is signed up, this is not yet done

# Sending email
Ref: https://mailtrap.io/blog/flask-email-sending/

# Webserver
gunicorn
Gunicorn configuration is found under apps/config/gunicorn_conf.py

# Validations Done
1. Not a Json Format
2. Invalid Json Format
3. Extra attribute is passed in request.
4. Required attribute is not passed in request.
5. Customer Name attribute has more than 2 spaces.
6. Insurance plan name is more than 200 characters.
7. Insured Amount is more than 50000
8. Data type validation for json body
9. Blacklisted email

# Assumptions
For blacklisted emails, we are sending https status code 422 with message
saying "Email Validation Failed. You are not allowed to create an account with us."