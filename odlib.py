# computes the dot product of two vectors
def dot(v1,v2):
    dot_product = v1[0]*v2[0]+v1[1]*v2[1]+v1[2]*v2[2]
    return dot_product


# computes the cross product of two vectors
def cross(v1,v2):
    cross_product = []
    cross_product.append(v1[1]*v2[2] - v1[2]*v2[1])
    cross_product.append(-(v1[0]*v2[2] - v1[2]*v2[0]))
    cross_product.append(v1[0]*v2[1] - v1[1]*v2[0])
    return cross_product


# computes the triple product of three vectors
def tri_product(v1,v2,v3):
    c = cross(v2,v3)
    d = dot(v1,c)
    return d


# computes the local sidereal time from a given date and time
def lst(year, month, day, hour, minute, second):
    HMS = str(hour) + 'h : ' + str(minute) + 'm : ' + str(second) + 's'     
    longitude = 105.2705
    UT = [hour + 6, minute, second]
    UTC = UT[0] + UT[1] / 60 + UT[2] / 3600
    J0 = 367 * year - int((7 * (year + int((month + 9) / 12))) / 4) + int(275 * month / 9 ) + day + 1721013.5
    J = (J0 - 2451545) / 36525
    theta0 = (100.46061837 + (36000.77053608 * J) + (3.87933 * (10**-4) * (J**2)) - ((J**3) / (3.871 * 10**7))) % 360
    thetag = (theta0 + (360.985647366 * (UTC/24)))
    theta = (thetag - longitude) % 360
    hour1 = theta / 15
    minute1 = (theta % 15) * 4
    second1 = ((theta % 15) % 0.25) * 3600 / 15
    LST = str(int(hour1)) + 'h : ' + str(int(minute1)) + 'm : ' + str(second1) + 's'
    return 'Local time is ' + HMS + ', Expected LST is 6h : 40m : 10s, Calculated LST is ' + LST



#numerically calculates an integral
import numpy as np
from math import *
def integ(N):
    r = 0
    for i in np.arange(4 + 4/N, 12, 8/N):
        r += ((i**3 + 2 * sin(10/i))**.5) * (8 / N)
    return r
# Wolfram Alpha gives an answer of 187.107 or 187.11 using 5 sigfigs
# The integral can be calculated to an accurate 5 sigfigs with an N equal to 60 or greater


# Uncertainty of the mean
# Calculates the mean of a list
def mean(a):
    sum0 = 0
    for i in range(len(a)):
        sum0 += a[i]
    mean1 = sum0/len(a)
    return mean1


# Calculates the standard deviation within a list
def stdev():
    a = [6.2, 5.9, 5.8, 6.3, 6.1, 6.5, 6.2, 6.0, 6.1, 6.1, 6.4]
    sum0 = 0
    for i in range(len(a)):
        sum0 += (a[i] - mean())**2
    sd1 = (sum0/(len(a)-1))**.5
    return sd1    

# computes the RA value from HH:MM:SS to degrees
def HMStoDeg(hms):
    degrees = hms[0]*15 + hms[1]*15/60 + hms[2]*15/3600
    return degrees


# converts the declination from minutes and seconds to decimal
def DMStoDeg(dms):
    if dms[0] < 0:
        decimal = dms[0] - dms[1]/60 - dms[2]/3600
    else:
        decimal = dms[0] + dms[1]/60 + dms[2]/3600
    return decimal


# converts a right ascention from decimal form to hours minutes and seconds
def RAdecimalToHMS(deg):
    hour = int(deg / 15)
    # convert to an integer the decimal value times 60 of the RA
    minute = int(deg % 15 * 60 / 15)
    second = (deg % 15 * 60 / 15) % 1 * 60
    HMS = [hour, minute, second]
    return HMS


# converts the declination in decimal form to hours minutes and seconds
def DECdecimalToDMS(angle):
    degrees = int(angle)
    angle -= degrees
    if angle < 0:
        angle *= -1
    # convert to an integer the decimal value times 60 of the declination
    minute = int(angle * 60)
    # only multiply the digits after floating point 2
    angle %= (1/60)
    second = angle * 3600
    DMS = [degrees, minute, second]
    return DMS


# computes the magnitude of a vector
def mag(v1):
    magnitude = (v1[0]**2 + v1[1]**2 + v1[2]**2)**.5
    return magnitude

def rads(sin, cos):
    if sin < 0:
        angle = 2*pi - acos(cos)
    else:
        angle = acos(cos)
    return angle

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

def per_error(exp, act):
    percent = abs(exp - act) / act * 100
    return percent
