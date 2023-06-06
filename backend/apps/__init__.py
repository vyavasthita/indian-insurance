import os
from celery import Celery
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_cors import CORS
from apps.config.config import Config
from utils.make_celery import celery_init_app


db = SQLAlchemy()
migrate = Migrate()
mail = Mail()

celery = Celery(__name__, broker=Config.CELERY_BROKER_URL, result_backend=Config.CELERY_RESULT_BACKEND) 

### Helper Functions ###
def initialize_config(app):
   app.config.from_object(Config)

def initialize_extensions(app, db):
    mail.init_app(app=app)
    db.init_app(app=app)
    migrate.init_app(app=app, db=db)

def initialize():
    from apps.user import errors

def create_log_directory():
    base_dir = os.path.abspath(os.path.dirname(__name__))

    if not os.path.exists(os.path.join(base_dir, configuration.LOGS_DIR)):
        os.mkdir(os.path.join(base_dir, configuration.LOGS_DIR))

def register_blueprints(app):
    from apps.user.routes import user_blueprint

    app.register_blueprint(user_blueprint)

def create_app():
    app = Flask(__name__)

    print("Enabling CORS.")
    CORS(app)

    # Configure celery
    celery.conf.update(app.config)  

    print("Initializing Flask Configuration.")
    initialize_config(app=app)

    print("Creating log directory.")
    create_log_directory()

    print("Initializing Flask extentions.")
    initialize_extensions(app=app, db = db)

    print("Initializing others.")
    initialize()

    print("Registering blueprints.")
    register_blueprints(app=app)

    return app


configuration = Config()