import math
import numpy as np
import open3d as o3d
import time

def polar_to_cartesian(distances, translation):
    points = []
    for degree in range(360):
        distance = distances[degree]
        if distance == 0:
            continue  # Skip zero distances
        radians = math.radians(degree)
        x = distance * math.cos(radians) + translation[0]
        y = distance * math.sin(radians) + translation[1]
        z = 0  # Assuming 2D LiDAR
        points.append([x, y, z])
    return np.array(points)

def create_point_cloud(points, color):
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    pcd.colors = o3d.utility.Vector3dVector(np.tile(color, (points.shape[0], 1)))
    return pcd

def update_view(vis, pcd):
    vis.update_geometry(pcd)
    vis.poll_events()
    vis.update_renderer()

    # Fit the view to the new set of points
    view_ctl = vis.get_view_control()
    bounds = pcd.get_axis_aligned_bounding_box()
    center = bounds.get_center()
    extent = bounds.get_extent()

    # Set the lookat point to the center of the bounding box
    view_ctl.set_lookat(center)
    # Set the front to a reasonable direction
    view_ctl.set_front([0.0, 0.0, -1.0])
    # Set the up direction
    view_ctl.set_up([0.0, 1.0, 0.0])
    # Adjust the zoom to fit the bounding box
    view_ctl.set_zoom(2.0 / max(extent))  # Adjust this factor as needed


def calculate_trajectory(translation, distance_traveled, angle_degrees):
    angle_radians = math.radians(angle_degrees)
    translation[0] += distance_traveled * math.cos(angle_radians)
    translation[1] += distance_traveled * math.sin(angle_radians)
    return translation


# Initialize Open3D visualizer with specific window dimensions
vis = o3d.visualization.Visualizer()
vis.create_window(window_name='LiDAR Point Cloud', width=800, height=600)

# Initial distance values
distances = [10] * 360
# Initial translation
translation = [0, 0, 0]
# Store all points
all_points = []

# Create an empty point cloud object for initial visualization
pcd = o3d.geometry.PointCloud()
vis.add_geometry(pcd)

# Main loop to update point cloud every second
try:
    while True:
        # Convert to Cartesian coordinates with current translation
        new_points = polar_to_cartesian(distances, translation)

        # Add new points to the accumulated points
        all_points.extend(new_points)

        # Create point cloud from all accumulated points
        pcd.points = o3d.utility.Vector3dVector(np.array(all_points))
        pcd.colors = o3d.utility.Vector3dVector(np.tile([1, 0, 0], (len(all_points), 1)))  # Red color

        # Update the visualizer
        vis.clear_geometries()
        vis.add_geometry(pcd)

        # Adjust view to fit all points
        update_view(vis, pcd)

        # Simulate movement by updating the translation
        translation[1] += 10  # Move 10 units along the x-axis each iteration

        # Increment distances for the next iteration
        distances = [d + 1 for d in distances]  # Increment each distance by 1 for demonstration

        # Wait for 1 second before the next update
        time.sleep(1)

except KeyboardInterrupt:
    # Close the visualizer on interrupt
    vis.destroy_window()
