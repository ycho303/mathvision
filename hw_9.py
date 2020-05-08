from utils import *
import glob
from alignment import image_alignment
from PIL import Image
import argparse


def main(args):
    '''additional booleans for convenience'''
    PLOT_ORIGINAL = False
    PLOT_MEAN = False
    PLOT_EIGEN = False
    PLOT_RECONSTRUCT = False
    PLOT_PREDICTION = True

    '''read image'''
    if args.res:
        extension = 'pgm'
        path = './og_att_faces/s'
    else:
        extension = 'png'
        path = './att_faces/s'

    att_faces = glob.glob(path + f'*.{extension}')
    att_faces.sort(key=lambda x : int(''.join(x[len(path):-4].split('_')) if f'10.{extension}' in x else int('0'.join(x[len(path):-4].split('_')))))

    '''prepare dataset'''
    if args.align:
        train_x = np.array([image_alignment(image) for image in att_faces if f'_1.{extension}' not in image], dtype=np.float64)
        test_x = np.array([image_alignment(image) for image in att_faces if f'_1.{extension}' in image], dtype=np.float64)
    else:
        train_x = np.array([plt.imread(image) for image in att_faces if f'_1.{extension}' not in image], dtype=np.float64)
        test_x = np.array([plt.imread(image) for image in att_faces if f'_1.{extension}' in image], dtype=np.float64)

    train_y = [image.replace(path, '')[:-4] for image in att_faces if f'_1.{extension}' not in image]
    test_y = [image.replace(path, '')[:-4] for image in att_faces if f'_1.{extension}' in image]

    '''convert to a (n, w * h) vector'''
    n, w, h = train_x.shape
    train_x = train_x.reshape(n, w * h)
    tn, tw, th = test_x.shape
    test_x = test_x.reshape(tn, tw * th)

    '''plot original face'''
    if PLOT_ORIGINAL:
        plot_face(train_x, 'Original Image', train_y, w, h, n_row=1, n_col=9)

    '''center train/test dataset'''
    train_centered, mean = subtract_mean(train_x)
    test_centered, _ = subtract_mean(test_x, mean)

    '''visualize mean face'''
    if PLOT_MEAN:
        plot_avg(mean, 'Average Face', w, h)

    '''compute and visualize eigenface'''
    eigenspace = eigen_space(train_centered, args.k)
    if PLOT_EIGEN:
        plot_face(eigenspace.reshape(args.k, w, h), f'Eigenfaces (k={args.k})', ["eigenface_%d" % i for i in range(args.k)], w, h, n_row=1, n_col=args.k)

    '''reconstruct image'''
    _from = 72
    _next = 9
    target = train_centered[_from : _from + _next].reshape(_next, w * h)
    target, eigenvector = reconstruct_image(train_x, target, mean, args.k)
    if PLOT_RECONSTRUCT:
        plot_face(target.reshape(_next, w, h), f'Reconstructed Image (k={args.k})', ['Reconstructed ' + train_y[i] for i in range(_from, _from+_next)], w, h, n_row=1, n_col=_next)

    '''find the closest face'''
    predictions, labels = compute_distance(train_x, train_y, train_centered, test_centered, eigenspace, args.k)
    select = 34
    if PLOT_PREDICTION:
        plot_face(np.vstack([test_x[select], predictions[select]]).reshape(2, tw, th), f'Prediction (k={args.k})', ['Given class: {}'.format(test_y[select].split('_')[0]), 'Closest class: {}'.format(labels[select].split('_')[0])], w, h, n_row=1, n_col=2)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--k', '-k', type=int, default=2)
    parser.add_argument('--align', '-a', dest='align', action='store_true')
    parser.set_defaults(align=False)
    parser.add_argument('--res', '-r', dest='res', action='store_true')
    parser.set_defaults(res=False)
    args = parser.parse_args()
    main(args)

    plt_show(plt)