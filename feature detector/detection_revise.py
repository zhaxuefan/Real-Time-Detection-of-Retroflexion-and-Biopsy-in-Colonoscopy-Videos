import cv2
import numpy as np
import matplotlib.pyplot as plt

cap = cv2.VideoCapture('Cold.mp4')
kernal = np.ones((2 ,2), "uint8")
while True:
    _, frame = cap.read()
    image = frame[30:550,400:930]
    cv2.imshow('frame',image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    blurred = cv2.GaussianBlur(gray, (11,11), 0)
    #cv2.imshow('blur',blurred)
    # threshold the image to reveal light regions in the
    # blurred image
    thresh = cv2.threshold(blurred, 170, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.erode(thresh, None, iterations=2)
    thresh = cv2.dilate(thresh, None, iterations=4)
    cv2.imshow('blur',thresh)
    #_, contours, _ = cv2.findContours(thresh,cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    sobelX = cv2.Sobel(gray,cv2.CV_64F,1,0,ksize=1)#x
    sobelY = cv2.Sobel(gray,cv2.CV_64F,0,1,ksize=1)#y
    mag_image,angle = cv2.cartToPolar(sobelX,sobelY,angleInDegrees=True)
    mag = mag_image.copy()
    mag[mag_image < np.mean(mag_image)+10] = 0
    mag = cv2.dilate(mag, None, iterations=3)
    mag = cv2.erode(mag,None,iterations=2)
    cv2.imshow('mag1',mag)
    #cv2.imshow('angle',angle)
    #delete blur
    mag[thresh!=0] = 0
    #cv2.imshow('mag',mag)
    mag = np.uint8(mag)
    _, final_contours, _ = cv2.findContours(mag, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    max = 0
    for contour in final_contours:
        area = cv2.contourArea(contour)
        x = contour[:,0][:,1]
        y = contour[:,0][:,0]
        if mag[int(np.max(x)/2+np.min(x)/2),int(np.max(y)/2+np.min(y)/2)] !=0:
            mag[x,y] = 0
    mag = cv2.threshold(mag, 10, 255, cv2.THRESH_BINARY)[1]
    mag = cv2.erode(mag,None,iterations=4)
    mag = cv2.dilate(mag,kernal,iterations=4)
    cv2.imshow('after',mag)
    _, final_contours, _ = cv2.findContours(mag, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    for contour in final_contours:
        area = cv2.contourArea(contour)
        if area > max:
            target = contour
            max = area
        if max > 1000:
            cv2.drawContours(image, target, -1, (0, 255, 0), 3)

    cv2.imshow('image',image)
    key = cv2.waitKey(1)
    if key == 2:
        break

cap.release()
cv2.destroyAllWindows()