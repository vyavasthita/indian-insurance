import pytest
from apps import create_app, db as _db


flask_app = create_app()


@pytest.fixture
def app():
    yield flask_app
    
@pytest.fixture
def client(app):
    """
    Note that if we are testing for assertions or exceptions in our 
    application code, we must set app.testing = True in order for 
    the exceptions to propagate to the test client. 

    Otherwise, the exception will be handled by the 
    application (not visible to the test client) and the only 
    indication of an AssertionError or other exception will be a 
    500 status code response to the test client
    """
    app.testing = True
    return app.test_client()

@pytest.fixture()
def db(app, request):
    # Create the database and the database table
    def teardown():
        _db.drop_all()

    _db.create_all()

    yield _db

@pytest.fixture(scope='function')
def session(db, request):
    """Creates a new database session for a test."""
    # connect to the database
    connection = db.engine.connect()
    # begin a non-ORM transaction
    transaction = connection.begin()

    # bind an individual session to the connection
    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    # overload the default session with the session above
    db.session = session

    def teardown():
        session.close()
        # rollback - everything that happened with the
        # session above (including calls to commit())
        # is rolled back.
        transaction.rollback()
        # return connection to the Engine
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session