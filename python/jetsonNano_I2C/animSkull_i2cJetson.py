# Keyboard and i2c control for Sylvie 2021 (Animatronic Skull)

from adafruit_servokit import ServoKit
from time import sleep

import board
import busio
# import time

import keyboard
import os

# Nvidia Jetson Nano i2c Bus 0 and 1

i2c_bus0 = (busio.I2C(board.SCL_1, board.SDA_1))
i2c_bus1 = (busio.I2C(board.SCL, board.SDA))

kit = ServoKit(channels=16, i2c=i2c_bus1)

# These are the adresses we setup in the Arduino Program
nema17z_address = 0x20
nema17y_address = 0x10

# Slots on the PCA9685 PWM Driver, and the corresponding servos

sg90_1 = 0
sg90_2 = 1
sg90_3 = 2
sg90_4 = 3

sg90_1b = 4
sg90_2b = 5
sg90_3b = 6
sg90_4b = 7

sg90_brow1 = 8
sg90_brow2 = 9

sg90_lip = 10
sg90_corner1 = 11
sg90_corner2 = 12

sg90_jaw1 = 13
sg90_jaw2 = 14

# Offsets of articulation points... for fine tuning

offset_lid_top_right = 0
offset_lid_top_left = 25

offset_lid_bottom_right = -30
offset_lid_bottom_left = 0

offset_right_y = -10
offset_right_x = 0

offset_left_y = 17
offset_left_x = -10

offset_brow1 = 10
offset_brow2 = 0

offset_lip = -7
offset_corner1 = 5
offset_corner2 = -17

offset_jaw = -10

# Set status of message and value

previous_status = "0"
previous_message = ""

#def writeNumber(value, message):
#i2c_bus0.writeto(address, value, stop=False)
#    return -1

def initialize_servos():

	kit.servo[sg90_1].angle = 90 + offset_right_y
	kit.servo[sg90_2].angle = 90 + offset_left_y
	
	kit.servo[sg90_3].angle = 90 + offset_right_x
	kit.servo[sg90_4].angle = 90 + offset_left_x
	
	kit.servo[sg90_1b].angle = 90 + offset_lid_top_right
	kit.servo[sg90_2b].angle = 90 + offset_lid_top_left
	kit.servo[sg90_3b].angle = 90 + offset_lid_bottom_right
	kit.servo[sg90_4b].angle = 90 + offset_lid_bottom_left
	
	kit.servo[sg90_jaw].angle = 90 + offset_jaw
	
	kit.servo[sg90_corner1].angle = 90 + offset_corner1         
	kit.servo[sg90_corner2].angle = 90 + offset_corner2
	
	kit.servo[sg90_brow1].angle = 90 + offset_brow1         
	kit.servo[sg90_brow2].angle = 90 + offset_brow2
	
	kit.servo[sg90_lip].angle = 90 + offset_lip

def clear_terminal(status):
	global previous_status
	if status != previous_status:
		os.system('clear')
		print("WAITING FOR USER INPUT! (TRY Q,W,E,R,T,A,S,D,F)")
		# i2c_bus0.writeto(nema17z_address, status, stop=False)        
		# i2c_bus0.writeto(nema17y_address, status, stop=False)
		previous_status = status

def sys_message(message):
	global previous_message
	if message != previous_message:
		os.system('clear')
		print(message)
		previous_message = message        

initialize_servos() 

while True:
	if keyboard.is_pressed('q'): 	
		sys_message("KEYBOARD KEY [Q] PRESSED!")
		
		kit.servo[sg90_1b].angle = 5 + offset_lid_top_right
		kit.servo[sg90_2b].angle = 155 + offset_lid_top_left
		kit.servo[sg90_3b].angle = 135 + offset_lid_bottom_right
		kit.servo[sg90_4b].angle = 35 + offset_lid_bottom_left
		
		sleep(0.25)
		clear_terminal(0)
	
	elif keyboard.is_pressed('w'): 	
		sys_message("KEYBOARD KEY [W] PRESSED!")
		
		kit.servo[sg90_1b].angle = 90 + offset_lid_top_right
		kit.servo[sg90_2b].angle = 90 + offset_lid_top_left
		kit.servo[sg90_3b].angle = 90 + offset_lid_bottom_right
		kit.servo[sg90_4b].angle = 90 + offset_lid_bottom_left
		
		sleep(0.25)
		clear_terminal(0)
	
	elif keyboard.is_pressed('e'): 	
		sys_message("KEYBOARD KEY [E] PRESSED!")
		
		kit.servo[sg90_1b].angle = 65 + offset_lid_top_right
		kit.servo[sg90_2b].angle = 115 + offset_lid_top_left
		kit.servo[sg90_3b].angle = 115 + offset_lid_bottom_right
		kit.servo[sg90_4b].angle = 65 + offset_lid_bottom_left        
		
		sleep(0.25)  
		clear_terminal(0)
	
	elif keyboard.is_pressed('r'): 	
		sys_message("KEYBOARD KEY [R] PRESSED!") 
		
		kit.servo[sg90_1b].angle = 90 + offset_lid_top_right
		kit.servo[sg90_2b].angle = 90 + offset_lid_top_left
		kit.servo[sg90_3b].angle = 90 + offset_lid_bottom_right
		kit.servo[sg90_4b].angle = 90 + offset_lid_bottom_left
		
		sleep(0.25)
		clear_terminal(0)
	
	elif keyboard.is_pressed('a'): 	
		sys_message("KEYBOARD KEY [A] PRESSED!") 
		
		kit.servo[sg90_1].angle = 100 + offset_right_y
		kit.servo[sg90_2].angle = 65 + offset_left_y
		
		kit.servo[sg90_1b].angle = 100 + offset_lid_top_right
		kit.servo[sg90_2b].angle = 80 + offset_lid_top_left
		kit.servo[sg90_3b].angle = 100 + offset_lid_bottom_right
		kit.servo[sg90_4b].angle = 80 + offset_lid_bottom_left
		
		sleep(0.25)
		clear_terminal(0)
	
	elif keyboard.is_pressed('s'): 	
		sys_message("KEYBOARD KEY [S] PRESSED!")
		
		kit.servo[sg90_1].angle = 75 + offset_right_y
		kit.servo[sg90_2].angle = 130 + offset_left_y
		
		kit.servo[sg90_1b].angle = 70 + offset_lid_top_right
		kit.servo[sg90_2b].angle = 110 + offset_lid_top_left
		kit.servo[sg90_3b].angle = 70 + offset_lid_bottom_right
		kit.servo[sg90_4b].angle = 110 + offset_lid_bottom_left
		
		sleep(0.25)
		clear_terminal(0)
	
	elif keyboard.is_pressed('d'): 	
		sys_message("KEYBOARD KEY [D] PRESSED!")
		
		kit.servo[sg90_3].angle = 65 + offset_right_x
		kit.servo[sg90_4].angle = 65 + offset_left_x
		
		sleep(0.25)
		clear_terminal(0)
	
	elif keyboard.is_pressed('f'): 	
		sys_message("KEYBOARD KEY [F] PRESSED!")
		
		kit.servo[sg90_3].angle = 110 + offset_right_x
		kit.servo[sg90_4].angle = 120 + offset_left_x
		
		sleep(0.25)
		clear_terminal(0)
	
	# elif keyboard.is_pressed('z'): 	
	#    sys_message("KEYBOARD KEY [Z] PRESSED!")
	#    sleep(0.25)
	#    clear_terminal(0)
	
	# elif keyboard.is_pressed('x'): 	
	#    sys_message("KEYBOARD KEY [X] PRESSED!")         
	#    sleep(0.25)
	#    clear_terminal(0)
	
	elif keyboard.is_pressed('t'): 	
		sys_message("KEYBOARD KEY [T] PRESSED!")   
		
		i2c_bus0.writeto(nema17z_address, "2", stop=False)
		
		sleep(0.25)
		clear_terminal(0)
	
	elif keyboard.is_pressed('y'): 	
		sys_message("KEYBOARD KEY [Y] PRESSED!") 
		
		i2c_bus0.writeto(nema17z_address, "3", stop=False)
		
		sleep(0.25)
		clear_terminal(0)
	
	elif keyboard.is_pressed('g'): 	
		sys_message("KEYBOARD KEY [G] PRESSED!")    
		
		i2c_bus0.writeto(nema17y_address, "2", stop=False)
		
		sleep(0.25)
		clear_terminal(0)
	
	elif keyboard.is_pressed('h'): 	
		sys_message("KEYBOARD KEY [H] PRESSED!")
		
		i2c_bus0.writeto(nema17y_address, "3", stop=False)
		
		sleep(0.25)
		clear_terminal(0)
	
	elif keyboard.is_pressed('b'): 	
		sys_message("KEYBOARD KEY [B] PRESSED!")         
		
		kit.servo[sg90_brow1].angle = 50 + offset_brow1
		kit.servo[sg90_brow2].angle = 130 + offset_brow2
		
		sleep(0.25)
		clear_terminal(0)
	
	elif keyboard.is_pressed('n'): 	
		sys_message("KEYBOARD KEY [N] PRESSED!")  
		
		kit.servo[sg90_brow1].angle = 110 + offset_brow1
		kit.servo[sg90_brow2].angle = 70 + offset_brow2
		
		sleep(0.25)
		clear_terminal(0)
	
	elif keyboard.is_pressed('u'): 	
		sys_message("KEYBOARD KEY [U] PRESSED!")
		
		kit.servo[sg90_lip].angle = 150 + offset_lip
		
		sleep(0.25)
		clear_terminal(0)
	
	elif keyboard.is_pressed('i'): 	
		sys_message("KEYBOARD KEY [I] PRESSED!")     
		
		kit.servo[sg90_lip].angle = 90 + offset_lip
		
		sleep(0.25)
		clear_terminal(0)   
	
	elif keyboard.is_pressed('j'): 	
		sys_message("KEYBOARD KEY [J] PRESSED!")
		
		kit.servo[sg90_corner1].angle = 70 + offset_corner1
		kit.servo[sg90_corner2].angle = 110 + offset_corner2         
		
		kit.servo[sg90_1b].angle = 90 + offset_lid_top_right
		kit.servo[sg90_2b].angle = 90 + offset_lid_top_left
		kit.servo[sg90_3b].angle = 90 + offset_lid_bottom_right
		kit.servo[sg90_4b].angle = 90 + offset_lid_bottom_left
		
		kit.servo[sg90_brow1].angle = 50 + offset_brow1
		kit.servo[sg90_brow2].angle = 130 + offset_brow2
		
		kit.servo[sg90_lip].angle = 90 + offset_lip
		
		sleep(0.25)
		clear_terminal(0) 
	
	elif keyboard.is_pressed('k'): 	
		sys_message("KEYBOARD KEY [K] PRESSED!")   
		
		kit.servo[sg90_corner1].angle = 120 + offset_corner1
		kit.servo[sg90_corner2].angle = 60 + offset_corner2         
		
		kit.servo[sg90_1b].angle = 70 + offset_lid_top_right
		kit.servo[sg90_2b].angle = 110 + offset_lid_top_left
		kit.servo[sg90_3b].angle = 110 + offset_lid_bottom_right
		kit.servo[sg90_4b].angle = 70 + offset_lid_bottom_left
		
		kit.servo[sg90_brow1].angle = 85 + offset_brow1
		kit.servo[sg90_brow2].angle = 85 + offset_brow2
		
		kit.servo[sg90_lip].angle = 105 + offset_lip
		
		sleep(0.25)
		clear_terminal(0) 
	
	elif keyboard.is_pressed('1'): 	
		sys_message("KEYBOARD KEY [1] PRESSED!")         
		
		kit.servo[sg90_jaw].angle = 160 + offset_jaw
		
		kit.servo[sg90_corner1].angle = 60 + offset_corner1         
		kit.servo[sg90_corner2].angle = 120 + offset_corner2
		
		kit.servo[sg90_brow1].angle = 100 + offset_brow1         
		kit.servo[sg90_brow2].angle = 80 + offset_brow2
		
		kit.servo[sg90_lip].angle = 90 + offset_lip
		
		sleep(0.25)
		clear_terminal(0)  
	
	elif keyboard.is_pressed('2'): 	
		sys_message("KEYBOARD KEY [2] PRESSED!")         
		
		kit.servo[sg90_jaw].angle = 70 + offset_jaw
		
		kit.servo[sg90_corner1].angle = 90 + offset_corner1         
		kit.servo[sg90_corner2].angle = 90 + offset_corner2
		
		kit.servo[sg90_brow1].angle = 90 + offset_brow1         
		kit.servo[sg90_brow2].angle = 90 + offset_brow2
		
		kit.servo[sg90_lip].angle = 90 + offset_lip
		
		sleep(0.25)
		clear_terminal(0) 
	
	elif keyboard.is_pressed('o'): 	
		sys_message("POSITIONS RESET!")
		
		kit.servo[sg90_1].angle = 90 + offset_right_y
		kit.servo[sg90_2].angle = 90 + offset_left_y
		
		kit.servo[sg90_3].angle = 90 + offset_right_x
		kit.servo[sg90_4].angle = 90 + offset_left_x
		
		kit.servo[sg90_1b].angle = 90 + offset_lid_top_right
		kit.servo[sg90_2b].angle = 90 + offset_lid_top_left
		kit.servo[sg90_3b].angle = 90 + offset_lid_bottom_right
		kit.servo[sg90_4b].angle = 90 + offset_lid_bottom_left
		
		kit.servo[sg90_jaw].angle = 90 + offset_jaw
		
		kit.servo[sg90_corner1].angle = 90 + offset_corner1         
		kit.servo[sg90_corner2].angle = 90 + offset_corner2
		
		kit.servo[sg90_brow1].angle = 90 + offset_brow1         
		kit.servo[sg90_brow2].angle = 90 + offset_brow2
		
		kit.servo[sg90_lip].angle = 90 + offset_lip
		
		sleep(0.25)  
		clear_terminal(0)  
	
	elif keyboard.is_pressed('p'):
		sys_message("DONE.")	
		sleep(1)
		os.system('stty echo')                
		os.system('clear')
		exit()
	else:		
		sys_message("WAITING FOR USER INPUT! (TRY Q,W,E,R,T,A,S,D,F)")  

# while True:
#    var = input("")
#    if not var:
#        continue

#    writeNumber(var)
