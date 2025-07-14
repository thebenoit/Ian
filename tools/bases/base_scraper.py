from abc import ABC, abstractmethod
import json


class BaseScraper(ABC):
    
    @abstractmethod
    def scrape(self, url: str) -> str:
        """scrape the url and return the data"""
        raise NotImplementedError
    
    def get_har_entry(self):
        # Extrait les headers de toutes les requêtes dans le HAR
        try:
            # Ouvre et lit le fichier HAR
            with open("data/facebook.har", "r") as f:
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

         