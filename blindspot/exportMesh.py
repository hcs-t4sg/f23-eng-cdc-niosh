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

# Which parts should be ommitted from obstruction
CAB = constants.CAB

absPathRoot = constants.ABS_PATH_ROOT

# Iterate through each part of the truck
for obj in doc.Objects:

    # Get the name to track progress
    name_i = obj.FullName.split('#')[1]
    print(f"Extracted Object: {name_i}")

    # We only want to process this if we expect the object to block view, so we check if the part is in the pre-defined transparent part
    is_opaque = True
    for transparent_name in CAB:
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
    print(f"Reconstruction of {name_i} consists of {len(points_i)} points and {len(faces_i)} faces")
    
    # Save all points and facets when converting an object to a mesh
    points_i = np.array([a for a in points_i.keys()])
    faces_i = np.array(faces_i)

    np.save(f'{absPathRoot}/mesh_files_npy/{name_i}_points.npy', points_i)
    np.save(f'{absPathRoot}/mesh_files_npy/{name_i}_faces.npy', faces_i)
