import struct

class V3 (object):
    def __init__(self, x, y, z = None):
        self.x = x
        self.y = y
        self.z = z
    
    def __getitem__(self, i):
        if i == 0:
            return self.x
        elif i == 1:
            return self.y
        elif i == 2:
            return self.z
    
    def __repr__(self):
        return "V3(%s, %s, %s)" % (self.x, self.y, self.z)

def ccolor(v):
    return max(0, min(255, int(v)))

class color(object):
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def __repr__(self):
        b = ccolor(self.b)
        g = ccolor(self.g)
        r = ccolor(self.r)

        return "ccolor(%s, %s, %s)" % (r, g, b)

    def toBytes(self):
        b = ccolor(self.b)
        g = ccolor(self.g)
        r = ccolor(self.r)

        return bytes([b, g, r])

    def __add__ (self, other):
        r = ccolor(self.r + other.r)
        g = ccolor(self.g + other.g)
        b = ccolor(self.b + other.b)

        return color(r, g, b)

    def __mul__(self, k):
        r = ccolor(self.r * k)
        g = ccolor(self.g * k)
        b = ccolor(self.b * k)

        return color(r, g, b)

def sum(v0, v1):
    return V3(v0.x + v1.x, v0.y + v1.y, v0.z + v1.z)

def sub(v0, v1):
    return V3(v0.x - v1.x, v0.y - v1.y, v0.z - v1.z)


def mul(v0, k):
    return V3(v0.x * k, v0.y * k, v0.z * k)

def dot(v0, v1):
    return v0.x * v1.x + v0.y * v1.y + v0.z * v1.z

def length(v0):
    return (v0.x**2 + v0.y**2 + v0.z**2)**0.5

def norm(v0):
    v0length = length(v0)

    if not v0length:
        return V3(0, 0, 0)

    return V3(v0.x/v0length, v0.y/v0length, v0.z/v0length)

def cross(v1, v2):
    return V3(
        v1.y * v2.z - v1.z * v2.y,
        v1.z * v2.x - v1.x * v2.z,
        v1.x * v2.y - v1.y * v2.x,
    )

def barycentric(A, B, C, P):
    bc = cross(
        V3(B.x - A.x, C.x - A.x, A.x - P.x),
        V3(B.y - A.y, C.y - A.y, A.y - P.y)
    )

    if abs(bc.z) < 1:
        return -1, -1, -1

    u = bc.x/bc.z
    v = bc.y/bc.z
    w = 1 - (bc.x + bc.y)/bc.z

    return w, v, u

def bbox(*vertices):
    xs = [vertex.x for vertex in vertices]
    ys = [vertex.y for vertex in vertices]

    return (max(xs), max(ys), min(xs), min(ys))

def char(c):
    return struct.pack('=c', c.encode('ascii'))


def word(w):
    return struct.pack('=h', w)


def dword(d):
    return struct.pack('=l', d)

def glWriteBmp(filename, width, height, buffer):
    f = open(filename, 'wb')

    f.write(char('B'))
    f.write(char('M'))
    f.write(dword(14 + 40 + width * height * 3))
    f.write(dword(0))
    f.write(dword(14 + 40))

    f.write(dword(40))
    f.write(dword(width))
    f.write(dword(height))
    f.write(word(1))
    f.write(word(24))
    f.write(dword(0))
    f.write(dword(width * height * 3))
    f.write(dword(0))
    f.write(dword(0))
    f.write(dword(0))
    f.write(dword(0))

    for x in range(height):
        for y in range(width):
            f.write(buffer[x][y].toBytes())

    f.close()

def reflect(I, N):
    return norm(sub(I, mul(N, 2 * dot(I, N))))

def refract(I, N, refractive_index):
    cosi = -max(-1, min(1, dot(I, N)))

    etai = 1
    etat = refractive_index

    if cosi < 0:
        cosi = -cosi
        etai, etat = etat, etai
        N = mul(N, -1)

    eta = etai / etat
    k = 1 - eta**2 * (1 - cosi**2)

    if k < 0:
        return None
    
    k = k**1/2

    return norm(sum(mul(I, eta), mul(N, (eta * cosi) + k**0.5)))



################################################################################
########################## Materiales ##########################################
################################################################################

class Material(object):
    def __init__(self, diffuse, albedo, spec, refractive_index= 0):
        self.diffuse = diffuse
        self.albedo = albedo
        self.spec = spec
        self.refractive_index = refractive_index

class Intersect(object):
    def __init__(self, distance, point, normal):
        self.distance = distance
        self.point = point
        self.normal = normal

class Light(object):
    def __init__(self, position, intensity, color):
        self.position = position
        self.intensity = intensity
        self.color = color