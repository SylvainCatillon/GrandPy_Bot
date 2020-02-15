import pytest

from ..views import app

@pytest.fixture(scope='module')
def test_client():
    """Pytest fixture to test the connection at the app"""
    app.config.from_object("app.tests.config")
    testing_client = app.test_client()
    ctx = app.app_context()
    ctx.push()
    yield testing_client
    ctx.pop()

def test_home_page(test_client):
    """Tests the access to the home page,
    and assures that its contains the name of the project and
    the name of its developer"""
    response = test_client.get("/")
    assert response.status_code == 200
    assert b"GrandPy Bot" in response.data
    assert b"Sylvain Catillon" in response.data

def test_wrong_url(test_client):
    """Tests a wrong URL"""
    response = test_client.get("/wrong_url")
    assert response.status_code == 404

def test_get_answer(test_client):
    """Tests get_answer"""
    response = test_client.get("/get_answer?user_message='tour eiffel'")
    assert response.status_code == 200
    assert response.is_json
    result = response.get_json()
    assert "story" in result
    assert "address" in result
    assert "tour eiffel" in result["address"].lower()
