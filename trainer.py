import os
import numpy as np
import keras
from keras import backend as K
from keras.layers.core import Dense, Activation
from keras.optimizers import Adam
from keras.metrics import categorical_crossentropy
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image
from keras.models import Model
from keras.layers import Dense,GlobalAveragePooling2D
from keras.applications import Xception
from keras.applications.xception import preprocess_input
from sys import platform

path = os.getcwd()
slash = "/"
if platform == "win32":
    slash = "\\"

dataset = path+slash+"Dataset"
BATCH_SIZE = 32
EPOCHS = 30

base_model=Xception(weights='imagenet',include_top=False) #imports the mobilenet model and discards the last 1000 neuron layer.

x=base_model.output
x=GlobalAveragePooling2D()(x)
x=Dense(1024,activation='relu')(x) #we add dense layers so that the model can learn more complex functions and classify for better results.
x=Dense(1024,activation='relu')(x) #dense layer 2
x=Dense(512,activation='relu')(x) #dense layer 3
preds=Dense(4,activation='softmax')(x) #final layer with softmax activation

model=Model(inputs=base_model.input,outputs=preds)

for layer in model.layers[:20]:
    layer.trainable=False
for layer in model.layers[20:]:
    layer.trainable=True

model.compile(optimizer='Adam',loss='categorical_crossentropy',metrics=['accuracy'])

train_datagen=ImageDataGenerator(preprocessing_function=preprocess_input) 
train_generator=train_datagen.flow_from_directory(dataset+slash+"train",
                                                 target_size=(110,110),
                                                 color_mode='rgb',
                                                 batch_size=BATCH_SIZE,
                                                 class_mode='categorical',
                                                 shuffle=True)

val_datagen=ImageDataGenerator(preprocessing_function=preprocess_input) 
val_generator=val_datagen.flow_from_directory(dataset+slash+"val",
                                                 target_size=(110,110),
                                                 color_mode='rgb',
                                                 batch_size=BATCH_SIZE,
                                                 class_mode='categorical',
                                                 shuffle=True)

step_size_train=train_generator.n//train_generator.batch_size
VALIDATION_STEPS=val_generator.n//val_generator.batch_size
model.fit_generator(generator=train_generator, validation_data=val_generator,
                   steps_per_epoch=step_size_train, validation_steps=VALIDATION_STEPS,
                   epochs=EPOCHS)

model.save('model.h5')
