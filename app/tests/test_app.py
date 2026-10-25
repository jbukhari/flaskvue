import pytest

def test_base(client):
    assert client.get('/').status_code == 200

def test_app(client, app):
    assert client.get('/app').status_code == 200

def test_login(client):
    response = client.get('/login')
    assert response.status_code == 200

    response = client.post('/login', data={})
    assert response.status_code == 200

    #user = default_users['admin']
    #rv = login(client, user['email'], user['password'])
    #assert rv.status_code == 200