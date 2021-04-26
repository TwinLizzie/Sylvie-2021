# Keyboard and i2c control for Sylvie 2021 (Bipedal Robot Lower Body)

import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../inverse_kinematics')
sys.path.insert(1, '../registry')

from time import sleep
import serial
import keyboard
import bluetooth
import os

import nanoik_v2 as nanoik
import bipedalGame_data as bipedalGame

server_socket=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
port = 1

ser = serial.Serial('/dev/ttyUSB0', 9600)

# n17_sRockL1_address = 0x11
# n17_sRockR1_address = 0x12

# Our global variables
previous_menu = 0
menu = 0      
encoded_command = ""

limb = 0
link_1 = 0
link_2 = 0

hypotenuse = 0
foot_dist = 0

ee_zL = 0
ee_xL = 0.001

ee_zR = 0
ee_xR = 0.001

gbx_L1 = 100
gbx_L2 = 100
gbx_L3 = 100

gbx_R1 = 100
gbx_R2 = 100
gbx_R3 = 100

gbx_sr_all = 100

gbx_waist = 100

ra1L_old = 0
ra2L_old = 0
ra3L_old = 0

ra1R_old = 0
ra2R_old = 0
ra3R_old = 0

on_startup = True

def quickRnd(val):
    newVal = str(int(round((val * 10), 1)))
    return newVal

def show_key(keyboard_key):
    os.system('clear')
    print("KEYBOARD KEY [" + keyboard_key + "] PRESSED")

    sleep(0.25)

    global on_startup
    global previous_menu

    on_startup = False
    previous_menu = -1

def broadcaster_use(keyboard_key, menu_num):
    if menu_num == 1:
        encoded_command = bipedalGame.enc_message_one(keyboard_key)
    elif menu_num == 2:
        encoded_command = bipedalGame.enc_message_two(keyboard_key)
    ser.write(encoded_command.encode("utf-8"))

    show_key(keyboard_key)

print("Waiting for Bluetooth connection...")
server_socket.bind(("",port))
server_socket.listen(1)
client_socket,address = server_socket.accept()
print("Accepted connection from ",address)

while True:
    res = client_socket.recv(1024)
    client_socket.send(res)
        
    if menu == 0:
        os.system('clear')
        limb = 0
        link_1 = 0
        link_2 = 0

        hypotenuse = 0
        ee_z = 0
        ee_x = 0.01

        print("Welcome to SylvieOS 2020!")
        print("Make sure both of your robot legs are in line and parallel to each other.")
        print("")
        print("Protip: 1 meter = 1, 50 centimeters = 0.5. Measure joints from the pivot point/center.")

        hypotenuse = float(input("Enter the distance between Joint 1 and Joint 3 i.e. Hypotenuse: "))
        link_1 = float(input("Enter the distance between Joint 1 and Joint 2 i.e. Thigh length: "))
        link_2 = float(input("Enter the distance between Joint 2 and Joint 3 i.e. Leg length: "))

        if hypotenuse > 0:
            ee_zL = hypotenuse
            ee_zR = hypotenuse
            menu = 1

    elif menu == 1:
        solvedik_left = nanoik.solveKinematicsSide(ee_zL, ee_xL, link_1, link_2) 
        solvedik_right = nanoik.solveKinematicsSide(ee_zR, ee_xR, link_1, link_2)

        if menu != previous_menu:
            if on_startup == False:          
                gbx_L1 = gbx_L1 + (solvedik_left[0] - ra1L_old)
                gbx_L2 = gbx_L2 + (ra2L_old - solvedik_left[1]) # To reverse motor direction, swap these!
                gbx_L3 = gbx_L3 + (solvedik_left[2] - ra3L_old)

                gbx_R1 = gbx_R1 + (ra1R_old - solvedik_right[0])
                gbx_R2 = gbx_R2 + (ra2R_old - solvedik_right[1])
                gbx_R3 = gbx_R3 + (ra3R_old - solvedik_right[2])

                encoded_command = "none,none," + quickRnd(gbx_L1) + "," + quickRnd(gbx_L2) + "," + quickRnd(gbx_L3) + "," + quickRnd(gbx_R1) + "," + quickRnd(gbx_R2) + "," + quickRnd(gbx_R3) + ",none,none\n"

                ser.write(encoded_command.encode("utf-8"))

                sleep(0.25)

            os.system('clear')

            l_leg_angles = [quickRnd(gbx_L1), quickRnd(gbx_L2), quickRnd(gbx_L3)]
            r_leg_angles = [quickRnd(gbx_R1), quickRnd(gbx_R2), quickRnd(gbx_R3)]

            l_ee_pos = round(ee_zL, 3), round(ee_xL, 3)
            r_ee_pos = round(ee_zR, 3), round(ee_xR, 3)

            sr_angles = str(int(round((gbx_sr_all * 10), 1)))
            waist_angle = str(int(round((gbx_waist * 10), 1)))
     
            bipedalGame.menuOneText(l_leg_angles, r_leg_angles, l_ee_pos, r_ee_pos, sr_angles, waist_angle, encoded_command)

            previous_menu = menu

        ra1L_old = solvedik_left[0]
        ra2L_old = solvedik_left[1]
        ra3L_old = solvedik_left[2]

        ra1R_old = solvedik_right[0]
        ra2R_old = solvedik_right[1]
        ra3R_old = solvedik_right[2]

        # Bluetooth Control

        if str(res)[2] == 'w':
            ee_zL = ee_zL - 0.1
            show_key('w')
        elif str(res)[2] == 's':
            ee_zL = ee_zL + 0.1
            show_key('s')
        elif str(res)[2] == 'd':
            ee_xL = ee_xL + 0.1
            show_key('d')
        elif str(res)[2] == 'a':
            ee_xL = ee_xL - 0.1
            show_key('a')
        elif str(res)[2] == 't':
            ee_zR = ee_zR - 0.1
            show_key('t')
        elif str(res)[2] == 'g':
            ee_zR = ee_zR + 0.1
            show_key('g')
        elif str(res)[2] == 'h':
            ee_xR = ee_xR + 0.1
            show_key('h')
        elif str(res)[2] == 'f':
            ee_xR = ee_xR - 0.1
            show_key('f')
        elif str(res)[2] == 'i':
            ee_zL = ee_zL - 0.1
            ee_zR = ee_zR - 0.1
            show_key('i')
        elif str(res)[2] == 'k':
            ee_zL = ee_zL + 0.1
            ee_zR = ee_zR + 0.1
            show_key('k')
        elif str(res)[2] == 'l':
            ee_xL = ee_xL + 0.1
            ee_xR = ee_xR + 0.1
            show_key('l')
        elif str(res)[2] == 'j':
            ee_xL = ee_xL - 0.1
            ee_xR = ee_xR - 0.1
            show_key('j')

        elif str(res)[2] == 'c':
            gbx_waist = gbx_waist + 0.5
            show_key('c')
        elif str(res)[2] == 'v':
            gbx_waist = gbx_waist - 0.5
            show_key('v')
        elif str(res)[2] == 'b':
            gbx_sr_all = gbx_sr_all + 0.1
            broadcaster_use('b', 1)
        elif str(res)[2] == 'n':
            gbx_sr_all = gbx_sr_all - 0.1
            broadcaster_use('n', 1)
        elif str(res)[2] == '4':
            broadcaster_use('4', 1)
        elif str(res)[2] == '5':
            broadcaster_use('5', 1)                         
        elif str(res)[2] == '6':
            broadcaster_use('6', 1)
        elif str(res)[2] == '7':
            broadcaster_use('7', 1)
        elif str(res)[2] == '8':
            broadcaster_use('8', 1)
        elif str(res)[2] == '9':
            broadcaster_use('9', 1)  
        elif str(res)[2] == '2':
            os.system('clear')
            print("NAVIGATING TO MENU 2")

            sleep(1)

            on_startup = False
            menu = 2
            previous_menu

    elif menu == 2:
        if menu != previous_menu:
            os.system('clear')    
            print("Individual joint tweaking menu")
            print("This is where gearboxes can be adjusted one at a time")
            print("Press QWERTYASDFGH to move one gearbox by 0.5 degrees")

            previous_menu = menu

        # Left leg

        if str(res)[2] == 'q':
            broadcaster_use('q', 2)
        elif str(res)[2] == 'w':
            broadcaster_use('w', 2)
        elif str(res)[2] == 'e':
            broadcaster_use('e', 2)
        elif str(res)[2] == 'r':
            broadcaster_use('r', 2)
        elif str(res)[2] == 't':
            broadcaster_use('t', 2)
        elif str(res)[2] == 'y':
            broadcaster_use('y', 2)

        # Right leg

        elif str(res)[2] == 'a':
            broadcaster_use('a', 2)
        elif str(res)[2] == 's':
            broadcaster_use('s', 2)
        elif str(res)[2] == 'd':
            broadcaster_use('d', 2)
        elif str(res)[2] == 'f':
            broadcaster_use('f', 2)
        elif str(res)[2] == 'g':
            broadcaster_use('g', 2)
        elif str(res)[2] == 'h':
            broadcaster_use('h', 2)
        elif str(res)[2] == 'u':
            broadcaster_use('u', 2)
        elif str(res)[2] == 'i':
            broadcaster_use('i', 2)
        elif str(res)[2] == 'z':
            broadcaster_use('z', 2)
        elif str(res)[2] == 'x':
            broadcaster_use('x', 2)
        elif str(res)[2] == 'c':
            broadcaster_use('c', 2)
        elif str(res)[2] == 'v':
            broadcaster_use('v', 2)
        elif str(res)[2] == 'b':
            broadcaster_use('b', 2)
        elif str(res)[2] == 'n':
            broadcaster_use('n', 2)
        elif str(res)[2] == '1':
            os.system('clear')
            print("RETURNING TO MENU 1")

            sleep(1)

            on_startup = False
            menu = 1
            previous_menu = -1

client_socket.close()
server_socket.close()
