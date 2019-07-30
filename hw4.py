
from math import *
def tay_sin(x, n):
    result = 0
    for i in range(n):
        if i % 2 == 0:
            result += 0
        else:
            if i in range(1, n+1, 4):
                result += x**i / factorial(i)
            if i in range(3, n+1, 5):
                result += -1 * x**i / factorial(i)    
    print(result)
    
import odlib as od
import numpy as np
import matplotlib.pyplot as plt

def vel_verlet(x1, y1, x2, y2, v1x, v1y, v2x, v2y):
    delT = 1000000
    time = np.arange(0,6000000000,delT)

    m = 2 * 10**30
    G = 6.67 * 10**-11
    r_1 = (x1**2 + y1**2)**.5
    r_2 = (x2**2 + y2**2)**.5

    sin1 = y1 / r_1
    cos1 = x1 / r_1
    sin2 = y2 / r_2
    cos2 = x2 / r_2
    for t in time:
        
        a1 = -G * m / (r_1)**2
        a1x = a1 * cos1
        a1y = a1 * sin1
        a1x1 = a1x
        a1y1 = a1y
        a2 = -G * m / (r_2)**2
        a2x = a2 * cos2
        a2y = a2 * sin2
        a2x1 = a2x
        a2y1 = a2y
        
        x1 = x1 + v1x * delT + .5 * a1x * delT**2
        y1 = y1 + v1y * delT + .5 * a1y * delT**2
        x2 = x2 + v2x * delT + .5 * a2x * delT**2
        y2 = y2 + v2y * delT + .5 * a2y * delT**2



        r_1 = (x1**2 + y1**2)**.5
        r_2 = (x2**2 + y2**2)**.5

        sin1 = y1 / r_1
        cos1 = x1 / r_1
        sin2 = y2 / r_2
        cos2 = x2 / r_2
        
        a1 = -G * m / (r_1)**3
        a1x = a1 * cos1
        a1y = a1 * sin1
        a2 = -G * m / (r_2)**2
        a2x = a2 * cos2
        a2y = a2 * sin2
        v1x = v1x + .5 * (a1x + a1x1) * delT
        v1y = v1y + .5 * (a1y + a1y1) * delT
        v2x = v2x + .5 * (a2x + a2x1) * delT
        v2y = v2y + .5 * (a2y + a2y1) * delT
        print(v2x)
        plt.plot(x1, y1, 'bo')
        plt.plot(x2, y2, 'go')
        plt.plot(0,0, "y*")
        plt.xlim(-1.5 * 10 ** 12, 1.5 * 10 ** 12)
        plt.ylim(-1.5 * 10 ** 12, 1.5 * 10 ** 12)
        plt.pause(0.03)
vel_verlet(1.5 * 10 ** 11, 0, 5 * 10**11, 0, 0, 28000, 0, 15000)

import random
def rando_walk(N):
    distance = 0
    x = []
    for i in range(1, N+1):
        x.append(i)
        if random.random() > .5:
            distance += 1
        else:
            distance += -1
    return distance

def run_rando(X, N):
    final = []
    x1 = range(-80, 80)
    rmsp = []
    for i in range(X):
        final.append(rando_walk(N))
        
    
    for i in x1:
        px = (2 * (2 / (pi * N))**.5 * e**((-(i)**2) / (2 * N))) / 4
        rmsp.append(px)
    print(final)
    plt.xlim(-80, 80)
    plt.plot(x1, rmsp)
    plt.hist(final, 30, density = True, alpha = 0.75)
    plt.show()

        

       # rms.append(distance)
        #rms.append((dist_2 / i)**.5)
       # rms_p.append(2 * (2 / (pi * i))**.5 * e**(-(distance**2) / (2 * i)))
    print('The total distance is: ', distance)
    #print('The RMS is: ', rms)
    print('The sqrt of N is: ', sqrt(N))
# run_rando(1000, 1000)
