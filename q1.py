import numpy as np
import matplotlib.pyplot as plt
import random
from tqdm import tqdm
import scipy.stats
np.random.seed(123)
random.seed(123)

'''RANSAC Param'''
iteration = 10
threshold = 0.5
sample = 3
outlier = 40

'''Random input to save time'''
def random_line(a, b, sigma, size=10):
    x = np.linspace(0, 10, size)
    y = a*x + b + scipy.stats.norm.rvs(loc=0, scale=sigma, size=size)
    return x, y

x, y = random_line(2, 3, 0.1, size=30)
rx, ry = random_line(2, 3, 10, size=outlier)
x = np.concatenate((x, rx), axis=None)
y = np.concatenate((y, ry), axis=None)

def set_boundary(x, minx, maxx):
    result = x
    if result > maxx:
        result = maxx
    if result < minx:
        result = minx
    return result

'''Implicit function: ax+by+c=0'''
inputs = [(_x, _y, 1) for (_x, _y) in zip(x, y)]
A = np.array(inputs)
_, _, V = np.linalg.svd(A, full_matrices=False)
IP = V.T[:, -1]
Iy = (-IP[0]*x - IP[2]) / IP[1]

'''RANSAC'''
best = None
best_iter = 0
inlier = -1
best_inlier_pts = None
for i in tqdm(range(iteration)):
    n_inputs = random.sample(inputs, sample)
    A = np.array(n_inputs)
    _, _, V = np.linalg.svd(A, full_matrices=False)
    RIP = V.T[:, -1]
    RIy = (-RIP[0]*x - RIP[2]) / RIP[1]

    p1 = np.array([x[0], set_boundary(RIy[0], -10, 50)])
    p2 = np.array([x[-1], set_boundary(RIy[-1], -10, 50)])
    print(p1)
    print(p2)
    
    cur = 0
    inlier_pts = []
    for _x, _y in zip(x, y):
        p3 = np.array([_x, _y])
        dist = np.abs(np.cross(p2-p1, p3-p1)) / np.linalg.norm(p2-p1)
        if threshold > dist:
            cur += 1
            inlier_pts.append((_x, _y))
    
    print(f'iteration {i}:\tinliers: {cur}\tbest: {inlier}')
    if cur > inlier:
        inlier = cur
        best = RIy
        best_iter = i
        best_inlier_pts = inlier_pts

'''Plot'''
fig = plt.figure()
plt.plot(x, Iy, '-r', label='ax+by+c=0', alpha=0.3)
plt.plot(x, best, '-g', label=f'RANSAC: ax+by+c=0 at iter: {best_iter}', alpha=0.3)
plt.scatter(x, y, s=6, color='b', alpha=0.1)
plt.scatter([x for x, _ in best_inlier_pts] , [y for _, y in best_inlier_pts], s=6, color='g')
plt.title(f'Sample: {sample}      Iteration: {iteration}      Threshold: {threshold}      Outliers: {outlier}')
plt.legend()
plt.grid()
plt.xlim([0, 10])
plt.ylim([-10, 50])
# plt.show()
fig.savefig(f'sam{sample}_iter{iteration}_thresh{threshold}_out{outlier}.png', dpi=fig.dpi)