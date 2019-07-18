import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.feature import hog
from skimage import data, color, exposure
import heapq
from scipy import stats


def auto_canny(image, sigma=0.33):
    # compute the median of the single channel pixel intensities
    v = np.median(image)

    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)
    # return the edged image
    return edged

def gen_sift_features(gray_img):
    sift = cv2.xfeatures2d.SIFT_create()
    # kp is the keypoints
    #
    # desc is the SIFT descriptors, they're 128-dimensional vectors
    # that we can use for our final features
    kp, desc = sift.detectAndCompute(gray_img, None)
    return kp, desc

def show_sift_features(gray_img, color_img, kp):
    return plt.imshow(cv2.drawKeypoints(gray_img, kp, color_img.copy()))
#blur detection
image = cv2.imread('data/4.png')
cv2.imshow('image',image)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#hsv = cv2.cvtColor(gray, cv2.COLOR_GRAY2HSV)
lightness = np.median(gray)#heapq.nlargest(9,hsv)
print(lightness)
blurred = cv2.GaussianBlur(gray, (7, 7), 0)
#cv2.imshow('blur',blurred)
# threshold the image to reveal light regions in the
# blurred image
'''if lightness < 100:
    threshold = 150
elif lightness <= 110:
    threshold = 190
else:
    threshold = 200'''
thresh = cv2.threshold(blurred, 150, 255, cv2.THRESH_BINARY)[1]
thresh = cv2.dilate(thresh, None, iterations=2)
cv2.imshow('threshold',thresh)
#_, contours, _ = cv2.findContours(thresh,cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

image = cv2.imread('data/4.png')
cv2.imshow('orin',image)
print(image.shape)
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
cv2.imshow('gray',gray)
sobelX = cv2.Sobel(gray,cv2.CV_64F,1,0,ksize=1)#x
sobelY = cv2.Sobel(gray,cv2.CV_64F,0,1,ksize=1)#y
mag,angle = cv2.cartToPolar(sobelX,sobelY,angleInDegrees=True)
mag[mag<10] = 0
kernal = np.ones((2 ,2), "uint8")
mag = cv2.erode(mag,None,iterations=1)
mag = cv2.dilate(mag, kernal, iterations=3)
#mag = cv2.erode(mag,None,iterations=4)
cv2.imshow('mag1',mag)
#print(mag)
#delete blur
mag[thresh!=0] = 0
#mag = cv2.erode(mag,None,iterations=3)
#mag = cv2.dilate(mag,None,iterations=3)
cv2.imshow('mag',mag)
cv2.waitKey(0)
cv2.destroyAllWindows()

'''image = cv2.imread('data/4.png')
cv2.imshow('orin',image)
print(image.shape)
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
cv2.imshow('gray',gray)
sobelX = cv2.Sobel(gray,cv2.CV_64F,1,0,ksize=1)#x
sobelY = cv2.Sobel(gray,cv2.CV_64F,0,1,ksize=1)#y
mag,angle = cv2.cartToPolar(sobelX,sobelY,angleInDegrees=True)
mag[mag<10] = 0
mag = cv2.erode(mag,None,iterations=3)
#mag = cv2.dilate(mag, None, iterations=2)
mag = cv2.erode(mag,None,iterations=4)
cv2.imshow('mag',mag)
print(angle.max())
cv2.waitKey(0)
cv2.destroyAllWindows()'''