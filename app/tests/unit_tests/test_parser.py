import pytest

from app.utils import parser as script

class TestParser:
    """Tests the class Parser"""
    def setup_method(self):
        """Prepare the tests by creating an instance of Parser
        and a test sentence"""
        self.parser = script.Parser()
        self.sentence = "Salut GrandPy ! Est-ce que tu connais \
l'adresse d'OpenClassrooms ?"

    def test_not_a_string(self):
        """Assures that an assertion error is raised 
        if an int is given to Parser.parse()"""
        with pytest.raises(AssertionError):
            self.parser.parse(25)

    def test_split_in_words(self):
        """Assures that Parser.split_in_words()
        splits a sentence in a list of words"""
        parsed = self.parser._split_in_words(self.sentence)
        assert parsed == [
            "salut", "grandpy", "!", "est-ce", "que", "tu",
            "connais", "l", "'", "adresse", "d", "'", "openclassrooms", "?"
        ]

    def test_parse(self):
        """Tests the main function Parser.parse()"""
        parsed = self.parser.parse(self.sentence)
        assert parsed == ["d", "'", "openclassrooms"]
