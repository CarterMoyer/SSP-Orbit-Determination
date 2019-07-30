from math import *
import odlib as od

def find_vector():
    RA = [[18, 41, 48.08], [18, 14, 30.53], [17, 54, 29.36]]
    DEC = [[36, 15, 14.1], [36, 9, 46.0], [34, 29, 32.2]]

    for i in range(3):
        RA[i] = od.HMStoDeg(RA[i]) * pi / 180
        DEC[i] = od.DMStoDeg(DEC[i]) * pi / 180
    rho_hat1 = [cos(RA[0]) * cos(DEC[0]), sin(RA[0]) * cos(DEC[0]), sin(DEC[0])] # calculating rho from RA and Dec
    rho_hat2 = [cos(RA[1]) * cos(DEC[1]), sin(RA[1]) * cos(DEC[1]), sin(DEC[1])]
    rho_hat3 = [cos(RA[2]) * cos(DEC[2]), sin(RA[2]) * cos(DEC[2]), sin(DEC[2])]

    rho1 = [0.07410335127715940, -.4015611046271995, 0.2994573000142365] # exact rho values
    rho2 = [0.02816887198319436, -0.4437310883473226, 0.3249882273840305]
    rho3 = [-0.01187334735101580, -0.4953819999141603, 0.3404906007681184]

    rho_hat_1_ex = [rho1[0] / od.mag(rho1), rho1[1] / od.mag(rho1), rho1[2] / od.mag(rho1)] # rho hat calculation from exact values
    rho_hat_2_ex = [rho2[0] / od.mag(rho2), rho2[1] / od.mag(rho2), rho2[2] / od.mag(rho2)]
    rho_hat_3_ex = [rho3[0] / od.mag(rho3), rho3[1] / od.mag(rho3), rho3[2] / od.mag(rho3)]


    error_1x = (rho_hat1[0] - rho_hat_1_ex[0])**2 # error by component
    error_1y = (rho_hat1[1] - rho_hat_1_ex[1])**2
    error_1z = (rho_hat1[2] - rho_hat_1_ex[2])**2

    error_2x = (rho_hat2[0] - rho_hat_2_ex[0])**2
    error_2y = (rho_hat2[1] - rho_hat_2_ex[1])**2
    error_2z = (rho_hat2[1] - rho_hat_2_ex[1])**2

    error_3x = (rho_hat3[0] - rho_hat_3_ex[0])**2
    error_3y = (rho_hat3[1] - rho_hat_3_ex[1])**2
    error_3z = (rho_hat3[2] - rho_hat_3_ex[2])**2
    
    error_1 = error_1x - error_1y - error_1z # cummulative error
    error_2 = error_2x - error_2y - error_2z
    error_3 = error_3x - error_3y - error_3z

    print('Error for rho 1: ', error_1)
    print('Error for rho 2: ', error_2)
    print('Error for rho 3: ', error_3)
find_vector()
