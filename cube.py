from lib import *
from plane import *

class Cube(object):
  def __init__(self, position, size, material):
      self.position = position
      self.size = size
      self.material = material
      self.half = size / 2
      self.eps =  1e-6
      

  def ray_intersect(self, origin, direction):

      self.faces = [
          Plane(sum(self.position, V3(self.half, 0, 0)), V3(1, 0, 0), self.material),
          Plane(sum(self.position, V3(-self.half, 0, 0)), V3(-1, 0, 0), self.material),
          Plane(sum(self.position, V3(0, self.half, 0)), V3(0, 1, 0), self.material),
          Plane(sum(self.position, V3(0, -self.half, 0)), V3(0, -1, 0), self.material),
          Plane(sum(self.position, V3(0, 0, self.half)), V3(0, 0, 1), self.material),
          Plane(sum(self.position, V3(0, 0, -self.half)), V3(0, 0, -1), self.material)
      ]

      maxArray, minArray = self.getBounds()

      t = float("inf")
      intersect = None

      for plane in self.faces:
          p_intersect = plane.ray_intersect(origin, direction)
          if p_intersect is not None:
              if (
                  p_intersect.point[0] >= minArray[0] and p_intersect.point[0] <= maxArray[0]
              ):
                  if (
                      p_intersect.point[1] >= minArray[1] and p_intersect.point[1] <= maxArray[1]
                  ):
                      if (
                          p_intersect.point[2] >= minArray[2] and p_intersect.point[2] <= maxArray[2]
                      ):
                          if p_intersect.distance < t:
                              t = p_intersect.distance
                              intersect = p_intersect


      if intersect is None:
          return None

      return Intersect(
          distance=intersect.distance, 
          point=intersect.point, 
          normal=intersect.normal, 
      )

  def getBounds(self, ):
    minArray = [0,0,0]
    maxArray = [0,0,0]
    for i in range(3):
        minArray[i] = self.position[i] - (self.eps + self.size / 2)
        maxArray[i] = self.position[i] + (self.eps + self.size / 2)
    
    return maxArray, minArray
