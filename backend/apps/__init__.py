from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app=app)
migrate = Migrate(app=app, db=db)

from apps.user.routes import user_blueprint

app.register_blueprint(user_blueprint)

@app.get("/")
def home():
    return {'message': 'Welcome to Indian Insurance Company'}
