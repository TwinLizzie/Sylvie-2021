from time import sleep
from serial import Serial

import serial
import keyboard
import os
import sys

ser = serial.Serial('/dev/ttyUSB0', 9600) # Establish the connection on a specific port

while True:
    print("Welcome to SylvieOS 2020!")
    keyboardInput = str(input("Please enter an angle for the gearbox to move to: "))

    if keyboardInput == "exit":
        exit()
    else:                                     
        ser.write(keyboardInput.encode())	
