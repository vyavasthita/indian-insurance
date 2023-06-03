import os
import ast


# The root directory where the sqlite db file is created.
base_dir = os.path.abspath(os.path.dirname(__name__))


class Config:
    FLASK_ENV = os.getenv('FLASK_ENV', default='main.py')
    DEBUG = os.getenv('DEBUG', default=True)

    # To be used by Flask Form (WTF package)
    SECRET_KEY = os.getenv('SECRET_KEY') or 'not really a secret'

    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT') or 'security password salt'

    EMAIL_TOKEN_EXPIRATION = os.getenv('EMAIL_TOKEN_EXPIRATION') or 180 #  Seconds

    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
    
    # DATABASE url to be connected by the app
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI') or 'sqlite:///' + os.path.join(base_dir, 'insurance.db')
    
    # We do not want to track the modifications done in the DB.
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', default = False)  # Convert string to boolean or False

    # The length of the randomely generated password
    PASSWORD_LENGTH = os.getenv('PASSWORD_LENGTH') or 10

    # mail settings
    MAIL_SERVER = 'sandbox.smtp.mailtrap.io'
    MAIL_PORT = 2525
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

    # gmail authentication
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')

    # mail accounts
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')