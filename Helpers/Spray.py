import RPi.GPIO as gpio
import time

def toggle_spray(pred : int):
    '''
    Takes int the prediction value of the image rec and sends a digital signal to the gpio pin
    GPIO pin done in function to reduce memory cluster
    Params:
        pred: The prediction value from the Image rec model
    Return:
        (void)
    '''
    pin = 7
    
    # decide the switch value
    if(pred==0):
        print("Corn predicted\n")
        gpio.output(pin, gpio.LOW)
        time.sleep(0.5)
        gpio.output(pin, gpio.HIGH)
        print("Corn")
        # wait for spray to complete
        # time.sleep(4)
    else:
        print("Soy predicted\n")
        gpio.output(pin,gpio.HIGH)
        print("Soy")
        
    return