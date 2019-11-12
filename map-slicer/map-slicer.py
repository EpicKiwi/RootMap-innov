import sys
import mapGraph
import osmium

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
		self.graph = mapGraph.MapGraph()

	def add_way(self, way):
		for i in range(0, len(way.nodes) - 1):
			node = way.nodes[i]
			next_node = way.nodes[i+1]

			if i == 0:
				self.graph.add_node(node.ref, node.location.lat, node.location.lon)

			self.graph.add_node(next_node.ref, next_node.location.lat, next_node.location.lon)

			self.graph.add_relation(node.ref, next_node.ref)
			self.graph.add_relation(next_node.ref, node.ref)

	def way(self, w):
		if "highway" in w.tags and w.tags["highway"] not in self.excluded_highways and not w.deleted:
			self.highways += [w]
			if len(w.nodes) > 1:
				self.add_way(w)
				print("Added way {} ({}) to graph".format(w.id, w.nodes[0].location))
			else:
				print("Ignored single-node way at {}".format(w.nodes[0].location), file=sys.stderr)


h = HighwayHandler()
h.apply_file("data/cesi-ecully.pbf", locations=True)