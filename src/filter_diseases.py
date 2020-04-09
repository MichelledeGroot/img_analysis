import os
import pandas
from collections import defaultdict
from shutil import copyfile
import re
from tkinter import Tk
from tkinter.filedialog import *
import ctypes  # An included library with Python install.

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
directory = f'{ROOT_DIR}'
diseases = ['effusion', 'cardiomegaly', 'pneumothorax']

def open_dir():
    Tk().withdraw()
    file_path = askdirectory()
    return file_path

def open_dataset():
    Tk().withdraw()
    file_path = askopenfilename()
    return file_path

def copy_images(disease):
    """
    Copies images with a disease from the list above from a the original dataset to a folder
    with only 3 different diseases

    INPUT
        disease: The disease from which the images will be moved

    OUTPUT
        None
    """
    skipped = 0
    number_of_images = 0
    directory = ROOT_DIR + '/Data/imagesK3' 
    if not os.path.exists(directory):
        os.makedirs(directory)
    for key in images_per_disease.keys():

        if re.search(".*"+disease+".*", key, re.IGNORECASE):
            #print(key)
            for image in images_per_disease[key]:
                try:
                    copyfile(os.path.join(original_dataset_dir, image), os.path.join(directory, image))
                    number_of_images += 1
                except FileNotFoundError:
                    skipped += 1
                    continue
    return skipped, number_of_images

if __name__ == '__main__':
    ctypes.windll.user32.MessageBoxW(0, "Select image directory", "Selection menu", 1)
    original_dataset_dir = open_dir()
    ctypes.windll.user32.MessageBoxW(0, "Select dataset csv ", "Selection menu", 1)
    data_entry = open_dataset()

    fields = ['Image Index','Finding Labels']
    try:
        data_frame = pandas.read_csv(os.path.abspath(data_entry), usecols=fields)
        data_dict = data_frame.set_index('Image Index').T.to_dict('list')
        images_per_disease = defaultdict(list)
        for k, v in data_dict.items():
            images_per_disease[v[0].lower()].append(k)


        for disease in diseases:
            print("Copying images for:  " + disease)
            skipped, number_of_images = copy_images(disease)
            print("Number of images not found for : " + disease + " is " + str(skipped))
            print("Number of images for : " + disease + " is " + str(number_of_images))
    except pandas.errors.emptydataerror:
        print("Csv file is empty, load new csv.")

