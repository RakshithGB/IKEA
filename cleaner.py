import os
from os import listdir
from PIL import Image
from sys import platform
import split_folders

data_set = "Downloads"

slash = "/"
if platform == "win32":
    slash = "\\"

PATH = os.getcwd()
# Define data path
data_path = PATH+slash+data_set
data_dir_list = listdir(data_path)

for dataset in data_dir_list:
    print(dataset)
    img_list=listdir(data_path+slash+dataset)

    print ('Loaded the images of dataset-'+'{}\n'.format(dataset))
    for filename in img_list:
        if filename.endswith('.JPG'):
            try:
                img = Image.open(data_path+slash+dataset+slash+filename) # open the image file
                print(img._getexif())
            except (IndexError,AttributeError,OSError) as e:
                print("DELTED FILE")
                os.system('rm '+data_path+slash+dataset+slash+filename)

        if filename.endswith('.db'):
            print("DELTED FILE")
            os.system('rm '+data_path+slash+dataset+slash+filename)

split_folders.ratio(data_set, output="Dataset", seed=1337, ratio=(.8, .1, .1)) # default values