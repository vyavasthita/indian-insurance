import os
from celery import Celery
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_cors import CORS
from apps.config.config import config_by_name


db = SQLAlchemy()
migrate = Migrate()
mail = Mail()


environment = os.getenv('FLASK_ENV') or 'development'

### Helper Functions ###
def initialize_config(app):   
   app.config.from_object(config_by_name[environment])
   print(app.config)

def create_log_directory():
    base_dir = os.path.abspath(os.path.dirname(__name__))

    if not os.path.exists(os.path.join(base_dir, configuration.LOGS_DIR)):
        os.mkdir(os.path.join(base_dir, configuration.LOGS_DIR))

def initialize_extensions(app, db):
    mail.init_app(app=app)
    db.init_app(app=app)
    migrate.init_app(app=app, db=db)

def initialize_error_handlers():
    from apps.user import errors

def register_blueprints(app):
    from apps.user.routes import user_blueprint
    app.register_blueprint(user_blueprint)

def create_app() -> Flask:
    app = Flask(__name__)

    print("Enabling CORS.")
    CORS(app) 

    print("Initializing Flask Configuration.")
    initialize_config(app=app)

    print("Enabling CORS.")
    CORS(app)

    print("Creating log directory.")
    create_log_directory()

    print("Initializing Flask extentions.")
    initialize_extensions(app=app, db = db)

    print("Initializing Error handlers.")
    initialize_error_handlers()

    print("Registering blueprints.")
    register_blueprints(app=app)

    return app


configuration = config_by_name[environment]

celery = Celery(__name__, broker=configuration.CELERY_BROKER_URL, 
                result_backend=configuration.CELERY_RESULT_BACKEND) 