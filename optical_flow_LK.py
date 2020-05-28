# code based on https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_video/py_lucas_kanade/py_lucas_kanade.html

import numpy as np
import cv2
from tqdm import tqdm
import glob

RGB_OUTPUT = False
SHOW_IMG = False
SAVE_IMG = True

vid_path = './input2/'
for vid in glob.glob(vid_path+'*'):
    vid_name = vid.replace(vid_path, '')[:-4]
    # vid = ['traffic.mov', 'ppl.mp4']
    cap = cv2.VideoCapture(vid)
    fps = cap.get(cv2.CAP_PROP_FPS)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)-5)
    if length > 1950: # to prevent crash
        length = 1950

    # params
    feature_params = dict(maxCorners=1000,
                          qualityLevel=0.3,
                          minDistance=1,
                          blockSize=7)

    lk_params = dict(winSize=(15,15), 
                     maxLevel=2, 
                     criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

    ret, old_frame = cap.read()
    old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
    w, h = old_gray.shape
    p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)
    
    img_array = []
    search_next_frame = 0
    for i in tqdm(range(length), desc=vid_name):
        if i % 3 == 0:
            mask = np.zeros_like(old_frame)
        ret,frame = cap.read()
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if i % 1 == 0: # For testing
            if search_next_frame > 0:
                p0 = cv2.goodFeaturesToTrack(old_gray, mask=None, **feature_params)
                search_next_frame = 0
            p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)

            for i,(old, new) in enumerate(zip(p0, p1)):
                a,b = old.ravel()
                c,d = new.ravel()
                if c > w or d > h:
                    search_next_frame += 1
                mask = cv2.arrowedLine(mask, (a,b), (c,d), [255, 0, 255], 2)

            if RGB_OUTPUT:
                img = cv2.add(frame, mask)
            else:
                img = cv2.add(cv2.merge((frame_gray, frame_gray, frame_gray)),mask)
            img_array.append(img)

            if SHOW_IMG:
                cv2.imshow(vid_name,img)
                k = cv2.waitKey(10)
                if k == ord('q'):
                        break

            old_gray = frame_gray.copy()
            p0 = p1.reshape(-1,1,2)

    cv2.destroyAllWindows()
    cap.release()

    if SAVE_IMG:
        out = cv2.VideoWriter('./output/optical_{}.avi'.format(vid_name), cv2.VideoWriter_fourcc(*'XVID'), fps, (h, w))
        for i in range(len(img_array)):
            out.write(img_array[i])
        out.release()