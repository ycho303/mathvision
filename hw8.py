import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

COL_LABEL = ['sweetness', 'density', 'color', 'moisture']

# Read data
data_a = pd.read_csv('/Users/Young/Downloads/hw8_____/data_a.txt', sep=",", names=COL_LABEL)
data_b = pd.read_csv('/Users/Young/Downloads/hw8_____/data_b.txt', sep=",", names=COL_LABEL)
test = pd.read_csv('/Users/Young/Downloads/hw8_____/test.txt', sep=",", names=COL_LABEL)

# # Add label
data_a['label'] = 'a'
data_b['label'] = 'b'

# Combine data_a and data_b
data_ab = pd.concat([data_a, data_b], ignore_index=True)
label = data_ab.loc[:, 'label'].values
data_ab = data_ab.loc[:, COL_LABEL].values

# Compute covariance matrix
cov_ab = np.cov(data_ab.transpose())

# Compute eigenvectors and corresponding egienvalues
w, v = np.linalg.eig(cov_ab)

# Get principal component vector v1 and v2
v2, v1 = np.argsort(w)[-2:]

print('v1 and v2')
print(f'v1: {v[v1]}')
print(f'v2: {v[v2]}')

# Create subspace from (v1, v2)
subspace = v.dot(data_ab.transpose())
data_ab = pd.DataFrame([subspace[v1], subspace[v2]]).transpose()
data_ab['label'] = label
data_a = data_ab.loc[data_ab['label'] == 'a']
data_b = data_ab.loc[data_ab['label'] == 'b']

# Draw plot
plt.figure()
plt.title("data_a and data_b in subspace of (v1, v2)")
plt.scatter(x=data_a[0], y=data_a[1], color='red', alpha=0.3, marker=".", label='data_a')
plt.scatter(x=data_b[0], y=data_b[1], color='blue', alpha=0.3, marker=".", label='data_b')
plt.legend()
plt.show()

# Gaussian model
data_a = np.array([data_a[0], data_a[1]])
data_b = np.array([data_b[0], data_b[1]])
mean_a = np.mean(data_a, axis=1)
mean_b = np.mean(data_b, axis=1)
cov_a = np.cov(data_a)
cov_b = np.cov(data_b)

def multivariate_gaussian(data, mean, cov):
    fac = np.einsum('...k,kl,...l->...', data - mean, np.linalg.inv(cov), data - mean)
    return np.exp(-fac / 2) / np.sqrt((2*np.pi)**mean.shape[0] * np.linalg.det(cov))

def plot_gauss(x, y, z, title):
    fig = plt.figure()

    ax1 = fig.add_subplot(2, 1, 1, projection='3d')
    ax1.plot_surface(x, y, z, rstride=3, cstride=3, linewidth=1, antialiased=True, cmap=cm.viridis)
    ax1.view_init(55, -70)

    ax2 = fig.add_subplot(2, 1, 2, projection='3d')
    ax2.contourf(x, y, z, zdir='z', offset=0, cmap=cm.viridis)
    ax2.view_init(90, 270)
    ax2.grid(False)
    ax2.set_zticks([])

    fig.suptitle(title)
    plt.show()

data = np.linspace(-10, 10, 100)
x, y = np.meshgrid(data, data)
data = np.empty(x.shape + (2,))
data[:, :, 0] = x
data[:, :, 1] = y

z = multivariate_gaussian(data, mean_a, cov_a)
plot_gauss(x, y, z, 'data_a')

z = multivariate_gaussian(data, mean_b, cov_b)
plot_gauss(x, y, z, 'data_b')

# Mahalanobis distance
test_1 = v.dot(test.iloc[[0]].transpose())
test_1 = np.array([test_1[v1], test_1[v2]]).transpose()

test_2 = v.dot(test.iloc[[1]].transpose())
test_2 = np.array([test_2[v1], test_2[v2]]).transpose()

def mahalanobis_distance(data, mean, cov):
    return np.sqrt(np.matmul(data - mean, np.matmul(np.linalg.inv(cov), (data - mean).transpose()))).item(0)

test_1a = mahalanobis_distance(test_1, mean_a, cov_a)
test_1b = mahalanobis_distance(test_1, mean_b, cov_b)
test_2a = mahalanobis_distance(test_2, mean_a, cov_a)
test_2b = mahalanobis_distance(test_2, mean_b, cov_b)

print('\nmahalanobis distance')
print(f"test[0]: {[test_1a, test_1b]}")
print(f"test[1]: {[test_2a, test_2b]}")