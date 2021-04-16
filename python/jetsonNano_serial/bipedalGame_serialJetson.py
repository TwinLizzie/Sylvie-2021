# Keyboard and i2c control for Sylvie 2021 (Bipedal Robot Lower Body)

import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../inverse_kinematics')

from time import sleep
import serial
import keyboard
import os

import nanoik_v2 as nanoik

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

while True:
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

        if keyboard.is_pressed('1'):
            os.system('clear')
            print("KEYBOARD KEY [1] PRESSED!")

            sleep(0.125)

            nanoik.drawRadarSide(solvedik_left[0], solvedik_left[1], solvedik_left[2], link_1, link_2, "blue")

            on_startup = False
            previous_menu = -1
        elif keyboard.is_pressed('2'):
            os.system('clear')
            print("KEYBOARD KEY [2] PRESSED!")

            sleep(0.125)

            nanoik.drawRadarSide(solvedik_right[0], solvedik_right[1], solvedik_right[2], link_1, link_2, "red")

            on_startup = False
            previous_menu = -1
        elif keyboard.is_pressed('3'):
            os.system('clear')
            print("KEYBOARD KEY [3] PRESSED!")

            sleep(0.125)

            nanoik.drawRadarFront((gbx_sr_all - 100), ee_zL, ee_zR, foot_dist, "green")

            on_startup = False
            previous_menu = -1
        elif keyboard.is_pressed('w'):
            os.system('clear')
            print("KEYBOARD KEY [W] PRESSED!")

            sleep(0.25)

            ee_zL = ee_zL - 0.0025

            on_startup = False
            previous_menu = -1
        elif keyboard.is_pressed('s'):
            os.system('clear')
            print("KEYBOARD KEY [S] PRESSED!")

            sleep(0.25)

            ee_zL = ee_zL + 0.0025

            on_startup = False
            previous_menu = -1
        elif keyboard.is_pressed('d'):
            os.system('clear')
            print("KEYBOARD KEY [D] PRESSED!")

            sleep(0.25)

            ee_xL = ee_xL + 0.0025

            on_startup = False
            previous_menu = -1
        elif keyboard.is_pressed('a'):
            os.system('clear')
            print("KEYBOARD KEY [A] PRESSED!")

            sleep(0.25)

            ee_xL = ee_xL - 0.0025

            on_startup = False
            previous_menu = -1       
        elif keyboard.is_pressed('t'):
            os.system('clear')
            print("KEYBOARD KEY [T] PRESSED!")

            sleep(0.25)

            ee_zR = ee_zR - 0.0025

            on_startup = False
            previous_menu = -1
        elif keyboard.is_pressed('g'):
            os.system('clear')
            print("KEYBOARD KEY [G] PRESSED!")

            sleep(0.25)

            ee_zR = ee_zR + 0.0025

            on_startup = False
            previous_menu = -1
        elif keyboard.is_pressed('h'):
            os.system('clear')
            print("KEYBOARD KEY [H] PRESSED!")

            sleep(0.25)

            ee_xR = ee_xR + 0.0025

            on_startup = False
            previous_menu = -1
        elif keyboard.is_pressed('f'):
            os.system('clear')
            print("KEYBOARD KEY [F] PRESSED!")

            sleep(0.25)

            ee_xR = ee_xR - 0.0025

            on_startup = False
            previous_menu = -1    
        elif keyboard.is_pressed('i'):
            os.system('clear')
            print("KEYBOARD KEY [I] PRESSED!")

            sleep(0.25)

            ee_zL = ee_zL - 0.0025
            ee_zR = ee_zR - 0.0025

            on_startup = False
            previous_menu = -1
        elif keyboard.is_pressed('k'):
            os.system('clear')
            print("KEYBOARD KEY [K] PRESSED!")

            sleep(0.25)

            ee_zL = ee_zL + 0.0025
            ee_zR = ee_zR + 0.0025

            on_startup = False
            previous_menu = -1
        elif keyboard.is_pressed('l'):
            os.system('clear')
            print("KEYBOARD KEY [L] PRESSED!")

            sleep(0.25)

            ee_xL = ee_xL + 0.0025
            ee_xR = ee_xR + 0.0025

            on_startup = False
            previous_menu = -1
        elif keyboard.is_pressed('j'):
            os.system('clear')
            print("KEYBOARD KEY [J] PRESSED!")

            sleep(0.25)

            ee_xL = ee_xL - 0.0025
            ee_xR = ee_xR - 0.0025

            on_startup = False
            previous_menu = -1
        elif keyboard.is_pressed('z'):
            os.system('clear')
            print("KEYBOARD KEY [Z] PRESSED!")

            sleep(0.25)

            ee_zL = ee_zL - 0.0025
            ee_zR = ee_zR + 0.0025

            ee_zL_sr = ee_zL_sr - 0.0025
            ee_zR_sr = ee_zR_sr + 0.0025

            gbx_sr_all = 100 + nanoik.solveKinematicsFront(ee_zL_sr, ee_zR_sr, foot_dist)

            on_startup = False
            previous_menu = -1  
        elif keyboard.is_pressed('x'):
            os.system('clear')
            print("KEYBOARD KEY [X] PRESSED!")

            sleep(0.25)

            ee_zL = ee_zL + 0.0025
            ee_zR = ee_zR - 0.0025

            ee_zL_sr = ee_zL_sr + 0.0025
            ee_zR_sr = ee_zR_sr - 0.0025

            gbx_sr_all = 100 + nanoik.solveKinematicsFront(ee_zL_sr, ee_zR_sr, foot_dist)

            on_startup = False
            previous_menu = -1 
        elif keyboard.is_pressed('c'):
            os.system('clear')
            print("KEYBOARD KEY [C] PRESSED!")

            sleep(0.25)

            gbx_waist = gbx_waist + 0.5

            on_startup = False
            previous_menu = -1  
        elif keyboard.is_pressed('v'):
            os.system('clear')
            print("KEYBOARD KEY [V] PRESSED!")

            sleep(0.25)

            gbx_waist = gbx_waist - 0.5

            on_startup = False
            previous_menu = -1
        elif keyboard.is_pressed('4'):
            os.system('clear')
            print("KEYBOARD KEY [4] PRESSED!")

            sleep(0.25)

            encoded_message = "2002,none,none,2003,none,none\n"
            ser.write(encoded_message.encode("utf-8"))

            on_startup = False
            previous_menu = -1
        elif keyboard.is_pressed('5'):
            os.system('clear')
            print("KEYBOARD KEY [5] PRESSED!")

            sleep(0.25)

            encoded_message = "2003,none,none,2002,none,none\n"
            ser.write(encoded_message.encode("utf-8"))

            on_startup = False
            previous_menu = -1                          
        elif keyboard.is_pressed('6'):
            os.system('clear')
            print("KEYBOARD KEY [6] PRESSED!")

            sleep(0.25)

            encoded_message = "none,2002,none,none,2003,none\n"
            ser.write(encoded_message.encode("utf-8"))

            on_startup = False
            previous_menu = -1
        elif keyboard.is_pressed('7'):
            os.system('clear')
            print("KEYBOARD KEY [7] PRESSED!")

            sleep(0.25)

            encoded_message = "none,2003,none,none,2002,none\n"
            ser.write(encoded_message.encode("utf-8"))

            on_startup = False
            previous_menu = -1
        elif keyboard.is_pressed('8'):
            os.system('clear')
            print("KEYBOARD KEY [8] PRESSED!")

            sleep(0.25)

            encoded_message = "none,none,2002,none,none,2003\n"
            ser.write(encoded_message.encode("utf-8"))

            on_startup = False
            previous_menu = -1
        elif keyboard.is_pressed('9'):
            os.system('clear')
            print("KEYBOARD KEY [9] PRESSED!")

            sleep(0.25)

            encoded_message = "none,none,2003,none,none,2002\n"
            ser.write(encoded_message.encode("utf-8"))

            on_startup = False
            previous_menu = -1  
    if keyboard.is_pressed('right'):
            os.system('clear')
            print("NAVIGATING TO MENU 2")

            sleep(1)

            on_startup = False
            menu = 2
            previous_menu = -1
    elif menu == 2:
        if menu != previous_menu:
            os.system('clear')    
            print("Individual joint tweaking menu")
            print("This is where gearboxes can be adjusted one at a time")
            print("Press QWERTYASDFGH to move one gearbox by 0.5 degrees")

            previous_menu = menu

        # Left leg

        if keyboard.is_pressed('q'):
            os.system('clear')
            print("KEYBOARD KEY [Q] PRESSED!")

            sleep(0.25)

            encoded_message = "2002,none,none,none,none,none\n"
            ser.write(encoded_message.encode("utf-8"))

            on_startup = False
            previous_menu = -1
        if keyboard.is_pressed('w'):
            os.system('clear')
            print("KEYBOARD KEY [W] PRESSED!")

            sleep(0.25)

            encoded_message = "2003,none,none,none,none,none\n"
            ser.write(encoded_message.encode("utf-8"))

            on_startup = False
            previous_menu = -1
        if keyboard.is_pressed('e'):
            os.system('clear')
            print("KEYBOARD KEY [E] PRESSED!")

            sleep(0.25)

            encoded_message = "none,2002,none,none,none,none\n"
            ser.write(encoded_message.encode("utf-8"))

            on_startup = False
            previous_menu = -1
        if keyboard.is_pressed('r'):
            os.system('clear')
            print("KEYBOARD KEY [R] PRESSED!")

            sleep(0.25)

            encoded_message = "none,2003,none,none,none,none\n"
            ser.write(encoded_message.encode("utf-8"))

            on_startup = False
            previous_menu = -1
        if keyboard.is_pressed('t'):
            os.system('clear')
            print("KEYBOARD KEY [T] PRESSED!")

            sleep(0.25)

            encoded_message = "none,none,2002,none,none,none\n"
            ser.write(encoded_message.encode("utf-8"))

            on_startup = False
            previous_menu = -1
        if keyboard.is_pressed('y'):
            os.system('clear')
            print("KEYBOARD KEY [Y] PRESSED!")

            sleep(0.25)

            encoded_message = "none,none,2003,none,none,none\n"
            ser.write(encoded_message.encode("utf-8"))

            on_startup = False
            previous_menu = -1

        # Right leg

        if keyboard.is_pressed('a'):
            os.system('clear')
            print("KEYBOARD KEY [A] PRESSED!")

            sleep(0.25)

            encoded_message = "none,none,none,2002,none,none\n"
            ser.write(encoded_message.encode("utf-8"))

            on_startup = False
            previous_menu = -1
        if keyboard.is_pressed('s'):
            os.system('clear')
            print("KEYBOARD KEY [S] PRESSED!")

            sleep(0.25)

            encoded_message = "none,none,none,2003,none,none\n"
            ser.write(encoded_message.encode("utf-8"))

            on_startup = False
            previous_menu = -1
        if keyboard.is_pressed('d'):
            os.system('clear')
            print("KEYBOARD KEY [D] PRESSED!")

            sleep(0.25)

            encoded_message = "none,none,none,none,2002,none\n"
            ser.write(encoded_message.encode("utf-8"))

            on_startup = False
            previous_menu = -1
        if keyboard.is_pressed('f'):
            os.system('clear')
            print("KEYBOARD KEY [F] PRESSED!")

            sleep(0.25)

            encoded_message = "none,none,none,none,2003,none\n"
            ser.write(encoded_message.encode("utf-8"))

            on_startup = False
            previous_menu = -1
        if keyboard.is_pressed('g'):
            os.system('clear')
            print("KEYBOARD KEY [G] PRESSED!")

            sleep(0.25)

            encoded_message = "none,none,none,none,none,2002\n"
            ser.write(encoded_message.encode("utf-8"))

            on_startup = False
            previous_menu = -1
        if keyboard.is_pressed('h'):
            os.system('clear')
            print("KEYBOARD KEY [H] PRESSED!")

            sleep(0.25)

            encoded_message = "none,none,none,none,none,2003\n"
            ser.write(encoded_message.encode("utf-8"))

            on_startup = False
            previous_menu = -1
        if keyboard.is_pressed('left'):
            os.system('clear')
            print("RETURNING TO MENU 1")

            sleep(1)

            on_startup = False
            menu = 1
            previous_menu = -1
