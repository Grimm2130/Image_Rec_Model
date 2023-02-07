# Camera function for taking pictures and saving them to a file
import os
import matplotlib.pyplot as plt
import matplotlib.image as pmg

def getPicture():
    '''Takes a picture of a sspecified size and returns the path image name
        Args:
            NONE
        Returns:
            image
    '''
    previewTime = 10
    size = 224
    imagePath = "Images/image.jpg"
    # take picture
    os.system(f"libcamera-jpeg -o {imagePath} -t {previewTime} --width {size} --height {size}")
    image = pmg.imread(imagePath)
    return image, image.shape