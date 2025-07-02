from tools.base_tool import BaseTool
from myHandler import MyHandler

from typing import List


class GetCoordinates(BaseTool):
    def __init__(self):
        self.osm_file = "Montreal.osm.pbf"

    def execute(self, city: str, location_near: List[str], radius: str):
        
        wanted = set(location_near)
        handler = MyHandler(wanted)
        
        handler.apply_file(self.osm_file, locations=True)
        
        return [
            {
                "name": name,
                "lat": lat,
                "lon": lon
            }
            for name, (lat, lon) in handler.found.items()
        ]
        
        
        
    
    
    
    
    
    
    
    
    