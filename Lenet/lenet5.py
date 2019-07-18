import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, runniЃng this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("C:/Users/xzha/Desktop/resnet/data/resnetinput_white"))

from tensorflow.python.keras.applications import ResNet50
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense, Flatten, GlobalAveragePooling2D, BatchNormalization
from tensorflow.python.keras.applications.resnet50 import preprocess_input
from tensorflow.python.keras.preprocessing.image import ImageDataGenerator
from tensorflow.python.keras.preprocessing.image import load_img, img_to_array

resnet_weights_path = 'C:/Users/xzha/Desktop/resnet/resnet50_weights_tf_dim_ordering_tf_kernels_notop.h5'

data_generator = ImageDataGenerator(horizontal_flip=True,
                                   width_shift_range = 0.4,
                                   height_shift_range = 0.4,
                                   zoom_range=0.3,
                                   rotation_range=20,
                                   )


batch_size = 20
train_generator = data_generator.flow_from_directory(
        'C:/Users/xzha/Desktop/resnet/data/resnetinput_white/',
        target_size=(431, 401),
        batch_size=batch_size,
        class_mode='categorical')

num_classes = len(train_generator.class_indices)

model = Sequential()

model.add(layers.Conv2D(filters=6, kernel_size=(3, 3), activation='relu'))
model.add(layers.AveragePooling2D())

model.add(layers.Conv2D(filters=16, kernel_size=(3, 3), activation='relu'))
model.add(layers.AveragePooling2D())

model.add(layers.Flatten())

model.add(layers.Dense(units=120, activation='relu'))

model.add(layers.Dense(units=84, activation='relu'))

model.add(layers.Dense(units=10, activation = 'softmax')

model.layers[0].trainable = False
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
count = sum([len(files) for r, d, files in os.walk("C:/Users/xzha/Desktop/resnet/data/resnetinput_white/")])

model.fit_generator(
        train_generator,
        steps_per_epoch= 100,
        epochs=10)

model.save('mymodel_white.h5')