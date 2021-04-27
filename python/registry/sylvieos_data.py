from time import sleep
import pyfiglet
import os

version = "2021 (1.1)"

def splash():
    ascii_banner = pyfiglet.figlet_format("Sylvie OS")
    print(ascii_banner)
    print("Version : " + version)
    
    sleep(3)
    
    os.system('clear')
