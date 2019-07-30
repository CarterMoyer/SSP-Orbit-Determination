from math import *
import numpy as np
import matplotlib.pyplot as plt


# problem 1
# using Newton's method to find the value of E when...
# given the value of the Mean anomaly and eccentricity

# finds the function value for given E
def find_E(E):
    M = 3*pi/4
    e = 0.41
    root = E + e*sin(E) - M # have to set this equal to zero for root
    return root

# finds the derivative of the function for given E
def find_E_der(E):
    e = 0.41
    df = e*cos(E) + 1
    return df

# combines the two functions above into a single function, programable error
def find_E_solve(guess, find_E, find_E_der, error):
    xi_1 = guess
    while abs(find_E(xi_1)) > error:
        guess = xi_1
        xi_1 = guess - find_E(guess) / find_E_der(guess)
    return xi_1

# end of 1

# problem 8
import copy as cp
def san_shi_qi(pos_1, vel_1, pos_2, vel_2):
    delT = 50000
    time = np.arange(0, 600000000, delT)

    m1 = 2 * 10**30
    m2 = 5.972 * 10**24
    m3 = 7.34767309 * 10**22
    G = 6.67 * 10**-11
    r_1 = (pos_1[0]**2 + pos_1[1]**2)**.5
    r_2 = ((pos_2[0] - pos_1[0])**2 + (pos_2[1] - pos_2[1])**2)**.5 # earth to moon
    r_21 = (pos_2[0]**2 + pos_2[1]**2)**.5 # sun to moon

    sin1 = pos_1[1] / r_1
    cos1 = pos_1[0] / r_1
    sin2 = (pos_2[1] - pos_1[1]) / r_2
    cos2 = (pos_2[0] - pos_1[0]) / r_2
    sin21 = pos_2[1] / r_21
    cos21 = pos_2[0] / r_21
    sin12 = (pos_1[1] - pos_2[1]) / r_2 # moon to earth
    cos12 = (pos_1[0] - pos_2[0]) / r_2

    for t in time:
        
        a1 = [((-G * m1 / (r_1)**2 )* cos1),
              ((-G * m1 / (r_1)**2 )* sin1)]
        a1_1 = cp.deepcopy(a1)
        a2 = [((-G * m2 / (r_2)**2) * cos2),
              ((-G * m2 / (r_2)**2) * sin2)] # earth on moon
        a2_1 = cp.deepcopy(a2)
        a21 = [((-G * m1 / (r_21)**2) * cos21),
               ((-G * m1 / (r_21)**2) * sin21)] # sun on moon
        a21_1 = cp.deepcopy(a21)
        a12 = [((-G * m3 / (r_2)**2) * cos12),
               ((-G * m3 / (r_2)**2) * sin12)] # moon on earth
        a12_1 = cp.deepcopy(a12)
        
        pos_1 = [(pos_1[0] + vel_1[0] * delT + .5 * (a1[0] + a12[0]) * delT**2),
                 (pos_1[1] + vel_1[1] * delT + .5 * (a1[1] + a12[1]) * delT**2)] # x and y position for earth
        pos_2 = [(pos_2[0] + vel_2[0] * delT + .5 * (a2[0] + a21[0]) * delT**2),
                 (pos_2[1] + vel_2[1] * delT + .5 * (a2[1] + a21[1]) * delT**2)] # x and y position for moon

        r_1 = (pos_1[0]**2 + pos_1[1]**2)**.5 #sun to earth
        r_2 = ((pos_2[0] - pos_1[0])**2 + (pos_2[1] - pos_2[1])**2)**.5 # earth to moon
        r_21 = (pos_2[0]**2 + pos_2[1]**2)**.5 # sun to moon

        sin1 = pos_1[1] / r_1 # earth and sun
        cos1 = pos_1[0] / r_1
        sin2 = (pos_2[1] - pos_1[1]) / r_2 # earth to moon
        cos2 = (pos_2[0] - pos_1[0]) / r_2
        sin21 = pos_2[1] / r_21 # sun to moon
        cos21 = pos_2[0] / r_21
        sin12 = (pos_1[1] - pos_2[1]) / r_2 # moon to earth
        cos12 = (pos_1[0] - pos_2[0]) / r_2

        a1 = [((-G * m1 / (r_1)**2) * cos1),
              ((-G * m1 / (r_1)**2) * sin1)] # sun on earth
        a2 = [((-G * m2 / (r_2)**2) * cos2),
              ((-G * m2 / (r_2)**2) * sin2)] # earth on moon
        a21 = [((-G * m1 / (r_21)**2) * cos21),
               ((-G * m1 / (r_21)**2) * sin21)] # sun on moon
        a12 = [((-G * m3 / (r_2)**2) * cos12),
               ((-G * m3 / (r_2)**2) * sin12)] # moon on earth
       
        vel_1 = [(vel_1[0] + .25 * (a1[0] + a1_1[0] + a12[0] + a12_1[0]) * delT),
                 (vel_1[1] + .25 * (a1[1] + a1_1[1] + a12[1] + a12_1[1]) * delT)] # x and y velocity of earth
        vel_2 = [(vel_2[0] + .25 * (a2[0] + a2_1[0] + a21[0] + a21_1[0]) * delT),
                 (vel_2[1] + .25 * (a2[1] + a2_1[1] + a21[1] + a21_1[1]) * delT)] # x and y velocity of moon

        plt.plot(pos_1[0], pos_1[1], 'bo')
        plt.plot(pos_2[0], pos_2[1], 'go')
        plt.plot(0,0, "y*")
        plt.xlim(-2 * 10 ** 12, 2 * 10 ** 12)
        plt.ylim(-2 * 10 ** 12, 2 * 10 ** 12)
        plt.pause(0.03)

san_shi_qi([1.496 * 10**11, 0], [0, 29780], [1.499 * 10**11, 0], [0, 30800]) # initial values sensitive, easily ejects
    
