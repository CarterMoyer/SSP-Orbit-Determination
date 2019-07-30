import odlib as od
from math import *
import numpy as np
import copy as cp

# defining input values!
RA = [[18, 41, 48.08], [18, 14, 30.53], [17, 54, 29.36]]
DEC = [[36, 15, 14.1], [36, 9, 46.0], [34, 29, 32.2]]
R = [[-0.2069177625542078, 0.9132792377095497, 0.3959074080096284],
     [-0.3689266994628273, 0.8690904003976556, 0.3767540914983889],
     [-0.5205074019556455, 0.8003914633545058, 0.3469760777959491]]
k = 0.01720209847
t1 = 2458303.5
t2 = 2458313.5
t3 = 2458323.5

for i in range(3):
    RA[i] = od.HMStoDeg(RA[i]) * pi / 180
    DEC[i] = od.DMStoDeg(DEC[i]) * pi / 180
rho_hat1 = [cos(RA[0]) * cos(DEC[0]), sin(RA[0]) * cos(DEC[0]), sin(DEC[0])] # calculating rho from RA and Dec
rho_hat2 = [cos(RA[1]) * cos(DEC[1]), sin(RA[1]) * cos(DEC[1]), sin(DEC[1])]
rho_hat3 = [cos(RA[2]) * cos(DEC[2]), sin(RA[2]) * cos(DEC[2]), sin(DEC[2])]

T0 = k * (t3 - t1)
T1 = k * (t1 - t2)
T3 = k * (t3 - t2)
a1 = T3 / T0
a2 = -1
a3 = -T1 / T0
a = [a1, a2, a3]

D0 = od.dot(rho_hat1, od.cross(rho_hat2, rho_hat3))
D = np.ones((3,3))

rho = np.ones(3)

rho_hat = np.array([rho_hat1, rho_hat2, rho_hat3])

r2 = [0, 0, 0]
r2_dot = [0, 0, 0] # set values for while loop to carry over

r2_old = [1, 1, 1]
r2_dot_old = [1, 1, 1]

# setting up while loop
def bool_comp(vec1, vec2):
    diff = 0
    for i in range(len(vec1)):
        diff += abs(vec1[i] - vec2[i])
    return diff

iteration = 0
while bool_comp(r2, r2_old) > 10**-30 and bool_comp(r2_dot, r2_dot_old) > 10**-30 and iteration < 1000:

    # calculating rho vector
    r = []
    for i in range(3):
        D[0,i] = od.dot(od.cross(R[i], rho_hat[1]), rho_hat[2])
        D[1,i] = od.dot(od.cross(rho_hat[0], R[i]), rho_hat[2])
        D[2,i] = od.dot(rho_hat[0], od.cross(rho_hat[1], R[i]))
        rho[i] = (a1 * D[i,0] + a2 * D[i,1] + a3 * D[i,2]) / (a[i] * D0)
        r.append(rho[i] * rho_hat[i] - R[i])
    r = np.array(r)
    if iteration == 0:
        r2_dot = (r[2] - r[0]) / T0
    else:
        r2_dot = b1 * r[0] + b3 * r[2]
    r2_mag = od.mag(r[1])

    
    # time correction
    c = 173.145 # c in au / day

    T0 = k * ((t3 - rho[2] / c) - (t1 - rho[0] / c))
    T1 = k * ((t1 - rho[0] / c) - (t2 - rho[1] / c))
    T3 = k * ((t3 - rho[2] / c) - (t2 - rho[1] / c))
    a1 = T3 / T0
    a2 = -1
    a3 = -T1 / T0
    a = [a1, a2, a3]

    # defining f and g series
    def f(tau):
        series_pt1 = 1-(tau**2)/(2*r2_mag**3) + \
                 (tau**3)*od.dot(r2, r2_dot)/(2*r2_mag**5)
        coeff = (tau**4)/(24*r2_mag**3)
        disgusting = 3*(od.dot(r2_dot, r2_dot)/(r2_mag)**2) - 1/(r2_mag**3) - \
                 15*(od.dot(r2, r2_dot)/(r2_mag**2))**2 + 1/(r2_mag**3)
        return series_pt1 + coeff*disgusting
    def g(tau):
        return tau - (tau**3)/(6*r2_mag**3) + (tau**4)*(od.dot(r2, r2_dot))/(4*r2_mag**5)

    a1 = g(T3) / (f(T1) * g(T3) - f(T3) * g(T1))
    a3 = g(T1) / (f(T3) * g(T1) - f(T1) * g(T3))
    b1 = f(T3) / (f(T3) * g(T1) - f(T1) * g(T3))
    b3 = f(T1) / (f(T1) * g(T3) - f(T3) * g(T1))

    # copying list to compare
    r2_old = cp.deepcopy(r2)
    r2_dot_old = cp.deepcopy(r2_dot)
    r2 = a1 * r[0] + a3 * r[2]
    r2_dot = b1 * r[0] + b3 * r[2]

    iteration += 1
    

# coordinate rotation
r2 = od.co_rot(r2, 23.4367505323, 'x')
r2_dot = od.co_rot(r2_dot, 23.4367505323, 'x')

# defining actual vectors
r2_act = [0.3970630876567,
          -1.22507372544802,
          0.4747425864661720]

r2_dot_act = [0.662642317731134,
              0.155785644680128,
              0.218046327693182]

# error calculations
er_r2 = [abs(r2[0]-r2_act[0]) / od.mean([r2[0], r2_act[0]]),
         abs(r2[1]-r2_act[1]) / od.mean([r2[1], r2_act[1]]),
         abs(r2[2]-r2_act[2]) / od.mean([r2[2], r2_act[2]])]
er_r2_dot = [abs(r2_dot[0]-r2_dot_act[0]) / od.mean([r2_dot[0], r2_dot_act[0]]),
             abs(r2_dot[1]-r2_dot_act[1]) / od.mean([r2_dot[1], r2_dot_act[1]]),
             abs(r2_dot[2]-r2_dot_act[2]) / od.mean([r2_dot[2], r2_dot_act[2]])]

print('R2 vector: ', r2)
print('R2 dot vector: ', r2_dot)
print('Error of R2: ', er_r2)
print('Error of R2 dot: ', er_r2_dot)


