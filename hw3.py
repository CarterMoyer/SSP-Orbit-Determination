from math import *

# problem 1a
# takes sin and cos and outputs approrpiate value in corresponding quadrant
def rads(sin, cos):
    if sin < 0:
        angle = 2*pi - acos(cos)
    else:
        angle = acos(cos)
    return angle

# problem 1b
def sphere_tri(side1, side2, angle3):
    deg = 0 # keeps track of if the inputs are degrees or radians
    if side1 > 2 * pi: # an assumption that degree values will not be < 2pi
        side1 = side1 * pi / 180
        deg = 1
    if side2 > 2 * pi:
        side2 = side2 * pi / 180
        deg = 1
    if angle3 > 2 * pi:
        angle3 = angle3 * pi / 180
        deg = 1
    cos_side3 = cos(side1) * cos(side2) + sin(side1) * sin(side2) * cos(angle3)
    side3 = acos(cos_side3)
    cos_angle1 = (cos(side1) - cos(side2) * cos(side3)) / (sin(side2) * sin(side3))
    angle1 = acos(cos_angle1)
    cos_angle2 = (cos(side2) - cos(side1) * cos(side3)) / (sin(angle1) * sin(angle3))
    angle2 = acos(cos_angle2)
    if deg == 1:
        side3 = side3 * 180 / pi
        angle1 = angle1 * 180 / pi
        angle2 = angle2 * 180 / pi
    return "First angle value: ", angle1, "Second angle value: ", angle2, "Side length: ",side3


# problem 2a
# rotates a vector
def co_rot(vector, angle, axis):
    matrix = []
    vector_final = []
    angle = angle * pi / 180
    a = 0 # final matrix
    if axis == 'x':
        matrix = [ [1, 0, 0],
                   [0, cos(angle), sin(angle)],
                   [0, -sin(angle), cos(angle)]]
    if axis == 'y':
        matrix = [ [cos(angle), 0, -sin(angle)],
                   [0, 1, 0],
                   [sin(angle), 0, cos(angle)]]
    if axis == 'z':
        matrix = [ [cos(angle), sin(angle), 0],
                   [-sin(angle), cos(angle), 0],
                   [0, 0, 1]]
    for row in range(3):
        for i in range(3):
            a += matrix[row][i] * vector[i]
        vector_final.append(a)
        a = 0
    return vector_final


# returns the final after x rotations
def co_rot_x(vector, angle, axis):
    vector_i = list(vector)
    for i in range(len(axis)):
        vector = co_rot(vector, angle[i], axis[i])
    print('Input angles: ', angle)
    print('Input vector: ', vector_i)
    print('Expected vector: [0.13835636117566708, -2.3771265213278054, 4.830127018922194]')
    print('Rotated vector: ', vector)

import matplotlib.pyplot as plt
import numpy as np
# problem 8
# spherical trigonometry and distance between points
def earth_trig(point1_deg, point2_deg):
    r = 6371
    p1 = [r]
    p2 = [r]
    angle = 0
    for i in range(2):
        p1.append(point1_deg[i] * pi / 180)
        p2.append(point2_deg[i] * pi / 180)
    long_dif = (p1[1] - p2[1])
    angle = acos(sin(p1[2]) * sin(p2[2]) + cos(p1[2]) * cos(p2[2]) * cos(long_dif))
    distance = r * angle
    print('Locations chosen: Boulder and Hong Kong')
    print('Long and lat of Boulder: 40.0076N, 105.2659W')
    print('Long and lat of Hong Kong: 22.2193N, 114.1694W')
    print('Distance according to web applet: 11970 km')
    print('Distance according to code: ', distance, 'km')
##earth_trig([114.1694, 22.2193], [-105.2659, 40.0076])


# 8c
#spherical trigonometry beteen asteroid and moon
import odlib as od
def moon_asteroid(pos):
    moon_RA_deg = od.HMStoDeg(pos[0])
    ast_RA_deg = od.HMStoDeg(pos[1])
    moon_dec_deg = od.DMStoDeg(pos[2])
    ast_dec_deg = od.DMStoDeg(pos[3])
    angle = 0

    m_RA = moon_RA_deg * pi / 180
    a_RA = ast_RA_deg * pi / 180
    m_dec = moon_dec_deg * pi / 180
    a_dec = ast_dec_deg* pi /180

    RA_dif = abs(m_RA - a_RA)
    angle = acos(sin(m_dec) * sin(a_dec) + cos(m_dec) * cos(a_dec) * cos(RA_dif))
    ang_sep_deg = angle / pi * 180
    deg = int(ang_sep_deg)
    minute = int((ang_sep_deg - int(ang_sep_deg)) * 60)
    sec = ang_sep_deg % 15 / 1000 * 60

    ang_sep = str(deg) + ':' + str(minute) + ':' + str(sec)

    print('Date and time: July 7 05:00 to 08:00 UTC')
    print('RA and Dec for 99795: 17:37:59.80, -24:55:30.8')
    print('RA and Dec for moon: 11:07:22.52, +09:31:09.1')
    print('Angular separation between the Moon and 99795: ', ang_sep)
##moon_asteroid([[11,7,22.52], [9,31,9.1], [17,27,59.8], [-24,55,30.8]])

# problem 12
# a
# canon projectile simulation

def canon(speed_i, angle):
    delT = 0.2
    time = np.arange(0, 8, delT)
    flight_time = 0
    x = 0
    y = 0
    plt.figure()
    theta = angle / 180 * pi
    v0x = speed_i * cos(theta)
    v0y = speed_i * sin(theta)
    for t in time:
        v0y -= 9.81 * delT
        x += v0x * delT
        y += v0y * delT
        flight_time += delT
        plt.plot(x, y, 'bo')
        plt.ylim(0, 40)
        plt.xlim(0, 40)
        plt.pause(delT)
        if y <= 0:
            v0y = 0
            v0x = 0
            delT = 0
        print(x, 'meters')

# b
# football projectile simulation w/ air
def football(speed_i):
    delT = 0.2
    time = np.arange(0, 10, delT)
    flight_time = 0
    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0
    plt.figure()
    theta = 45 / 180 * pi
    v0x1 = speed_i * cos(theta)
    v0y1 = speed_i * sin(theta)
    v0x2 = speed_i * cos(theta)
    v0y2 = speed_i * sin(theta)
    b = 1.358 * 10**-3
    for t in time:
        v0y1 -= 9.81 * delT + (b * v0y1**2)/0.4 * delT
        v0x1 -= (b * v0y1**2)/0.4 * delT
        x1 += v0x1 * delT
        y1 += v0y1 * delT
        v0y2 -= 9.81 * delT
        x2 += v0x2 * delT
        y2 += v0y2 * delT
        flight_time += delT
        plt.plot(x1, y1, 'bo')
        plt.plot(x2, y2, 'go')
        plt.ylim(0, 80)
        plt.xlim(0, 110)
        plt.pause(delT)
        if y1 <= 0:
            v0y1 = 0
            v0x1 = 0
            print(x1, 'meters')
        if y2 <= 0:
            v0y2 = 0
            v0x2 = 0
            delT = 0
            print(x2, 'meters w/o air')


# problem 13
# returns the slope and best fit line of a set of data points
def best_fit(x_val, y_val):
    x1 = []
    y1 = []
    for i in range(len(x_val)):
        x1.append(x_val[i])
        y1.append(y_val[i])
        
    xbar = sum(x_val)/len(x_val)
    ybar = sum(y_val)/len(y_val)
    n = len(x_val)

    top = sum([xi*yi for xi,yi in zip(x_val, y_val)]) - n * xbar * ybar # looked up a way to collate data on stack overflow
    bottom = sum([xi**2 for xi in x_val]) - n * xbar**2

    b = top / bottom
    a = ybar - b * xbar
    plt.scatter(x1,y1)
    yfit = [a + b * xi for xi in x_val]
    plt.plot(x_val, yfit)
    plt.show()

best_fit([1, 2.6, 3, 4.3, 5.7, 6.1, 7.7, 9], [0.5, 2, 3.7, 3.5, 4.2, 6, 8, 7.9])
