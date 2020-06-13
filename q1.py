import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import random
random.seed(1)

PLOT_Q1 = False
PLOT_Q2 = True
PLOT_Q3 = True
PLOT_Q4 = False


def get_Z(x, y, grad=0):
    if grad == 0:
        return np.sin(x + y - 1) + (x - y - 1)**2 - 1.5*x + 2.5*y + 1
    elif grad == 1:
        return np.cos(-x - y + 1) + 2*x - 2*y - 3.5, \
               np.cos(-x - y + 1) - 2*x + 2*y + 4.5
               
    elif grad == 2:
        return np.array([[np.sin(-x-y+1)+2, np.sin(-x-y+1)-2],\
                         [np.sin(-x-y+1)-2, np.sin(-x-y+1)+2]])
    else:
        raise NotImplementedError(f'Gradient of {grad} not implemented!')

'''Q1.1'''
dense = 100
step = 0.1
_X = np.arange(-1, 5+step, step)
_Y = np.arange(-3, 4+step, step)
X, Y = np.meshgrid(_X, _Y)
Z = get_Z(X, Y)

if PLOT_Q1:
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    surface = ax.contour3D(X, Y, Z, dense, cmap='summer') 
    fig.colorbar(surface, shrink=0.5, aspect=5) 

'''Q1.2'''
LAMBDA = 0.1
x0 = random.uniform(-1, 5)
y0 = random.uniform(-3, 4)
z0 = get_Z(x0, y0, grad=0)
print(f'x0: {x0}, y0: {y0}')

if PLOT_Q2 or PLOT_Q4:
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    surface = ax.contour3D(X, Y, Z, dense, alpha=0.3, cmap='summer') 
    fig.colorbar(surface, shrink=0.5, aspect=5)

    ga = (x0, y0)
    gd = (x0, y0)
    ga_epsilon = np.amax(Z) # cheating for better vis
    gd_epsilon = np.amin(Z)

    ga_optimal, gd_optimal = False, False
    iteration, ga_optimal_found, gd_optimal_found = [0]*3
    while not gd_optimal: #or not ga_optimal:
        iteration+=1
        # if not ga_optimal:
        #     ga_x, ga_y = get_Z(*ga, grad=1)
        #     ga = (ga[0] + LAMBDA * ga_x, ga[1] + LAMBDA * ga_y)
        #     ga_z = get_Z(*ga, grad=0)
        #     ax.scatter(*ga, ga_z, alpha=0.5, marker="*", c='red')

        if not gd_optimal:
            gd_x, gd_y = get_Z(*gd, grad=1)
            gd = (gd[0] - LAMBDA * gd_x, gd[1] - LAMBDA * gd_y)
            gd_z = get_Z(*gd, grad=0)
            ax.scatter(*gd, gd_z, alpha=0.5, marker="*", c='blue')

        # if ga_z > ga_epsilon and not ga_optimal:
        #     ga_optimal = True
        #     ga_optimal_found = iteration
        #     ga_epsilon = ga_z

        if gd_z < gd_epsilon and not gd_optimal:
            gd_optimal = True
            gd_optimal_found = iteration
            gd_epsilon = gd_z

    # ax.scatter(x0, y0, z0, alpha=0.5, marker="*", c='red', label=f'gradient ascend  ({round(ga_epsilon, 2)} at iter {ga_optimal_found})')
    ax.scatter(x0, y0, z0, alpha=0.5, marker="*", c='blue', label=f'gradient descent ({round(gd_epsilon, 2)} at iter {gd_optimal_found})')
    ax.set_xlabel(f'init: ({round(x0, 2)}, {round(y0, 2)}, {round(z0, 2)})')
    # plt.axis('off')
    plt.title('SGD')
    fig.legend()

'''Q1.3'''
if PLOT_Q3:
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    surface = ax.contour3D(X, Y, Z, dense, alpha=0.3, cmap='summer') 
    fig.colorbar(surface, shrink=0.5, aspect=5)

if PLOT_Q3 or PLOT_Q4:

    gd = (x0, y0)
    epsilon = -9999
    iteration = 0
    while True:
        iteration+=1

        gd_g = get_Z(*gd, grad=1)
        hessian = get_Z(*gd, grad=2)
        u, s, v = np.linalg.svd(hessian, full_matrices=True)
        newton_hessian = np.linalg.inv(np.matmul(u*abs(s), v))
        gd = gd - np.matmul(newton_hessian, gd_g)

        gd_z = get_Z(*gd, grad=0)
        ax.scatter(*gd, gd_z, alpha=0.5, marker="*", c='m')

        gd_z = round(gd_z, 4)
        if gd_z == epsilon:
            break
        else:
            epsilon = gd_z


    ax.scatter(x0, y0, z0, alpha=0.8, marker="*", c='m', label=f'Newton\'s Method ({round(epsilon, 2)} at iter {iteration})')
    ax.set_xlabel(f'init: ({round(x0, 2)}, {round(y0, 2)}, {round(z0, 2)})')
    # plt.axis('off')
    if not PLOT_Q4:
        plt.title('Newton\'s Method')
    else:
        plt.title('')
    fig.legend()

plt.show()