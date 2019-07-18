

# Import python libraries
import numpy as np
import cv2
import skimage.measure

# set to 1 for pipeline images
debug = 0


class Detectors(object):
    """Detectors class to detect objects in video frame
    Attributes:
        None
    """
    def __init__(self):
        """Initialize variables used by Detectors class
        Args:
            None
        Return:
            None
        """
        self.fgbg = cv2.createBackgroundSubtractorMOG2()
    def auto_canny(self,image, sigma=0.33):
        # compute the median of the single channel pixel intensities
        v = np.median(image)

        # apply automatic Canny edge detection using the computed median
        lower = int(max(0, (1.0 - sigma) * v))
        upper = int(min(255, (1.0 + sigma) * v))
        edged = cv2.Canny(image, 20, 100)
        # return the edged image
        return edged

    def Detect1(self, frame):


        # Convert BGR to GRAY
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect edges
        blurred = cv2.GaussianBlur(gray, (7, 7), 0)
        edges = self.auto_canny(blurred)
        mask = cv2.dilate(edges,None)

        # Find contours
        _, contours, hierarchy = cv2.findContours(mask,
                                                  cv2.RETR_EXTERNAL,
                                                  cv2.CHAIN_APPROX_SIMPLE)


        centers = []  # vector of object centroids in a frame
        # we only care about centroids with size of bug in this example
        # recommended to be tunned based on expected object size for
        # improved performance
        blob_lower_radius_thresh = 8
        # Find centroid for each valid contours
        mask = np.zeros_like(mask)
        for cnt in contours:
            try:
                hull = cv2.convexHull(cnt)
                perimeter = cv2.arcLength(cnt,True)
                rect = cv2.minAreaRect(hull)#( center (x,y), (width, height), angle of rotation )
                box = np.int0(cv2.boxPoints(rect))
                rect_w,rect_h = rect[1]
                if len(cnt) > 5:
                    ell=cv2.fitEllipse(cnt)
                    ell_area =np.pi*ell[1][0]*ell[1][1]
                x,y,w,h = cv2.boundingRect(cnt)
                area = cv2.contourArea(cnt)
                aspect_ratio = float(w)/h
                if area >= 2000 and rect_w >= 90: #or perimeter > 200:
                    #print(rect_w,rect_h)
                    # Calculate and draw circle
                    cv2.drawContours(mask,[hull],0,255,-1)
                    #cv2.drawContours(frame,[box],0,(0,0,255),2)
                    #cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                    (x, y), radius = cv2.minEnclosingCircle(cnt)
                    centeroid = (int(x), int(y))
                    radius = int(radius)
                    if (radius > blob_lower_radius_thresh and (max(rect[1])/min(rect[1]) <= 5)):
                        #cv2.circle(frame, centeroid, radius, (0, 255, 0), 2)
                        cv2.drawContours(frame,[hull], -1, (0,255,0),2)
                        b = np.array([[x], [y]])
                        centers.append(np.round(b))
                        #cv2.imshow('circle',frame)
                cv2.imshow('mask',mask)
                cv2.imshow('frame',frame)
            except ZeroDivisionError:
                pass

        # show contours of tracking objects
        # cv2.imshow('Track Bugs', frame)
        return centers



    def Detect2(self, image,num):

        centers = []  # vector of object centroids in a frame
        HSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        h_channel, s_channel, v_channel = cv2.split(HSV)
        lower_black = np.array([0,0,0])
        upper_black = np.array([180,255,60])
        mask = cv2.inRange(HSV, lower_black, upper_black)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        #--------find background----------
        #this part is use to find back ground and align different region, delete small area
        label = skimage.measure.label(mask, connectivity = 2)
        area_n,area_num = np.unique(label,return_counts= True)
        background_label = area_n[area_num == max(area_num)]
        effect_label = area_n[area_num > 3000]
        effect_label = effect_label[effect_label != background_label]
        mask = np.zeros_like(mask)
        for i in effect_label:
            mask[label == i] = 255#background
        # -------find contour------
        _,contours,hierarchy= cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        #--------get mask----------
        all = []
        frame_PPD = []
        frame_reck = []
        frame_ratio = []
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
            except ZeroDivisionError:
                    pass
            #print('extent:',extent)
            if len(cnt) >5:
                (x,y),(MA,ma),angle = cv2.fitEllipse(cnt)#find Orientation is the angle at which object is directed
                #print(x,y,MA,ma,angle)
            #for every contour give judge
            #first judge based on area then
            #and abs(ma-MA)<=200
            if area <= 30000 and area >= 3000  and w < 300 and w > 90:
                frame_PPD.append(PPD_score)
                frame_reck.append(reck)
                frame_ratio.append(abs(ma-MA))
                if PPD_score>=0.65 and PPD_score <=0.88 and reck <0.6 and reck > 0.2 and abs(ma-MA)<=200:#area
                    all.append(hull)
                    #text = 'black tube'
                    #cv2.putText(image,text,(100,100),cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), lineType=cv2.LINE_AA)
                    mask = np.zeros(gray.shape,np.uint8)
                    cv2.drawContours(mask,[hull],0,255,-1)
                    pixelpoints = np.transpose(np.nonzero(mask))
                    #cut = gray[min(pixelpoints[:,0]):max(pixelpoints[:,0]+10),min(pixelpoints[:,1]):max(pixelpoints[:,1]+10)]
                    b = np.array([[(min(pixelpoints[:,0])+max(pixelpoints[:,0]))/2], [(min(pixelpoints[:,1])+max(pixelpoints[:,1]))/2]])
                    centers.append(np.round(b))
                    kernel = np.ones((3,3),np.uint8)
                    mask = cv2.erode(mask,kernel,iterations=2)
                    cv2.imshow('mask',mask)
        if all != []:
            num += 1
        cv2.drawContours(image, all, -1, (0,255,0), 3)
         #   x,y,w,h = cv2.boundingRect(cnt)
        return centers,num,frame_PPD,frame_reck,frame_ratio