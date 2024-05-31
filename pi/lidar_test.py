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
import time

""" [Constants] """
UART_RDY_PIN = 23
UART_PI_2_PICO_PIN = 24
PICO_DISABLE_PIN = 25
KP = 0.6

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
GPIO.setup(PICO_DISABLE_PIN, GPIO.OUT)

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
        #print(f"Travel Distance {travel_distance}")
        UART_Rdy = 1
        if travel_distance is None:
            UART_Rdy = -1

def write_pid_ctrl(direction, percent_ang):
    #Write to Pico
    GPIO.output(UART_PI_2_PICO_PIN, True)
    message = direction + ' ' + str(percent_ang) + '\n'
    #print(message)
    ser.write(message.encode())
    ser.flush()
    GPIO.output(UART_PI_2_PICO_PIN, False)

def polar_to_cartesian(r, theta):
    """Convert polar coordinates to Cartesian coordinates."""
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    return x, y

def cartesian_to_polar(x, y):
    """Convert Cartesian coordinates to polar coordinates."""
    r = math.sqrt(x**2 + y**2)
    theta = math.atan2(y, x)
    return r, theta

def sum_polar_vectors(vectors):
    """Sum vectors in polar coordinates."""
    sum_x = 0
    sum_y = 0

    for theta, r in vectors:
        x, y = polar_to_cartesian(r, theta)
        sum_x += x
        sum_y += y

    return cartesian_to_polar(sum_x, sum_y)

def find_mag(vectors):
    """Sum vectors given in polar coordinates and return the magnitude of the resultant vector."""
    cartesian_vectors = np.array([polar_to_cartesian(angle, distance) for angle, distance in vectors])
    resultant_cartesian = np.sum(cartesian_vectors, axis=0)
    resultant_magnitude = np.linalg.norm(resultant_cartesian)
    return resultant_magnitude

def find_longest_string_of_zeros(arr):
    max_length = 0
    current_length = 0
    max_start_index = -1
    max_end_index = -1
    current_start_index = -1

    for i, num in (arr):
        if num == 0:
            if current_length == 0:
                current_start_index = i  # Start of a new sequence of 0s
            current_length += 1
        else:
            if current_length > max_length:
                max_length = current_length
                max_start_index = current_start_index
                max_end_index = i - 1
            current_length = 0

    # Final check in case the array ends with a sequence of 0s
    if current_length > max_length:
        max_length = current_length
        max_start_index = current_start_index
        max_end_index = len(arr) - 1

    return max_start_index, max_end_index

def PID_control(scan_data):
    """
    Handles PID control calculations based on input scan_data
    
    return: (motor_spd: int, motor_dir: char, servo_ang: int, servo_dir: char)
      * motor_spd and servo_ang are returned as a percentage of the maximum i.e. (0 - 100%)
    """
    rh_vectors = []
    lh_vectors = []
    fw_vectors = []
    for angle, distance in enumerate(scan_data):
        # Process Right Hand Vectors
        if (angle >= 0 and angle <= 20) or (angle >= 340 and angle <= 360):
            lh_vectors.append((angle, distance))
        elif (angle >= 160 and angle <= 200):
            rh_vectors.append((angle, distance))
        if (angle >= 0 and angle <= 180):
            fw_vectors.append((angle, distance))
            # print(fw_vectors)
        else:
            pass  # for now
    # Get the longest string of zeros array (the angle we want to be)
    zero_start, zero_end = find_longest_string_of_zeros(fw_vectors)
    zero_avg_angle = int((zero_start + zero_end) / 2)

    rh_mag = find_mag(rh_vectors)
    lh_mag = find_mag(lh_vectors)
    # error = (rh_mag - lh_mag) * KP
    error = (zero_avg_angle - 90)
    #deadband = (rh_mag + lh_mag) * 0.1
    #max_error =  (rh_mag + lh_mag) * 0.3
    deadband = 2
    max_error = 60
    #print(f"Error calculated: {error} | RH {rh_mag} LH {lh_mag}")  
    # Go Right
    if error >= deadband:
        direction = 'R'
        if error >= max_error:
            percent_ang = 0.5
        else:
            percent_ang = error / max_error * 0.3
    # Go Left
    elif error <= -deadband:
        direction = 'L'
        if error <= -max_error:
            percent_ang = 0.5
        else:
            percent_ang = error / max_error * 0.3
    else:
        direction = 'N'
        percent_ang = 0.0
    print(f"Direction {direction} | Percent Ang {percent_ang}")
    return direction, abs(percent_ang)


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
    if tmp_cnt % 2 == 0:
        direction, percent_ang = PID_control(data)
        write_pid_ctrl(direction, percent_ang)
       # print(json.dumps(data_json))

    tmp_cnt += 1
    #print(json.dumps(data_json))
    #requests.post('http://10.42.0.61:8069', json=data_json)

if True:
    # Setup Interrupt Handler (what is bouncetime?)
    GPIO.output(UART_PI_2_PICO_PIN, False)
    GPIO.output(PICO_DISABLE_PIN, False)
    GPIO.add_event_detect(UART_RDY_PIN, GPIO.RISING, callback=uart_irq_handler, bouncetime=200)
    try:
        print("=== [Beginning Lidar Scans] ===")
        for scan in lidar.iter_scans():
            for(quality, angle, distance) in scan:
                scan_data[min([359, math.floor(angle)])] = distance
            process_data(scan_data)
            scan_data = [0]*360
    except RPLidarException as e:
        print("Error has occured with LiDar. Shutting Down ")
        print(e)
        GPIO.output(PICO_DISABLE_PIN, True)
        lidar.stop()
        lidar.stop_motor()
        lidar.clear_input()
        lidar.disconnect()
        GPIO.output(PICO_DISABLE_PIN, False)
    except KeyboardInterrupt:
        print("Stopping")   
        GPIO.output(PICO_DISABLE_PIN, True)
        lidar.stop()
        lidar.stop_motor()
        lidar.clear_input()
        lidar.disconnect()
        GPIO.output(PICO_DISABLE_PIN, False)
