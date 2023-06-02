from flask import Flask


app = Flask(__name__)

from apps.user.routes import user_blueprint

app.register_blueprint(user_blueprint)

@app.get("/")
def home():
    return {'message': 'Welcome to Indian Insurance Company'}
