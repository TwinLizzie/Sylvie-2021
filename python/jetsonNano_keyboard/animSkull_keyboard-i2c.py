# Keyboard and i2c control for Sylvie 2021 (Animatronic Skull)

from adafruit_servokit import ServoKit
from time import sleep

import time
import board
import busio
import bluetooth
# import time

import keyboard
import os

# Nvidia Jetson Nano i2c Bus 0 and 1

i2c_bus0 = (busio.I2C(board.SCL_1, board.SDA_1))
i2c_bus1 = (busio.I2C(board.SCL, board.SDA))

kit = ServoKit(channels=16, i2c=i2c_bus1)

# These are the adresses we setup in the Arduino Program
nema17z_address = 0x20
nema17x_address = 0x10

# Slots on the PCA9685 PWM Driver, and the corresponding servos

servo_0_eyeR_y = 0
servo_1_eyeL_y = 1
servo_2_eyeR_x = 2
servo_3_eyeL_x = 3

servo_4_lidR_top = 4
servo_5_lidL_top = 5
servo_6_lidR_bot = 6
servo_7_lidL_bot = 7

servo_8_browR = 8
servo_9_browL = 9

servo_10_lip = 10
servo_11_cornerR = 11
servo_12_cornerL = 12

servo_13_jawR = 13
servo_14_jawL = 14

# Offsets of articulation points... for fine tuning

offset_lid_top_right = 10
offset_lid_top_left = -5

offset_lid_bottom_right = -20
offset_lid_bottom_left = 30

offset_right_y = -10
offset_right_x = -10

offset_left_y = 15
offset_left_x = -10

offset_brow1 = -15
offset_brow2 = 5

offset_lip = -34
offset_corner1 = 0
offset_corner2 = -8

offset_jaw = 45
offset_jaw2 = 0

# previous servo positions for smooth motion

previous_pos_browR = 90
previous_pos_browL = 90

previous_pos_lip = 90

previous_pos_cornerR = 90
previous_pos_cornerL = 90

previous_pos_jawR = 90
previous_pos_jawL = 90

# Set status of message and value

previous_status = "0"
previous_message = ""

default_msg0 = ""
default_msg1 = "Welcome to SylvieOS 2021! App: Animatronic Skull"
default_msg2 = "WAITING FOR USER INPUT! (TRY Q,W,E,R,T,A,S,D,F)"

def clear_terminal(status):
	global previous_status
	if status != previous_status:
		os.system('clear')
		print(default_msg1)
		print(default_msg2)
		previous_status = status

def sys_message(msg1, msg2=default_msg0):
	global previous_message
	if msg1 != previous_message:
		os.system('clear')
		print(msg1)
		print(msg2)
		previous_message = msg1    

def initialize_servos():

	kit.servo[servo_0_eyeR_y].angle = 90 + offset_right_y
	kit.servo[servo_1_eyeL_y].angle = 90 + offset_left_y
	
	kit.servo[servo_2_eyeR_x].angle = 90 + offset_right_x
	kit.servo[servo_3_eyeL_x].angle = 90 + offset_left_x
	
	kit.servo[servo_4_lidR_top].angle = 90 + offset_lid_top_right
	kit.servo[servo_5_lidL_top].angle = 90 + offset_lid_top_left
	kit.servo[servo_6_lidR_bot].angle = 90 + offset_lid_bottom_right
	kit.servo[servo_7_lidL_bot].angle = 90 + offset_lid_bottom_left

	kit.servo[servo_8_browR].angle = 90 + offset_brow1         
	kit.servo[servo_9_browL].angle = 90 + offset_brow2	

	kit.servo[servo_10_lip].angle = 90 + offset_lip
	kit.servo[servo_11_cornerR].angle = 90 + offset_corner1         
	kit.servo[servo_12_cornerL].angle = 90 + offset_corner2
	
	kit.servo[servo_13_jawR].angle = 90 + offset_jaw
	kit.servo[servo_14_jawL].angle = 90 + offset_jaw2

def move_eye_servos(posR_y=None, posL_y=None, posR_x=None, posL_x=None):

	if posR_y is not None:	
		kit.servo[servo_0_eyeR_y].angle = posR_y + offset_right_y
	if posL_y is not None:
		kit.servo[servo_1_eyeL_y].angle = posL_y + offset_left_y
	if posR_x is not None:
		kit.servo[servo_2_eyeR_x].angle = posR_x + offset_right_x
	if posL_x is not None:	
		kit.servo[servo_3_eyeL_x].angle = posL_x + offset_left_x

def move_eyelid_servos(posR_top=None, posL_top=None, posR_bot=None, posL_bot=None):

	if posR_top is not None:	
		kit.servo[servo_4_lidR_top].angle = posR_top + offset_lid_top_right
	if posL_top is not None:
		kit.servo[servo_5_lidL_top].angle = posL_top + offset_lid_top_left
	if posR_bot is not None:
		kit.servo[servo_6_lidR_bot].angle = posR_bot + offset_lid_bottom_right
	if posL_bot is not None:	
		kit.servo[servo_7_lidL_bot].angle = posL_bot + offset_lid_bottom_left	

def move_face_servos(pos_browR=None, pos_browL=None, pos_lip=None, pos_cornerR=None, pos_cornerL=None, pos_jawR=None, pos_jawL=None):

	global previous_pos_browR
	global previous_pos_browL

	global previous_pos_lip

	global previous_pos_cornerR
	global previous_pos_cornerL

	global previous_pos_jawR
	global previous_pos_jawL

	if pos_browR is not None:
		kit.servo[servo_8_browR].angle = pos_browR + offset_brow1
		previous_pos_browR = pos_browR
	if pos_browL is not None:	
		kit.servo[servo_9_browL].angle = pos_browL + offset_brow2
		previous_pos_browL = pos_browL
	if pos_lip is not None:	
		kit.servo[servo_10_lip].angle = pos_lip + offset_lip
		previous_pos_lip = pos_lip
	if pos_cornerR is not None:	
		kit.servo[servo_11_cornerR].angle = pos_cornerR + offset_corner1
		previous_pos_cornerR = pos_cornerR
	if pos_cornerL is not None:	
		kit.servo[servo_12_cornerL].angle = pos_cornerL + offset_corner2
		previous_pos_cornerL = pos_cornerL
	if pos_jawR is not None:	
		kit.servo[servo_13_jawR].angle = pos_jawR + offset_jaw
		previous_pos_jawR = pos_jawR
	if pos_jawL is not None:	
		kit.servo[servo_14_jawL].angle = pos_jawL + offset_jaw2
		previous_pos_jawL = pos_jawL

initialize_servos() 

while True:
	if keyboard.is_pressed('q'):
		sys_message("KEYBOARD KEY [Q] PRESSED!")

		move_eyelid_servos(15, 155, 120, 50) # Fixed on Jan 11, 2021. Bottom eyelids were squeezing too much!
		
		sleep(0.25)
		clear_terminal(0)
	
	elif keyboard.is_pressed('w'): 	
		sys_message("KEYBOARD KEY [W] PRESSED!")

		move_eyelid_servos(90, 90, 90, 90) # Eyelashes make it easier to close the eyes completely.
		
		sleep(0.25)
		clear_terminal(0)
	
	elif keyboard.is_pressed('e'): 	
		sys_message("KEYBOARD KEY [E] PRESSED!")       

		move_eyelid_servos(60, 120, 120, 60)
		
		sleep(0.25)  
		clear_terminal(0)
	
	elif keyboard.is_pressed('r'): 	
		sys_message("KEYBOARD KEY [R] PRESSED!") 
		
		move_eyelid_servos(90, 90, 90, 90)

		sleep(0.25)
		clear_terminal(0)
	
	elif keyboard.is_pressed('a'): 	
		sys_message("KEYBOARD KEY [A] PRESSED!") 

		move_eye_servos(105, 70)		
		move_eyelid_servos(120, 60, 95, 85)

		sleep(0.25)
		clear_terminal(0)
	
	elif keyboard.is_pressed('s'): 	
		sys_message("KEYBOARD KEY [S] PRESSED!")

		move_eye_servos(75, 100)		
		move_eyelid_servos(80, 100, 75, 115)
		
		sleep(0.25)
		clear_terminal(0)
	
	elif keyboard.is_pressed('d'): 	
		sys_message("KEYBOARD KEY [D] PRESSED!")

		move_eye_servos(None, None, 65, 120)
		
		sleep(0.25)
		clear_terminal(0)
	
	elif keyboard.is_pressed('f'): 	
		sys_message("KEYBOARD KEY [F] PRESSED!")

		move_eye_servos(None, None, 130, 60)
		
		sleep(0.25)
		clear_terminal(0)
	
	elif keyboard.is_pressed('t'): 	
		sys_message("KEYBOARD KEY [T] PRESSED!")   
		
		i2c_bus0.writeto(nema17x_address, "6", stop=False)
		
		sleep(0.25)
		clear_terminal(0)
	
	elif keyboard.is_pressed('y'): 	
		sys_message("KEYBOARD KEY [Y] PRESSED!") 
		
		i2c_bus0.writeto(nema17x_address, "7", stop=False)
		
		sleep(0.25)
		clear_terminal(0)
	
	elif keyboard.is_pressed('g'): 	
		sys_message("KEYBOARD KEY [G] PRESSED!")    
		
		i2c_bus0.writeto(nema17z_address, "2", stop=False)
		
		sleep(0.25)
		clear_terminal(0)
	
	elif keyboard.is_pressed('h'): 	
		sys_message("KEYBOARD KEY [H] PRESSED!")
		
		i2c_bus0.writeto(nema17z_address, "3", stop=False)
		
		sleep(0.25)
		clear_terminal(0)
	
	elif keyboard.is_pressed('b'): 	
		sys_message("KEYBOARD KEY [B] PRESSED!")         
		
		move_face_servos(80, 100)
		
		sleep(0.25)
		clear_terminal(0)
	
	elif keyboard.is_pressed('n'): 	
		sys_message("KEYBOARD KEY [N] PRESSED!")  

		move_face_servos(100, 80)
		
		sleep(0.25)
		clear_terminal(0)
	
	elif keyboard.is_pressed('u'): 	
		sys_message("KEYBOARD KEY [U] PRESSED!")

		move_face_servos(None, None, 110)
		
		sleep(0.25)
		clear_terminal(0)
	
	elif keyboard.is_pressed('i'): 	
		sys_message("KEYBOARD KEY [I] PRESSED!")     

		move_face_servos(None, None, 90)
		
		sleep(0.25)
		clear_terminal(0)   
	
	elif keyboard.is_pressed('j'): 	
		sys_message("KEYBOARD KEY [J] PRESSED!")
		
		move_face_servos(90, 90, 90, 90, 90, 90, 90)
		time.sleep(0.05)
		move_face_servos(80, 100, 90, 80, 100, 90, 90)
		time.sleep(0.05)
		move_eyelid_servos(90, 90, 90, 90)

		sleep(0.25)
		clear_terminal(0) 
	
	elif keyboard.is_pressed('k'): 	
		sys_message("KEYBOARD KEY [K] PRESSED!")   

		move_face_servos(90, 90, 90, 90, 90, 90, 90)
		time.sleep(0.05)
		move_face_servos(95, 85, 93, 97, 83, 115, 65)
		time.sleep(0.05)
		move_eyelid_servos(70, 110, 105, 70)
		
		sleep(0.25)
		clear_terminal(0) 

	elif keyboard.is_pressed('z'): 	
		sys_message("KEYBOARD KEY [Z] PRESSED!")   

		move_eyelid_servos(15, 90, 120, 90)
		
		sleep(0.25)
		clear_terminal(0) 

	elif keyboard.is_pressed('x'): 	
		sys_message("KEYBOARD KEY [X] PRESSED!")   

		move_eyelid_servos(90, 155, 90, 50)
		
		sleep(0.25)
		clear_terminal(0) 
	
	elif keyboard.is_pressed('1'): 	
		sys_message("KEYBOARD KEY [1] PRESSED!")         

		move_face_servos(105, 80, 100, 80, 100, 110, 70)
		time.sleep(0.05)
		move_face_servos(105, 80, 100, 80, 100, 120, 60)
		time.sleep(0.05)		
		move_face_servos(105, 80, 100, 80, 100, 135, 45)

		sleep(0.25)
		clear_terminal(0)  
	
	elif keyboard.is_pressed('2'): 	
		sys_message("KEYBOARD KEY [2] PRESSED!")         

		move_face_servos(90, 90, 90, 90, 90, 125, 55)
		time.sleep(0.05)		
		move_face_servos(90, 90, 90, 90, 90, 115, 65)
		time.sleep(0.05)
		move_face_servos(90, 90, 90, 90, 90, 105, 75)

		sleep(0.25)
		clear_terminal(0) 
	
	elif keyboard.is_pressed('o'): 	
		sys_message("POSITIONS RESET!")

		move_eye_servos(90, 90, 90, 90)
		move_eyelid_servos(90, 90, 90, 90)
		move_face_servos(90, 90, 90, 90, 90, 90, 90)	

		sleep(0.25)  
		clear_terminal(0)  
	
	elif keyboard.is_pressed('p'):
		sys_message("DONE.")	
		sleep(1)
		os.system('stty echo')                
		os.system('clear')
		exit()
	else:		
		sys_message(default_msg1, default_msg2)  

# while True:
#    var = input("")
#    if not var:
#        continue

#    writeNumber(var)
