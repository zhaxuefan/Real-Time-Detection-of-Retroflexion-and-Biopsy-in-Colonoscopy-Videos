import cv2
import numpy as np
import skimage.feature
import cv2 #for resizing image
import glob as gb
import skimage.measure
from skimage.filters import gaussian
import scipy.io as sio




img_path = gb.glob("data/Retroflexion/normal/*.png")
total_area = []
total_perimeter = []
total_boundrect_width = []
total_PPD = []
total_r = []
total_reock = []
total_eccentricity = []
total_aspectratio = []
total_extent = []
total_solidity = []
total_RGB = []
total_HSV = []
total_LAB = []
num = 0
for path in img_path:
    contour_area = []
    contour_perimeter = []
    contour_boundrect_width = []
    contour_PPD = []
    contour_r = []
    contour_reock = []
    contour_eccentricity = []
    contour_aspectratio = []
    contour_extent = []
    contour_solidity = []
    contour_RGB = []
    contour_HSV = []
    contour_LAB = []
    image = cv2.imread(path)#3766 3767  3768 3832-3835
    HSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h_channel, s_channel, v_channel = cv2.split(HSV)
    LAB = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    lower_black = np.array([0,0,0])
    upper_black = np.array([180,255,40])
    mask = cv2.inRange(HSV, lower_black, upper_black)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # -------find contour------
    _,contours,hierarchy= cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    #--------get mask----------
    all = []
    for cnt in contours:
        hull = cv2.convexHull(cnt)
        # first feature: area
        area = cv2.contourArea(hull)
        if area <= 30000 and area >= 3000:
            contour_area.append(area)
            #second feature: perimeter
            perimeter = cv2.arcLength(hull,True)
            contour_perimeter.append(perimeter)
            #third feature: boundRect
            x,y,w,h = cv2.boundingRect(cnt)
            contour_boundrect_width.append(w)
            # Fourth: ppd score
            if perimeter != 0:
                PPD_score = (4*np.pi*area)/(perimeter**2)
                contour_PPD.append(PPD_score)
            # Fifth: enclosing circle radium
            (cx, cy), radius = cv2.minEnclosingCircle(hull)
            contour_r.append(radius)
            #sixth: reock score
            if radius != 0:
                circle_area = np.pi * (radius**2)
                reck = area / circle_area
                contour_reock.append(reck)
            #seventh: Eccentricity
            if len(cnt) >5:
                (x,y),(MA,ma),angle = cv2.fitEllipse(cnt)
                ma = ma/2
                MA = MA/2
                eccentricity = np.sqrt(1 - pow(MA, 2)/pow(ma, 2))
                contour_eccentricity.append(eccentricity)
            #eight:aspect_ratio
            aspect_ratio = float(w)/h
            contour_aspectratio.append(aspect_ratio)
            #Nine: extent
            obj_area = cv2.contourArea(cnt)
            rect_area = w*h
            extent = float(obj_area)/rect_area
            contour_extent.append(extent)
            #Ten: Solidity
            solidity = obj_area / area
            contour_solidity.append(solidity)
            #11:RGB mean intensity
            mean_val_BGR = cv2.mean(image,mask = mask)
            contour_RGB.append(mean_val_BGR)
            #12:
            mean_val_HSV = cv2.mean(HSV,mask = mask)
            contour_HSV.append(mean_val_HSV)
            #13:
            mean_val_LAB = cv2.mean(LAB,mask = mask)
            contour_LAB.append(mean_val_LAB)


        if area <= 30000 and area >= 3000  and w < 300 and w > 90  and PPD_score>=0.65 and PPD_score <=0.88 and abs(ma-MA)<=200: #and reck <0.6 and reck > 0.15 and abs(ma-MA)<=200:#area
            all.append(hull)
            text = 'black tube'
            cv2.putText(image,text,(100,100),cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), lineType=cv2.LINE_AA)
    if all != []:
        num += 1
    print(num)
    cv2.drawContours(image, all, -1, (0,255,0), 3)
    cv2.imshow('img',image)
    cv2.waitKey(0)
#1
    if contour_area == []:
        total_area.append([0])
    else:
        total_area.append(contour_area)
#2
    if contour_perimeter == []:
        total_perimeter.append([0])
    else:
        total_perimeter.append(contour_perimeter)
#3
    if contour_boundrect_width == []:
        total_boundrect_width.append([0])
    else:
        total_boundrect_width.append(contour_boundrect_width)
#4
    if contour_PPD == []:
        total_PPD.append([0])
    else:
        total_PPD.append(contour_PPD)
#5
    if contour_r == []:
        total_r.append([0])
    else:
        total_r.append(contour_r)
#6
    if contour_reock == []:
        total_reock.append([0])
    else:
        total_reock.append(contour_reock)
#7
    if contour_eccentricity == []:
        total_eccentricity.append([1])
    else:
        total_eccentricity.append(contour_eccentricity)
#8
    if contour_aspectratio == []:
        total_aspectratio.append([0])
    else:
        total_aspectratio.append(contour_aspectratio)
#9
    if contour_extent == []:
        total_extent.append([0])
    else:
        total_extent.append(contour_extent)
#10
    if contour_solidity == []:
        total_solidity.append([0])
    else:
        total_solidity.append(contour_solidity)
#11
    total_RGB.append(contour_RGB)
#12
    total_HSV.append(contour_HSV)
#13
    total_LAB.append(contour_LAB)

#1
sio.savemat('result/Retroflexion/area_n.mat', {
        'area': total_area
    })
#2
sio.savemat('result/Retroflexion/perimeter_n.mat', {
        'perimeter': total_perimeter
    })
#3
sio.savemat('result/Retroflexion/rect_width_n.mat', {
        'rect_width': total_boundrect_width
    })
#4
sio.savemat('result/Retroflexion/PPD_score_n.mat', {
        'PPD': total_PPD
    })
#5
sio.savemat('result/Retroflexion/circleradium_n.mat', {
        'circlerad': total_r
    })
#6
sio.savemat('result/Retroflexion/reock_score_n.mat', {
        'reock_score': total_reock
    })
#7
sio.savemat('result/Retroflexion/eccentricity_n.mat', {
        'eccentricity_score': total_eccentricity
    })
#8
sio.savemat('result/Retroflexion/aspect_ratio_n.mat', {
        'aspect_ratio_score': total_aspectratio
    })
#9
sio.savemat('result/Retroflexion/extent_n.mat', {
        'extent_score': total_extent
    })
#10
sio.savemat('result/Retroflexion/solidity_n.mat', {
        'solidity_score': total_solidity
    })
#11
sio.savemat('result/Retroflexion/areaRGB_n.mat', {
        'areaRGB_score': total_RGB
    })
#12
sio.savemat('result/Retroflexion/areaHSV_n.mat', {
        'areaHSV_score': total_HSV
    })
#13
sio.savemat('result/Retroflexion/areaLAB_n.mat', {
        'areaLAB_score': total_LAB
    })


cv2.destroyAllWindows()