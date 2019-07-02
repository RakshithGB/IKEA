from keras.models import load_model
from sys import platform
import numpy as np
from sklearn.metrics import confusion_matrix 
from keras.preprocessing import image
import os
from keras.preprocessing.image import ImageDataGenerator
from keras.applications.xception import preprocess_input
import time

TEST_FOLDER = "test"
BATCH_SIZE = 1

path = os.getcwd()
slash = "/"
dataset = path+"/Dataset"

if platform == "win32":
    slash = "\\"
    dataset = path+"\\Dataset"

test_datagen=ImageDataGenerator(preprocessing_function=preprocess_input) 
test_generator=test_datagen.flow_from_directory(dataset+slash+TEST_FOLDER,
                                                 target_size=(110,110),
                                                 color_mode='rgb',
                                                 batch_size=BATCH_SIZE,
                                                 class_mode='categorical',
                                                 shuffle=False)

model = load_model('model.h5')
TEST_STEPS=test_generator.n//test_generator.batch_size
start = time.time()
predictions = model.predict_generator(test_generator, steps=TEST_STEPS)
end = time.time()
y_pred = np.argmax(predictions, axis=1)
y_true = test_generator.labels
matrix = confusion_matrix(y_true, y_pred)
l = len(y_true)
accuracy = sum([y_pred[i]==y_true[i] for i in range(l)])/l

print(" ")
print("Xception CNN")
print(" ")
print("Time Taken: %.3fs"%(end-start))
print("Accuracy: "+str(accuracy*100)+"%")
print(" ")
print("CONFUSION MATRIX:")
print(matrix)
print(" ")
print("CONFUSION MATRIX NORMALISED:")
print(matrix / matrix.astype(np.float).sum(axis=1, keepdims=True))
print(" ")