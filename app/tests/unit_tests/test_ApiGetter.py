import pytest
import requests

from app.utils import ApiGetter as script
from instance import config as instance_config


class MockResponse:
    @staticmethod
    def json():
        return {
           "candidates" : [
              {
                 "formatted_address" : "7 Cité Paradis, 75010 Paris, France",
                 "geometry" : {
                    "location" : {
                       "lat" : 48.8748465,
                       "lng" : 2.3504873
                    },
                    "viewport" : {
                       "northeast" : {
                          "lat" : 48.87622362989272,
                          "lng" : 2.351843679892722
                       },
                       "southwest" : {
                          "lat" : 48.87352397010727,
                          "lng" : 2.349144020107278
                       }
                    }
                 },
                 "name" : "OpenClassrooms"
              }
           ],
           "status" : "OK"
        }

@pytest.fixture
def mock_response(monkeypatch):
    """Requests.get() mocked to return {'mock_key':'mock_response'}."""

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)

class TestApiGetter:
    def setup_method(self):
        self.words_list = ["d", "'", "openclassrooms"]
        self.api_getter = script.ApiGetter(instance_config.GOOGLE_API_KEY, self.words_list)

    def test_get_api_response(self, mock_response):
        result = self.api_getter._request_address("fake query")
        assert result == MockResponse.json()

    def test_get_address(self, mock_response):
        address = self.api_getter.get_address()[0]
        assert address == "7 Cité Paradis, 75010 Paris, France"

    def test_get_geoloc(self, mock_response):
        geoloc = self.api_getter.get_address()[1]
        assert geoloc["lat"] == 48.8748465
        assert geoloc["lng"] == 2.3504873

    def test_main(self):
      result = self.api_getter.main()
      for key in ["status","address", "map_url", "story"]:
        assert key in result
      assert result["status"] == "OK"
