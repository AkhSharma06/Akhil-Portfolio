import os
from math import cos, sin, pi, floor
from adafruit_rplidar import RPLidar
import requests
import json
import RPi.GPIO as GPIO

SPEED_SENSOR = 3

GPIO.setmode(GPIO.BCM)

LIDAR_PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar(None, LIDAR_PORT_NAME, timeout = 3)

MOTOR_FREQ = 5000  # 5kHz; optimal VNH freq
SERVO_FREQ = 100
MOTOR_SPD_MAX = 200000  # Based on MOTOR_FREQ ! Must Change if MOTOR_FREQ is modified
TIMER_FREQ = 2  # Hz
COUNTS_TO_ROTATION = 3  # Number of counters per wheel rotation (aka # of tape pieces)

max_distance = 0
scan_data = [0]*360

counter = 0

def process_data(data):
    data_json = {
        "scan_data" : data
    }
    print(json.dumps(data_json))
    requests.post('http://10.42.0.61:8069', json=data_json)

def spd_irq_handler(edge_type):
    """
    Interrupt handler for speed sensor
    
    :param edge_type <Pin obj>: Falling or rising edge irq detection
    :return: none
    """
    global counter
    counter += 1

def spd_counter(timer):
    global counter
    global traveled_distance
    if counter != 0:
        distance = (counter / COUNTS_TO_ROTATION) * 4.1 * pi  # Distance formula 'Rotations * Wheel Dia * Pi = Inches'
        print(f'Traveled {distance} inches')
        traveled_distance += distance
    counter = 0

GPIO.setup(SPEED_SENSOR, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(SPEED_SENSOR, callback=spd_irq_handler, bouncetime=50)


try:
    #print(lidar.info)
    for scan in lidar.iter_scans():
        for(_, angle, distance) in scan:
            scan_data[min([359, floor(angle)])] = distance
        process_data(scan_data)

except KeyboardInterrupt:
    print("Stopping")
    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()