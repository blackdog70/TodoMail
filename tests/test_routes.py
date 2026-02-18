import sys
from pathlib import Path
import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app import create_app
from app.auth import users

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    return app.test_client()

def register(client, username='user', password='pass', language='en'):
    data = {
        'username': username,
        'password': password,
        'first_name': 'First',
        'last_name': 'Last',
        'email': 'user@example.com',
        'language': language,
    }
    return client.post('/register', data=data)


def login(client, username='user', password='pass'):
    return client.post('/login', data={'username': username, 'password': password})

def test_login_required(client):
    resp = client.get('/')
    assert resp.status_code == 302
    assert '/login' in resp.headers['Location']

def test_registration_and_access(client):
    register(client)
    resp = client.get('/')
    assert resp.status_code == 200
    assert b'Hello, World!' in resp.data


def test_login_after_register(client):
    register(client, username='alice', password='secret')
    client.get('/logout')
    login(client, username='alice', password='secret')
    resp = client.get('/')
    assert resp.status_code == 200


def test_registration_italian(client):
    register(client, username='mario', password='ciao', language='it')
    resp = client.get('/')
    assert b'Ciao, Mondo!' in resp.data


def test_settings_requires_login(client):
    resp = client.get('/settings')
    assert resp.status_code == 302
    assert '/login' in resp.headers['Location']


def test_add_mail_server(client):
    register(client, username='bob')
    data = {
        'protocol': 'imap',
        'server': 'smtp.example.com',
        'port': '25',
        'username': 'alice',
        'password': 'secret',
    }
    resp = client.post('/settings', data=data, follow_redirects=True)
    assert resp.status_code == 200
    assert users['bob']['mail_servers'][0]['protocol'] == 'imap'
    assert users['bob']['mail_servers'][0]['server'] == 'smtp.example.com'
