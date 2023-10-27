import math
import FreeCAD as App
import Part

import math
import FreeCAD as App
import Part

'''
generateSightLines():
Parameters: 
- n, the number of sightlines
- origin, (x, y, z) coordinates of the camera
Returns: a list of n sightlines, each a vector from the given origin

Sources: 
- https://arxiv.org/pdf/0912.4540.pdf
- https://extremelearning.com.au/how-to-evenly-distribute-points-on-a-sphere-more-effectively-than-the-canonical-fibonacci-lattice/
'''

def generateSightLineDirections(N = 200):
    
    vectors = []
    inverseGoldenRatio = (5**0.5 - 1)/2

    for i in range(0, N):
        theta = 2 * math.pi * i * inverseGoldenRatio
        phi = math.acos(1 - 2 * (i+0.5) / N)

        direction = ( math.cos(theta) * math.sin(phi) * 100, math.sin(theta) * math.sin(phi) * 100, math.cos(phi) * 100 )
        vectors.append(
            (round(direction[0], 6), round(direction[1], 6), round(direction[2], 6))
        )

    return vectors 

'''
my_create_line():
Parameters:
- pt1, pt2, points on the line in the form (x, y, z)
- obj_name, name of Line Object
Return: 
- Updated active document

Source:
- Updated active documenthttps://wiki.freecad.org/Part_scripting
'''
def my_create_line(pt1, pt2, obj_name, color = (0, 0, 0)):
    obj = App.ActiveDocument.addObject("Part::Line", obj_name)
    obj.ViewObject.LineColor = color
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
sightlines = generateSightLineDirections(300)

# list of mesh objects
doc = App.ActiveDocument

mesh_list = []
parts_list = [
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
for obj_name in parts_list: # omitted "Chasis_Detached_" in place of windows
    print(f"Extracted Object: {obj_name}")
    mesh_list.append(doc.getObject(obj_name).Mesh)

print("RUNNING")

BUGGY_COUNTER = 0

# Find intersections
for i, sightline_dir in enumerate(sightlines):

    intersects = False

    for name_i, mesh_i in zip(parts_list, mesh_list):
        # print(f"PART NAME: {name_i}")
        
        intersectionList = mesh_i.nearestFacetOnRay(driverHead, sightline_dir)
        if len(intersectionList)!=0:
            # print(f"intersects: {list(intersectionList.values())} times")
            intersects = True
            break
        else:
            intersects = False
            #my_create_line(driverHead, sightline_end, f"nointline_{i}", (0, 0, 0))
            print("doesnt intersect")

    if intersects:
        sightline_end = tuple([a + 10 * b for a, b in zip(driverHead, sightline_dir)])
        intersection_dir = tuple([b - a for a, b in zip(driverHead, list(intersectionList.values())[0])])
        
        if not(sightline_dir[0] * intersection_dir[0] > 0 and sightline_dir[1] * intersection_dir[1] > 0 and sightline_dir[2] * intersection_dir[2] > 0) : 
            #my_create_line(driverHead, sightline_end, f"buggyline_{i}", (100, 0, 100))
            print("Directions don't align", intersection_dir, sightline_dir)
            BUGGY_COUNTER += 1
            intersectionList = mesh_i.nearestFacetOnRay(sightline_dir, driverHead)
            if len(intersectionList)!=0:
                my_create_line(driverHead, sightline_end, f"buggyline_{i}", (200, 0, 0))
            else:
                my_create_line(driverHead, sightline_end, f"buggyline_{i}", (0, 200, 0))

        #else:
            #my_create_line(driverHead, sightline_end, f"intline_{i}", (255, 0, 0))
    

print(f"{BUGGY_COUNTER} BUGS OUT OF {300}")

