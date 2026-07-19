# API route tests. Fixtures are defined in conftest.py.

import pytest, json
from flask.testing import FlaskClient

PRE = '/api/v1'

def test_docs(client: FlaskClient):
    # Response code is 308 because of redirect to docs
    assert client.get('/api').status_code == 308

def test_records(client: FlaskClient):
    route = f'{PRE}/records'
    assert client.get(route).status_code == 200
    assert client.post(route, data=json.dumps({'id': 42})).status_code == 201

def test_record(client: FlaskClient):
    route = f'{PRE}/record'
    assert client.get(route).status_code == 200