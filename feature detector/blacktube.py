import cv2
import numpy as np
import skimage.feature
import cv2 #for resizing image
import glob as gb
import skimage.measure
from skimage.filters import gaussian
from skimage.segmentation import active_contour



def auto_canny(image, sigma=0.33):
    # compute the median of the single channel pixel intensities
    v = np.min(image)

    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)
    # return the edged image
    return edged


def con_bri(image,a,b):
    color=a * image + b
    color[color > 255] = 255
    color[color < 0] = 0
    return color



img_path = gb.glob("data/Retroflect-at-end/tube/black/*.png")
num = 0
for path in img_path:
    image = cv2.imread(path)#3766 3767  3768 3832-3835
    HSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h_channel, s_channel, v_channel = cv2.split(HSV)
    lower_black = np.array([0,0,0])
    upper_black = np.array([180,255,40])
    mask = cv2.inRange(HSV, lower_black, upper_black)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imshow('image',image)
    cv2.imshow('mask_h',h_channel)
    cv2.imshow('mask_s',s_channel)
    cv2.imshow('mask_v',v_channel)
    #--------find background----------
    #this part is use to find back ground and align different region, delete small area
    label = skimage.measure.label(mask, connectivity = 2)
    area_n,area_num = np.unique(label,return_counts= True)
    background_label = area_n[area_num == max(area_num)]
    effect_label = area_n[area_num > 3000]
    effect_label = effect_label[effect_label != background_label]
    sum_mask = []
    ROI = []
    mask = np.zeros_like(mask)
    for i in effect_label:
        #mask = np.zeros_like(mask)
        mask[label == i] = 255#background
        cv2.imshow('mask',mask)
    # -------find contour------
    _,contours,hierarchy= cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    #cv2.drawContours(image, contours, -1, (0,255,0), 3)
    #cv2.imshow('small',image)
    #--------get mask----------
    all = []
    for cnt in contours:
        epsilon = 0.01*cv2.arcLength(cnt,True)
        hull = cv2.convexHull(cnt)
        perimeter = cv2.arcLength(hull,True)
        area = cv2.contourArea(hull)
        (cx, cy), radius = cv2.minEnclosingCircle(hull)
        circle_area = np.pi * (radius**2)
        x,y,w,h = cv2.boundingRect(cnt)
        aspect_ratio = float(w)/h
        rect_area = w*h
        extent = float(area)/rect_area
        try:
            PPD_score = (4*np.pi*area)/(perimeter**2) # {\displaystyle PP(D)={\frac {4\pi A(D)}{p^{2}}}} {\displaystyle PP(D)={\frac {4\pi A(D)}{p^{2}}}}
            reck = area / circle_area
            # print(reck)
        except ZeroDivisionError:
                pass
        #print('extent:',extent)
        if len(cnt) >5:
            (x,y),(MA,ma),angle = cv2.fitEllipse(cnt)#find Orientation is the angle at which object is directed
            #print(x,y,MA,ma,angle)
        #for every contour give judge
        #first judge based on area then
        #and abs(ma-MA)<=200
        if area <= 30000 and area >= 3000  and w < 300 and w > 90  and PPD_score>=0.65 and PPD_score <=0.88 and abs(ma-MA)<=200: #and reck <0.6 and reck > 0.15 and abs(ma-MA)<=200:#area
            all.append(hull)
            text = 'Retroflexion'
            cv2.putText(image,text,(100,100),cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), lineType=cv2.LINE_AA)
        mask = np.zeros(gray.shape,np.uint8)
        cv2.drawContours(mask,[hull],0,255,-1)
        pixelpoints = np.transpose(np.nonzero(mask))
        cut = gray[min(pixelpoints[:,0]):max(pixelpoints[:,0]+10),min(pixelpoints[:,1]):max(pixelpoints[:,1]+10)]
        kernel = np.ones((3,3),np.uint8)
        mask = cv2.erode(mask,kernel,iterations=2)
        #cv2.imshow('small',cut)
        cv2.imshow('mask2',mask)
    if all != []:
        num += 1
    print(num)
    cv2.drawContours(image, all, -1, (0,255,0), 3)
     #   x,y,w,h = cv2.boundingRect(cnt)
    cv2.imshow('img',image)




    #retval2,threshold2 = cv2.threshold(ROI,125,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)'''
    cv2.waitKey(0)

cv2.destroyAllWindows()