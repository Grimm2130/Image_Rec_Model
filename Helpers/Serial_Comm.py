import serial

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.reset_input_buffer()


def send(data):
    if type(data) is not str:
        data = str(data)
    ser.write(data)

def read():
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        return line
    


# print(val)   
            