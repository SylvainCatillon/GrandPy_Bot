from .. import utils as script
from instance import config as instance_config

import pytest
import requests


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

class TestParser:
    def setup_method(self):
        self.parser = script.Parser()
        self.sentence = "Salut GrandPy ! Est-ce que tu connais l'adresse d'OpenClassrooms ?"

    def test_not_a_string(self):
        with pytest.raises(AssertionError):
            self.parser.parse(25)
        
    def test_split_in_words(self):
        parsed = self.parser.split_in_words(self.sentence)
        assert parsed == ["salut", "grandpy", "!", "est-ce", "que", "tu",
        "connais", "l", "'", "adresse", "d", "'", "openclassrooms", "?"]

    def test_remove_stopwords(self):
        parsed = self.parser.parse(self.sentence)
        assert parsed == ["d", "'", "openclassrooms"]

    def test_sentences(self):
        p = self.parser.parse
        print(p("J'aimerais bien aller à la tour eiffel"))
        print(p("dis grandpy, c'est où la tour eiffel"))
        print(p("j'ai déjà cherché, mais j'arrive pas à trouver la tour eiffel..."))
        print(p("dis granpy, tu connais l'adresse d'openclassrooms, histoire que j'y fasse un tour?"))

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

    def test_construct_static_map_url(self):
        geoloc = {"lat" : 48.8748465, "lng" : 2.3504873}
        test_url = "https://maps.googleapis.com/maps/api/staticmap?zoom=15&\
size=300x150&markers=48.8748465,2.3504873&\
key={}".format(instance_config.GOOGLE_API_KEY)
        assert self.api_getter.construct_static_map_url(geoloc) == test_url
