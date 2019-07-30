from odlib import *
from matrices import *
import matplotlib.pyplot as plt

def lspr(x, y):
    data = np.loadtxt('LSPR Data.csv',dtype = float,delimiter=',')
    N = len(data)
    RA = []
    DEC = []
    sum_x = 0
    sum_y = 0
    sum_x2 = 0
    sum_y2 = 0
    sum_xy = 0
    sum_RA = 0
    sum_RAx = 0
    sum_RAy = 0
    sum_DEC = 0
    sum_DECx = 0
    sum_DECy = 0
    for i in range(len(data)):
        RA.append(HMStoDeg([data[i][2], data[i][3], data[i][4]]))
        DEC.append(DMStoDeg([data[i][5], data[i][6], data[i][7]]))
        sum_x += data[i][0]
        sum_y += data[i][1]
        sum_x2 += (data[i][0])**2
        sum_y2 += (data[i][1])**2
        sum_xy += data[i][0] * data[i][1]
        sum_RA += RA[i]
        sum_RAx += data[i][0] * RA[i]
        sum_RAy += data[i][1] * RA[i]
        sum_DEC += DEC[i]
        sum_DECx += data[i][0] * DEC[i]
        sum_DECy += data[i][1] * DEC[i]
    coef = [[N, sum_x, sum_y], [sum_x, sum_x2, sum_xy], [sum_y, sum_xy, sum_y2]]
    constant = [[sum_RA, sum_RAx, sum_RAy], [sum_DEC, sum_DECx, sum_DECy]]
    b1 = cramer_matrix(coef, constant[0])[0]
    a11 = cramer_matrix(coef, constant[0])[1]
    a12 = cramer_matrix(coef, constant[0])[2]
    b2 = cramer_matrix(coef, constant[1])[0]
    a21 = cramer_matrix(coef, constant[1])[1]
    a22 = cramer_matrix(coef, constant[1])[2]

    res_alph = []
    res_delt = []
    alph = 0
    alph = b1 + a11 * x + a12 * y
    dec = 0
    dec = b2 + a21 * x + a22 * y
    for i in range(len(RA)):
        res_alph.append(RA[i] - (b1 + a11 * data[i][0] + a12 * data[i][1]))
        res_delt.append(DEC[i] - (b2 + a21 * data[i][0] + a22 * data[i][1]))

    st_dev_a = 0
    st_dev_b = 0
    st_dev_a2 = 0
    st_dev_b2 = 0
    for i in range(len(res_alph)):
        st_dev_a2 += (res_alph[i])**2
        st_dev_b2 += (res_delt[i])**2
    st_dev_a = (st_dev_a2 / (N - 3))**.5
    st_dev_b = (st_dev_b2 / (N - 3))**.5
    print('RA of the asteroid is:', alph, '+/-', st_dev_a)
    print('DEC of the asteroid is:', dec, '+/-', st_dev_b)
    print(RA)
    
lspr(57.373320, 22.486560)

