import requests

from .stopwords_fr import stopwords_list

class Parser:

    def _find_word(self, words_list, search_list, start=0):
        matches = []
        for word in search_list:
            if word in words_list[start:]:
                matches.append(words_list.index(word, start))
        if not matches:
            return None
        return sorted(matches)[0]

    def split_in_words(self, sentence):
        assert type(sentence) == str
        wrong_letters = []
        for letter in sentence:
            if letter not in ["-"] and not letter.isalnum():
                wrong_letters.append(letter)
        for letter in wrong_letters:
            sentence = sentence.replace(letter, " "+letter+" ")
        return sentence.lower().split()

    def parse_by_key_word(self, words_list):
        start = self._find_word(words_list, ["adresse", "où", "l'adresse"]) # place this list in a config file?
        if start:
            stop = self._find_word(words_list, ["?", ".", ",", "!", ";"], start=start) # place this list in a config file?
            if not stop:
                stop = len(words_list)+1
            return words_list[start+1:stop]
        return []

    def parse_by_filter(self, words_list):
        parsed_list = []
        for word in words_list:
            if word.isalnum() and word not in stopwords_list+["grandpy", "bot"]:
                parsed_list.append(word)
        return parsed_list

    def parse(self, sentence):
        words_list = self.split_in_words(sentence)
        parsed_list = self.parse_by_key_word(words_list)
        if not parsed_list:
            parsed_list = self.parse_by_filter(words_list)
        return parsed_list

class ApiGetter:

    def __init__(self, google_key):
        self.google_key = google_key

    def _request_adress(self, query):
        raw_result = requests.get(
            "https://maps.googleapis.com/maps/api/place/findplacefromtext/json\
?input={}&language=fr&inputtype=textquery&fields=formatted_address,name,\
geometry&language=french&key={}".format(query, self.google_key))
        return raw_result.json()

    def get_adress(self, words_list):
        query = " ".join(words_list)
        result = self._request_adress(query)
        return result["candidates"][0]["formatted_address"]
