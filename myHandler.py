import osmium, sqlite3
from typing import Set, Dict, Tuple

class MyHandler(osmium.SimpleHandler):
    def __init__(self, wanted: Set[str]):
        print("MyHandler initialized")
        ##initialiser la sous classe (osmium.SimpleHandler)
        super().__init__()
        self.wanted = wanted
        self.found: Dict[str, Tuple[float,float]] = {}
    
    # called by apply_file    
    def node(self,n):
        #n est un objet de type osmium.Node
        name = n.tags.get("name")
        #si le nom est dans la liste des wanted,
        if name in self.wanted:
            # on ajoute le nom et les coordonnées dans le dictionnaire found
            self.found[name] = (n.lat, n.lon)

    # called by apply_file
    def way(self,w):
        name = w.tags.get("name")
        if name in self.wanted:
            self.found[name] = (w.nodes[0].lat, w.nodes[0].lon)
        

    
        