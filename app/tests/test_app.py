import pytest, flask

def test_base(client):
    assert client.get('/').status_code == 200

def test_app(app, client):
    assert client.get('/app').status_code == 200
