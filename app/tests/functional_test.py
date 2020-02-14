import pytest

from ..views import app

@pytest.fixture(scope='module')
def test_client():
    app.config.from_object("app.tests.config")
    testing_client = app.test_client()
    ctx = app.app_context()
    ctx.push()
    yield testing_client
    ctx.pop()

def test_home_page(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert b"GrandPy Bot" in response.data
    assert b"Sylvain Catillon" in response.data

def test_wrong_url(test_client):
    response = test_client.get("/wrong_url")
    assert response.status_code == 404

def test_get_response(test_client):
    response = test_client.get("/get_response?user_message='tour eiffel'")
    assert response.status_code == 200
    assert response.is_json
    r = response.get_json()
    assert "story" in r
    assert "address" in r
    assert "tour eiffel" in r["address"].lower()
