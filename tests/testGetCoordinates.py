import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.getCooridinates import GetCoordinates

infos = {"city": "Montreal", "location_near": {"amenity": ["college"]}, "radius": "1000"}


if __name__ == "__main__":

    get_coordinates = GetCoordinates()
    print(get_coordinates.execute(**infos))
