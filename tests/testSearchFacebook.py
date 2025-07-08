import json
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from tools.searchFacebook import SearchFacebook


def test_search_facebook():
    query = {"lat":"45.4215","lon":"-75.6990","bedrooms":2,"minBudget":80000,"maxBudget":200000,"bedrooms":3,"minBedrooms":3,"maxBedrooms":4}
    scraper = SearchFacebook()
    
    listings = scraper.scrape(query["lat"], query["lon"],query)
    print("Listings trouvés:")
    print("=" * 50)
    for listing in listings:
        print(f"Titre: {listing['for_sale_item']['marketplace_listing_title']}")
        print(f"Prix: {listing['for_sale_item']['formatted_price']['text']}")
        print(f"Adresse: {listing['for_sale_item']['custom_sub_titles_with_rendering_flags'][0]['subtitle']}")
        print("-" * 50)

if __name__ == "__main__":

    test_search_facebook()
    
    