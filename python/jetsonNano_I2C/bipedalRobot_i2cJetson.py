# Keyboard and i2c control for Sylvie 2021 (Bipedal Robot Lower Body)

from time import sleep

#import board
#import busio
import keyboard
import os

import nanoik

# Nvidia Jetson Nano i2c Bus 0 and 1

# i2c_bus0 = (busio.I2C(board.SCL_1, board.SDA_1))
# i2c_bus1 = (busio.I2C(board.SCL, board.SDA))

# These are the adresses we setup in the Arduino Program
n17_waist_address = 0x10

n17_sRockL1_address = 0x11
n17_sRockR1_address = 0x12

n23_thighL1_address = 0x13
n23_thighR1_address = 0x14

n23_kneeL1_address = 0x15
n23_kneeR1_address = 0x16

n23_legL1_address = 0x17
n23_legR1_address = 0x18

n17_sRockL2_address = 0x19
n17_sRockR2_address = 0x20

# Our global variables
previous_menu = 0
menu = 0      

limb = 0
link_1 = 0
link_2 = 0

hypotenuse = 0
ee_z = 0
ee_x = 0.01

gbx_1 = 100
gbx_2 = 100
gbx_3 = 100

ra1_old = 0
ra2_old = 0
ra3_old = 0

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
        print("Protip: 1 meter = 1, 50 centimeters = 0.5")
        hypotenuse = float(input("Enter the distance between Joint 1 and Joint 3 i.e. Hypotenuse: "))
        link_1 = float(input("Enter the distance between Joint 1 and Joint 2 i.e. Thigh length: "))
        link_2 = float(input("Enter the distance between Joint 2 and Joint 3 i.e. Leg length: "))

        if hypotenuse > 0:
            ee_z = hypotenuse
            menu = 1

    elif menu == 1:
        os.system('clear')
        if menu is not previous_menu:
            print("Choose which of these legs you wish to control: ")
            print("1. Left Leg")
            print("2. Right leg")
            print("")
            previous_menu = menu

        keyboardInput = str(input("Please enter your choice using a number: "))

        if keyboardInput == "exit":
            exit()
        elif keyboardInput == "1":
            limb = 1
            menu = 2
        elif keyboardInput == "2":
            limb = 2
            menu = 2

    elif menu == 2:
        os.system('clear')

        solvedik = nanoik.solveKinematics(ee_z, ee_x, link_1, link_2)
        routeAngles = nanoik.getRoute(solvedik[0], solvedik[1], solvedik[2], link_1, link_2, solvedik[3])         

        if on_startup == False:          
            gbx_1 = gbx_1 + (routeAngles[0] - ra1_old)
            gbx_2 = gbx_2 + (routeAngles[1] - ra2_old)
            gbx_3 = gbx_3 + (routeAngles[2] - ra3_old)

            if limb == 1:
		    # i2c_bus0.writeto(n23_thighL1_address, int(round(gbx_1, 1), stop=False)                
		    # i2c_bus0.writeto(n23_kneeL1_address, int(round(gbx_2, 1), stop=False)
		    # i2c_bus0.writeto(n23_legL1_address, int(round(gbx_3, 1), stop=False)
                pass
            elif limb == 2:
		    # i2c_bus0.writeto(n23_thighR1_address, int(round(gbx_1, 1), stop=False)                
		    # i2c_bus0.writeto(n23_kneeR1_address, int(round(gbx_2, 1), stop=False)
		    # i2c_bus0.writeto(n23_legR1_address, int(round(gbx_3, 1), stop=False)
                pass

        print("Current joint angles are: ", round(routeAngles[0], 2), round(routeAngles[1], 2), round(routeAngles[2], 2))
        print("Current gearbox positions are: ", round(gbx_1, 2), round(gbx_2, 2), round(gbx_3, 2))

        print("Current Z position: ", ee_z)
        print("Current X position: ", ee_x)
        print("")
        print("..Type 'exit' if you wish to quit the program.")
        print("..Type 'radar' to view current position of the limb.")

        print("..Type 'm0 or m1' to return to previous menus.")
        previous_menu = menu
        ra1_old = routeAngles[0]
        ra2_old = routeAngles[1]
        ra3_old = routeAngles[2]

        keyboardInput = str(input("Please enter the 'Z, X' position for the end effector to move to: "))

        if keyboardInput == "exit":
            exit()
        elif keyboardInput == "m0":
            menu = 0
        elif keyboardInput == "m1":
            menu = 1
        elif keyboardInput == "radar":
            nanoik.drawRadar(solvedik[0], solvedik[1], solvedik[2], link_1, link_2, solvedik[3])
            os.system('clear')
        else:
            movementVal = keyboardInput.split(", ")
            ee_z = float(movementVal[0])
            ee_x = float(movementVal[1])
            
            print("Updating new position...")       
            sleep(0.5)  
            os.system('clear')
            on_startup = False
            previous_menu = -1        
