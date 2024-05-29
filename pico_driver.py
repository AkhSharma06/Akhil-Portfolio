import os
import serial
import time

def flash_pico():
    os.system("ampy --port /dev/ttyACM0 put pico/EEC195_Team5.py")
    os.system("ampy --port /dev/ttyACM0 run pico/EEC195_Team5.py")
    print("Done flashing")

flash_pico()