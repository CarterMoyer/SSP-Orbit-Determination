import odlib as od
from math import *
def orbit_ele(x_pos1, y_pos1, z_pos1, x_pos2, y_pos2, z_pos2, J1, J2):

    k = 0.01720209847
    r_dot = [(x_pos2 - x_pos1) / (k * (J2 - J1)),
             (y_pos2 - y_pos1) / (k * (J2 - J1)),
             (z_pos2 - z_pos1) / (k * (J2 - J1))]
    
    r = [x_pos1, y_pos1, z_pos1]
    r_mag = od.mag(r)
    
    h = od.cross(r, r_dot)
    h_x = h[0]
    h_y = h[1]
    h_z = h[2]
    h_mag = od.mag(h)
    v2 = od.dot(r_dot, r_dot)

    a = 1 / ((2 / r_mag) - v2)
    ecc = (1 - (h_mag)**2 / a)**.5
    inc = acos(h_z / h_mag)

    cO = -h_y / (h_mag * sin(inc)) # cos of Omega
    sO = h_x / (h_mag * sin(inc)) # sin of Omega
    Ome = od.rads(sO, cO)

    cU = (x_pos1 * cO + y_pos1 * sO) / r_mag # cos of U
    sU = z_pos1 / (r_mag * sin(inc)) # sin of U
    U = od.rads(sU, cU)

    cV = (1 / ecc) * ((a * (1 - ecc**2)) / r_mag - 1) # cos of V
    sV = (1 / ecc) * (((a * (1 - ecc**2)) / h_mag) * (od.dot(r, r_dot)) / r_mag)
    V = od.rads(sV, cV)

    w = U - V
    E = acos((1 / ecc) * (1 - r_mag / a))
    M = E - ecc*sin(E)

    inc = inc * 180 / pi
    U = U * 180 / pi
    V = V * 180 / pi
    Ome = Ome * 180 / pi
    w = w * 180 / pi
    if w < 0:
        w = 360 + w
    E = E * 180 / pi
    M = M * 180 / pi
    experi = [a, ecc, inc, Ome, V, w, M]
    expect = [1.056800057682216, 3.442331106521022 * 10**-1,
              2.515525601713781 * 10, 236.2379793903064, 1.589559274581728 * 10**2, 
              255.5046093427637, 1.404194621765141 * 10**2]
    per_error = []
    for i in range(len(experi)):
        per_error.append(abs(experi[i] - expect[i]) / expect[i] * 100)
    print('Semi-major axis: ', a, ', Expected: ', expect[0], ', % error: ', per_error[0])
    print('Eccentricity: ', ecc, ', Expected: ', expect[1], ', % error: ', per_error[1])
    print('Inclination (degrees): ', inc, ', Expected: ', expect[2], ', % error: ', per_error[2])
    print('Longitude of the Ascending Node (degrees): ', Ome,
          ', Expected: ', expect[3], ', % error: ', per_error[3])
    print('True Anomoly (degrees): ', V, ', Expected: ', expect[4], ', % error: ', per_error[4])
    print('Argument of Perihelion, (degrees): ', w, ', Expected: ', expect[5], ', % error: ', per_error[5])
    print('Mean Anomaly (degrees): ', M, ', Expected: ', expect[6], ', % error: ', per_error[6])
orbit_ele(3.970630876566811 * 10**-1, -1.225073725448021,
          4.747425864661729 * 10**-1, 3.971026666688517 * 10**-1,
          -1.225064419633509, 4.747556099354516 * 10**-1,
          2458313.500000000, 2458313.503472222)
