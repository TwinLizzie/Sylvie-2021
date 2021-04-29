# PC Keyboard and Serial control for Sylvie 2021 (Bipedal Robot Lower Body)

import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../inverse_kinematics')
sys.path.insert(1, '../registry')

from time import sleep
import serial
import keyboard
import os

import nanoik_v2 as nanoik
import bipedalGame_data as bipedalGame
import sylvieos_data as sylvieOS

ser = serial.Serial('/dev/ttyUSB0', 9600)

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

ver_speed = [0, 0.1, 0.25, 0.4]
hor_speed = [0, 0.1, 0.25, 0.4]
sr_speed = [0, 0.025, 0.05, 0.1]

gbx_L1 = 100
gbx_L2 = 100
gbx_L3 = 100

gbx_R1 = 100
gbx_R2 = 100
gbx_R3 = 100

gbx_sr_L2 = 100
gbx_sr_R2 = 100

gbx_waist = 100

ra1L_old = 0
ra2L_old = 0
ra3L_old = 0

ra1R_old = 0
ra2R_old = 0
ra3R_old = 0

ra2L_sr_old = 0
ra2R_sr_old = 0

on_startup = True
speed_setting = 1

# Quick rounder and stringifyer

def quickRnd(val):
    newVal = str(int(round((val * 10), 1)))
    return newVal
    
# Show key pressed
    
def show_key(keyboard_key):
    os.system('clear')
    print("KEYBOARD KEY [" + keyboard_key + "] PRESSED")

    sleep(0.25)

    global on_startup
    global previous_menu

    on_startup = False
    previous_menu = -1

# Toggle joint movement angles per key press

def switch_speed(dial):
    os.system('clear')

    global speed_setting

    if dial == "up":
        if speed_setting < 3:
            speed_setting = speed_setting + 1                   

    elif dial == "down":
        if speed_setting > 1:
            speed_setting = speed_setting - 1         
            
    print("SPEED SET TO [" + str(speed_setting) + "]")            

    sleep(0.25)

    global on_startup
    global previous_menu

    on_startup = False
    previous_menu = -1

# Send string values to serial

def broadcaster_use(keyboard_key, menu_num):
    encoded_command = bipedalGame.speed_select(keyboard_key, menu_num, speed_setting)
    ser.write(encoded_command.encode("utf-8"))

    show_key(keyboard_key)

# Main loop

while True:
    
    if menu == 0:
        os.system('clear')
        limb = 0
        link_1 = 0
        link_2 = 0

        hypotenuse = 0
        ee_z = 0
        ee_x = 0.01
        
        sylvieOS.splash()

        print("Now running: Bipedal Robot Control (Version : " + bipedalGame.version + ")")
        print("")
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
        solvedik_front = nanoik.solveKinematicsFront(ee_zL_sr, ee_zR_sr, foot_dist)

        # Handle startup and post-startup calculations

        if menu != previous_menu:
            if on_startup == False:          
                gbx_L1 = gbx_L1 + (solvedik_left[0] - ra1L_old)
                gbx_L2 = gbx_L2 + (solvedik_left[1] - ra2L_old)
                gbx_L3 = gbx_L3 + (solvedik_left[2] - ra3L_old)

                gbx_R1 = gbx_R1 + (solvedik_right[0] - ra1R_old)
                gbx_R2 = gbx_R2 + (ra2R_old - solvedik_right[1]) # To reverse motor direction, swap these!
                gbx_R3 = gbx_R3 + (solvedik_right[2] - ra3R_old)

                gbx_sr_L2 = gbx_sr_L2 + (ra2L_sr_old - solvedik_front)
                gbx_sr_R2 = gbx_sr_R2 + (ra2R_sr_old - solvedik_front)

                encoded_command = "none,none," + quickRnd(gbx_L1) + "," + quickRnd(gbx_L2) + "," + quickRnd(gbx_L3) + "," + quickRnd(gbx_R1) + "," + quickRnd(gbx_R2) + "," + quickRnd(gbx_R3) + "," + quickRnd(gbx_sr_L2) + "," + quickRnd(gbx_sr_R2) + "\n"

                ser.write(encoded_command.encode("utf-8"))

                sleep(0.25)

            os.system('clear')
            
            # Print joint angles on screen

            l_leg_angles = [quickRnd(gbx_L1), quickRnd(gbx_L2), quickRnd(gbx_L3)]
            r_leg_angles = [quickRnd(gbx_R1), quickRnd(gbx_R2), quickRnd(gbx_R3)]

            l_ee_pos = round(ee_zL, 3), round(ee_xL, 3)
            r_ee_pos = round(ee_zR, 3), round(ee_xR, 3)

            sr_angles = str(int(round((gbx_sr_L2 * 10), 1)))
            waist_angle = str(int(round((gbx_waist * 10), 1)))
     
            bipedalGame.menuOneText(l_leg_angles, r_leg_angles, l_ee_pos, r_ee_pos, sr_angles, waist_angle, encoded_command)

            previous_menu = menu

        ra1L_old = solvedik_left[0]
        ra2L_old = solvedik_left[1]
        ra3L_old = solvedik_left[2]

        ra1R_old = solvedik_right[0]
        ra2R_old = solvedik_right[1]
        ra3R_old = solvedik_right[2]
        
        ra2L_sr_old = solvedik_front
        ra2R_sr_old = solvedik_front

        # Keyboard Control

        if keyboard.is_pressed('1'):
            nanoik.drawRadarSide(solvedik_left[0], solvedik_left[1], solvedik_left[2], link_1, link_2, "blue")
            show_key('1')
        elif keyboard.is_pressed('2'):
            nanoik.drawRadarSide(solvedik_right[0], solvedik_right[1], solvedik_right[2], link_1, link_2, "red")
            show_key('2')
        elif keyboard.is_pressed('3'):
            nanoik.drawRadarFront((gbx_sr_L2 - 10), ee_zL, ee_zR, foot_dist, "green")
            show_key('3')
        elif keyboard.is_pressed('w'):
            ee_zL = ee_zL - ver_speed[speed_setting]
            show_key('w')
        elif keyboard.is_pressed('s'):
            ee_zL = ee_zL + ver_speed[speed_setting]
            show_key('s')
        elif keyboard.is_pressed('d'):
            ee_xL = ee_xL + hor_speed[speed_setting]
            show_key('d')
        elif keyboard.is_pressed('a'):
            ee_xL = ee_xL - hor_speed[speed_setting]
            show_key('a')
        elif keyboard.is_pressed('t'):
            ee_zR = ee_zR - ver_speed[speed_setting]
            show_key('t')
        elif keyboard.is_pressed('g'):
            ee_zR = ee_zR + ver_speed[speed_setting]
            show_key('g')
        elif keyboard.is_pressed('h'):
            ee_xR = ee_xR + hor_speed[speed_setting]
            show_key('h')
        elif keyboard.is_pressed('f'):
            ee_xR = ee_xR - hor_speed[speed_setting]
            show_key('f')
        elif keyboard.is_pressed('i'):
            ee_zL = ee_zL - ver_speed[speed_setting]
            ee_zR = ee_zR - ver_speed[speed_setting]
            show_key('i')
        elif keyboard.is_pressed('k'):
            ee_zL = ee_zL + ver_speed[speed_setting]
            ee_zR = ee_zR + ver_speed[speed_setting]
            show_key('k')
        elif keyboard.is_pressed('l'):
            ee_xL = ee_xL + hor_speed[speed_setting]
            ee_xR = ee_xR + hor_speed[speed_setting]
            show_key('l')
        elif keyboard.is_pressed('j'):
            ee_xL = ee_xL - hor_speed[speed_setting]
            ee_xR = ee_xR - hor_speed[speed_setting]
            show_key('j')

        elif keyboard.is_pressed('z'):
            ee_zL = ee_zL - sr_speed[speed_setting]
            ee_zR = ee_zR + sr_speed[speed_setting]

            ee_zL_sr = ee_zL_sr - sr_speed[speed_setting]
            ee_zR_sr = ee_zR_sr + sr_speed[speed_setting]

            show_key('z')			
        elif keyboard.is_pressed('x'):
            ee_zL = ee_zL + sr_speed[speed_setting]
            ee_zR = ee_zR - sr_speed[speed_setting]

            ee_zL_sr = ee_zL_sr + sr_speed[speed_setting]
            ee_zR_sr = ee_zR_sr - sr_speed[speed_setting]
                                   
            show_key('x')
        elif keyboard.is_pressed('c'):
            gbx_waist = gbx_waist + 0.5
            show_key('c')
        elif keyboard.is_pressed('v'):
            gbx_waist = gbx_waist - 0.5
            show_key('v')
        elif keyboard.is_pressed('b'):
            broadcaster_use('b', 1)
        elif keyboard.is_pressed('n'):
            broadcaster_use('n', 1)
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
            
        elif keyboard.is_pressed('up'):
            switch_speed('up')  
        elif keyboard.is_pressed('down'):
            switch_speed('down')          
               
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
        elif keyboard.is_pressed('u'):
            broadcaster_use('u', 2)
        elif keyboard.is_pressed('i'):
            broadcaster_use('i', 2)
        elif keyboard.is_pressed('z'):
            broadcaster_use('z', 2)
        elif keyboard.is_pressed('x'):
            broadcaster_use('x', 2)
        elif keyboard.is_pressed('c'):
            broadcaster_use('c', 2)
        elif keyboard.is_pressed('v'):
            broadcaster_use('v', 2)
        elif keyboard.is_pressed('b'):
            broadcaster_use('b', 2)
        elif keyboard.is_pressed('n'):
            broadcaster_use('n', 2)
            
        elif keyboard.is_pressed('up'):
            switch_speed('up')  
        elif keyboard.is_pressed('down'):
            switch_speed('down')  
            
        elif keyboard.is_pressed('left'):
            os.system('clear')
            print("RETURNING TO MENU 1")

            sleep(1)

            on_startup = False
            menu = 1
            previous_menu = -1
