class MapGraph:

	nodes = {}

	def add_node(self, id, lat, lon):
		self.nodes[id] = MapGeoNode(id, lat, lon)

	def add_relation(self, fromNodeId, toNodeId):
		self.nodes[fromNodeId].add_relation(self.nodes[toNodeId])


class MapGeoNode:

	id = None
	latlon = None
	relations = None

	def __init__(self, id, lat, lon):
		self.latlon = (lat, lon)
		self.relations = dict()
		self.id = id

	def add_relation(self, toNode):
		self.relations[toNode.id] = toNode