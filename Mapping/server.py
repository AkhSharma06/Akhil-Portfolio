"""
\file       server.py
\brief      Code to run a local server on computer and receive POST requests
            Requires finding local IP (run 'ifconfig | grep inet')
            Save the inet IP that is NOT localhost (127.0.0.1)

\authors    Corbin Warmbier
            Brian Barcenas
            Akhil Sharma
            Alize De Leon

\date       Initial: 05/21/24  |  Last: 05/22/24
"""

""" [Imports] """
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
from sys import argv
import numpy as np
import math

"""
Server Handling Class
Provides code for POST capabilities
"""
class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])  # Gets the size of data
        post_data = self.rfile.read(content_length)  # Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))
        gen_file_out(post_data.decode('utf-8'))
        self._set_response()  # Send received response
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=S, port=8069):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    print(server_address)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

def deg_to_rad(degrees):
    return degrees * (math.pi / 180)

# Experimental WIP #
def gen_file_out(data, car_distance):
    with open('lidar_scans.txt', 'a') as fp:
        # Initialize x and y components
        x_sum = 0
        y_sum = 0
        for angle, distance in data:
            angle_rad = deg_to_rad(angle)
            x_sum += distance * math.cos(angle_rad)
            y_sum += distance * math.sin(angle_rad)
        # Calculate Resulting Angle of Vectors
        angle_resultant = math.atan2(y_sum, x_sum)
        angle_resultant_deg = math.degrees(angle_resultant)

        # Ensure the angle is in the range [0, 360)
        if angle_resultant_deg < 0:
            angle_resultant_deg += 360

        line = f"{{{angle_resultant_deg},{car_distance}}} {data}"
        fp.writelines(line)

# ========================================= #
#          === [Main Function] ===          #
# ========================================= #
if __name__ == '__main__':
    open('data.out', 'w').close()  # Clear data.out file
    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()