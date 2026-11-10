# Pytest fixtures

import pytest
from collections.abc import Generator
from flask import Flask
from flask.testing import FlaskClient, FlaskCliRunner
from flask_login import FlaskLoginClient
from mongomock import MongoClient
from app.app import APP
from app.config import Config
from app.db import DB, User

@pytest.fixture()
def db() -> Generator[DB]:
    # Yields a DB instance then drops the database

    db = DB()
    assert isinstance(db.client, MongoClient) # DB uses a mock database if this is a testing environment
    database = db.client.get_database(Config.DATABASE_NAME)

    # Prepopulate test data here if needed

    yield db
    db.client.drop_database(Config.DATABASE_NAME)

@pytest.fixture()
def app() -> Generator[Flask]:
    APP.config.update({
        "TESTING": True,
    })

    # Setup here

    yield APP

    # Cleanup here

@pytest.fixture()
def client(app) -> FlaskClient:
    return app.test_client()

@pytest.fixture()
def runner(app) -> FlaskCliRunner:
    return app.test_cli_runner()

@pytest.fixture()
def user(db) -> User:
    User.collection = db.get_collection('test')

    return User.add_user('test', 'pw')

@pytest.fixture()
def client_logged_in(app, user) -> FlaskClient:
    # Returns a Flask test client with a user already logged in

    app.test_client_class = FlaskLoginClient
    user = User.add_user('x', 'yz')

    return app.test_client(user=user)


