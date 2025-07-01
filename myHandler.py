import osmium

class MyHandler(osmium.SimpleHandler):
    def __init__(self, filter_fn):
        print("MyHandler initialized")
        ##initialiser la sous classe (osmium.SimpleHandler)
        super().__init__()
        self.filter_fn = filter_fn
        self.results = []
        
    def node(self,n):
        if self.filter_fn(n):
            self.results.append({
                "type":"node",
                "id":n.id,
                "lat":n.lat,
                "lon":n.lon,
                "tags":dict(n.tags),
                
            })
            
    def way(self,w):
        if self.filter_fn(w):
            self.results.append({
                "type":"way",
                "id":w.id,
                "refs":list(w.nodes),
                "tags":dict(w.tags),
            })
        

    
        