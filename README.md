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

# Pending
Some of the endpoints should be accessed once user is signed up, this is not yet done

# Sending email
Ref: https://mailtrap.io/blog/flask-email-sending/

# Webserver
gunicorn
Gunicorn configuration is found under apps/config/gunicorn_conf.py
