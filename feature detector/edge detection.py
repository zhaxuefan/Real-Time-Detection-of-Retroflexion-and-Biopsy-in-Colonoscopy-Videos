import cv2
import numpy as np
import matplotlib.pyplot as plt

def auto_canny(image, sigma=0.33):
    # compute the median of the single channel pixel intensities
    v = np.mean(image)

    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, 50, 100)
    # return the edged image
    return edged


cap = cv2.VideoCapture('test1.mp4')
#cap = cv2.VideoCapture('Retroflect-at-end.mp4')
while True:
    _, frame = cap.read()

    #blurred_frame = cv2.GaussianBlur(frame, (3, 3), 0)
    crop_frame = frame[30:550,400:930]
    #crop_frame = frame[18:345,110:390]
    image_gray = cv2.cvtColor(crop_frame,cv2.COLOR_BGR2GRAY)
    blurred = cv2.blur(image_gray, (2,2), dst=None)
    laplacian = cv2.Laplacian(blurred,cv2.CV_8U)
    cv2.imshow('frame1',laplacian)
    _,thresh = cv2.threshold(laplacian, 10, 255, cv2.THRESH_BINARY)
    cv2.imshow('spot image',thresh)
    #_,thresh2 = cv2.threshold(blurred, np.mean(image_gray), 255, cv2.THRESH_BINARY)
    #cv2.imshow('revisedimage',thresh2)
    #blurred = cv2.GaussianBlur(image_gray, (7, 7), 0)
    #ret,th2 = cv2.threshold(blurred,50,255,cv2.THRESH_BINARY)

    #cv2.imshow('frame2',th2)
    th2 = auto_canny(laplacian)
    kernal = kernel = np.array([[-1, -1, -1],[-1,  8, -1],[-1, -1, -1]])
    #th2 = cv2.dilate(th2,kernal)
    #ret2,th2 = cv2.threshold(image_gray,0,255,cv2.THRESH_OTSU)
    #th2[thresh == 255] = 0
    cv2.imshow('edges',th2)

    _, contours, _ = cv2.findContours(th2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for contour in contours:
        area = cv2.contourArea(contour)

        if area > 1500:
            #cv2.rectangle(crop_frame,(min(contour[:,:,0]),min(contour[:,:,1])),(max(contour[:,:,0]),max(contour[:,:,1])),(0, 255, 0),3)
            cv2.drawContours(crop_frame, contour, -1, (0, 255, 0), 3)
    '''perimeter = cv2.arcLength(cnt,True)
    epsilon = 0.01*cv2.arcLength(cnt,True)
    approx = cv2.approxPolyDP(cnt,epsilon,True)
    hull = cv2.convexHull(cnt)'''
    cv2.imshow("Frame", frame)


    #cv2.imshow("Frame", frame)
    #cv2.imshow("Mask", mask)

    key = cv2.waitKey(1)
    if key == 2:
        break

cap.release()
cv2.destroyAllWindows()