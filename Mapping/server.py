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
from math import radians, cos, sin

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

# Experimental WIP #
def polar_to_cartesian(distances):
    points = []
    for degree in range(360):
        distance = distances[degree]
        radians = radians(degree)
        x = distance * cos(radians)
        y = distance * sin(radians)
        z = 0  # Assuming 2D LiDAR
        points.append([x, y, z])
    return np.array(points)

# Experimental WIP #
# Need to convert polar to cartesian first       #
# Then generate an LAS file for each cloud-point #
def gen_file_out(data):
    with open('data.out', 'a') as fp:
        for angle, distance in enumerate(data):
            line = f"{angle}, {distance}"
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