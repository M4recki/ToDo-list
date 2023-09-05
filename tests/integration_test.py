from conftest import client

# Test the home page route


def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200, "Home page failed with status code {}".format(
        response.status_code)

# Test the login route


def test_login(client):
    response = client.post('/signup', data={
        'first_name': 'test', 'last_name': 'test', 'email': 'X@test.com', 'password': 'test'})

    response = client.post('/login', data={
        'email': 'X@test.com',
        'password': 'test'
    }, follow_redirects=True)

    response = client.get('/?name=test')

    assert response.status_code == 200, "Login failed with status code {}".format(
        response.status_code)

# Test the unauthorized path


def test_unauthorized_path(client):
    response = client.get('/create')
    assert response.status_code == 401, "Unauthorized path failed with status code {}".format(
        response.status_code)
    assert b'<h1>Unauthorized</h1>' in response.data