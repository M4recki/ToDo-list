import pytest
from main import app as flask_app

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SESSION_COOKIE_SAMESITE'] = None
    app.config['SESSION_COOKIE_SECURE'] = False
    return app.test_client()