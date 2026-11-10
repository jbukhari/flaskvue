import pytest, re
from app.config import Config

def test_base(client):
    assert client.get('/').status_code == 200

def test_app(client, app):
    assert client.get('/app').status_code == 200

def test_login(client, user):
    assert client.get('/login').status_code == 200
    assert client.post('/login', data={'userId': 'invalid', 'password': ''}).status_code == 404
    assert client.post('/login', data={'userId': 'test', 'password': 'invalid'}).status_code == 401
    assert client.post('/login', data={'userId': 'test', 'password': 'pw'}).status_code == 302
    assert client.post('/login', data={'userId': 'test', 'password': 'pw'}).status_code == 200

def test_logout(client_logged_in):
    client = client_logged_in
    
    assert client.post('/login').status_code == 200
    assert client.get('/logout').status_code == 302
    assert client.post('/login').status_code == 404
