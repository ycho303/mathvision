import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import decimal
from scipy import linalg as LA

def float_range(start, stop, step):
    while start < stop:
        yield float(start)
        start = decimal.Decimal(start) + decimal.Decimal(step)

def get_Z(x, y, grad=0):
    if grad == 0:
        return (x + y) * (x*y + x*y**2)
    elif grad == 1:
        return (1 + y)*(x*y + x*y**2) + (x + y)*(1*y + 1*y**2), \
               (x + 1)*(x*y + x*y**2) + (x + y)*(x*1 + 2*x*y)
    elif grad == 2:
        return np.array([[2*y**2+2*y, 2*x*y+(2*y+1)*(x+y)+x+y**2+y],\
                        [2*x*y+(2*y+1)*(x+y)+x+y**2+y, 4*x*y+2*x*(x+y)+2*x]])
    else:
        raise NotImplementedError(f'Gradient of {grad} not implemented!')

def find_critical(x, y):
    X = (1 + y)*(x*y + x*y**2) + (x + y)*(1*y + 1*y**2)
    Y = (x + 1)*(x*y + x*y**2) + (x + y)*(x*1 + 2*x*y)
    for idx, x in enumerate(X):
        for idy, y in enumerate(Y):
            if x == 0:
                if y == 0:
                    print(idx, idy)

'''Q1.1'''
dense = 100
step = 0.1
_X = np.arange(-1, 1.5+step, step)
_Y = np.arange(-1.2, 0.2+step, step)
X, Y = np.meshgrid(_X, _Y)
Z = get_Z(X, Y)

fig = plt.figure()
ax = plt.axes(projection='3d')
surface = ax.contour3D(X, Y, Z, dense, cmap=cm.jet) 
fig.colorbar(surface, shrink=0.5, aspect=5) 

'''Q1.2'''
print(f"Gradent of f(1, 0) = {get_Z(1, 0, grad=1)}")
gX, gY = get_Z(X, Y, grad=1)
fig = plt.figure() 
ax = plt.axes() 
ax.contour(X, Y, Z) 
ax.quiver(X, Y, gX, gY, alpha=0.5)
fig.colorbar(surface, shrink=0.5, aspect=5) 


'''Q1.3'''
critical_point = []
for x in np.array(list(float_range(-1, 1.5, '0.005'))):
    for y in np.array(list(float_range(-1, 0.2, '0.005'))):
        if sum(get_Z(x, y, grad=1)) == 0:
            critical_point.append((x, y))

for x, y in critical_point:
  hessian = get_Z(x, y, grad=2)
  (l1, l2), _ = LA.eig(hessian)
  print(f"x: {x}\ty: {y}\teigenvalues: {[round(float(l1), 4), round(float(l2), 4)]}")

fig = plt.figure()
ax = plt.axes(projection='3d')
surface = ax.contour3D(X, Y, Z, dense, cmap=cm.jet, alpha=0.5) 
ax.scatter([x for x, _ in critical_point], [y for _, y in critical_point], marker="*", c='black')
fig.colorbar(surface, shrink=0.5, aspect=5) 

plt.show()