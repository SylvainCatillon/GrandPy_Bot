import re
import requests

from bs4 import BeautifulSoup

import config

class ApiGetter:
    """This class requests Wikipedia and Google APIs,
    gathers the results, and returns them"""

    def __init__(self):
        self.google_key = config.GOOGLE_API_KEY

    def request_address(self, query):
        """Takes a string arg as 'query'.
        Requests Google Place API and return the result in Json format"""
        payload = {
            "input": query,
            "inputtype": "textquery",
            "fields": "formatted_address,geometry,name",
            "key": self.google_key}
        raw_result = requests.get(
            "https://maps.googleapis.com/maps/api/place/\
findplacefromtext/json",
            params=payload)
        return raw_result.json()

    def get_embed_map_url(self, geoloc):
        """Takes an arg {"lat":float,"lng":float} as 'geoloc'.
        Returns an URL to an embeb google map"""
        payload = {
            "q": "{lat},{lng}".format(**geoloc),
            "key": self.google_key}
        return "https://www.google.com/maps/embed/v1/place?\
q={q}&key={key}".format(**payload)

    def request_wikipedia(self, geoloc):
        """Takes an arg {"lat":float,"lng":float} as 'geoloc'.
        Requests Wikipedia API and return the result in Json format"""
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
        """Takes a list of dict as 'pages' and a string as 'name'.
        Checks if a page has the arg 'name' as title, and return its ID.
        If there is no match, returns the ID of the first page"""
        for page in pages:
            if page["title"] == name:
                return page["pageid"]
        return pages[0]["pageid"]

    def get_section_text(self, pageid):
        """Takes an int arg 'pageid'.
        Requests the Wikipedia Parse API to get the content of the first
        section of the 'pageid' page, in html format.
        Uses 'BeautifulSoup' lib to convert HTML to plain text.
        Uses regex 're' lib to eliminate some unwanted text.
        Returns the parsed text of the section and the page title"""
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
        raw_text = BeautifulSoup(html_text, "html.parser").p.get_text()
        parsed_text = re.sub("\\[.*]", "", raw_text)
        title = result['parse']['title']
        return parsed_text, title

    def get_story(self, geoloc, name):
        """Takes an arg {"lat":float,"lng":float} as 'geoloc'
        and a string as 'name'.
        Launches the methods to get a story from a Wikipedia page.
        Returns the story, the page title and the page URL"""
        pages = self.request_wikipedia(geoloc)
        pageid = self.select_pageid(pages, name)
        story, title = self.get_section_text(pageid)
        url = "https://fr.wikipedia.org/?curid={}".format(pageid)
        return story, title, url

    def construct_result(self, result):
        """Takes a dict as result.
        Lauchn this function if the Google status was 'OK'.
        Return the full result"""
        geoloc = result["geometry"]["location"]
        name = result["name"]
        map_url = self.get_embed_map_url(geoloc)
        story, story_title, story_url = self.get_story(geoloc, name)
        return {
            "status": "OK",
            "address":  config.TEXT["address"].format(
                name=name, address=result["formatted_address"]),
            "map_url": map_url,
            "story": config.TEXT["story"].format(
                story=story, story_title=story_title),
            "story_url": story_url,
            "story_link_text": config.TEXT["story_link"]
        }

    def address_not_found(self):
        """Return a result to send if the address wasn't found"""
        return {
            "status": "ADDRESS_NOT_FOUND",
            "message": config.TEXT["address_not_found"]
        }

    def construct_fail_result(self, response):
        """Return a result to send if the Google request failed"""
        fail_result = {
            "status": "GOOGLE_REQUEST_FAILED",
            "message": "Error durring the Google API request"
        }
        if "status" in response:
            fail_result["status"] = response["status"]
        if "error_message" in response:
            fail_result["message"] = response["error_message"]
        return fail_result

    def main(self, words_list):
        """Takes a list of words as 'words_list'.
        Request an address, and lauchnes a method to get a result,
        accorded to the request status"""
        query = " ".join(words_list)
        response = self.request_address(query)
        #  Next line is to deal with case sensitivity
        response["status"] = response["status"].upper()
        if response["status"] == "OK":
            return self.construct_result(response["candidates"][0])
        elif response["status"] == "ZERO_RESULTS":
            return self.address_not_found()
        return self.construct_fail_result(response)
