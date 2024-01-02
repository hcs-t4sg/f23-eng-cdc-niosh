import math
import FreeCAD as App
import Part
import numpy as np
import os, sys
sys.path.append(os.path.dirname(__file__))

import constants
print("DAOJFIJDSA")
def my_create_line(pt1, pt2, obj_name):
    obj = App.ActiveDocument.addObject("Part::Line", obj_name)
    obj.X1 = pt1[0]
    obj.Y1 = pt1[1]
    obj.Z1 = pt1[2]

    obj.X2 = pt2[0]
    obj.Y2 = pt2[1]
    obj.Z2 = pt2[2]

    App.ActiveDocument.recompute()
    return obj

driverHead = constants.DRIVER_HEAD

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
] 

doc = App.ActiveDocument

CANDIDATES_SET = set()
NONCANDIDATES_SET = set()

for name_i in FULL_LIST:

    absPathRoot = constants.ABS_PATH_ROOT
    ray_directions = np.load(f"{absPathRoot}/result_files_npy/{name_i}_directions.npy")
    results = np.load(f"{absPathRoot}/result_files_npy/{name_i}_results.npy")

    for direction_j, results_j, in zip(ray_directions, results):    
        direction_j = tuple(direction_j)

        if results_j == True:
            # Intersects
            if direction_j in CANDIDATES_SET:
                CANDIDATES_SET.remove(direction_j)
            NONCANDIDATES_SET.add(direction_j)
        else:
            # No intersection
            if not direction_j in NONCANDIDATES_SET:
                CANDIDATES_SET.add(direction_j)
            
for i, direction_i in enumerate(CANDIDATES_SET):
    sightline_end = [
        50 * direction_i[0] + driverHead[0],
        50 * direction_i[1] + driverHead[1],
        50 * direction_i[2] + driverHead[2],
    ]
    my_create_line(driverHead, sightline_end, f"{i}")