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
import math
import numpy as np
from adafruit_rplidar import RPLidar, RPLidarException
import requests
import json
import serial
import RPi.GPIO as GPIO

""" [Constants] """
UART_RDY_PIN = 23
UART_PI_2_PICO_PIN = 24

""" [Initializations] """
ser = serial.Serial ("/dev/ttyS0", timeout=0)    #Open named port 
ser.baudrate = 115200 #Set baud rate to 9600

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

tmp_cnt = 0

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

def polar_to_cartesian(angle, distance):
    """Convert polar coordinates to Cartesian coordinates."""
    x = distance * np.cos(np.radians(angle))
    y = distance * np.sin(np.radians(angle))
    return np.array([x, y])

def find_mag(vectors):
    """Sum vectors given in polar coordinates and return the magnitude of the resultant vector."""
    cartesian_vectors = np.array([polar_to_cartesian(angle, distance) for angle, distance in vectors])
    resultant_cartesian = np.sum(cartesian_vectors, axis=0)
    resultant_magnitude = np.linalg.norm(resultant_cartesian)
    return resultant_magnitude

def PID_control(scan_data):
    """
    Handles PID control calculations based on input scan_data
    
    return: (motor_spd: int, motor_dir: char, servo_ang: int, servo_dir: char)
      * motor_spd and servo_ang are returned as a percentage of the maximum i.e. (0 - 100%)
    """

    for angle, distance in enumerate(scan_data):
        rh_vectors = []
        lh_vectors = []
        for angle, distance in enumerate(scan_data):
            # Process Right Hand Vectors
            if (angle >= 0 and angle <= 20) or (angle >= 340 and angle <= 360):
                rh_vectors.append(angle, distance)
            elif (angle >= 160 and angle <= 200):
                lh_vectors.append(angle, distance)
            else:
                pass  # for now
        rh_mag = find_mag(rh_vectors)
        lh_mag = find_mag(lh_vectors)
        error = rh_mag - lh_mag
        deadband = 10
        print(f"Error calculated: {error} | RH {rh_mag} - LH {lh_mag}")
        if error >= deadband:
            print(f"Closer to Right Wall Turn Left !%")
        elif error <= -deadband:
            print(f"Closer to Left Wall Turn Right !")



def process_data(data):
    global tmp_cnt
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
    if tmp_cnt % 5 == 0:
        PID_control(data)
    tmp_cnt += 1
    print(json.dumps(data_json))
    requests.post('http://10.42.0.61:8069', json=data_json)

#while True:
#    lidar.start()

if True:
    # Setup Interrupt Handler (what is bouncetime?)
    GPIO.add_event_detect(UART_RDY_PIN, GPIO.RISING, callback=uart_irq_handler, bouncetime=200)
    # lidar.start()
    try:
        print("=== [Beginning Lidar Scans] ===")
        for scan in lidar.iter_scans():
            for(quality, angle, distance) in scan:
                normalized_angle = min([359, math.floor(angle)])
                if ((normalized_angle >= 340 and normalized_angle <= 360) or (normalized_angle <= 20 and normalized_angle >=0)) or (normalized_angle >= 160 and normalized_angle <= 200):
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
