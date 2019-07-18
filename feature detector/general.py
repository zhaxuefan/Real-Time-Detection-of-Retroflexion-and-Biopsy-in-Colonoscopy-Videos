import cv2
import numpy as np
import skimage.feature
import cv2 #for resizing image
import glob as gb
import skimage.measure
from skimage.filters import gaussian

def auto_canny(image, sigma=0.33):
    # compute the median of the single channel pixel intensities
    v = np.min(image)

    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper,apertureSize = 3,L2gradient= True)
    # return the edged image
    return edged

img_path = gb.glob("data/Cold_biopsy/loop/*.png")
num = 0
for path in img_path:
    img = cv2.imread(path)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    cv2.imshow('gray',img)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    #edges = cv2.Canny(blurred,20,150,apertureSize = 3,L2gradient= True)
    #edges = cv2.Canny(blurred,20,100)
    edges = auto_canny(blurred)
    cv2.imshow('blur',blurred)
    kernel = np.ones((3,3),np.uint8)
    #mask = cv2.erode(edges,kernel)
    mask = cv2.dilate(edges,kernel)
    cv2.imshow('edge',mask)
    _,contours,hierarchy= cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    mask = np.zeros(gray.shape,np.uint8)
    all = []
    for cnt in contours:
        hull = cv2.convexHull(cnt)
        area = cv2.contourArea(cnt)
        rect = cv2.minAreaRect(hull)#( center (x,y), (width, height), angle of rotation )
        box = np.int0(cv2.boxPoints(rect))
        rect_w,rect_h = rect[1]
        if area >= 1200 and rect_w >= 80:
            all.append(hull)
            cv2.drawContours(img,[cnt], -1, (0,255,0), 3)
            #cv2.drawContours(mask,[hull],0,255,-1)
            M = cv2.moments(cnt)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            pixelpoints = np.transpose(np.nonzero(mask))
            kernel = np.ones((3,3),np.uint8)
            mask = cv2.dilate(mask,kernel,iterations=1)
            mask  = cv2.erode(mask,kernel,iterations=1)
            '''rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(img,[box],0,(0,0,255),2)
            print(rect[1])'''
    if all!= []:
        text = 'forceps biopsy'
        cv2.putText(img,text,(100,100),cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), lineType=cv2.LINE_AA)
        num += 1
        cv2.drawContours(mask,all,0,255,-1)
    print(num)
    cv2.imshow('mask',mask)
    #draw_lines(img,lines)
    cv2.imshow('img',img)
    cv2.waitKey(0)

cv2.destroyAllWindows()