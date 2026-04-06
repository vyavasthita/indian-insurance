import pytest


@pytest.mark.config
def test_development_config(app):
    app.config.from_object('apps.config.config.DevelopmentConfig')

    assert app.config['FLASK_ENV'] == "development"
    assert app.config['DEBUG'] == True
    assert app.config['TESTING'] == False
    assert app.config['FLASK_RUN_HOST'] == "0.0.0.0"
    assert app.config['FLASK_RUN_PORT'] == '5000'
    assert app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] == False
    
@pytest.mark.config
def test_config(app):
    app.config.from_object('apps.config.config.AutomatedTestingConfig')

    assert app.config['FLASK_APP'] == "wsgi.py"
    assert app.config['FLASK_ENV'] == "automated_testing"
    assert app.config['DEBUG'] == False
    assert app.config['TESTING'] == True
    assert app.config['FLASK_RUN_HOST'] == "0.0.0.0"
    assert app.config['FLASK_RUN_PORT'] == '5001'
    assert app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] == False