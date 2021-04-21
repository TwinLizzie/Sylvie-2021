import smbus
import time
# Nvidia Jetson Nano i2c Bus 0
bus = smbus.SMBus(0)

# This is the address we setup in the Arduino Program
address = 0x10

def writeNumber(value):
    bus.write_byte(address, value)
    return -1

#def readNumber():
#    number = bus.read_byte(address)
#    return number

while True:
    var = input("")
    if not var:
        continue

    writeNumber(var)
#    number = readNumber()
