import requests
import re

from bs4 import BeautifulSoup

import config

class ApiGetter:

    def __init__(self):
        self.google_key = config.GOOGLE_API_KEY

    def request_address(self, query):
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

    def get_address(self, words_list): # to rename
        query = " ".join(words_list)
        result = self.request_address(query)
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

    def request_wikipedia(self, geoloc):
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
        pages = self.request_wikipedia(geoloc)
        pageid = self.select_pageid(pages, name)
        story, title = self.get_section_text(pageid)
        url = "https://fr.wikipedia.org/?curid={}".format(pageid)
        return story, title, url

    def main(self, words_list):
        found_address = self.get_address(words_list)
        if found_address:
            address, geoloc, name = found_address
            map_url = self.get_embed_map_url(geoloc)
            story, story_title, story_url = self.get_story(geoloc, name)
            return {
                "status": "OK",
                "address":  config.TEXT["address"].format(
                    name=name, address=address),
                "map_url": map_url,
                "story": config.TEXT["story"].format(
                    story=story, story_title=story_title),
                "story_url": story_url,
                "story_link_text": config.TEXT["story_link"]}
        else:
            return {
                "status": "address_not_found",
                "message": config.TEXT["address_not_found"]}
