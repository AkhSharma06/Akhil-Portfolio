import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import use
import time

use('MacOSX')

print('To stop - close the plot window')
data_wait = 0
IMIN: int = 0
IMAX: int = 50
DMAX: int = 4000

def parse_data(input_str):
    try:
        # Split the line into two parts: angle-distance and distances array
        parts = input_str.split(' ', 1)  # Split only at the first space
        if len(parts) < 2:
            print(f"Invalid input format: {input_str}")
            return None, None, None
        
        # Extract and parse the angle and distance travelled
        angle_distance_str = parts[0].strip('{}')
        angle_distance_parts = angle_distance_str.split(',')
        
        if len(angle_distance_parts) < 2:
            print(f"Invalid angle-distance format: {angle_distance_str}")
            return None, None, None
        
        angle = float(angle_distance_parts[0])
        distance_travelled = float(angle_distance_parts[1])
        
        # Extract and parse the distances array
        distances_str = parts[1].strip('[]').strip()
        if not distances_str:
            print(f"Empty distances array: {input_str}")
            return angle, distance_travelled, []
        
        distances = list(map(float, distances_str.split(',')))
        return angle, distance_travelled, distances
    except Exception as e:
        print(f"Error parsing input data: {e}")
        print(f"Input string causing error: {input_str}")
        return None, None, None

def update_line(num, iterator, line):
    scan = next(iterator)
    offsets = np.array([(np.radians(meas[1]), meas[2]) for meas in scan])
    line.set_offsets(offsets)
    intents = np.array([meas[0] for meas in scan])
    line.set_array(intents)
    return line

file_position = 0
while True:
    with open('lidar_scans.txt', 'r') as file:
        file.seek(file_position)  # Move to the last read position
        scan_body = file.readline().strip()
        file_position = file.tell()  # Update the file position

    if not scan_body:
        if data_wait == 0:
            print("No new data. Waiting for new data...")
            data_wait = 1
        time.sleep(1)
        continue

    # New Data Found, Plot
    data_wait = 0
    fig = plt.figure()
    title = 'RPLIDAR'
    fig.set_label(title)
    fig.canvas.manager.set_window_title(title)

    ax = plt.subplot(111, projection='polar')
    line = ax.scatter([0, 0], [0, 0], s=5, c=[IMIN, IMAX], cmap=plt.cm.Greys_r, lw=0)
    ax.set_title('360° scan result')
    ax.set_rmax(DMAX)
    ax.grid(True)

    angle, distance_travelled, distances = parse_data(scan_body)
    iterator = distances
    ani = animation.FuncAnimation(fig, update_line, fargs=(iterator, line), interval=50)

    plt.show()
    