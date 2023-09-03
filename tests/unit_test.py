from conftest import client
from flask import session


# Test the home page route


def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200, "Home page failed with status code {}".format(response.status_code)
    
# Test the login route


def test_login(client):
    response = client.post('/login', data={
        'email': 'test@email.com',
        'password': 'test'
    }, follow_redirects=True)

    assert response.status_code == 200, "Login failed with status code {}".format(response.status_code)