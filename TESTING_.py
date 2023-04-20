import os
import RPi.GPIO as gpio
import time
import tensorflow as tf
import numpy as np      
import threading                            

##===========Helper Functions===============
from Helpers.Camera import takePicture_Front, takePicture_Side, getImage_Side       # Image handling functions                             # Image handling functions
from Helpers.ImageRec_handler import in_mem_Load_model, predictOnPicture            # Model Control functions 
from Helpers.Spray import toggle_spray                                              # GPIO spray control Functions 
# from Helpers.Serial_Comm import send, read                                          # Serial Communication Functions
import random

# Constant 
# Delay time for each camera
FRONT_CAMERA_DELAY = 5                # 0.5 s
SIDE_CAMERA_DELAY = 5                   # 1 s

# GPIO pin control

serial_pin = 11
spray_pin = 7
# Setup the gpio
gpio.setmode(gpio.BOARD)
gpio.setup(serial_pin, gpio.OUT)
gpio.setup(spray_pin, gpio.OUT)


gpio.output(spray_pin, gpio.LOW)
gpio.output(serial_pin, gpio.LOW)



# Global variables
prediction_seq = [0,1,1,0,1,1,0,1,1,0]
pred_idx = 0
side_seq_len = len(prediction_seq)

sides = ["l", "r"]
front_cam_position_seq = [ str(random.choice(sides))+":"+str( (random.choice(range(450,600)),
                                                           random.choice(range(80,100)),
                                                           random.choice(range(0,35)))) 
                          for i in range(20) ]
front_idx = 0
front_seq_len = len(front_cam_position_seq)

# Load Model
# model = in_mem_Load_model()

# Start times
front_start = time.time()
side_start = time.time()

# print(f"Start times:\n-front:{front_start}\n-side:{side_start}")
def toggleServo(pred : int):
    serial_pin = 11
    
    def SetAngle(angle):
        '''Function to turn the servo'''
        print("Turning")
        duty = angle / 18 + 2
        gpio.output(serial_pin, True)
        pwm.ChangeDutyCycle(duty)
        time.sleep(1)
        gpio.output(serial_pin, False)
        pwm.ChangeDutyCycle(0)


    # Setup the gpio
    gpio.setmode(gpio.BOARD)
    gpio.setup(serial_pin, gpio.OUT)

    pwm=gpio.PWM(serial_pin, 50)

    pwm.start(0)

    SetAngle(180) 
    SetAngle(0)

    pwm.stop()
    gpio.cleanup()

while True:
    print("Busy Work...")
    # Curr times
    front_curr = time.time()
    side_curr = time.time()
    # print(f"Curr offsets:\n-front:{front_curr-front_start}\n-side:{side_curr-side_start}")
    time.sleep(1)
    # Front Image Process
    # if ((front_curr - front_start) >= FRONT_CAMERA_DELAY):
    #     print("Processing front image")
    #     # Emulate positional information
    #     front_info = front_cam_position_seq[front_idx]
        
    #     # Emulate front camera send to the arduino
    #     send(front_info)
    #     print(f"sent demo front coords: {front_info}")

    #     # update index info
    #     front_idx = (front_idx+1)%front_seq_len
    #     front_start = front_curr
    #     pass
    
    
    if ( (side_curr-side_start) >= SIDE_CAMERA_DELAY):
        
        print("Processing side image")
        
        # get a prediction
        pred = prediction_seq[pred_idx]
        
        # pass to the spray function
        print(f"Prediction: {pred}, Spray should be toggled")
        # toggle_spray(pred)
        t = threading.Thread(target=toggleServo, args = (pred,))
        
        # update prediction sequence
        pred_idx = (pred_idx + 1)%side_seq_len
        side_start = side_curr
        t.start()
        t.join()
        # update the side frame
    

