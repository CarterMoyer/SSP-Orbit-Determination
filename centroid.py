# centroid weighted center project

import numpy as np

data = np.loadtxt('output1.csv',dtype = float,delimiter=',')

def centroid(mat, x0, y0):
    x_cm_top = 0
    y_cm_top = 0
    N = 0
    for i in range(len(mat)):
        row = mat[i]
        for j in range(len(row)):
            x_cm_top += row[j] * (j - x0)
            y_cm_top += row[j] * (i - y0)
            N += row[j]
    x_cm = x_cm_top / N
    y_cm = y_cm_top / N

    x_cm_unc = 0
    y_cm_unc = 0
    for i in range(len(mat)):
        row = mat[i]
        for j in range(len(row)):
            x_cm_unc += ((j - x_cm - x0) / N)**2 * row[j]
            y_cm_unc += ((i - y_cm - y0) / N)**2 * row[j]
    x_cm_unc = (x_cm_unc)**.5
    y_cm_unc = (y_cm_unc)**.5

    print(x_cm, '+/-', x_cm_unc, ',', y_cm, '+/-', y_cm_unc)

        
centroid(data, 0, 0)
