import math
import FreeCAD as App
import Part
import FreeCADGui as Gui
import numpy as np


def find_intersection_point(line_vertices, plane_vertices):

    # Get direction
    line_direction = np.subtract(line_vertices[1], line_vertices[0])
    # line_parametric(t): return line_start + t * line_direction

    print("ld:", line_direction)

    # Find two vectors in the plane
    vector1 = np.subtract(plane_vertices[1], plane_vertices[0])
    vector2 = np.subtract(plane_vertices[2], plane_vertices[0])

    print("v1:", vector1)
    print("v2:", vector2)

    # Find the normal vector
    normal_vector = np.cross(vector1, vector2)

    coeff1 = normal_vector[0]
    coeff2 = normal_vector[1]
    coeff3 = normal_vector[2]

    sum = coeff1 * plane_vertices[0][0] + coeff2 * \
        plane_vertices[0][1] + coeff3 * plane_vertices[0][2]

    print(normal_vector)
    print("sum: ", sum)

    eq1 = np.Eq(coeff1 * (line_vertices[0][0] + line_direction[0] * t) + coeff2 * (
        line_vertices[0][1] + line_direction[1] * t) + coeff3 * (line_vertices[0][2] + line_direction[2] * t), sum)
    ans = np.solve(eq1, t)
    print("answer", ans)


def get_line_vertices(line):
    line_vertices = [[0 for i in range(3)] for j in range(2)]
    for i in range(2):
        line_vertices[i][0] = line.Shape.Vertexes[i].X
        line_vertices[i][1] = line.Shape.Vertexes[i].Y
        line_vertices[i][2] = line.Shape.Vertexes[i].Z
    return line_vertices


def get_plane_vertices(plane):
    plane_vertices = [[0 for i in range(3)] for j in range(4)]
    for i in range(4):
        plane_vertices[i][0] = plane.Shape.Vertexes[i].X
        plane_vertices[i][1] = plane.Shape.Vertexes[i].Y
        plane_vertices[i][2] = plane.Shape.Vertexes[i].Z
    return plane_vertices

def generateSightLines(N = 200, origin = (0, 0, 0)):
    vectors = []
    inverseGoldenRatio = (5**0.5 - 1)/2

    for i in range(0, N):
        theta = 2 * math.pi * i * inverseGoldenRatio
        phi = math.acos(1 - 2 * (i+0.5) / N)

        vectors.append((
            origin[0] + math.cos(theta) * math.sin(phi) * 10000, 
            origin[1] + math.sin(theta) * math.sin(phi) * 10000,
            origin[2] + math.cos(phi) * 10000
        ))

    return vectors 

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
sightlines = generateSightLines(300, driverHead)

# list of mesh objects
doc = App.ActiveDocument

mesh_list = []
face_list = []
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
    face_list.append(doc.getObject(obj_name).Mesh.Facets[0].Points)


# Find intersections
for i,sightline_dir in enumerate(sightlines):
    intersects = False
    for mesh_i in mesh_list:
        print(mesh_i)
        for p in face_list:
            #if len(mesh_i.nearestFacetOnRay(driverHead, sightline_dir))!=0:
            print(p)
            if find_intersection_point([driverHead, sightline_dir], p) == True:
                #print(mesh_i)
                #print(mesh_i.nearestFacetOnRay(driverHead, sightline_dir))
                #print(driverHead)
                #print(sightline_dir)
                intersects = True
                break
    
    if intersects:
        #intersectpoint = mesh_i.nearestFacetOnRay(driverHead, sightline_dir)
        intersectpoint = mesh_i.nearestFacetOnRay(driverHead, [0,0,0])
        #print(intersectpoint)
        #print(sightline_dir)
        my_create_line(driverHead, sightline_dir, f"line_{i}", (255, 0, 0))
    else:
        my_create_line(driverHead, sightline_dir, f"line_{i}")
        print(mesh_i.nearestFacetOnRay(driverHead, sightline_dir))

    