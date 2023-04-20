# password == ochiwar18

# import os
# import ffmpeg
import RPi.GPIO as gpio
import time
# import tensorflow as tf
import numpy as np        
import threading                          

##===========Helper Functions===============
from Helpers.Camera import takePicture_Front, takePicture_Side, getImage_Side       # Image handling functions
from Helpers.ImageRec_handler import in_mem_Load_model, predictOnPicture            # Model Control functions 
# from Helpers.Spray import toggle_spray                                              # GPIO spray control Functions 
# from Helpers.Serial_Comm import send, read                                          # Serial Communication Functions
# from Helpers.pathDetection import frontMain

FRONT_CAMERA_DELAY = 1
SIDE_CAMERA_DELAY = 0.5


def toggleServo():
    serial_pin = 11
    # Setup the gpio
    gpio.setmode(gpio.BOARD)
    gpio.setup(serial_pin, gpio.OUT)
    pwm=gpio.PWM(serial_pin, 50)
    pwm.start(0)

    def SetAngle(angle):
        '''Function to turn the servo'''
        print("Turning")
        duty = angle / 18 + 2
        gpio.output(serial_pin, True)
        pwm.ChangeDutyCycle(duty)
        time.sleep(1)
        gpio.output(serial_pin, False)
        pwm.ChangeDutyCycle(0)

    SetAngle(180) 
    SetAngle(0)
    
    pwm.stop()
    gpio.cleanup()

if __name__ == "__main__":
    
    # os.system(f"ffmpeg -f video4linux2 -s 1280x720 -i /dev/video1 -vframes 1 -y image.jpeg")
    
    # Load Model
    model = in_mem_Load_model()
    
    # Save the current time
    image = np.array([])
    front_start_Time = time.time()
    side_start_Time = time.time()
    
    # begin operation
    while True:
        # time.sleep(0.5)
        # print("Waiting...")
        # Get most recent time
        front_delay_endTime = time.time()
        side_delay_endTime = time.time()

        ## Capture the Front and rear images
        
        # if front_delay_endTime - front_start_Time >= FRONT_CAMERA_DELAY :
        #     # TODO : Insert front camera code here
        #     # print("Front Camera")
        #     frontImage = takePicture_Front("front")
            
        #     # pass to path detection function & send offsets for turns
        #     frontMain(frontImage)
            
        #     # Update the upcounter
        #     front_start_Time = front_delay_endTime
        
        
        if side_delay_endTime - side_start_Time >= SIDE_CAMERA_DELAY:
            print("side Camera")
            image = takePicture_Side("side")
        
            #  predict on image
            pred, pred_class = predictOnPicture(model, image)        
            
            if pred == 0:
                print("Corn predicted")
            # Call the spray function
                t = threading.Thread(target=toggleServo, args = ())
                t.start()
                t.join()
            # Update the upcounter
            side_start_Time = side_delay_endTime
        
    
    
    

