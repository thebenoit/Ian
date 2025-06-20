from typing import Any
import os
from dotenv import load_dotenv
from seleniumwire import webdriver  # Import from seleniumwire
import seleniumwire.undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from pymongo import MongoClient 
from seleniumwire.utils import decode
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import logging
import sys
# rotating ip library
from requests_ip_rotator import ApiGateway

# # other
import requests
import json
import time
import random
import urllib
import urllib.parse
from time import sleep

load_dotenv()

from tools import BaseTool, BaseScraper

class SearchFacebook(BaseTool, BaseScraper):
    def __init__(self):
        self.name = "search_facebook"
        self.description = "Search in facebook marketplace for a listing according to the user's request(query)"

    def execute(self, inputs: dict[str, Any]) -> Any:
        query = inputs.get("query")
        
        return "Facebook search result"
    
    def scrape(self,url:str) -> str:
     try:
        ##change according to the computer install here: https://googlechromelabs.github.io/chrome-for-testing/#stable
        self.driver = os.getenv("DRIVER_PATH")
        
        proxies = {
            "http": os.getenv("PROXIES_URL"),
            "https": os.getenv("PROXIES_URL")
        }
        
        chrome_options = uc.ChromeOptions()
        chrome_options.add_argument('--ignore-ssl-errors=yes')
        chrome_options.add_argument('--ignore-certificate-errors')
        
        service = Service(self.driver)
        
        self.session =  requests.Session()
        self.session.proxies.update(proxies)
        self.session.verify = False
        
        self.init_session()
        self.driver.close()
        
        self.max_retries = 3
        self.retry_delay = 10
        
     except Exception as e:
        print(f"Error during the initialization of the Scraper: {e}")
        raise
    
    def get_first_req(self):
        self.driver.get(f"https://www.facebook.com/marketplace/montreal/propertyrentals?exact=false&latitude=45.50889&longitude=-73.63167&radius=7&locale=fr_CA")
        #allow the page to load fully including any JavaScript that triggers API requests
        time.sleep(15)

        # get first request through selenium to get the headers and first results
        for request in self.driver.requests:
            #if request is a response
            if request.response:
                #if request is a graphql request
                if "graphql" in request.url:
                    print("graphql request found")
                    #decode the response body
                    resp_body = decode(request.response.body, request.response.headers.get('Content-Encoding', 'identity'))
                    #convert the response body to a json object
                    resp_body = json.loads(resp_body)

                    #if the response body contains the data we want
                    if "marketplace_rentals_map_view_stories" in resp_body["data"]["viewer"]:
                        print("marketplace_rentals_map_view_stories found")
                        #return the headers, body, and response body
                        return request.headers.__dict__["_headers"], request.body, resp_body
        print("No matching request found")
        return None
    
    def load_headers(self, headers):
        # Cette méthode charge les en-têtes HTTP dans la session
        
        # Pour chaque paire clé-valeur dans les en-têtes fournis
        for key, value in headers:
            # Met à jour les en-têtes de la session avec la nouvelle paire clé-valeur
            self.session.headers.update({key: value})
        
        # Ajoute un en-tête spécifique pour identifier le type de requête Facebook
        # Cet en-tête indique qu'on utilise l'API de recherche immobilière sur la carte
        self.session.headers.update({"x-fb-friendly-name": "CometMarketplaceRealEstateMapStoryQuery"})
    
    
    def get_next_cursor(self, body):
        try:
            return body["data"]["marketplace_feed_stories"]["page_info"]["end_cursor"]
        except KeyError as e:
            print(f"Erreur d'accès aux données : {e}")
        # Vous pouvez ajouter ici un logging plus détaillé de la structure de body
        return None
    
    def parse_payload(self, payload):
        # Decode the data string
        decoded_str = urllib.parse.unquote(payload.decode())

        # Parse the string into a dictionary
        data_dict = dict(urllib.parse.parse_qsl(decoded_str))
        
        return data_dict    
    
    