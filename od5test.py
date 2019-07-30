from odlib import *
from math import *
import numpy as np
import copy as cp

# defining input values
RA = [RAdecimalToHMS(17.633096*15),
      RAdecimalToHMS(17.642617*15),
      RAdecimalToHMS(17.661737*15)]
DEC = [DECdecimalToDMS(-24.906182),
       DECdecimalToDMS(-22.779707),
       DECdecimalToDMS(-21.790782)]
print('RA1:', RA)
print('Dec1:', DEC)
t1 = 2458671.778
t2 = 2458679.772
t3 = 2458683.774
R = [[-2.568180989317604E-01,  9.026400560686667E-01,  3.912553385188193E-01],
     [-3.849247965056879E-01, 8.631971645323986E-01, 3.741557451122443E-01],
     [-4.465913217555757E-01, 8.375970194890799E-01,  3.630559556728792E-01]] #in equatorial coordinates REAL
k = 0.01720209847
c = 173.145

# Convert data to radians
RA_rad = [HMStoDeg([x[0], x[1], x[2]]) * pi/180 for x in RA]
DEC_rad = [DMStoDeg([x[0], x[1], x[2]]) * pi/180 for x in DEC]

# Calculate rho hat from RA and DEC values
rho_x = [cos(RA_rad[x])*cos(DEC_rad[x]) for x in range(len(RA_rad))]
rho_y = [sin(RA_rad[x])*cos(DEC_rad[x]) for x in range(len(RA_rad))]
rho_z = [sin(DEC_rad[x]) for x in range(len(RA_rad))]
rho_hat_calc = [[rho_x[x], rho_y[x], rho_z[x]] for x in range(len(RA))]
rho_hat = np.array(rho_hat_calc)

# Adjust for time difference w/ taus
tau1 = k*(t1-t2)
tau3 = k*(t3-t2)
tau0 = tau3 - tau1

# Approximate a1 and a3
a1 = tau3/tau0
a3 = -tau1/tau0
count = 0

r2 = [5]
r2dot = [5]
r2o = [0]
r2doto = [0]

def f(tau):
    series_pt1 = 1-(tau**2)/(2*mag(r2)**3) + \
                 (tau**3)*dot(r2, r2dot)/(2*mag(r2)**5)
    coeff = (tau**4)/(24*mag(r2)**3)
    disgusting = 3*(dot(r2dot, r2dot)/(mag(r2)**2) - 1/(mag(r2)**3)) - \
                 15*(dot(r2, r2dot)/(mag(r2)**2))**2 + 1/(mag(r2)**3)
    return series_pt1 + coeff*disgusting
def g(tau):
    return tau - (tau**3)/(6*(mag(r2)**3)) + (tau**4)*(dot(r2, r2dot))/(4*mag(r2)**5)

def determineClose(v1, v2):
    for i in range(len(v1)):
        if(abs(v1[i]-v2[i]) > 10**-11):
            return False
    return True

while(determineClose(r2, r2o) == False and determineClose(r2dot, r2doto) == False):
    D0 = dot(rho_hat[0], cross(rho_hat[1], rho_hat[2]))
    D = np.ones((3,3))
    for j in range(3):
        D[0,j] = dot(cross(R[j], rho_hat[1]), rho_hat[2])
        D[1,j] = dot(cross(rho_hat[0], R[j]), rho_hat[2])
        D[2,j] = dot(rho_hat[0], cross(rho_hat[1], R[j]))
    
    # Calculate rhos
    rho = np.ones(3)
    rho[0] = (a1*D[0,0]+(-1)*D[0,1]+a3*D[0,2])/(a1*D0)
    rho[1] = (a1*D[1,0]+(-1)*D[1,1]+a3*D[1,2])/(-1*D0)
    rho[2] = (a1*D[2,0]+(-1)*D[2,1]+a3*D[2,2])/(a3*D0)

    # Adjust taus
    tau1 = k*((t1-rho[0]/c)-(t2-rho[1]/c))
    tau3 = k*((t3-rho[2]/c)-(t2-rho[1]/c))
    tau0 = tau3 - tau1
    
    # Approximate vectors r1, r2, r3, r2dot
    rvec = []
    for i in range(3):
        rvec.append(rho[i]*rho_hat[i] - R[i])
    rvec = np.array(rvec)
    r2o = r2
    r2 = rvec[1]
    if(count == 0):
        count += 1
        r2dot = (rvec[2]-rvec[0])/tau0

    # Calculate f and g series
    f1 = f(tau1)
    f3 = f(tau3)
    g1 = g(tau1)
    g3 = g(tau3)

    # Update a and b
    a1 = g3/(f1*g3-f3*g1)
    a3 = g1/(f3*g1-f1*g3)
    b1 = f3/(f3*g1-f1*g3)
    b3 = f1/(f1*g3-f3*g1)

    # Update r2dot
    r2doto = r2dot
    r2dot = b1*rvec[0] + b3*rvec[2]


r2 = co_rot(r2, 23.4367505323, 'x')
r2dot = co_rot(r2dot, 23.4367505323, 'x')

# defining actual vectors
r2_act = [0.3970630876567,
          -1.22507372544802,
          0.4747425864661720]

r2_dot_act = [0.662642317731134,
              0.155785644680128,
              0.218046327693182]

print('R2 vector: ', r2)
print('R2 dot vector: ', r2dot)


# error calculations
er_r2 = [abs(r2[0]-r2_act[0]) / mean([r2[0], r2_act[0]]),
         abs(r2[1]-r2_act[1]) / mean([r2[1], r2_act[1]]),
         abs(r2[2]-r2_act[2]) / mean([r2[2], r2_act[2]])]
er_r2_dot = [abs(r2dot[0]-r2_dot_act[0]) / mean([r2dot[0], r2_dot_act[0]]),
             abs(r2dot[1]-r2_dot_act[1]) / mean([r2dot[1], r2_dot_act[1]]),
             abs(r2dot[2]-r2_dot_act[2]) / mean([r2dot[2], r2_dot_act[2]])]

r2_mag = mag(r2)
h = cross(r2, r2dot)
print(h)
h_x = h[0]
h_y = h[1]
h_z = h[2]
h_mag = mag(h)
v2 = dot(r2dot, r2dot)

a = 1 / ((2 / r2_mag) - v2)
ecc = (1 - (h_mag)**2 / a)**.5
inc = acos(h_z / h_mag)

cO = -h_y / (h_mag * sin(inc)) # cos of Omega
sO = h_x / (h_mag * sin(inc)) # sin of Omega
Ome = rads(sO, cO)

cU = (r2[0] * cO + r2[1] * sO) / r2_mag # cos of U
sU = r2[2] / (r2_mag * sin(inc)) # sin of U
U = rads(sU, cU)

cV = (1 / ecc) * ((a * (1 - ecc**2)) / r2_mag - 1) # cos of V
sV = (1 / ecc) * (((a * (1 - ecc**2)) / h_mag) * (dot(r2, r2dot)) / r2_mag)
V = rads(sV, cV)

w = U - V
E = acos((1 / ecc) * (1 - r2_mag / a))
M = E - ecc*sin(E)

# converting Orbital Elements into degrees
inc = inc * 180 / pi
U = U * 180 / pi
V = V * 180 / pi
Ome = Ome * 180 / pi
w = w * 180 / pi
if w < 0:
    w = 360 + w
E = E * 180 / pi
M = M * 180 / pi
experi = [a, ecc, inc, Ome, w, M]

# Element error calculation
expect = [2.640226301080940, 4.059008132819690E-01,
          9.527069429767748, 2.809685769461632E+02, 
          3.567195418376240E+02, 1.777935844299149]

per_error = []
for i in range(len(experi)):
    per_error.append(abs(experi[i] - expect[i]) / expect[i] * 100)

# print statement
print('Semi-major axis: ', a, ', Expected: ', expect[0], ', % error: ', per_error[0])
print('Eccentricity: ', ecc, ', Expected: ', expect[1], ', % error: ', per_error[1])
print('Inclination (degrees): ', inc, ', Expected: ', expect[2], ', % error: ', per_error[2])
print('Longitude of the Ascending Node (degrees): ', Ome,
      ', Expected: ', expect[3], ', % error: ', per_error[3])
print('Argument of Perihelion, (degrees): ', w, ', Expected: ', expect[4], ', % error: ', per_error[4])
print('Mean Anomaly (degrees): ', M, ', Expected: ', expect[5], ', % error: ', per_error[5])
    
