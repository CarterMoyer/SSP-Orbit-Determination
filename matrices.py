def det_2(matrix):
    determ = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    return determ

def det_3(matrix):
    det_x = [[matrix[1][1], matrix[1][2]], [matrix[2][1], matrix[2][2]]]
    det_y = [[matrix[1][0], matrix[1][2]], [matrix[2][0], matrix[2][2]]]
    det_z = [[matrix[1][0], matrix[1][1]], [matrix[2][0], matrix[2][1]]]
    term1 = matrix[0][0] * det_2(det_x)
    term2 = -matrix[0][1] * det_2(det_y)
    term3 = matrix[0][2] * det_2(det_z)
    determ = term1 + term2 + term3
    return determ

import copy as c
def spliceColumn(coef, constant, j):
    spliced_matrix = c.deepcopy(coef)
    if j == 'x':
        j = 0
    if j == 'y':
        j = 1
    if j == 'z':
        j = 2
    for i in range(3):
        spliced_matrix[i][j] = constant[i]
    return spliced_matrix

def cramer_matrix(coef, constant):
    solution = []
    for i in range(3):
        matrix = spliceColumn(coef, constant, i)
        equ = det_3(matrix) / det_3(coef)
        solution.append(equ)
    return solution
