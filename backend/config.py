import os
import ast


# The root directory where the sqlite db file is created.
base_dir = os.path.abspath(os.path.dirname(__name__))


class Config:
    FLASK_ENV = os.getenv('FLASK_ENV')
    # DEBUG = ast.literal_eval(os.getenv('DEBUG', default=True))  # Convert string to boolean

    # To be used by Flask Form (WTF package)
    SECRET_KEY = os.getenv('SECRET_KEY') or 'not really a secret'
    
    # DATABASE url to be connected by the app
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI') or 'sqlite:///' + os.path.join(base_dir, 'insurance.db')
    
    # We do not want to track the modifications done in the DB.
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', default = False)  # Convert string to boolean or False

    # The length of the randomely generated password
    PASSWORD_LENGTH = os.getenv('PASSWORD_LENGTH') or 10
