"""
\file       lidar_test.py
\brief      RPi Code for interfacing with Lidar sensor
            Communicates with Pico via UART to send motor control signals
            Posts to server on remote laptop for data visualization

\authors    Corbin Warmbier
            Brian Barcenas
            Akhil Sharma
            Alize De Leon

\date       Initial: 05/19/24  |  Last: 05/29/24
"""
""" [Imports] """
from math import cos, sin, pi, floor
from adafruit_rplidar import RPLidar, RPLidarException
import requests
import json
import serial
import RPi.GPIO as GPIO

""" [Constants] """
UART_RDY_PIN = 23
UART_PI_2_PICO_PIN = 24

""" [Initializations] """
ser = serial.Serial(
    port = '/dev/ttyS0',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    bytesize=serial.EIGHTBITS,
    stopbits=serial.STOPBITS_ONE,
    timeout=1
)


# Setup UART_Rdy pin on RPi (Dummy Interrupt)
UART_Rdy = 0  # Global flag for UART reading
GPIO.setmode(GPIO.BCM)
GPIO.setup(UART_RDY_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(UART_PI_2_PICO_PIN, GPIO.OUT)

LIDAR_PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar(None, LIDAR_PORT_NAME, timeout = 3)

travel_distance = 0
max_distance = 0
scan_data = [0]*360

counter = 0

""" [Local Functions] """
def uart_irq_handler(channel):
    """
    Handles interrupts received on UART_RDY_PIN
    Sets UART_Rdy global flag when data has been received

    return: none
    """
    global UART_Rdy
    global travel_distance
    # Sanity Check If Statement
    if channel == UART_RDY_PIN:
        travel_distance = float(ser.readline().decode())
        UART_Rdy = 1
        if travel_distance is None:
            UART_Rdy = -1

def pid_calculations():
    #Write to Pico
    GPIO.output(UART_PI_2_PICO_PIN, False)
    ser.write("hello".encode())
    GPIO.output(UART_PI_2_PICO_PIN, True)

def process_data(data):
    global UART_Rdy
    global travel_distance
    if UART_Rdy != 1:
        travel_distance = float(UART_Rdy)
    data_json = {
        "scan_data" : data,
        "distance" : travel_distance
    }
    UART_Rdy = 0
    travel_distance = 0
    ## PID CALCULATIONS
    pid_calculations()
    print(json.dumps(data_json))
    # requests.post('http://10.42.0.61:8069', json=data_json)

#while True:
#    lidar.start()
GPIO.output(UART_PI_2_PICO_PIN, True)
if True:
    # Setup Interrupt Handler (what is bouncetime?)
    GPIO.add_event_detect(UART_RDY_PIN, GPIO.RISING, callback=uart_irq_handler, bouncetime=200)
    # lidar.start()
    try:
        print("=== [Beginning Lidar Scans] ===")
        for scan in lidar.iter_scans():
            for(quality, angle, distance) in scan:
                normalized_angle = min([359, floor(angle)])
                if (normalized_angle >= 0 and normalized_angle <= 10) or (normalized_angle >= 180 and normalized_angle <= 200):
                    scan_data[normalized_angle] = distance
            process_data(scan_data)
    except RPLidarException:
        print("Error has occured with LiDar. Shutting Down ")
        lidar.stop()
        lidar.stop_motor()
        lidar.clear_input()
        lidar.disconnect()
    except KeyboardInterrupt:
        print("Stopping")
        lidar.stop()
        lidar.stop_motor()
        lidar.clear_input()
        lidar.disconnect()
