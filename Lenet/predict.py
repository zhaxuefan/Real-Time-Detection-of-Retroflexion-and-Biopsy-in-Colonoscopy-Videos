# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 22:13:53 2019

@author: xzha
"""

from IPython.display import Image, display
from tensorflow.python.keras.preprocessing.image import ImageDataGenerator
from tensorflow.python.keras.preprocessing.image import load_img, img_to_array
import tensorflow.keras
from tensorflow.python.keras.applications import ResNet50
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense, Flatten, GlobalAveragePooling2D, BatchNormalization
import os, random
from tensorflow.python.keras.applications.resnet50 import preprocess_input
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import glob as gb
data_generator = ImageDataGenerator(horizontal_flip=True,
                                   width_shift_range = 0.4,
                                   height_shift_range = 0.4,
                                   zoom_range=0.3,
                                   rotation_range=20,
                                   )

model = tensorflow.keras.models.load_model('mymodel.h5')
model.summary()
batch_size = 20
train_generator = data_generator.flow_from_directory(
        'C:/Users/xzha/Desktop/resnet/Retroflexion/',
        target_size=(431, 401),
        batch_size=batch_size,
        class_mode='categorical')

num_classes = len(train_generator.class_indices)
feature = []
correct_num = 0

imgpath = gb.glob('C:/Users/xzha/Desktop/resnet/Retroflexion/tube/*.png')
for path in imgpath:  
    imgs = load_img(path, target_size=(431,401))
    img_array = np.array(img_to_array(imgs))
    img_array = np.expand_dims(img_array,axis = 0)
    imginput = preprocess_input(img_array)
    prediction = model.predict_classes(imginput)
    classes = dict((v,k) for k,v in train_generator.class_indices.items())
    feature.append(classes[prediction[0]])
    print(classes[prediction[0]],'tube')
    if classes[prediction[0]] == 'tube':
        correct_num += 1
