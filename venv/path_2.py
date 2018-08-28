import math


class coordinate:
    def __init__(self):
        latitude = float(0.0)
        longitude = float(0.0)
        height = float(0.0)

def the_first_point(a1, a2, a3):
    b1 = pow(a1.latitude, 2) + pow(a1.longitude, 2)
    b2 = pow(a2.longitude, 2) + pow(a2.latitude, 2)
    b3 = pow(a3.latitude, 2) + pow(a3.longitude, 2)
    p1 = coordinate()
    p2 = coordinate()
    p3 = coordinate()
    if (b1 <= b2 and b1 <= b3):
        p1 = a1
        p2 = a2
        p3 = a3
    else:
        if (b2 <= b1 and b2 <= b3):
            p1 = a2
            p2 = a1
            p3 = a3
        else:
            if (b3 <= b2 and b3 <= b1):
                p1 = a3
                p2 = a1
                p3 = a2
    x = [p1, p2, p3]
    return x

def show_coordinate(a):
    str="(%f,%f,%f)"%(a.longitude,a.latitude,a.height)
    print str

def first_O(p1,p2):
    k1 =  (p1.longitude * -1.0) / (p1.latitude * 1.0)
    k2 = ((p2.longitude - p1.longitude) * -1.0) / ((p2.latitude - p1.latitude) * 1.0)
    print k1
    print k2
    a1 = p1.longitude * 1.0 / 2
    b1 = p1.latitude * 1.0 / 2
    a2 = p2.longitude
    b2 = p2.latitude
    print "%f %f %f %f"%(a1,b1,a2,b2)
    O = coordinate()
    O.longitude = (b1 - b2 + k2 * a2 - k1 * a1) / (k2 - k1)
    O.latitude = k1 * (O.longitude - a1) + b1
    O.height = 0
    return O

def path(x):
    p1 = x[0]
    p2 = x[1]
    p3 = x[2]


a1 = coordinate()
a2 = coordinate()
a3 = coordinate()
o = coordinate()

a1.longitude = float(2.0)
a1.latitude = float(3.0)
a1.height = float(20.0)

a2.longitude = float(4.0)
a2.latitude = float(1.0)
a2.height = float(20.0)

a3.longitude = float(5.0)
a3.latitude = float(4.0)
a3.height = float(20.0)


show_coordinate(first_O(a1,a2))