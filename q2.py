import numpy as np
import matplotlib.pyplot as plt
import random

PLOT_ALL_ITER = False

'''Random input to save time'''
def rtuple(minx, maxx, miny, maxy):
    return (random.uniform(minx, maxx), random.uniform(miny, maxy))
inputs = [(1*i, 1*i) for i in range(1, 6)] + [(2, 6), (3, 7)]

'''Explicit function: y=ax+b'''
A = np.array([(x, 1) for x, _ in inputs])
Y = np.array([y for _, y in inputs]).T
# EP = np.matmul(np.matmul(np.linalg.inv(np.matmul(A.T, A)), A.T), Y)
EP = np.matmul(np.linalg.pinv(A), Y)

'''Plot'''
x = np.linspace(0, 10, 10)
Ey = EP[0]*x + EP[1]
plt.plot(x, Ey, '-r', label='LS: y=ax+b')

'''Residual Explicit function: y=ax+b'''
for i in range(1, 10):
    r = Y - np.matmul(A, EP)
    w = 1 / (abs(r) / 1.3398 + 1)
    EP = np.matmul(np.matmul(np.linalg.inv(np.matmul(A.T * w, A)), A.T), w * Y)

    if PLOT_ALL_ITER:
        Ey = EP[0]*x + EP[1]
        plt.plot(x, Ey, label=f'Robust LS: y=ax+b, iter: {i}')

if not PLOT_ALL_ITER:
    Ey = EP[0]*x + EP[1]
    plt.plot(x, Ey, '-g', label='Robust LS: y=ax+b')

plt.scatter([i for i, _ in inputs], [i for _, i in inputs], s=6, color='b')
plt.title('Estimation')
plt.legend()
plt.grid()
plt.xlim([0, 10])
plt.ylim([0, 10])
plt.show()