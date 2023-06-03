from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from apps.config.config import Config


db = SQLAlchemy()
migrate = Migrate()
mail = Mail()

### Helper Functions ###
def register_blueprints(app):
    from apps.user.routes import user_blueprint

    app.register_blueprint(user_blueprint)

def initialize_extensions(app, db):
    mail.init_app(app=app)
    db.init_app(app=app)
    migrate.init_app(app=app, db=db)

def initialize_config(app):
   app.config.from_object(Config)

def create_app():
    app = Flask(__name__)

    initialize_config(app=app)

    initialize_extensions(app=app, db = db)

    register_blueprints(app=app)

    return app

configuration = Config()