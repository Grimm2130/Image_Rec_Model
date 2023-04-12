# Capture class:
# This class serves a Holder for functions that have to do with 
# Image 
# * Capture 
# * manipulation


import os
import time
import tensorflow as tf
import matplotlib.pyplot as plt
import matplotlib.image as pmg

def takePicture_Front(image_name):
    ''' Function to take pictures using the front camera.
        Different function was used since a USB camera was used.
    '''
    image_name += ".jpeg"
    imagePath = "/home/pi/Documents/SeniorDesign/Images"
    # append the picture type to the image
    imagePath = os.path.join(imagePath, image_name)
    # take picture
    os.system(f"ffmpeg -f video4linux2 -s 1280x720 -i /dev/video1 -vframes 1 -y {imagePath}")
    # Validate image capture
    if(os.path.exists(imagePath)):
        image = tf.io.read_file(imagePath)
        image = tf.image.decode_jpeg(image)
        image = tf.image.resize(image, [224,224])
    else:
        print("No image")
        image = []
        
    return image

def takePicture_Side(image_name):
    '''Takes a picture of a sspecified size and returns the path image name
        Args:
            NONE
        Returns:
            image
    '''
    image_name += ".jpeg"
    imagePath = "/home/pi/Documents/SeniorDesign/Images"
    # append the picture type to the image
    imagePath = os.path.join(imagePath, image_name)
    previewTime = 10
    size = 224
    # take picture
    os.system(f"libcamera-jpeg -o {imagePath} -t {previewTime} --width {size} --height {size}")
    if(os.path.exists(imagePath)):
        image = tf.io.read_file(imagePath)
        image = tf.image.decode_jpeg(image)
        image = tf.image.resize(image, [224,224])
    else:
        print("No image")
        image = []
    return image

def getImage_Side(imagePath):
    '''Return an already available image'''
    image = tf.io.read_file(imagePath)
    image = tf.image.decode_jpeg(image)
    image = tf.image.resize(image, [224,224])
    return image

