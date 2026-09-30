# Pytest fixtures

import pytest
from mongomock import MongoClient
from app.app import APP
from app.config import Config

### Flask test utilities
# https://flask.palletsprojects.com/en/stable/testing/
@pytest.fixture()
def app():
    APP.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield APP

    # clean up / reset resources here

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

### Database
@pytest.fixture()
def db():
    from app.db import DB

    # DB will use a mock database if we are in a testing environment
    db = DB()
    assert isinstance(db.client, MongoClient)
    database = db.client.get_database(Config.DATABASE_NAME)

    # prepopulate test data here if needed

    yield db
    db.client.drop_database(Config.DATABASE_NAME)
    
