from math import *
import odlib as od

# input of elements
T1 = 2458313.500000000
T2 = 2458333.500000000
ecc1 = 0.3442331151448467
inc1 = 25.15524951609384
Ome1 = 236.2379850365209
W1 = 255.5046043258952
a = 1.056800057440251
MA = 140.4194630122296 * pi / 180


k = 0.0172020984
n = k * (1/a**3)**.5
T =  T1 - MA/(n)

M1 = n * (T2 - T)

# finds the function value for given E
def find_E(E):
    root = E - ecc1*sin(E) - M1 # have to set this equal to zero for root
    return root

# finds the derivative of the function for given E
def find_E_der(E):
    df = -ecc1*cos(E) + 1
    return df

# combines the two functions above into a single function, programable error
def find_E_solve(guess, find_E, find_E_der, error):
    xi_1 = guess
    while abs(find_E(xi_1)) > error:
        guess = xi_1
        xi_1 = guess - find_E(guess) / find_E_der(guess)
    return xi_1

# calculating position vector of asteroid
E = find_E_solve(160, find_E, find_E_der, 10**-20)
pos = [a * cos(E) - a*ecc1,
       a * (1 - ecc1**2)**.5 * sin(E),
       0]

# coordinate rotations
rvec1 = od.co_rot(pos, -W1, 'z')
rvec2 = od.co_rot(rvec1, -inc1, 'x')
rvec_ec = od.co_rot(rvec2, -Ome1, 'z')

rvec = od.co_rot(rvec_ec, -23.4367505323, 'x')

# vector of sun to earth
R = [-6.574011197988899E-01,
     7.092445968434601E-01,
     3.074588261788798E-01]

# calculating rho and rho hat
rho = [rvec[0] + R[0],
       rvec[1] + R[1],
       rvec[2] + R[2]]
rho_h = [rho[0] / od.mag(rho),
         rho[1] / od.mag(rho),
         rho[2] / od.mag(rho)]

# calculating RA and Dec
dec = asin(rho_h[2])
cosA = rho_h[0] / cos(dec)
sinA = rho_h[1] / cos(dec)

# convert into degrees and isolate for RA
ra = od.rads(sinA, cosA) * 180 / pi
dec = dec * 180 / pi

ra = od.RAdecimalToHMS(ra)
dec = od.DECdecimalToDMS(dec)

print(ra, dec)

