import math
import FreeCAD as App
import Part
import numpy as np

import os, sys
sys.path.append(os.path.dirname(__file__))

import constants

# list of mesh objects
doc = App.ActiveDocument

mesh_list = []

FULL_LIST = [
    "_73f_Bucket_",
    "_73f_Tire_FrontLeft_Detached_",
    "_73f_Tire_BackRight_Detached_",
    "_73f_Tire_BackLeft_Detached_",
    "_73f_Tire_FrontRight_Detached_",
    "Chasis_Detached_",
    "AxleRear_Detached_",
    "BatteryUnit_Detached_",
    "PistonsRear_Detached_",
    "Platform_Detached_",
    "RearHydraulics_Detached_",
] # "Cab_Detached_" is omitted, as we assume the windows are clear

# Iterate through parts
for name_i in FULL_LIST:
    print(f"Extracted Object: {name_i}")

    points_i = dict()
    faces_i = []

    # Iterate through facets of each part
    for obj in doc.Objects:
        if "Cab_Detached_" not in obj.FullName:
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
    
    print(f"Reconstruction of {name_i} consists of {len(points_i)} points and {len(faces_i)} faces")
    
    
    points_i = np.array([a for a in points_i.keys()])
    faces_i = np.array(faces_i)

    absPathRoot = constants.ABS_PATH_ROOT
    np.save(f'{absPathRoot}/mesh_files_npy/{name_i}_points.npy', points_i)
    np.save(f'{absPathRoot}/mesh_files_npy/{name_i}_faces.npy', faces_i)

    

    