from odlib import *
v1 = [ 1, 2, 3 ]
v2 = [ 4, -5, -6 ]
v3 = [ 0, 2, 0 ]
print('a = ', v1, ' b = ‘', v2, ' c = ', v3)
print( 'dot product of a and b is ', dot(v1,v2) )
print( 'cross product of a and b is ', cross(v1,v2) )
print( 'triple product of a, b, and c is ', tri_product( v1, v2, v3))
