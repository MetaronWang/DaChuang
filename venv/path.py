import math


class coordinate:
    def __init__(self):
        latitude = 0.0
        longitude = 0.0
        height = 0.0


def get_relative_coordinate(a, start):
    temp = coordinate()
    temp.height = a.height - start.height
    temp.latitude = a.latitude - start.latitude
    temp.longitude = a.longitude - start.longitude
    return temp


def get_first_angle(a1, a2):
    k1 = a1.latitude * 1.0 / (a1.latitude * 1.0)
    k2 = (a2.latitude - a1.latitude) * 1.0 / ((a2.longitude - a1.longitude) * 1.0)
    single = 2 * (math.atan(k1) - math.atan(-1.0 / k2))
    return math.fmod(single, 2 * math.pi)


def get_second_angle(k1, k2):
    return math.fmod((math.pi - abs(math.atan(k1) - math.atan(k2))), (2 * math.pi))


def set_first_go_path(a1, a2, a3, angle, n1, n2):
    n = n1 + n2
    x = []
    a = pow(pow(a1.longitude, 2) + pow(a1.latitude, 2), 0.5)
    r = a / (2 * math.sin(angle / 2))
    k = -1.0 * a1.longitude / a1.latitude
    temp = pow(1 + pow(k, 2), 0.5)
    o = coordinate
    o.latitude = a1.latitude / 2 - (r * k) / temp
    o.longitude = a1.longitude / 2 - r / temp
    k0 = o.latitude / o.longitude
    k1 = (a1.latitude - o.longitude) / (a1.latitude - o.latitude)
    s0 = math.atan(k0)
    s1 = math.atan(k1)
    temp_c = coordinate()
    for i in range(0, n1):
        temp_c.longitude = r * math.cos(s0 + i / (n1 - 1) * (s1 - s0)) + o.longitude
        temp_c.latitude = r * math.sin(s0 + i / (n1 - 1) * (s1 - s0)) + o.latitude
        temp_c.height = i / (n1 - 1) * a1.height
        x[i] = temp_c

    for i in range(1, n):
        temp_c.longitude = a1.longitude + (i - n1) / (n2 - 1) * (a2.longitude - a1.longitude)
        temp_c.latitude = a1.latitude + (i - n1) / (n2 - 1) * (a2.latitude - a1.latitude)
        temp_c.height = a1.height + (i - n1) / (n2 - 1) * (a2.height - a1.height)
        x[i] = temp_c
    return x


def set_second_go_path(p2, p3, k1, k2, angle, n):
    l = pow(pow(p3.latitude - p2.latitude, 2) + pow(p3.longitude - p2.longitude, 2), 0.5)
    r = l / (2 * math.sin(angle / 2))
    k_1 = (-1.0) / k1
    k_2 = (-1.0) / k2
    temp_1 = pow(1 + pow(k_1, 2), 0.5)
    temp_2 = pow(1 + pow(k_2, 2), 0.5)
    a_1 = coordinate()
    a_2 = coordinate()
    b_1 = coordinate()
    b_2 = coordinate()
    a_1.latitude = p2.latitude / 2 - (r * k_1) / temp_1
    a_1.longitude = p2.longitude / 2 - r / temp_1
    a_2.latitude = p2.latitude / 2 + (r * k_1) / temp_1
    a_2.longitude = p2.longitude / 2 + r / temp_1
    b_1.latitude = p3.latitude / 2 - (r * k_2) / temp_2
    b_1.longitude = p3.longitude / 2 - r / temp_2
    b_2.latitude = p3.latitude / 2 + (r * k_2) / temp_2
    b_2.longitude = p3.longitude / 2 + r / temp_2
    o = coordinate
    if (a_1.longitude == b_1.longitude & a_1.latitude == b_1.latitude):
        o = a_1

    else:
        if (a_1.longitude == b_2.longitude & a_1.latitude == b_2.latitude):
            o = a_1
        else:
            o = a_2  # 上面两步可以确定a_1不是所要找的点，计算无误情况下，可以确定a_2即为正确的圆心

    k_begin = (p2.latitude - o.latitude) / (p2.longitude - o.longitude)
    k_end = (p3.latitude - o.latitude) / (p3.longitude - o.longitude)  # 从p2开始，从p3结束，通过圆的参数方程进行计算
    s_begin = math.atan(k_begin)
    s_end = math.atan(k_end)
    x = []
    temp_c = coordinate()
    for i in range(0, n):
        temp_c.longitude = r * math.cos(s_begin + i / (n - 1) * (s_end - s_begin)) + o.longitude
        temp_c.latitude = r * math.sin(s_begin + i / (n - 1) * (s_end - s_begin)) + o.latitude
        temp_c.height = p2.height + i / (n - 1) * (p3.height - p2.height)
        x[i] = temp_c
    return x


def the_first_point(a1, a2, a3):
    b1 = pow(a1.latitude, 2) + pow(a1.longitude, 2)
    b2 = pow(a2.longitude, 2) + pow(a2.latitude, 2)
    b3 = pow(a3.latitude, 2) + pow(a3.longitude, 2)
    p1 = coordinate()
    p2 = coordinate()
    p3 = coordinate()
    if (b1 >= b2 and b1 >= b3):
        p1 = a1
        p2 = a2
        p3 = a3
    else:
        if (b2 >= b1 and b2 >= b3):
            p1 = a2
            p2 = a1
            p3 = a3
        else:
            if (b3 >= b2 and b3 >= b1):
                p1 = a3
                p2 = a1
                p3 = a2
    x = [p1, p2, p3]
    return x


def set_path(x):  # x是三个坐标点的集合
    p1 = x[0]
    p2 = x[1]
    p3 = x[2]
    a2 = get_first_angle(p1, p2)
    a3 = get_first_angle(p1, p3)
    if (a3 > a2):
        temp = p3
        p3 = p2
        p2 = temp
    k1 = p1.latitude * 1.0 / (p1.longitude * 1.0)
    k2 = (p2.latitude - p1.latitude) * 1.0 / ((p2.longitude - p1.longitude) * 1.0)
    k3 = (p3.latitude - p1.latitude) * 1.0 / ((p3.longitude - p1.longitude) * 1.0)
    path = set_first_go_path(p1, p2, p3, get_first_angle(p1, p2), 100, 100) + set_second_go_path(p2, p3, k2, k3,get_second_angle(k2,k3),200)
    # path为路径的集合


