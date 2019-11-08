import sys
from pprint import pprint

import osmium
import pysal.lib.cg as cg

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

	def __init__(self, chunkSize):
		super(HighwayHandler, self).__init__()
		self.highways = []
		self.wk = osmium.geom.WKTFactory()
		self.chunk_size = chunkSize
		self.chunks = []

	def node_to_point(self, node):
		return cg.Point((node.location.lon, node.location.lat))

	def slice_way(self, way):

		chunks = []
		remaining_points = list(map(lambda n: self.node_to_point(n), [*way.nodes]))

		points = []
		dist = 0
		while len(remaining_points) > 0:
			current_point = remaining_points[0]

			if len(points) == 0:
				points += [current_point]
				remaining_points = remaining_points[1:]
			else:
				last_point = points[len(points)-1]
				current_dist = cg.arcdist(last_point, current_point)

				if dist + current_dist > self.chunk_size:
					frac = (self.chunk_size - dist) / current_dist
					new_point = cg.geointerpolate(last_point, current_point, frac)
					remaining_points = [new_point, *remaining_points]
					points += [new_point]

					chunks += [points]
					points = []
					dist = 0

				elif dist + current_dist == self.chunk_size:
					points += [current_point]

					chunks += [points]
					points = []
					dist = 0

				else:
					points += [current_point]
					remaining_points = remaining_points[1:]
					dist += current_dist

		if len(points) > 1:
			chunks += [points]

		return chunks

	def get_dist(self, points):
		dist = 0
		for i in range(0, len(points) - 1):
			dist += cg.arcdist(points[i], points[i+1])
		return dist

	def way(self, w):
		if "highway" in w.tags and w.tags["highway"] not in self.excluded_highways and not w.deleted:
			self.highways += [w]
			if len(w.nodes) > 1:
				chunks = self.slice_way(w)
				print("Highway {} ({}) splitted in {} chunks".format(w.id, w.nodes[0].location, len(chunks)))
			else:
				print("Ignored single-node way at {}".format(w.nodes[0].location), file=sys.stderr)


h = HighwayHandler(0.2)
h.apply_file("data/cesi-ecully.pbf", locations=True)
