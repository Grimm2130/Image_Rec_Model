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
    # Setup the gpio
    gpio.setmode(gpio.BOARD)
    gpio.setup(pin, gpio.OUT)
    # decide the switch value
    if(pred[0]==0):
        gpio.output(pin,True)
        print("Corn")
        # wait for spray to complete
        # time.sleep(4)
    else:
        gpio.output(pin,False)
        print("Soy")
        
    gpio.cleanup()
    return