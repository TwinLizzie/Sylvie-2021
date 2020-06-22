import smbus
import time
import os

bus1 = smbus.SMBus(1)
bus0 = smbus.SMBus(0)

i2c_cmd = 0x01

def ConvertStringToBytes(src):
    converted = []
    for b in src:
        converted.append(ord(b))
    return converted

def writeToBytes(bus, i2c_address, message):
    bytesToSend = ConvertStringToBytes(message)

    if bus == 1:
        bus1.write_i2c_block_data(i2c_address, i2c_cmd, bytesToSend)
    else:
        bus0.write_i2c_block_data(i2c_address, i2c_cmd, bytesToSend)

def promptBytes():
#while True:
    message = input("Write some angles here: ")
    bytesToSend = ConvertStringToBytes(message)

    if message == "exit":
        exit()

    bus1.write_i2c_block_data(0x18, i2c_cmd, bytesToSend)
