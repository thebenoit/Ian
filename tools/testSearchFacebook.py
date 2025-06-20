import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from tools.searchFacebook import SearchFacebook


def test_search_facebook():
    scraper = SearchFacebook("https://www.facebook.com/marketplace/montreal/propertyrentals")
    #scraper.scrape(45.50889, -73.63167)

if __name__ == "__main__":
    test_search_facebook()