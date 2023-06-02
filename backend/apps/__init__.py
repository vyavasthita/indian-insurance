from flask import Flask


app = Flask(__name__)


@app.get("/")
def home():
    return {'message': 'Welcome to Indian Insurance Company'}
