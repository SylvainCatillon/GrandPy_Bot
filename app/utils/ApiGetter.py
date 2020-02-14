import requests
import re

from bs4 import BeautifulSoup

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

    def get_embed_map_url(self, geoloc):
        payload = {
            "q": "{lat},{lng}".format(**geoloc),
            "key": self.google_key}
        return "https://www.google.com/maps/embed/v1/place?q={q}&key={key}".format(**payload)

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
        section_text = re.sub("\\[.*]", "", BeautifulSoup(html_text, "html.parser").p.get_text())
        title = result['parse']['title']
        return section_text, title

    def get_story(self, geoloc, name):
        pages = self._request_wikipedia(geoloc)
        pageid = self.select_pageid(pages, name)
        story, title = self.get_section_text(pageid)
        url = "https://fr.wikipedia.org/?curid={}".format(pageid)
        return story, title, url

    def main(self):
        found_address = self.get_address()
        if found_address:
            address, geoloc, name = found_address
            map_url = self.get_embed_map_url(geoloc)
            story, story_title, story_url = self.get_story(geoloc, name)
            #  Mettre les phrases dans fichier de config
            address_text = "Comment?! {name}? Ahhhh, oui, je me souviens de cette adresse! c'est: {address}"
            story_text = "Mais t'ai-je déjà raconté l'histoire de ce quartier qui m'a vu en culottes courtes ? {story_title}: {story}"
            story_link_text = "En savoir plus sur Wikipedia"
            return {
                "status": "OK",
                "address":  address_text.format(name=name, address=address),
                "map_url": map_url,
                "story": story_text.format(
                    story=story, story_title=story_title),
                "story_url": story_url,
                "story_link_text": story_link_text}
        else:
            return {
                "status": "address_not_found",
                "message": "Désolé mon p'tit, je me souviens plus où c'est..."}
