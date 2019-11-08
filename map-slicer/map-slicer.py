import osmium
import shapely.wkb as wkblib

class HighwayHandler(osmium.SimpleHandler):

    excluded_highways = [
        "pedestrian",
        "bus_guideway",
        "escape",
        "footway",
        "bridleway",
        "steps",
        "path",
        "cycleway",
        "proposed",
        "construction",
        "bus_stop",
        "crossing",
        "elevator",
        "emergency_access_point",
        "give_way",
        "milestone",
        "platform"
    ]

    def __init__(self):
        super(HighwayHandler, self).__init__()
        self.highways = []

    def way(self, w):
        if "highway" in w.tags and w.tags["highway"] not in self.excluded_highways and not w.deleted:
            self.highways += [w]


h = HighwayHandler()
h.apply_file("data/cesi-ecully.pbf", locations=True)
print(len(h.highways))