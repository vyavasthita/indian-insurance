import os


# The root directory where the sqlite db file is created.
base_dir = os.path.abspath(os.path.dirname(__name__))


class Config:
    """
    Main Configuration file for the application.
    """

    # DATABASE url to be connected by the app
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or 'sqlite:///' + os.path.join(base_dir, 'insurance.db')
    
    # We do not want to track the modifications done in the DB.
    SQLALCHEMY_TRACK_MODIFICATIONS = False