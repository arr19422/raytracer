from lib import *
from plane import *

class Triangle(object):

    def __init__(self, vertices, material):
        self.material = material
        self.eps = 1e-6
        self.p1 = vertices[0]
        self.p2 = vertices[1]
        self.p3 = vertices[2]

    def ray_intersect(self, org, dir):
        
        normal = cross(sub(self.p2, self.p1), sub(self.p3, self.p1))
        distance = dot(normal, self.p1)
        d = dot(normal, dir)

        if d < 0:
            d = d * (-1)

        if d < self.eps:

            return None

        else:
            
            L = (dot(normal, org) + distance) / d

            div = L / d

            if L < 0:
                return None
            else:

                point = sum(org, mul(dir, L))
                u, v, w = barycentric(self.p1, self.p2, self.p3, point)

                if w < 0 or v < 0 or u < 0:
                    return None
                else:
                    return Intersect(distance=distance, point=point, normal=norm(normal))