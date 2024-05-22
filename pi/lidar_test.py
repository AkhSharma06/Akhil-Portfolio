import os
from math import cos, sin, pi, floor
from adafruit_rplidar import RPLidar
import socket
import json

LIDAR_PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar(None, LIDAR_PORT_NAME, timeout = 3)

max_distance = 0
scan_data = [0]*360

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.bind(('localhost', 8069))

def process_data(data):
    print(data)
    data_str = json.dumps(data)
    client_socket.send(data_str.encode())

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