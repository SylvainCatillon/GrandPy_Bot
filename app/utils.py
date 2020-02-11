import requests
import re
from bs4 import BeautifulSoup

from .stopwords_fr import stopwords_list

class Parser:

    def split_in_words(self, sentence):
        assert type(sentence) == str
        wrong_letters = []
        for letter in sentence:
            if letter not in wrong_letters+["-"] and not letter.isalnum():
                wrong_letters.append(letter)
        for letter in wrong_letters:
            sentence = sentence.replace(letter, " "+letter+" ")
        return sentence.lower().split()

    def _find_word(self, words_list, search_list, start=0):
        matches = []
        for word in search_list:
            if word in words_list[start:]:
                matches.append(words_list.index(word, start))
        if not matches:
            return None
        return sorted(matches)[0]

#    def _find_word(self, words_list, search_list, start=0):
#        match = None
#        for index, word in enumerate(words_list[start:]):
#            if word in search_list:
#                match = index
#                break
#        return match


    def parse_by_key_word(self, words_list):
        start = self._find_word(words_list, ["adresse", "où", "l'adresse"]) # place this list in a config file?
        if start:
            stop = self._find_word(words_list, ["?", ".", "!", ";"], start=start) # place this list in a config file?
            if not stop:
                stop = len(words_list)+1
            return words_list[start+1:stop]
        return []

    def parse_by_filter(self, words_list):
        parsed_list = []
        for word in words_list:
            if word.isalnum() and word not in stopwords_list+["grandpy", "bot", "grandpybot"]:
                parsed_list.append(word)
        return parsed_list

    def parse(self, sentence):
        words_list = self.split_in_words(sentence)
        parsed_list = self.parse_by_key_word(words_list)
        if not parsed_list:
            parsed_list = self.parse_by_filter(words_list)
        return parsed_list

class ApiGetter:

    def __init__(self, google_key, words_list):
        self.google_key = google_key
        self.words_list = words_list  #  passer cet ag plutot à ApiGetter.main()?

    def _request_address(self, query):
        payload = {
            "input": query,
            "inputtype": "textquery",
            "fields": "formatted_address,geometry,name",
            "key": self.google_key}
        raw_result = requests.get(
            "https://maps.googleapis.com/maps/api/place/findplacefromtext/json",
            params=payload)
        # if raw_result.status_code == 200?
        return raw_result.json()

    def get_address(self): # to rename
        query = " ".join(self.words_list)
        result = self._request_address(query)
        if result["status"].lower() == "ok":
            address = result["candidates"][0]["formatted_address"]
            geoloc = result["candidates"][0]["geometry"]["location"]
            name = result["candidates"][0]["name"]
            return address, geoloc, name
        else:
            return None # return status?

    def construct_static_map_url(self, geoloc):
        payload = {
            "zoom": 15,
            "size": "300x150",
            "markers": "{lat},{lng}".format(**geoloc),
            "key": self.google_key}
        return "https://maps.googleapis.com/maps/api/staticmap?zoom={zoom}&\
size={size}&markers={markers}&key={key}".format(**payload)

#    def _request_wikipedia(self, geoloc):
#        payload = {
#        "action": "query",
#        "generator": "geosearch",
#        "ggscoord": "{lat}|{lng}".format(**geoloc),
#        "ggsradius": 500,
#        "ggslimit": 20,
#        "format": "json",
#        "prop": "extracts",
#        "exsentences": 4,
#        "explaintext": 1,
#        "exintro": 1
#        }
#        raw_result = requests.get(
#            "https://fr.wikipedia.org/w/api.php",
#            params=payload)
#        intros = []
#        for page in raw_result.json()["query"]["pages"].values():
#            intros.append(page["extract"])
#        return intros

    def _request_wikipedia(self, geoloc):
        payload = {
            "action": "query",
            "list": "geosearch",
            "gscoord": "{lat}|{lng}".format(**geoloc),
            "gsradius": 500,
            "gslimit": 20,
            "format": "json"
            }
        raw_result = requests.get(
            "https://fr.wikipedia.org/w/api.php",
            params=payload)
        return raw_result.json()["query"]["geosearch"]

#    def _select_intro(self, intros):
#        max_len = 0
#        selected_intro = None
#        for intro in intros:
#            intro_len = len(intro)
#            if intro_len > max_len:
#                selected_intro = intro
#                max_len = intro_len
#        return selected_intro

    def select_pageid(self, pages, name):
        pageid = pages[0]["pageid"]
        for page in pages:
            if page["title"] == name:
                pageid = page["pageid"]
                break
        return pageid


    def get_section_text(self, pageid):
        payload = {
            "action": "parse",
            "pageid": pageid,
            "format": "json",
            "formatversion": 2,
            "prop": "text",
            "section": 1
            }
        raw_result = requests.get(
            "https://fr.wikipedia.org/w/api.php",
            params=payload)
        result = raw_result.json()
        html_text = result['parse']['text']
        section_text = re.sub("\[.*]", "", BeautifulSoup(html_text, "html.parser").p.get_text())
        title = result['parse']['title']
        return section_text, title

    def get_story(self, geoloc, name):
        pages = self._request_wikipedia(geoloc)
        pageid = self.select_pageid(pages, name)
        story, title = self.get_section_text(pageid)
        return story, title

    def main(self):
        found_address = self.get_address()
        result = {}
        if found_address:
            result["address"], geoloc, result["name"] = found_address
            result["static_map_url"] = self.construct_static_map_url(geoloc)
            result["story"], result["story_title"] = self.get_story(geoloc, result["name"])
            return result
        else:
            return None
