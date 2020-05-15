import numpy as np
import matplotlib.pyplot as plt
import random

# '''User inputs'''
# inputs = []
# while True:
#     ans = input(f'Input point in (x, y) format. Press enter when done:\n')
#     if ans == '':
#         if len(inputs) < 2:
#             print('\nMust have at least 2 points.\n')
#         else:
#             break
#     else:
#         if '(' in ans and ')' in ans:
#             ans = ans[1:-1]
#         try:
#             x, y = ans.split(',')
#             x = float(x)
#             y = float(y)
#             inputs.append((x, y))
#             print(f'\nCurrent inputs: {inputs}\n')
#         except:
#             print('Invalid input.\n')

'''Random input to save time'''
def rtuple():
    return (random.uniform(5, 5.5), random.uniform(1, 10))
inputs = [rtuple() for i in range(10)]

'''Explicit function: y=ax+b'''
A = np.array([(x, 1) for x, _ in inputs])
Y = np.array([y for _, y in inputs]).T
# EP = np.matmul(np.matmul(np.linalg.inv(np.matmul(A.T, A)), A.T), Y)
EP = np.matmul(np.linalg.pinv(A), Y)

'''Implicit function: ax+by+c=0'''
A = np.array([(x, y, 1) for x, y in inputs])
_, _, V = np.linalg.svd(A, full_matrices=False)
IP = V.T[:, -1]

'''Plot'''
x = np.linspace(0, 10, 10)
Ey = EP[0]*x + EP[1]
Iy = (-IP[0]*x - IP[2]) / IP[1]
plt.plot(x, Ey, '-g', label='y=ax+b')
plt.plot(x, Iy, '-r', label='ax+by+c=0')
plt.scatter([i for i, _ in inputs], [i for _, i in inputs], s=6, color='b')
plt.title('Estimation')
plt.legend()
plt.grid()
plt.xlim([0, 10])
plt.ylim([0, 10])
plt.show()