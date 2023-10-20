import math
import FreeCAD as App
import Part

from sightline import generateSightLines

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

driverHead = (352.5016492337469, 339.719522252282, -105.5012320445894)

# list of sightlines = generateSightLines(N = # of sightlines, origin = driver’s head coordinates)
sightlines = generateSightLines(300, driverHead)

# list of mesh objects
doc = App.ActiveDocument

mesh_list = []
for obj_name in [
    "_73f_Tire_FrontLeft_Detached_",
    "_73f_Tire_BackRight_Detached_",
    "_73f_Tire_BackLeft_Detached_",
    "_73f_Tire_FrontRight_Detached_",
    "Chasis_Detached_",
    "_73f_Bucket_",
    "AxleRear_Detached_",
    "BatteryUnit_Detached_",
    "PistonsRear_Detached_",
    "Platform_Detached_",
    "RearHydraulics_Detached_",
]: # omitted "Chasis_Detached_" in place of windows
    mesh_list.append(doc.getObject(obj_name).Mesh)

# Find intersections
for i, sightline_dir in enumerate(sightlines):
    intersects = False
    for mesh_i in mesh_list:
        if len(mesh_i.nearestFacetOnRay(driverHead, sightline_dir))!=0:
            intersects = True
            break  

    if intersects:
        my_create_line(driverHead, sightline_dir, f"line_{i}")