from tools.getCooridinates import GetCoordinates

infos = {"city": "Montreal", "location_near": {"amenity": ["cafe"]}, "radius": "1000"}


if __name__ == "__main__":

    get_coordinates = GetCoordinates()
    print(get_coordinates.execute(**infos))
