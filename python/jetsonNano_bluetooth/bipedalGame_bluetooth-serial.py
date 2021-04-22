# Keyboard and i2c control for Sylvie 2021 (Bipedal Robot Lower Body)

import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../inverse_kinematics')

from time import sleep
import serial
import keyboard
import bluetooth
import os

import nanoik_v2 as nanoik

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

ee_zL_sr = 0
ee_zR_sr = 0

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

def enc_message_one(i):
    switcher={
        "4":"2002,none,none,2003,none,none\n",
        "5":"2003,none,none,2002,none,none\n",
        "6":"none,2002,none,none,2003,none\n",
        "7":"none,2003,none,none,2002,none\n",
        "8":"none,none,2002,none,none,2003\n",
        "9":"none,none,2003,none,none,2002\n",
    }
    return switcher.get(i,"Invalid command")

def enc_message_two(i):
    switcher={
        "q":"2002,none,none,none,none,none\n",
        "w":"2003,none,none,none,none,none\n",
        "e":"none,2002,none,none,none,none\n",
        "r":"none,2003,none,none,none,none\n",
        "t":"none,none,2002,none,none,none\n",
        "y":"none,none,2003,none,none,none\n",
        "a":"none,none,none,2002,none,none\n",
        "s":"none,none,none,2003,none,none\n",
        "d":"none,none,none,none,2002,none\n",
        "f":"none,none,none,none,2003,none\n",
        "g":"none,none,none,none,none,2002\n",
        "h":"none,none,none,none,none,2003\n",
    }
    return switcher.get(i,"Invalid command")

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
        encoded_command = enc_message_one(keyboard_key)
    elif menu_num == 2:
        encoded_command = enc_message_two(keyboard_key)
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
    
    # Under Construction
    
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
        foot_dist = float(input("Enter the distance between the two foot gearboxes: "))
        link_1 = float(input("Enter the distance between Joint 1 and Joint 2 i.e. Thigh length: "))
        link_2 = float(input("Enter the distance between Joint 2 and Joint 3 i.e. Leg length: "))

        if hypotenuse > 0:
            ee_zL = hypotenuse
            ee_zR = hypotenuse
            ee_zL_sr = hypotenuse
            ee_zR_sr = hypotenuse
            menu = 1

    elif menu == 1:
        solvedik_left = nanoik.solveKinematicsSide(ee_zL, ee_xL, link_1, link_2) 
        solvedik_right = nanoik.solveKinematicsSide(ee_zR, ee_xR, link_1, link_2)
        # solvedik_front = nanoik.solveKinematicsFront(ee_zL, ee_zR, foot_dist)

        if menu != previous_menu:
            if on_startup == False:          
                gbx_L1 = gbx_L1 + (solvedik_left[0] - ra1L_old)
                gbx_L2 = gbx_L2 + (ra2L_old - solvedik_left[1])
                gbx_L3 = gbx_L3 + (solvedik_left[2] - ra3L_old)

                gbx_R1 = gbx_R1 + (ra1R_old - solvedik_right[0])
                gbx_R2 = gbx_R2 + (ra2R_old - solvedik_right[1])
                gbx_R3 = gbx_R3 + (ra3R_old - solvedik_right[2])

                encoded_command = str(int(round((gbx_L1 * 10), 1))) + "," + str(int(round((gbx_L2 * 10), 1))) + "," + str(int(round((gbx_L3 * 10), 1))) + "," + str(int(round((gbx_R1 * 10), 1))) + "," + str(int(round((gbx_R2 * 10), 1))) + "," + str(int(round((gbx_R3 * 10), 1))) + "\n"

                ser.write(encoded_command.encode("utf-8"))

                sleep(0.25)

            os.system('clear')

            print("Current left leg angles: ", str(int(round((gbx_L1 * 10), 1))), str(int(round((gbx_L2 * 10), 1))), str(int(round((gbx_L3 * 10), 1))))
            print("Current right leg angles: ", str(int(round((gbx_R1 * 10), 1))), str(int(round((gbx_R2 * 10), 1))), str(int(round((gbx_R3 * 10), 1))))
            print("")
            print("Left Leg End Effector position: ", round(ee_zL, 3), round(ee_xL, 3))
            print("Right Leg End Effector position: ", round(ee_zR, 3), round(ee_xR, 3))
            print("")
            print("Current rocking joints angles: ", str(int(round((gbx_sr_all * 10), 1))))
            print("Current waist joint angle: ", str(int(round((gbx_waist * 10), 1))))
            print("Current encoded command: ", encoded_command)
            print("")
            print("Use WASD,TFGH,IJKL,ZX,CV to move the lower body.")

            previous_menu = menu

        ra1L_old = solvedik_left[0]
        ra2L_old = solvedik_left[1]
        ra3L_old = solvedik_left[2]

        ra1R_old = solvedik_right[0]
        ra2R_old = solvedik_right[1]
        ra3R_old = solvedik_right[2]

        # Keyboard Control

        if keyboard.is_pressed('1'):
            nanoik.drawRadarSide(solvedik_left[0], solvedik_left[1], solvedik_left[2], link_1, link_2, "blue")
            show_key('1')
        elif keyboard.is_pressed('2'):
            nanoik.drawRadarSide(solvedik_right[0], solvedik_right[1], solvedik_right[2], link_1, link_2, "red")
            show_key('2')
        elif keyboard.is_pressed('3'):
            nanoik.drawRadarFront((gbx_sr_all - 100), ee_zL, ee_zR, foot_dist, "green")
            show_key('3')
        elif keyboard.is_pressed('w'):
            ee_zL = ee_zL - 0.0025
            show_key('w')
        elif keyboard.is_pressed('s'):
            ee_zL = ee_zL + 0.0025
            show_key('s')
        elif keyboard.is_pressed('d'):
            ee_xL = ee_xL + 0.0025
            show_key('d')
        elif keyboard.is_pressed('a'):
            ee_xL = ee_xL - 0.0025
            show_key('a')
        elif keyboard.is_pressed('t'):
            ee_zR = ee_zR - 0.0025
            show_key('t')
        elif keyboard.is_pressed('g'):
            ee_zR = ee_zR + 0.0025
            show_key('g')
        elif keyboard.is_pressed('h'):
            ee_xR = ee_xR + 0.0025
            show_key('h')
        elif keyboard.is_pressed('f'):
            ee_xR = ee_xR - 0.0025
            show_key('f')
        elif keyboard.is_pressed('i'):
            ee_zL = ee_zL - 0.0025
            ee_zR = ee_zR - 0.0025
            show_key('i')
        elif keyboard.is_pressed('k'):
            ee_zL = ee_zL + 0.0025
            ee_zR = ee_zR + 0.0025
            show_key('k')
        elif keyboard.is_pressed('l'):
            ee_xL = ee_xL + 0.0025
            ee_xR = ee_xR + 0.0025
            show_key('l')
        elif keyboard.is_pressed('j'):
            ee_xL = ee_xL - 0.0025
            ee_xR = ee_xR - 0.0025
            show_key('j')
        elif keyboard.is_pressed('z'):
            ee_zL = ee_zL - 0.0025
            ee_zR = ee_zR + 0.0025

            ee_zL_sr = ee_zL_sr - 0.0025
            ee_zR_sr = ee_zR_sr + 0.0025

            gbx_sr_all = 100 + nanoik.solveKinematicsFront(ee_zL_sr, ee_zR_sr, foot_dist)
            show_key('z')  
        elif keyboard.is_pressed('x'):
            ee_zL = ee_zL + 0.0025
            ee_zR = ee_zR - 0.0025

            ee_zL_sr = ee_zL_sr + 0.0025
            ee_zR_sr = ee_zR_sr - 0.0025

            gbx_sr_all = 100 + nanoik.solveKinematicsFront(ee_zL_sr, ee_zR_sr, foot_dist)
            show_key('x')
        elif keyboard.is_pressed('c'):
            gbx_waist = gbx_waist + 0.5
            show_key('c')
        elif keyboard.is_pressed('v'):
            gbx_waist = gbx_waist - 0.5
            show_key('v')
        elif keyboard.is_pressed('4'):
            broadcaster_use('4', 1)
        elif keyboard.is_pressed('5'):
            broadcaster_use('5', 1)                         
        elif keyboard.is_pressed('6'):
            broadcaster_use('6', 1)
        elif keyboard.is_pressed('7'):
            broadcaster_use('7', 1)
        elif keyboard.is_pressed('8'):
            broadcaster_use('8', 1)
        elif keyboard.is_pressed('9'):
            broadcaster_use('9', 1)  
        elif keyboard.is_pressed('right'):
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

        if keyboard.is_pressed('q'):
            broadcaster_use('q', 2)
        elif keyboard.is_pressed('w'):
            broadcaster_use('w', 2)
        elif keyboard.is_pressed('e'):
            broadcaster_use('e', 2)
        elif keyboard.is_pressed('r'):
            broadcaster_use('r', 2)
        elif keyboard.is_pressed('t'):
            broadcaster_use('t', 2)
        elif keyboard.is_pressed('y'):
            broadcaster_use('y', 2)

        # Right leg

        elif keyboard.is_pressed('a'):
            broadcaster_use('a', 2)
        elif keyboard.is_pressed('s'):
            broadcaster_use('s', 2)
        elif keyboard.is_pressed('d'):
            broadcaster_use('d', 2)
        elif keyboard.is_pressed('f'):
            broadcaster_use('f', 2)
        elif keyboard.is_pressed('g'):
            broadcaster_use('g', 2)
        elif keyboard.is_pressed('h'):
            broadcaster_use('h', 2)
        elif keyboard.is_pressed('left'):
            os.system('clear')
            print("RETURNING TO MENU 1")

            sleep(1)

            on_startup = False
            menu = 1
            previous_menu = -1
