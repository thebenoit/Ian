from typing import Any
import os
from dotenv import load_dotenv
from seleniumwire import webdriver  # Import from seleniumwire
import sys

# from setuptools._distutils import version as _version
# sys.modules['distutils.version'] = _version
import seleniumwire.undetected_chromedriver as uc
from seleniumwire.undetected_chromedriver import Chrome
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
import urllib3

# # other
import requests
import json
import time
import random
import urllib
import urllib.parse
from time import sleep

load_dotenv()

from base_tool import BaseTool
from bases.base_scraper import BaseScraper


class SearchFacebook(BaseTool, BaseScraper):

    @property
    def name(self) -> str:
        return "search_facebook"

    @property
    def description(self) -> str:
        return "Search in facebook marketplace for a listing according to the user's request(query)"

    def __init__(self, url: str):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        print("initialisation du scraper facebook...")

        self.url = url
        ##change according to the computer install here: https://googlechromelabs.github.io/chrome-for-testing/#stable
        self.driver = os.getenv("DRIVER_PATH")
        self.har = None
        self.filtered_har = None
        self.listings = []

        proxies = {"http": os.getenv("PROXIES_URL"), "https": os.getenv("PROXIES_URL")}

        proxy_options = {}

        chrome_options = uc.ChromeOptions()
        # ignore ssl errors
        chrome_options.add_argument("--ignore-ssl-errors=yes")
        chrome_options.add_argument("--ignore-certificate-errors")

        print(f"Chrome options chargées")

        service = Service(self.driver)

        # seleniumwire options
        sw_options = {"enable_har": True, "proxy": proxies}
        # self.driver = uc.Chrome(
        #     service=service,
        #     options=chrome_options,
        #     seleniumwire_options={"enable_har": True},

        # )

        # self.filtered_har = self.get_har()

        # create a http session
        self.session = (
            requests.Session()
        )  # Permet de réutiliser connexions, cookies et en-têtes entre plusieurs requêtes.
        self.session.proxies.update(proxies)
        # #ignore ssl errors
        self.session.verify = False

        print("les options de sessions sont chargées")

        self.init_session()

        # #close the driver
        # self.driver.close()

        self.max_retries = 3
        self.retry_delay = 10

    def execute(self, inputs: dict[str, Any]) -> Any:
        query = inputs.get("query")

        return "Facebook search result"

    ##methode to get the har file from the driver
    def get_har(self):
        print("Lancement du driver")
        self.driver.get(self.url)
        time.sleep(15)
        raw_har = self.driver.har
        # si c'est une chaîne JSON, on la parse
        if isinstance(raw_har, str):
            self.har = json.loads(raw_har)
        else:
            self.har = raw_har

        # Extract headers, payload, url and response body for graphql requests
        filtered_har = {
            "log": {
                "entries": [
                    {
                        "request": {
                            "url": entry["request"]["url"],
                            "headers": entry["request"]["headers"],
                            "method": entry["request"]["method"],
                            "postData": entry["request"].get("postData", {}),
                        },
                        "response": {
                            "content": entry["response"].get("content", {}),
                            "headers": entry["response"].get("headers", []),
                            "status": entry["response"].get("status"),
                            "statusText": entry["response"].get("statusText"),
                            "bodySize": entry["response"].get("bodySize"),
                            "body": entry["response"].get("body", ""),
                        },
                    }
                    for entry in self.har["log"]["entries"]
                    if entry["request"].get("url")
                    == "https://www.facebook.com/api/graphql/"
                ]
            }
        }

        # Write filtered HAR data to file
        with open("facebook.har", "w") as f:
            json.dump(filtered_har, f, indent=4)

        return filtered_har

    def get_har_entry(self):
        # Extrait les headers de toutes les requêtes dans le HAR
        try:
            # Ouvre et lit le fichier HAR
            with open("facebook.har", "r") as f:
                try:
                    har_data = json.load(f)
                except json.JSONDecodeError as e:
                    print(f"Erreur de décodage JSON: {e}")
                    return None, None, None
                except Exception as e:
                    print(f"Erreur lors du chargement du fichier HAR: {e}")
                    return None, None, None

            for entry in har_data["log"]["entries"]:

                if "graphql" in entry["request"]["url"]:
                    print("graphql request found")

                    headers = [
                        (h["name"], h["value"]) for h in entry["request"]["headers"]
                    ]
                    payload = entry["request"].get("postData", {}).get("text", "")
                    resp_text = entry["response"].get("content", {}).get("text", "")

                    return headers, payload, json.loads(resp_text)
                else:
                    print("no graphql request found")

            return None, None, None

        except Exception as e:
            print(f"Erreur lors de l'extraction des headers : {e}")
            return None, None, None

    def get_first_req(self):
        self.driver.get(self.url)
        # self.driver.get(f"https://www.facebook.com/marketplace/montreal/propertyrentals?exact=false&latitude=45.50889&longitude=-73.63167&radius=7&locale=fr_CA")

        # allow the page to load fully including any JavaScript that triggers API requests
        time.sleep(5)

        # get first request through selenium to get the headers and first results
        for request in self.driver.requests:
            # if request is a response
            if request.response:
                # if request is a graphql request
                if "graphql" in request.url:
                    print("graphql request found")
                    # decode the response body
                    resp_body = decode(
                        request.response.body,
                        request.response.headers.get("Content-Encoding", "identity"),
                    )
                    # convert the response body to a json object
                    resp_body = json.loads(resp_body)

                    # if the response body contains the data we want
                    if (
                        "marketplace_rentals_map_view_stories"
                        in resp_body["data"]["viewer"]
                    ):
                        print("marketplace_rentals_map_view_stories found")
                        # return the headers, body, and response body
                        return (
                            request.headers.__dict__["_headers"],
                            request.body,
                            resp_body,
                        )
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
        self.session.headers.update(
            {"x-fb-friendly-name": "CometMarketplaceRealEstateMapStoryQuery"}
        )

    # def fetch_graphql_call(query_url_fragments="/api/graphql/",timeout=10000):

    def get_next_cursor(self, body):
        try:
            # On descend dans data.viewer.marketplace_feed_stories.page_info
            page_info = body["data"]["viewer"]["marketplace_feed_stories"]["page_info"]
            raw_cursor = page_info["end_cursor"]

            # raw_cursor est une chaîne JSON encodée, on la parse si possible
            try:
                return json.loads(raw_cursor)
            except json.JSONDecodeError:
                # print(f"raw_cursor: {raw_cursor}")
                # si ce n'est pas du JSON valide, on retourne la chaîne brute
                return raw_cursor

        except KeyError as e:
            print(f"Erreur d'accès aux données : {e}")
            # on peut logger body pour debug :
            # print(json.dumps(body, indent=2))
            return None

    def parse_payload(self, payload):
        # Decode the data string
        # decoded_str = urllib.parse.unquote(payload.decode())

        # Parse the string into a dictionary
        data_dict = dict(urllib.parse.parse_qsl(payload))

        return data_dict

    def init_session(self):

        headers, payload_to_send, resp_body = self.get_har_entry()

        # si le headers n'est pas trouvé
        if headers is None:
            print("no headers found in har file")
            try:
                print("on récupère le har file")
                # on récupère le har file
                self.har = self.get_har()
                # on récupère les headers, payload et resp_body
                headers, payload_to_send, resp_body = self.get_har_entry()

            except Exception as e:
                print(
                    f"Erreur lors de l'obtention de la première requête : {e} header: {headers}"
                )

        self.next_cursor = self.get_next_cursor(resp_body)

        # self.listings.append(resp_body)

        # load headers to requests Sesssion
        self.load_headers(headers)

        # parse payload to normal format
        self.payload_to_send = self.parse_payload(payload_to_send)

        # update the api name we're using (map api)
        self.payload_to_send["fb_api_req_friendly_name"] = (
            "CometMarketplaceRealEstateMapStoryQuery"
        )

        self.variables = json.loads(self.payload_to_send["variables"])
        # self.variables = {"buyLocation":{"latitude":45.4722,"longitude":-73.5848},"categoryIDArray":[1468271819871448],"numericVerticalFields":[],"numericVerticalFieldsBetween":[],"priceRange":[0,214748364700],"radius":2000,"stringVerticalFields":[]}

        # self.driver.close()

    def add_listings(self, body):
        try:
            for node in body["data"]["viewer"]["marketplace_rentals_map_view_stories"][
                "edges"
            ]:
                if (
                    "for_sale_item" in node["node"]
                    and "id" in node["node"]["for_sale_item"]
                ):
                    listing_id = node["node"]["for_sale_item"]["id"]
                    # Utiliser listing_id comme _id dans le document
                    # data = node["node"]

                    # Traitement des images
                    listing_photos = []
                    if "listing_photos" in node["node"]["for_sale_item"]:
                        for photo in node["node"]["for_sale_item"]["listing_photos"]:
                            if "image" in photo:
                                # Modifier L"URL pour obtenir l'image en haute qualité
                                original_url = photo["image"]["uri"]
                                # Remplacer les paramètres de taille dans l'URL
                                # hq_url = original_url.split('?')[0] + "?width=1080&height=1080&quality=original"

                                listing_photos.append(
                                    {
                                        "id": photo.get("id", ""),
                                        "uri": original_url,
                                    }
                                )

                    # Extraire et nettoyer le prix pour le convertir en valeur numérique
                    price_numeric = None
                    if (
                        "formatted_price" in node["node"]["for_sale_item"]
                        and "text" in node["node"]["for_sale_item"]["formatted_price"]
                    ):
                        price_text = node["node"]["for_sale_item"]["formatted_price"][
                            "text"
                        ]
                        # Supprimer les espaces, le symbole $ et convertir en nombre
                        price_numeric = self.clean_price(price_text)

                        # Extraire le nombre de chambres et de salles de bain
                    custom_title = node["node"]["for_sale_item"].get("custom_title", "")
                    bedrooms = self.clean_bedrooms(custom_title)
                    bathrooms = self.clean_bathrooms(custom_title)

                    # Au lieu d'ajouter tout le nœud, créez un nouvel objet avec seulement les champs désirés
                    filtered_data = {
                        "_id": listing_id,
                        "scraped_at": time.time(),  # Ajoute un timestamp UNIX
                        "budget": price_numeric,
                        "bedrooms": bedrooms,
                        "bathrooms": bathrooms,
                        "for_sale_item": {
                            "id": node["node"]["for_sale_item"]["id"],
                            "marketplace_listing_title": node["node"][
                                "for_sale_item"
                            ].get("marketplace_listing_title", ""),
                            "formatted_price": node["node"]["for_sale_item"].get(
                                "formatted_price", {}
                            ),
                            "location": node["node"]["for_sale_item"].get(
                                "location", {}
                            ),
                            "custom_title": node["node"]["for_sale_item"].get(
                                "custom_title", ""
                            ),
                            "custom_sub_titles_with_rendering_flags": node["node"][
                                "for_sale_item"
                            ].get("custom_sub_titles_with_rendering_flags", []),
                            "listing_photos": listing_photos,
                            "share_uri": node["node"]["for_sale_item"].get(
                                "share_uri", ""
                            ),
                        },
                    }
                    # Vérifie si l'annonce existe déjà dans la liste
                    listing_exists = False
                    for listing in self.listings:
                        if listing.get("_id") == listing_id:
                            listing_exists = True
                            break

                    if not listing_exists:
                        print("Ajout de data--------->:")
                        self.listings.append(filtered_data)
        except KeyError as e:
            print(f"Erreur de structure dans le body : {e}")

    def clean_bathrooms(self, custom_title):
        """
        Extrait le nombre de salles de bain à partir du titre personnalisé
        Format typique: "X lits · Y salle de bain"

        Args:
            custom_title (str): Titre personnalisé de l'annonce

        Returns:
            int or None: Nombre de salles de bain ou None si non trouvé
        """
        try:
            if not custom_title:
                return None

            # Recherche le nombre avant "salle de bain" ou "salles de bain"
            import re

            match = re.search(
                r"(\d+)\s*(?:salle de bain|salles de bain|bath|baths)",
                custom_title.lower(),
            )
            if match:
                return int(match.group(1))
            return None
        except:
            return None

    def clean_bedrooms(self, custom_title):
        """
        Extrait le nombre de chambres à partir du titre personnalisé
        Format typique: "X lits · Y salle de bain"

        Args:
            custom_title (str): Titre personnalisé de l'annonce

        Returns:
            int or None: Nombre de chambres ou None si non trouvé
        """
        try:
            if not custom_title:
                return None

            # Recherche le nombre avant "lits" ou "lit"
            import re

            match = re.search(
                r"(\d+)\s*(?:lit|lits|chambre|chambres|bed|beds)", custom_title.lower()
            )
            if match:
                return int(match.group(1))
            return None
        except:
            return None

    def clean_price(self, price):
        try:
            # Supprime tous les caractères non numériques sauf le point
            cleaned = "".join(char for char in price if char.isdigit() or char == ".")
            return float(cleaned)
        except:
            return None

    def scrape(self, lat, lon, query):
        print("Initialisation de la methode Scrape...")
        for attempt in range(self.max_retries):
            # Méthode pour scraper les données à une position géographique donnée
            try:
                # Met à jour les coordonnées de recherche dans les variables
                self.variables["buyLocation"]["latitude"] = lat
                self.variables["buyLocation"]["longitude"] = lon
                self.variables["priceRange"] = [query["minBudget"], query["maxBudget"]]
                # Convertit les variables en JSON et les ajoute au payload
                self.payload_to_send["variables"] = json.dumps(self.variables)

                print("Payload a été mise à jour")

                # Fait une requête POST à l'API GraphQL de Facebook
                resp_body = self.session.post(
                    "https://www.facebook.com/api/graphql/",
                    data=urllib.parse.urlencode(self.payload_to_send),
                )

                print("reponse: ", resp_body.json())

                # Vérifie que la réponse contient bien les données d'appartements
                while (
                    "marketplace_rentals_map_view_stories"
                    not in resp_body.json()["data"]["viewer"]
                ):
                    print("pas le bon type de données")  # Affiche une erreur
                    # print(f" resp json {resp_body.json()["data"]["viewer"]}") # Affiche la réponse pour debug
                    # Réessaie la requête
                    resp_body = self.session.post(
                        "https://www.facebook.com/api/graphql/",
                        data=urllib.parse.urlencode(self.payload_to_send),
                    )
                

                # Ajoute les annonces trouvées à la base de données

                self.listings.append(resp_body.json())
                # self.add_listings(resp_body.json())

            except Exception as e:
                print(f"Erreur lors de la tentative {attempt + 1}: {e}")
                if attempt < self.max_retries - 1:
                    sleep_time = self.retry_delay * (attempt + 1) + random.uniform(1, 5)
                    print(f"Nouvelle tentative dans {sleep_time} secondes...")
                    sleep(sleep_time)
                else:
                    print(
                        "Nombre maximum de tentatives atteint, passage au point suivant"
                    )
                    return False

            # Attend 5 secondes entre chaque requête
            time.sleep(5)
        print(f"listings: {self.listings}")
        return False
