import serial
import time

data_serial = serial.Serial("COM4", 9600)

time.sleep(1)

while True:
    data = input("Enter signal for servo: ")
    data = data + '\r'
    
    data_serial.write(data.encode())