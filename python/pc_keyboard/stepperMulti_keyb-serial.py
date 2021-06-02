from time import sleep

import serial
import keyboard
import os

ser = serial.Serial('/dev/ttyUSB0', 115200) # Establish the connection on a specific port
os.system("stty -echo")

previous_status = "0"
previous_message = ""

def write_serial(status, printed):
    global previous_status
    if status != previous_status:
        os.system('clear')	
        print(printed)
        ser.write(str(status).encode())
        previous_status = status

def clear_serial(status):
    global previous_status
    if status != previous_status:
        os.system('clear')
        print("WAITING FOR USER INPUT! (TRY Q,W,E,R,T,A,S,D,F)")
        ser.write(str(status).encode())
        previous_status = status
        
def sys_message(message):
    global previous_message
    if message != previous_message:
        os.system('clear')
        print(message)
        previous_message = message        

while True:
    if keyboard.is_pressed('q'): 	
        write_serial(2, "KEYBOARD KEY [Q] PRESSED!")
        sleep(0.25)
        clear_serial(0)
    elif keyboard.is_pressed('w'): 	
        write_serial(3, "KEYBOARD KEY [W] PRESSED!")
        sleep(0.25)
        clear_serial(0)  
    elif keyboard.is_pressed('e'): 	
        write_serial(4, "KEYBOARD KEY [E] PRESSED!")
        sleep(0.25)
        clear_serial(0)   
    elif keyboard.is_pressed('r'): 	
        write_serial(5, "KEYBOARD KEY [R] PRESSED!")
        sleep(0.25)
        clear_serial(0)  
    elif keyboard.is_pressed('t'): 	
        write_serial(6, "KEYBOARD KEY [T] PRESSED!")
        sleep(0.25)
        clear_serial(0)   
    elif keyboard.is_pressed('y'): 	
        write_serial(7, "KEYBOARD KEY [Y] PRESSED!")
        sleep(0.25)
        clear_serial(0) 
    elif keyboard.is_pressed('a'): 	
        write_serial(8, "KEYBOARD KEY [A] PRESSED!")
        sleep(0.25)
        clear_serial(0)   
    elif keyboard.is_pressed('s'): 	
        write_serial(9, "KEYBOARD KEY [S] PRESSED!")
        sleep(0.25)
        clear_serial(0) 
    elif keyboard.is_pressed('d'): 	
        write_serial(10, "KEYBOARD KEY [D] PRESSED!")
        sleep(0.25)
        clear_serial(0)   
    elif keyboard.is_pressed('f'): 	
        write_serial(11, "KEYBOARD KEY [F] PRESSED!")
        sleep(0.25)
        clear_serial(0)
    elif keyboard.is_pressed('g'): 	
        write_serial(12, "KEYBOARD KEY [G] PRESSED!")
        sleep(0.25)
        clear_serial(0)   
    elif keyboard.is_pressed('h'): 	
        write_serial(13, "KEYBOARD KEY [H] PRESSED!")
        sleep(0.25)
        clear_serial(0) 
    elif keyboard.is_pressed('z'): 	
        write_serial(14, "KEYBOARD KEY [Z] PRESSED!")
        sleep(0.25)
        clear_serial(0)   
    elif keyboard.is_pressed('x'): 	
        write_serial(15, "KEYBOARD KEY [X] PRESSED!")
        sleep(0.25)
        clear_serial(0)
    elif keyboard.is_pressed('u'): 	
        write_serial(16, "KEYBOARD KEY [U] PRESSED!")
        sleep(0.25)
        clear_serial(0)  
    elif keyboard.is_pressed('i'): 	
        write_serial(17, "KEYBOARD KEY [I] PRESSED!")
        sleep(0.25)
        clear_serial(0) 
    elif keyboard.is_pressed('c'): 	
        write_serial(18, "KEYBOARD KEY [C] PRESSED!")
        sleep(0.25)
        clear_serial(0) 
    elif keyboard.is_pressed('v'): 	
        write_serial(19, "KEYBOARD KEY [V] PRESSED!")
        sleep(0.25)
        clear_serial(0)    
    elif keyboard.is_pressed('b'): 	
        write_serial(20, "KEYBOARD KEY [B] PRESSED!")
        sleep(0.25)
        clear_serial(0) 
    elif keyboard.is_pressed('n'): 	
        write_serial(21, "KEYBOARD KEY [N] PRESSED!")
        sleep(0.25)
        clear_serial(0)
    elif keyboard.is_pressed('j'): 	
        write_serial(22, "KEYBOARD KEY [J] PRESSED!")
        sleep(0.25)
        clear_serial(0) 
    elif keyboard.is_pressed('k'): 	
        write_serial(23, "KEYBOARD KEY [K] PRESSED!")
        sleep(0.25)
        clear_serial(0)                                                                                                            
    elif keyboard.is_pressed('p'):
        write_serial(1, "DONE.")	
        sleep(1)
        os.system('stty echo')                
        os.system('clear')
        exit()
    else:		
        sys_message("WAITING FOR USER INPUT! (TRY Q,W,E,R,T,A,S,D,F)")   
