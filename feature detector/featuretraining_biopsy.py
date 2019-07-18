import cv2
import numpy as np
import skimage.feature
import cv2 #for resizing image
import glob as gb
import skimage.measure
from skimage.filters import gaussian
import scipy.io as sio




img_path = gb.glob("data/Retroflect-at-end/normal/*.png")
total_area = []#1
total_perimeter = []#2
total_boundrect_width = []#3
total_PPD = []#4
total_roundness = []#5
total_convexity = []#6
total_curl = []#7
total_eccentricity = []#8
total_aspectratio = []#9
total_extent = []#10
total_solidity = []#11
total_kcurve = []#12
total_RGB = []#13
total_HSV = []#14
total_LAB = []#15
num = 0
for path in img_path:
    contour_area = []#1
    contour_perimeter = []#2
    contour_boundrect_width = []#3
    contour_PPD = []#4
    contour_roundness= []#5
    contour_convexity = []#6
    contour_curl = []#7
    contour_eccentricity = []#8
    contour_aspectratio = []#9
    contour_extent = []#10
    contour_solidity = []#11
    contour_kcurve = []#12
    contour_RGB = []#13
    contour_HSV = []#14
    contour_LAB = []#15
    image = cv2.imread(path)
    HSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h_channel, s_channel, v_channel = cv2.split(HSV)
    LAB = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    edges = cv2.Canny(blurred,20,100)
    kernel = np.ones((3,3),np.uint8)
    mask = cv2.dilate(edges,kernel)
    # -------find contour------
    _,contours,hierarchy= cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    #--------get mask----------
    all = []
    for cnt in contours:
        hull = cv2.convexHull(cnt)
        # 1: area
        area = cv2.contourArea(hull)
        if area <= 30000 and area >= 3000:
            contour_area.append(area)
            #2: perimeter
            perimeter = cv2.arcLength(cnt,True)
            contour_perimeter.append(perimeter)
            #3: boundRect
            x,y,w,h = cv2.boundingRect(cnt)
            contour_boundrect_width.append(w)
            # 4: ppd score
            obj_area = cv2.contourArea(cnt)
            if perimeter != 0:
                PPD_score = (4*np.pi*obj_area)/(perimeter**2)
                contour_PPD.append(PPD_score)
            # 5: Roundness
            convex_perimeter = cv2.arcLength(hull,True)
            roundness = (4*np.pi*obj_area)/(convex_perimeter**2)
            contour_roundness.append(roundness)
            # 6 : convexity
            if perimeter != 0:
                convexity = convex_perimeter / perimeter
                contour_convexity.append(convexity)
            #7 :Curl
            (ex,ey),(MA,ma),angle = cv2.fitEllipse(cnt)
            fibre_length = (perimeter - np.sqrt(perimeter**2 - 16 * obj_area))/4
            curl = ma / fibre_length
            contour_curl.append(curl)
            #8: Eccentricity
            if len(cnt) >5:
                M = cv2.moments(cnt)
                eccentricity = (M['mu02']-M['mu20'])**2 + 4 * M['mu11']
                eccentricity = eccentricity / obj_area
                contour_eccentricity.append(eccentricity)
            #9:aspect_ratio
            aspect_ratio = float(w)/h
            contour_aspectratio.append(aspect_ratio)
            #10: extent
            rect_area = w*h
            extent = float(obj_area)/rect_area
            contour_extent.append(extent)
            #11: Solidity
            solidity = obj_area / area
            contour_solidity.append(solidity)
            #12:k_curvature:
            tangent = np.reshape(cnt,(len(cnt),2))
            tangent_x = tangent[:, 0]
            tangent_y = tangent[:, 1]
            dx_dt= np.gradient(tangent_x)
            dy_dt = np.gradient(tangent_y)
            ds_dt = np.sqrt(dx_dt * dx_dt + dy_dt * dy_dt)
            d2s_dt2 = np.gradient(ds_dt)
            d2x_dt2 = np.gradient(dx_dt)
            d2y_dt2 = np.gradient(dy_dt)
            curvature = np.abs(d2x_dt2 * dy_dt - dx_dt * d2y_dt2) / (dx_dt * dx_dt + dy_dt * dy_dt)**1.5
            curvature = curvature[~np.isnan(curvature)]
            contour_kcurve.append(np.mean(curvature))
            #13:RGB mean intensity
            mean_val_BGR = cv2.mean(image,mask = mask)
            contour_RGB.append(mean_val_BGR)
            #14:
            mean_val_HSV = cv2.mean(HSV,mask = mask)
            contour_HSV.append(mean_val_HSV)
            #15:
            mean_val_LAB = cv2.mean(LAB,mask = mask)
            contour_LAB.append(mean_val_LAB)


        if area <= 30000 and area >= 3000 and w < 300 and w > 90: #and abs(ma-MA)<=200: #and PPD_score>=0.65 and PPD_score <=0.88 and abs(ma-MA)<=200: #and reck <0.6 and reck > 0.15 and abs(ma-MA)<=200:#area
            all.append(hull)
            text = 'Probe snare'
            cv2.putText(image,text,(100,100),cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255),2, lineType=cv2.LINE_AA)
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
    if contour_roundness == []:
        total_roundness.append([0])
    else:
        total_roundness.append(contour_roundness)
#6
    if contour_convexity == []:
        total_convexity.append([0])
    else:
        total_convexity.append(contour_convexity)
#7
    if contour_curl == []:
        total_curl.append([0])
    else:
        total_curl.append(contour_curl)
#8
    if contour_eccentricity == []:
        total_eccentricity.append([1])
    else:
        total_eccentricity.append(contour_eccentricity)
#9
    if contour_aspectratio == []:
        total_aspectratio.append([0])
    else:
        total_aspectratio.append(contour_aspectratio)
#10
    if contour_extent == []:
        total_extent.append([0])
    else:
        total_extent.append(contour_extent)
#11
    if contour_solidity == []:
        total_solidity.append([0])
    else:
        total_solidity.append(contour_solidity)
#12
    if contour_kcurve == []:
        total_kcurve.append([0])
    else:
        total_kcurve.append(contour_kcurve)
#13
    total_RGB.append(contour_RGB)
#14
    total_HSV.append(contour_HSV)
#15
    total_LAB.append(contour_LAB)

'''
#1
sio.savemat('result_curve/Retroflect-at-end/white/area_loop.mat', {
        'area': total_area
    })
#2
sio.savemat('result_curve/Retroflect-at-end/white/perimeter_loop.mat', {
        'perimeter': total_perimeter
    })
#3
sio.savemat('result_curve/Retroflect-at-end/white/rect_width_loop.mat', {
        'rect_width': total_boundrect_width
    })
#4
sio.savemat('result_curve/Retroflect-at-end/white/PPD_score_loop.mat', {
        'PPD': total_PPD
    })
#5
sio.savemat('result_curve/Retroflect-at-end/white/roundness_loop.mat', {
        'roundness': total_roundness
    })
#6
sio.savemat('result_curve/Retroflect-at-end/white/convexity_loop.mat', {
        'convexity': total_convexity
    })
#7
sio.savemat('result_curve/Retroflect-at-end/white/curl_loop.mat', {
        'curl': total_curl
    })
#8
sio.savemat('result_curve/Retroflect-at-end/white/eccentricity_loop.mat', {
        'eccentricity_score': total_eccentricity
    })
#9
sio.savemat('result_curve/Retroflect-at-end/white/aspect_ratio_loop.mat', {
        'aspect_ratio_score': total_aspectratio
    })
#10
sio.savemat('result_curve/Retroflect-at-end/white/extent_loop.mat', {
        'extent_score': total_extent
    })
#11
sio.savemat('result_curve/Retroflect-at-end/white/solidity_loop.mat', {
        'solidity_score': total_solidity
    })
#12
sio.savemat('result_curve/Retroflect-at-end/white/kcurve_loop.mat', {
        'kcurve': total_kcurve
    })
#13
sio.savemat('result_curve/Retroflect-at-end/white/areaRGB_loop.mat', {
        'areaRGB_score': total_RGB
    })
#14
sio.savemat('result_curve/Retroflect-at-end/white/areaHSV_loop.mat', {
        'areaHSV_score': total_HSV
    })
#15
sio.savemat('result_curve/Retroflect-at-end/white/areaLAB_loop.mat', {
        'areaLAB_score': total_LAB
    })
'''

cv2.destroyAllWindows()