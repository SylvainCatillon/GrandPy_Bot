import pytest

from app.utils import parser as script

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

    def test_parse(self):
        parsed = self.parser.parse(self.sentence)
        assert parsed == ["d", "'", "openclassrooms"]
