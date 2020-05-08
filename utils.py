import matplotlib.pyplot as plt
import numpy as np

def plot_face(images, title, labels, w, h, n_row=1, n_col=10):
    if n_row * n_col >= 40:
        print('Large input may result in crashing. Skipping visualization for >40 images...')
    else:
        plt.figure(figsize=(5 * n_col, 5 * n_row))
        plt.suptitle(title)
        for i in range(n_row * n_col):
            plt.subplot(n_row, n_col, i + 1)
            plt.imshow(np.real(images[i].reshape((w, h))), cmap=plt.cm.gray)
            plt.title(labels[i])
            plt.xticks([])
            plt.yticks([])

def plot_avg(M, title, w, h):
    plt.figure()
    plt.imshow(M.reshape(w, h), cmap=plt.cm.gray)
    plt.title(title)
    plt.xticks([])
    plt.yticks([])

def plt_show(plt):
    plt.show()

def eigen_space(img, k):
    img_cov = np.cov(img)
    w, v = np.linalg.eig(img_cov)
    top_k = np.argsort(w)[-k:]
    return np.array([v.dot(img)[i] for i in top_k])

def subtract_mean(img, mean=None):
    '''From given/computed mean, subtract from img'''
    if mean is None:
        mean = np.mean(img, axis=0)
    centered = img - mean
    return img, mean

def reconstruct_image(_all, img, mean, k):
    _, _, eigenvector = np.linalg.svd(_all, full_matrices=False)
    return np.dot(np.dot(img, eigenvector.T)[:, 0:k], eigenvector[0:k, :]), eigenvector

def predict_face(train_x, train_y, train_img, test_img, eigenvector, k):
    predictions = np.vstack([train_x[euclidian_distance(train_img, test_img, eigenvector, i, k), :] for i in range(test_img.shape[0])])
    labels = [train_y[euclidian_distance(train_img, test_img, eigenvector, i, k)] for i in range(test_img.shape[0])]
    return predictions, labels

def euclidian_distance(train_img, test_img, eigenvector, idx, k):
    train_space = np.dot(eigenvector[:k, :], train_img.T)
    test_space = np.dot(eigenvector[:k, :], test_img[idx: idx+1, :].T)
    euclidian = np.sqrt(np.sum((train_space - test_space) ** 2, axis=0))
    return np.argmin(euclidian)
