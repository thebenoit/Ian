import json
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from tools.searchFacebook import SearchFacebook


def test_search_facebook():
    query = {"lat":"40.7128","lon":"-74.0060","bedrooms":2,"minBudget":80000,"maxBudget":100000,"bedrooms":3,"minBedrooms":3,"maxBedrooms":4}
    scraper = SearchFacebook("https://www.facebook.com/marketplace/montreal/propertyrentals")
    listings = scraper.scrape(query["lat"], query["lon"],query)
    print("Listings trouvés:")
    print("=" * 50)
    for listing in listings:
        print(json.dumps(listing, indent=2, ensure_ascii=False))
        print("-" * 50)

if __name__ == "__main__":

    test_search_facebook()
    
    