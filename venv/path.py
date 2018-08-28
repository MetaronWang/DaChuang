import math


class coordinate:
    def __init__(self):
        latitude = float(0.0)
        longitude = float(0.0)
        height = float(0.0)


def get_relative_coordinate(a, start):
    temp = coordinate()
    temp.height = a.height - start.height
    temp.latitude = a.latitude - start.latitude
    temp.longitude = a.longitude - start.longitude
    return temp


def get_first_angle(a1, a2):
    k1 = a1.latitude * 1.0 / (a1.longitude * 1.0)
    k2 = (a2.latitude - a1.latitude) * 1.0 / ((a2.longitude - a1.longitude) * 1.0)
    single = math.pi + (2 * (math.atan(k1) - math.atan(-1.0 / k2)))
    return single


def get_second_angle(p1,p2,p3):
    a1=coordinate()
    a2=coordinate()
    a1.latitude=p2.latitude-p3.latitude
    a1.longitude=p2.longitude-p3.longitude
    a2.latitude=p1.latitude-p3.latitude
    a2.longitude=p1.longitude-p3.longitude
    k1 = a1.latitude * 1.0 / (a1.longitude * 1.0)
    k2 = (a2.latitude - a1.latitude) * 1.0 / ((a2.longitude - a1.longitude) * 1.0)
    single = math.pi + (2 * math.fmod(math.atan(k1) - math.atan(-1.0 / k2),math.pi/2))
    return math.fmod(single, 2 * math.pi)

def set_first_go_path(a1, a2, a3, angle, n1, n2):
    n = n1 + n2
    x = []
    a = pow(pow(a1.longitude, 2) + pow(a1.latitude, 2), 0.5)
    r = a / (2 * math.sin(angle / 2))
    tan1 = a1.latitude * 1.0 / (a1.longitude * 1.0)
    tan2 = (a2.latitude - a1.latitude) * 1.0 / ((a2.longitude - a1.longitude) * 1.0)
    if(tan1>tan2):
        dir=-1
    else:
        dir=1
    dir = dir * tan1 * tan2 / (math.fabs(tan1) * math.fabs(tan2))
    dir = dir * a1.latitude / (math.fabs(a1.latitude))
    k = dir * a1.longitude / a1.latitude
    temp = pow(1 + pow(k, 2), 0.5)
    o = coordinate()
    o.latitude = a1.latitude / 2 - (r * k) / temp
    o.longitude = a1.longitude / 2 - r / temp
    o.height = a1.height
    k0 = o.latitude / o.longitude
    k1 = (a1.latitude - o.longitude) / (a1.latitude - o.latitude)
    s0 = math.atan(k0)
    s1 = math.atan(k1)
    temp_c = coordinate()
    show_coordinate(o)
    print r
    '''
    for i in range(0, n1):
        temp_c.longitude = r * math.cos(s0 + i / (n1 - 1) * (s1 - s0)) + o.longitude
        temp_c.latitude = r * math.sin(s0 + i / (n1 - 1) * (s1 - s0)) + o.latitude
        temp_c.height = i / (n1 - 1) * a1.height
        x.append(temp_c)
    for i in range(1, n):
        temp_c.longitude = a1.longitude + (i - n1) / (n2 - 1) * (a2.longitude - a1.longitude)
        temp_c.latitude = a1.latitude + (i - n1) / (n2 - 1) * (a2.latitude - a1.latitude)
        temp_c.height = a1.height + (i - n1) / (n2 - 1) * (a2.height - a1.height)
        x.append(temp_c)
    return x
    '''


def set_second_go_path(p1,p2, p3,angle, n):
    x = []
    angle = angle#+(math.pi*2 - angle)*2/3
    a1 = coordinate()
    a2 = coordinate()
    a1.latitude = p2.latitude - p3.latitude
    a1.longitude = p2.longitude - p3.longitude
    a2.latitude = p1.latitude - p3.latitude
    a2.longitude = p1.longitude - p3.longitude
    a = pow(pow(a1.longitude, 2) + pow(a1.latitude, 2), 0.5)
    r = a / (2 * math.sin(angle / 2))
    tan1 = a1.latitude * 1.0 / (a1.longitude * 1.0)
    tan2 = (a2.latitude - a1.latitude) * 1.0 / ((a2.longitude - a1.longitude) * 1.0)
    if (tan1 > tan2):
        dir = -1
    else:
        dir = 1
    dir = dir * tan1 * tan2 / (math.fabs(tan1) * math.fabs(tan2))
    dir = dir * a1.latitude / (math.fabs(a1.latitude))
    k = dir * a1.longitude / a1.latitude
    temp = pow(1 + pow(k, 2), 0.5)
    o = coordinate()
    o.latitude = a1.latitude / 2 - (r * k) / temp + p3.latitude
    o.longitude = a1.longitude / 2 - r / temp + p3.longitude
    o.height = p1.height
    k1 = (o.latitude-p3.latitude) / (o.longitude-p3.longitude)
    k0 = (p2.latitude - o.longitude) / (p2.latitude - o.latitude)
    s0 = math.atan(k0)
    s1 = math.atan(k1)
    temp_c = coordinate()
    show_coordinate(o)
    print r
    '''
    for i in range(0, n):
        temp_c.longitude = r * math.cos(s0 + i / (n - 1) * (s1 - s0)) + o.longitude
        temp_c.latitude = r * math.sin(s0 + i / (n - 1) * (s1 - s0)) + o.latitude
        #temp_c.height = a1.height
        x.append(temp_c)
        return x
    '''


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

def set_path(x):
    p1 = x[0]
    p2 = x[1]
    p3 = x[2]
    '''
    show_coordinate(p1)
    show_coordinate(p2)
    show_coordinate(p3)
    '''
    a2 = get_first_angle(p1, p2)
    a3 = get_first_angle(p1, p3)
    if (a3 > a2):
        temp = p3
        p3 = p2
        p2 = temp
    k1 = p1.latitude * 1.0 / (p1.longitude * 1.0)
    k2 = (p2.latitude - p1.latitude) * 1.0 / ((p2.longitude - p1.longitude) * 1.0)
    k3 = (p3.latitude - p1.latitude) * 1.0 / ((p3.longitude - p1.longitude) * 1.0)
    set_first_go_path(p1, p2, p3, get_first_angle(p1, p2), 100, 100)
    set_second_go_path(p1,p2, p3, get_second_angle(p1,p2,p3),200)





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

o.longitude = float(0.0)
o.latitude = float(0.0)
o.height = float(20.0)

x = the_first_point(get_relative_coordinate(a1,o),get_relative_coordinate(a2,o),get_relative_coordinate(a3,o))
for i in x:
    show_coordinate(i)

