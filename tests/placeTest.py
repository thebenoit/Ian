import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.googlePlaces import GooglePlaces




if __name__ == "__main__":
    google_places = GooglePlaces()
    google_places.execute("Montreal",["Haitian food"])