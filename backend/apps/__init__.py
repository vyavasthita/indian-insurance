from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_cors import CORS
from apps.config.config import Config


db = SQLAlchemy()
migrate = Migrate()
mail = Mail()

### Helper Functions ###
def initialize_config(app):
   app.config.from_object(Config)

def initialize_extensions(app, db):
    mail.init_app(app=app)
    db.init_app(app=app)
    migrate.init_app(app=app, db=db)

def initialize():
    from apps.user import errors

def register_blueprints(app):
    from apps.user.routes import user_blueprint

    app.register_blueprint(user_blueprint)


def create_app():
    app = Flask(__name__)

    CORS(app)

    initialize_config(app=app)

    initialize_extensions(app=app, db = db)

    initialize()

    register_blueprints(app=app)

    return app

configuration = Config()