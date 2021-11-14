from lib import *
from plane import *
from triangle import *

class Pyramid(object):

    def __init__(self, vertices, material):
        self.faces = self.generate_faces(vertices, material)
        self.material = material

    def generate_faces(self, vertices, material):
        if len(vertices) != 4:
            return [None, None, None, None]
        v0, v1, v2, v3 = vertices
         # (2, -2, -8),  (1.3, 1.7, -8), (3.3, 1.5, -8),  (1, 1.5, -8) 
        faces = [
            Triangle([v0, v3, v2], material),
            Triangle([v0, v1, v2], material), 
            Triangle([v1, v3, v2], material), 
            Triangle([v0, v1, v3], material), 
        ]
        return faces

    def ray_intersect(self, origin, direction):
        t = float("inf")
        intersect = None

        for triangle in self.faces:
            intersec = triangle.ray_intersect(origin, direction)
            if intersec is not None:
                if intersec.distance < t:
                    t = intersec.distance
                    intersect = intersec

        return intersect