import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from tools.searchFacebook import SearchFacebook


def test_search_facebook():
    query = {"lat":"40.7128","lon":"-74.0060","bedrooms":2,"minBudget":80000,"maxBudget":200000}
    scraper = SearchFacebook("https://www.facebook.com/marketplace/montreal/propertyrentals")
    scraper.scrape(query["lat"], query["lon"],query)

if __name__ == "__main__":

    test_search_facebook()
    
    