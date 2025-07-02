from myHandler import MyHandler

def fetch_osm_feature(pbf_path,filter):
    my_handler = MyHandler(filter)
    my_handler.apply_file(pbf_path)
    return my_handler.results


if __name__ == "__main__":
    def is_cafe(entity):
        return entity.tags.get("amenity") == "cafe"
    
cafes = fetch_osm_feature("Montreal.osm.pbf",is_cafe)
print(f"found {len(cafes)} cafes")

for cafe in cafes[:100]:
        print(cafe["id"], cafe["lat"], cafe["lon"], cafe["tags"].get("name"))
    
    # results = fetch_osm_feature("data/montreal.pbf",lambda n: "amenity" in n.tags)
    # print(results)
    