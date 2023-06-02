from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()


### Helper Functions ###
def register_blueprints(app):
    from apps.user.routes import user_blueprint

    app.register_blueprint(user_blueprint)

def initialize_extensions(app, db):
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