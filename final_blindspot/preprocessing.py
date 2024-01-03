import os, sys, constants
import numpy as np
import math 
import trimesh
import tqdm

sys.path.append(constants.FREECADPATH)

absPathRoot = os.path.join(constants.ABS_PATH_ROOT, 'final_blindspot')

import FreeCAD

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

if __name__ == '__main__':

    # Delete Existing Files
    if os.path.exists(f"{absPathRoot}/preprocessed_cache/"):
        import shutil
        shutil.rmtree(f"{absPathRoot}/preprocessed_cache/")
    os.makedirs(f"{absPathRoot}/preprocessed_cache/")
               
    # Log for Debugging
    log_file = open(os.path.join(constants.ABS_PATH_ROOT, 'final_blindspot', 'log.txt'), 'w')
    log_file.write("LOG FILE OF MOST RECENT FINAL_BLINDSPOT RUN\nGENERATED AFTER EACH RUN\n\n")

    # Open FreeCAD Document
    doc = FreeCAD.open(os.path.join(constants.ABS_PATH_ROOT, 'models', constants.FILENAME))

    # Iterate through each part of the truck
    for obj in (pbar := tqdm.tqdm(doc.Objects)):

        # Get the name to track progress
        name_i = obj.FullName.split('#')[1]
        pbar.set_description(f"Procesing {name_i}")

        # We only want to process this if we expect the object to block view, so we check if the part is in the pre-defined transparent part
        is_opaque = True
        for transparent_name in constants.CAB:
            if transparent_name in name_i:
                is_opaque = False

        # If opaque, we process
        if is_opaque:
            points_i = dict()
            faces_i = []

            for facet_j in obj.Mesh.Facets:
                # For each facet, get a list of points that compose the facet
                point_list = facet_j.Points
                assert(len(point_list) == 3)

                # Add facet to indexes
                index_list = []
                for point in point_list:
                    # If points are not already stored, do so
                    point_stored = tuple([round(a, 10) for a in point])
                    if not point_stored in points_i:
                        points_i[point_stored] = len(points_i)

                    # Add indices to index_list
                    index_list.append(points_i[point_stored])
                assert(len(index_list) == 3)

                # Add index list to faces_i
                faces_i.append(index_list)

            # Progress tracking
            log_file.write(f"Reconstruction of {name_i} consists of {len(points_i)} points and {len(faces_i)} faces\n")

            points_i = np.array([a for a in points_i.keys()])
            faces_i = np.array(faces_i)

            # Make mesh for the list and compute intersector
            mesh = trimesh.Trimesh(vertices = points_i, faces = faces_i)
            mesh = trimesh.ray.ray_triangle.RayMeshIntersector(mesh)
            
            # Get rays and see if they intersect
            ray_directions, thetas, phis = generateSightLineDirectionsGridded(constants.THETAS, constants.PHIS)
            ret = mesh.intersects_any([constants.DRIVER_HEAD] * len(ray_directions), ray_directions)

            # Save results
            np.save(f"{absPathRoot}/preprocessed_cache/{name_i}_directions.npy", np.array(ray_directions))
            np.save(f"{absPathRoot}/preprocessed_cache/{name_i}_results.npy", np.array(ret))
            np.save(f"{absPathRoot}/preprocessed_cache/{name_i}_thetas.npy", np.array(thetas))
            np.save(f"{absPathRoot}/preprocessed_cache/{name_i}_phis.npy", np.array(phis))
    
    # Close logging file
    log_file.close()

