import numpy as np
import trimesh
import math

import constants

driverHead = constants.DRIVER_HEAD

absPathRoot = constants.ABS_PATH_ROOT
TRUCK_NAME = constants.TRUCK_NAME

FULL_LIST = np.load(f'{absPathRoot}/{TRUCK_NAME}_part_names.npy')

'''
generateSightLinesGridded():
Parameters: 
- theta_angles, the number of rays to split across theta (the horizontal angle spanning 360 degrees in the x-y plane)
- phi_angles, the number of rays to split across phi (the vertical angle with the z-axis, spans 180 degrees)
Returns: a list of n sightline directions, each a vector from the given origin, and their corresponding theta and phi
'''
def generateSightLineDirectionsGridded(theta_angles = 30, phi_angles = 15):
    
    ray_directions = []
    thetas = []
    phis = []

    # Iterate over all possible theta and phi combinations
    for i in range(0, theta_angles):
        for j in range(0, phi_angles):
            # Compute the correct theta and pi for this angle
            theta = 2 * math.pi * i / theta_angles
            phi = math.pi * j / phi_angles
            # Add thetas to arrays
            thetas.append(i)
            phis.append(j)
            # Convert spherical coordinates to Cartesian direction, assuming radius of 100 and append it to directions
            direction = (math.cos(theta) * math.sin(phi) * 100, math.sin(theta) * math.sin(phi) * 100, math.cos(phi) * 100 )
            ray_directions.append((round(direction[0], 6), round(direction[1], 6), round(direction[2], 6)))

    return ray_directions, thetas, phis

print(FULL_LIST)

# Iterate over each piece in full list
for name_i in FULL_LIST:
    print(name_i)
    # Import data
    points_i = np.load(f'{absPathRoot}/mesh_files_npy/{name_i}_points.npy')
    faces_i = np.load(f'{absPathRoot}/mesh_files_npy/{name_i}_faces.npy')

    # Make mesh for the list and compute intersector
    mesh = trimesh.Trimesh(vertices = points_i, faces = faces_i)
    mesh = trimesh.ray.ray_triangle.RayMeshIntersector(mesh)
    
    # Get rays and see if they intersect
    ray_directions, thetas, phis = generateSightLineDirectionsGridded(constants.THETAS, constants.PHIS)
    ret = mesh.intersects_any([driverHead] * len(ray_directions), ray_directions)

    # Save results
    np.save(f"{absPathRoot}/result_files_npy/{name_i}_directions.npy", np.array(ray_directions))
    np.save(f"{absPathRoot}/result_files_npy/{name_i}_results.npy", np.array(ret))
    np.save(f"{absPathRoot}/result_files_npy/{name_i}_thetas.npy", np.array(thetas))
    np.save(f"{absPathRoot}/result_files_npy/{name_i}_phis.npy", np.array(phis))
