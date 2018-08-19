import requests
import json

class Weblib():
    
    def __init__(self):
        self._session = requests.Session()
        self._base_url = "https://mhw-db.com/"

    def get(self, url: str, query_strings: dict = None):
        """
        Executes a GET request to the MHW database over a REST API.

        Args:
            url (str): Location of the resource in that is combined with the
                base url.
            query_strings (dict): Query strings for the request, optional.
        """


        if query_strings:
            if isinstance(query_strings, str):
                query_strings = json.loads(query_strings)
        else:
            query_strings = dict()

        real_url = "{}{}".format(self._base_url, url) 
        resp = self._session.get(real_url, params=query_strings)
        query_results = json.loads(resp.text)
        print("{} requested. Results: {}".format(url, len(query_results)))

        return query_results

        