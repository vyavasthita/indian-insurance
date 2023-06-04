"""Flask App Configuration.

SENECA GLOBAL CONFIDENTIAL & PROPRIETARY

@file config.py
@author Dilip Kumar Sharma
@copyright Seneca Global
@date 3rd Jun 2023

About; -
--------
    It is responsible for setting all configurations required for flask app.

Working; -
----------
    This configuration class is initialized at the time of creating flask app.

Uses; -
-------
    All other python modules can use this class for accessing configurations.

Reference; -
------------
    TBD
"""

import os
import ast
from dotenv import load_dotenv


# The root directory where the sqlite db file is created.
base_dir = os.path.abspath(os.path.dirname(__name__))


load_dotenv() # to load .env file. .flaskenv file is automatically loaded without using load_dotenv()


class Config:
    # To be used by Flask Form (WTF package)
    FLASK_ENV = os.getenv('FLASK_ENV')

    SECRET_KEY = os.getenv('SECRET_KEY')
    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT')

    EMAIL_TOKEN_EXPIRATION = ast.literal_eval(os.getenv('EMAIL_TOKEN_EXPIRATION'))

    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
    
    MYSQL_USER = os.getenv('MYSQL_USER')
    MYSQL_HOST = os.getenv('MYSQL_HOST')
    MYSQL_DB = os.getenv('MYSQL_DB')
    MYSQL_PORT = os.getenv('MYSQL_PORT')

    # USE_SQLITE = os.getenv('USE_SQLITE', default = False)

    if FLASK_ENV == 'development':
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'insurance.db')
    else:
        # DATABASE url to be connected by the app
        SQLALCHEMY_DATABASE_URI = "mysql://" + MYSQL_USER + ":" + "@" + MYSQL_HOST + ":" + MYSQL_PORT + "/" + MYSQL_DB
        
    # We do not want to track the modifications done in the DB.
    SQLALCHEMY_TRACK_MODIFICATIONS = ast.literal_eval(os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', default = False))
    
    # The length of the randomely generated password
    PASSWORD_LENGTH = ast.literal_eval(os.getenv('PASSWORD_LENGTH'))

    # Configuration file for logging
    LOG_CONFIG_FILE = os.getenv('LOG_CONFIG_FILE') or './apps/config/logging.conf'

    # Directory where logs will be generated.
    LOGS_DIR = os.getenv('LOGS_DIR') or '/tmp/insurance_logs'

    # Log File name
    LOG_FILE_NAME = os.getenv('LOG_FILE_NAME') or 'insurance.log'

    # mail settings
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = ast.literal_eval(os.getenv('MAIL_PORT'))
    MAIL_USE_TLS = ast.literal_eval(os.getenv('MAIL_USE_TLS'))
    MAIL_USE_SSL = ast.literal_eval(os.getenv('MAIL_USE_SSL'))

    # Email authentication
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
