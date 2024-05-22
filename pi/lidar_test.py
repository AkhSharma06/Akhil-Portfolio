import os
from math import cos, sin, pi, floor
from adafruit_rplidar import RPLidar
import requests
import json

LIDAR_PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar(None, LIDAR_PORT_NAME, timeout = 3)

max_distance = 0
scan_data = [0]*360

def process_data(data):
    data_str = json.dumps(data)
    print(data_str)
    requests.post('http://10.42.0.61:8069', data= data_str)

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