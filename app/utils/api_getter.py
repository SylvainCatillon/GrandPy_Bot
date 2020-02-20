from random import choice
import re
import requests

from bs4 import BeautifulSoup

import config

class ApiGetter:
    """This class requests Wikipedia and Google APIs,
    gathers the results, and returns them"""

    def __init__(self):
        self.google_key = config.GOOGLE_API_KEY

    def _request_address(self, query):
        """Takes a string arg as 'query'.
        Requests Google Place API and return the result in Json format"""
        payload = {
            "input": query,
            "inputtype": "textquery",
            "fields": "formatted_address,geometry,name",
            "language": "fr",
            "key": self.google_key}
        raw_result = requests.get(
            "https://maps.googleapis.com/maps/api/place/"
            "findplacefromtext/json",
            params=payload)
        return raw_result.json()

    def _get_embed_map_url(self, geoloc):
        """Takes an arg {"lat":float,"lng":float} as 'geoloc'.
        Returns an URL to an embeb google map"""
        payload = {
            "q": "{lat},{lng}".format(**geoloc),
            "key": self.google_key}
        return "https://www.google.com/maps/embed/v1/place?" \
                "q={q}&key={key}".format(**payload)

    @staticmethod
    def _request_wiki_geosearch(geoloc):
        """Takes an arg {"lat":float,"lng":float} as 'geoloc'.
        Requests Wikipedia API and its geosearch function
        and return the result in Json format"""
        payload = {
            "action": "query",
            "list": "geosearch",
            "gscoord": "{lat}|{lng}".format(**geoloc),
            "gsradius": 1000,
            "gslimit": 20,
            "format": "json"
            }
        raw_result = requests.get(
            "https://fr.wikipedia.org/w/api.php",
            params=payload)
        return raw_result.json()["query"]["geosearch"]

    @staticmethod
    def _request_wiki_parse(pageid):
        """Takes an arg 'pageid'.
        Requests Wikipedia API and its parse function to get the content
        of the first section and return the result in Json format"""
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
        return raw_result.json()

    @staticmethod
    def _search_relevant_page(pages, name):
        """Takes a list of dict as 'pages' and a string as 'name'.
        Checks if a page has the arg 'name' as title. If founded,
        places this page at the start of the list. Returns the list."""
        for index, page in enumerate(pages):
            if page["title"] == name:
                pages.insert(0, pages.pop(index))
                break
        return pages

    def _get_section_text(self, pages):
        """Takes a list of pages as arg 'pages'.
        Gets the content of the first page of the list in html format.
        Uses 'BeautifulSoup' lib to get the content of the
        first paragraph in text format.
        Uses regex 're' lib to eliminate some unwanted text.
        Returns the parsed text of the section and the page title"""
        if not pages:
            return None, None, None
        pageid = pages[0]["pageid"]
        result = self._request_wiki_parse(pageid)
        if not result or "parse" not in result:
            #  If the content isn't relevant, del the page and try again
            print(result)
            del pages[0]
            return self._get_section_text(pages)
        html_text = result["parse"]["text"]
        paragraph = BeautifulSoup(html_text, "html.parser").p
        if not paragraph:
            #  If the content isn't relevant, del the page and try again
            del pages[0]
            return self._get_section_text(pages)
        raw_text = paragraph.get_text()
        parsed_text = re.sub("\\[.*]", "", raw_text)
        title = result["parse"]["title"]
        return parsed_text, title, pageid

    def _get_story(self, geoloc, name):
        """Takes an arg {"lat":float,"lng":float} as 'geoloc'
        and a string as 'name'.
        Launches the methods to get a story from a Wikipedia page.
        Returns the story, the page title and the page URL"""
        pages = self._request_wiki_geosearch(geoloc)
        if not pages:
            return (config.TEXT["failed_story"], "...", "")
        relevant_pages = self._search_relevant_page(pages, name)
        story, title, pageid = self._get_section_text(relevant_pages)
        if not story:
            return (config.TEXT["failed_story"], "...", "")
        url = "https://fr.wikipedia.org/?curid={}".format(pageid)
        return story, title, url

    def _construct_result(self, result):
        """Takes a dict as result.
        Lauchn this function if the Google status was 'OK'.
        Return the full result"""
        geoloc = result["geometry"]["location"]
        name = result["name"]
        map_url = self._get_embed_map_url(geoloc)
        story, story_title, story_url = self._get_story(geoloc, name)
        return {
            "status": "OK",
            "address":  choice(config.TEXT["address"]).format(
                name=name, address=result["formatted_address"]),
            "map_url": map_url,
            "story": choice(config.TEXT["story"]).format(
                story=story, story_title=story_title),
            "story_url": story_url,
            "story_link_text": config.TEXT["story_link"]
        }

    @staticmethod
    def _address_not_found():
        """Return a result to send if the address wasn't found"""
        return {
            "status": "ADDRESS_NOT_FOUND",
            "message": config.TEXT["address_not_found"]
        }

    @staticmethod
    def _construct_fail_result(response):
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
        if not words_list:
            return self._address_not_found()
        query = " ".join(words_list)
        response = self._request_address(query)
        #  Next line is to deal with case sensitivity
        response["status"] = response["status"].upper()
        if response["status"] == "OK":
            return self._construct_result(response["candidates"][0])
        if response["status"] == "ZERO_RESULTS":
            return self._address_not_found()
        return self._construct_fail_result(response)
