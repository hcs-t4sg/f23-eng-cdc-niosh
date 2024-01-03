import math
import FreeCAD as App
import Part
import numpy as np
import os, sys
sys.path.append(os.path.dirname(__file__))

import constants

# Function to create a line in FreeCAD
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

# Origin from which all lines start
driverHead = constants.DRIVER_HEAD

# Get list of parts
FULL_LIST = constants.FULL_LIST

doc = App.ActiveDocument

CANDIDATES_SET = set()
NONCANDIDATES_SET = set()

# For each part for which sightlines were computed, we want to get the sightline directions and results
for name_i in FULL_LIST:

    absPathRoot = constants.ABS_PATH_ROOT
    ray_directions = np.load(f"{absPathRoot}/result_files_npy/{name_i}_directions.npy")
    results = np.load(f"{absPathRoot}/result_files_npy/{name_i}_results.npy")

    # We look at each line and corresponding result
    for direction_j, results_j, in zip(ray_directions, results):    
        direction_j = tuple(direction_j)

        # In the case that the line intersects, we add it to the NON-CANDIDATES SET -- lines we can't see
        # We remove it from the candidates if it had been added as well
        if results_j == True:
            if direction_j in CANDIDATES_SET:
                CANDIDATES_SET.remove(direction_j)
            NONCANDIDATES_SET.add(direction_j)

        # If no intersection, we add the line to the candidates if it hasn't been blocked yet
        else:
            if not direction_j in NONCANDIDATES_SET:
                CANDIDATES_SET.add(direction_j)
            
# Draw lines in candidate set -- visible set
for i, direction_i in enumerate(CANDIDATES_SET):
    sightline_end = [
        50 * direction_i[0] + driverHead[0],
        50 * direction_i[1] + driverHead[1],
        50 * direction_i[2] + driverHead[2],
    ]
    my_create_line(driverHead, sightline_end, f"{i}")