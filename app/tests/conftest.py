# Pytest fixtures

import pytest
from app.app import APP
from app.config import Config

Config.testing = True

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
