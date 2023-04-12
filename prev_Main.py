# password == ochiwar18

import os
import RPi.GPIO as gpio
import time
import tensorflow as tf
import numpy as np                                  

##===========Helper Functions===============
from Helpers.Camera import getImage, takePicture                             # Image handling functions
from Helpers.ImageRec_handler import in_mem_Load_model, predictOnPicture    # Model Control functions 
from Helpers.Spray import toggle_spray                                      # GPIO spray control Functions 
from Helpers.Serial_Comm import send, read                                  # Serial Communication Functions
from flask import Flask, render_template

app = Flask(__name__)


if __name__ == "__main__":
    # Load Model
    model = in_mem_Load_model()
    
    #define header path
    header_path = "/home/pi/Documents/SeniorDesign/SeniorDes_Images/Test/Corn"
    
    # Get list of image names
    image_names = os.listdir(header_path)
    
    pin = 7
    
    valids = 0
    # Predict across images
    for i in range(len(image_names)):
        print(f"Current image: {image_names[i]}")
        
        # get image path
        imagePath = header_path + '/' + image_names[i]
        
        # Get path to image matrix
        image = getImage(imagePath)
        
        # Predict on image
        pred = predictOnPicture(model=model, img = image)
        print(f"Image of: {pred[1]}")
        
        # Toggle Spray
       
        # time.sleep(0.5)
        toggle_spray(pred, valids)

    print(f"Number of valids Predictions: {valids}\nThat's a {valids/len(image_names)}% accuracy")


  
      