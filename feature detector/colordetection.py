import cv2
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib import colors
from sklearn.cluster import KMeans
from collections import Counter
import cv2 #for resizing image

def get_dominant_color(image, k=4, image_processing_size = None):
    """
    takes an image as input

    #>>> get_dominant_color(my_image, k=4, image_processing_size = (25, 25))
    [56.2423442, 34.0834233, 70.1234123]
    """
    #resize image if new dims provided
    if image_processing_size is not None:
        image = cv2.resize( image, image_processing_size, interpolation = cv2.INTER_AREA )
    cv2.imshow( 'image',image )
    #reshape the image to be a list of pixels
    image = image.reshape((image.shape[0] * image.shape[1], 3))

    #cluster and assign labels to the pixels
    clt = KMeans(n_clusters = k)
    labels = clt.fit_predict(image)
    #count labels to find most popular
    label_counts = Counter(labels)

    #subset out most popular centroid
    dominant_color = clt.cluster_centers_[label_counts.most_common(1)[0][0]]

    return list(dominant_color)

def plot_rgbcolorspace(image):
    r, g, b = cv2.split(image)
    plt.hist(r,bins='auto')
    fig = plt.figure()
    axis = fig.add_subplot(1, 1, 1, projection="3d")
    pixel_colors = image.reshape((np.shape(image)[0]*np.shape(image)[1], 3))
    norm = colors.Normalize(vmin=-1.,vmax=1.)
    norm.autoscale(pixel_colors)
    pixel_colors = norm(pixel_colors).tolist()
    axis.scatter(r.flatten(), g.flatten(), b.flatten(), facecolors=pixel_colors, marker=".")
    axis.set_xlabel("Red")
    axis.set_ylabel("Green")
    axis.set_zlabel("Blue")
    plt.show()

def plot_hsvcolorspace(image):
    hsv_nemo = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    h, s, v = cv2.split(image)
    fig1 = plt.figure()
    axis = fig1.add_subplot(1, 1, 1, projection="3d")
    pixel_colors = image.reshape((np.shape(image)[0]*np.shape(image)[1], 3))
    norm = colors.Normalize(vmin=-1.,vmax=1.)
    norm.autoscale(pixel_colors)
    pixel_colors = norm(pixel_colors).tolist()
    axis.scatter(h.flatten(), s.flatten(), v.flatten(), facecolors=pixel_colors, marker=".")
    axis.set_xlabel("Hue")
    axis.set_ylabel("Saturation")
    axis.set_zlabel("Value")
    plt.show()



def most_frequent_colour(image):

    w, h = image.size
    pixels = image.getcolors(w * h)

    most_frequent_pixel = pixels[0]

    for count, colour in pixels:
        if count > most_frequent_pixel[0]:
            most_frequent_pixel = (count, colour)

    return most_frequent_pixel[1]


image = cv2.imread('data/7.png')
#cv2.imshow('image',image)
image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
color = get_dominant_color(image, k=2)
print(color)
plot_rgbcolorspace(image)
plot_hsvcolorspace(image)
LAB = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
l_channel, a_channel, b_channel = cv2.split(LAB)
cl = 5*np.ones_like(l_channel)
merged_channels = cv2.merge((cl,a_channel, b_channel))
final_image = cv2.cvtColor(merged_channels, cv2.COLOR_LAB2RGB)
cv2.imshow('LAB',final_image)
hsv = cv2.cvtColor(final_image, cv2.COLOR_RGB2HSV)
h_channel, s_channel, v_channel = cv2.split(hsv)
lower_black = np.array([0,0,0])
upper_black = np.array([180,255,28])
mask = cv2.inRange(hsv, lower_black, upper_black)
cv2.imshow('mask',mask)
cv2.waitKey(0)
cv2.destroyAllWindows()

