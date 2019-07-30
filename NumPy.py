import numpy as np
from math import *
import matplotlib.pyplot as plt

# warm up 1
a = np.eye(10)
print(np.mean(a))
print(np.std(a))

# warm up 2
#b = np.linspace(-6*pi, 6*pi, 1000)
#bc = np.cos(b)
#x = range(1000)
#plt.plot(x, bc)
#plt.show()

# warm up 3
data = np.genfromtxt('output1.csv', delimiter=',')
x = np.cumsum(np.ones(data.shape), axis = 0) - 1
y = np.cumsum(np.ones(data.shape), axis = 1) - 1
s2x = x * data
s2y = y * data
x_top = np.sum(s2x)
_bottom = np.sum(data)
y_top = np.sum(s2y)
x_cm = x_top / _bottom
y_cm = y_top / _bottom

# uncertainty
x_unc = (np.sum((((x - x_cm)/_bottom)**2) * data))**.5
y_unc = (np.sum((((y - y_cm)/_bottom)**2) * data))**.5
# print(x_unc)
# print(y_unc)

values = np.genfromtxt('^DJI.csv', delimiter=',')[:,1]
x = range(244)
xv = range(253)
window = 10
weights = np.repeat(1.0, window)/window
smas = np.convolve(values, weights, 'valid')
plt.plot(x, smas)
plt.plot(xv, values,'g')
plt.show()

