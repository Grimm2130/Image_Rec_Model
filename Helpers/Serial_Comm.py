import serial
import RPi.GPIO as gpio
import time

ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
ser.reset_input_buffer()


def send(data):
    if type(data) is not str:
        data = str(data)
    data = bytes(data, 'utf-8')
    pin = 11
    # Turn toggle the switch
    gpio.output(pin,False)
    time.sleep(0.3)
    gpio.output(pin,True)
    # time.sleep(0.01)
    ser.write(data)
    return

def read():
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        return line
    


# print(val)   
            