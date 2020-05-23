import cv2
import numpy as np
import copy

DISPLAY_ORIGINAL = False
DISPLAY_ORIGINAL_THRESH = False
DISPLAY_APPROX = False 
DISPLAY_APPROX_SUB_ORIGINAL_THRESH = True

def cv_show_uint8(name, img):
    cv2.imshow(name, img.astype(np.uint8))

'''Global Thresholding'''
def gloabl_thresholding(title, n, img):
    w, h = img.shape
    thresh_img = copy.deepcopy(img)
    thresh_img[img>n] = 0
    name = str(n)
    cv_show_uint8(title + f': {name}', thresh_img)

'''Read image and get shape'''
img = cv2.imread('./hw11_sample.png').astype(int)
# img = cv2.imread('./test.png')
img = img[:,:,0]
w, h = img.shape

if DISPLAY_ORIGINAL:
    cv_show_uint8('Original', img)

'''Original image global thresholding (175)'''
if DISPLAY_ORIGINAL_THRESH:
    gloabl_thresholding('Original Thresholding', 175, img)
    
'''Find X (2nd)'''
A = []
B = []
for x in range(w):
    for y in range(h):
        B.append(img[x, y])
        A.append([x**2, y**2, x*y, x, y, 1])
A = np.array(A)
B = np.array(B)
X = np.matmul(np.matmul(np.linalg.inv(np.matmul(A.T, A)), A.T), B)

'''Get approximated background'''
app_back = copy.deepcopy(img)
for x in range(w):
    for y in range(h):
        app_back[x, y] = X[0] * x**2 + X[1] * y**2 + X[2] * x*y + X[3] * x + X[4] * y + X[5]

if DISPLAY_APPROX:
    cv_show_uint8('Approximated', app_back)

if DISPLAY_APPROX_SUB_ORIGINAL_THRESH:
    sub = np.clip(abs(img - app_back), 0, 255)
    sub[sub>=23]=255
    sub[sub<23]=0
    cv_show_uint8('Original - Approximated', sub)

cv2.waitKey(0)