import pytest
from apps import create_app 

flask_app = create_app()


@pytest.fixture
def app():
    yield flask_app
    
@pytest.fixture
def client(app):
    return app.test_client()
