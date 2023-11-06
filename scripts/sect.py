# import FreeCAD as App
# import FreeCADGui as Gui


# obj_name = "Sketch"
# line_name = "Sketch001"
# plane_name = "Sketch"

# # get the 3D model document
# doc = App.ActiveDocument
# # get the visual representation model document
# gui_doc = Gui.ActiveDocument

# obj = doc.getObject(obj_name)
# line = doc.getObject(line_name)
# plane = doc.getObject(plane_name)


import numpy as np
from sympy import Point3D, Plane, Line3D
import sympy as sp


def find_intersection_point(line_vertices, plane_vertices):

    t, tt = sp.symbols('t tt')

    line_start = np.array(line_vertices[0])
    line_end = np.array(line_vertices[1])
    line_direction = line_end - line_start

    line_x = line_start[0]*t + line_direction[0]
    line_y = line_start[1]*t + line_direction[1]
    line_z = line_start[2]*t + line_direction[2]

    print(line_x)
    print(line_y)
    print(line_z)

    # Find two vectors in the plane
    vector1 = np.subtract(plane_vertices[1], plane_vertices[0])
    vector2 = np.subtract(plane_vertices[2], plane_vertices[0])

    # Find the normal vector
    normal_vector = np.cross(vector1, vector2)
    print("normal vector: ", normal_vector)

    # normal_vector[0]*(line_x-plane_vertices)

    # constant = 0
    # for i in range(3):
    #     constant += normal_vector[i] * plane_vertices[0][i]
    #     print(plane_vertices[0][i])

    # print(constant)

    # Check if the line intersects the plane
    # denominator = np.dot(normal_vector, line_direction)
    # if denominator == 0:
    #     if np.dot(normal_vector, line_start) == constant:
    #         print("The line lies on the plane.")
    #     else:
    #         print("The line is parallel to the plane and does not intersect.")
    # else:
    #     t = (constant - np.dot(normal_vector, line_start)) / denominator
    #     intersection_point = line_start + t * line_direction
    #     print("The line intersects the plane at the point:", intersection_point)


# Example usage
line_vertices = [(-112.944015,  -52.98405,     0.),
                 (119.823814,  -48.912223,    0.)]
plane_vertices = [(-26.551074, 29.194627000000004, 0.0),
                  (45.091893, 29.194627000000004, 0.0),
                  (45.091893, -34.722119000000006, 0.0),
                  (-26.551074, -34.722119000000006, 0.0)]
find_intersection_point(line_vertices, plane_vertices)


def get_line_vetices(line):
    line_vertices = [[0 for i in range(3)] for j in range(2)]
    line_vertices = np.empty((2, 3))
    for i in range(2):
        line_vertices[i][0] = line.Shape.Vertexes[i].X
        line_vertices[i][1] = line.Shape.Vertexes[i].Y
        line_vertices[i][2] = line.Shape.Vertexes[i].Z
    return line_vertices


def get_plane_vertices(plane):
    plane_vertices = [[0 for i in range(3)] for j in range(4)]
    plane_vertices = np.empty((4, 3))
    for i in range(4):
        plane_vertices[i][0] = plane.Shape.Vertexes[i].X
        plane_vertices[i][1] = plane.Shape.Vertexes[i].Y
        plane_vertices[i][2] = plane.Shape.Vertexes[i].Z
    return plane_vertices


# print("\nvertices of the obj:")
# line_vertices = get_line_vetices(line)
# print(line_vertices)
# print("\nvertices of the obj:")
# plane_vertices = get_plane_vertices(obj)
# print(plane_vertices)


# Define the vertices of the plane as [x, y, z]
plane_vertices = [
    [-26.551074, 29.194627000000004, 0.0],
    [45.091893, 29.194627000000004, 0.0],
    [45.091893, -34.722119000000006, 0.0],
    [-26.551074, -34.722119000000006, 0.0]
]

plane_vertices = np.array(plane_vertices)

# Define the start and end points of the line segment
line_vertices = [
    [-112.944015, -52.98405, 0.0],
    [136.40151699999996, 39.730347999999985, 0.0]
]

line_vertices = np.array(line_vertices)

find_intersection_point(line_vertices, plane_vertices)


# plane Points
a1 = Point3D(-26.551074, 29.194627000000004, 0.0)
a2 = Point3D(45.091893, 29.194627000000004, 0.0)
a3 = Point3D(45.091893, -34.722119000000006, 0.0)
# line Points
p0 = Point3D(-112.944015, -52.98405, 0.0)  # point in line
line_direction = np.subtract(line_vertices[0], line_vertices[1])

print(line_direction)

# create plane and line
plane = Plane(a1, a2, a3)

line = Line3D(p0, direction_ratio=line_direction)


print(f"plane equation: {plane.equation()}")
print(f"line equation: {line.equation()}")

# find intersection:
# Find intersection
intr = plane.intersection(line)
if intr:
    intersection = intr[0]
    print("It intersects")
    print(f"Intersection: {intersection}")
else:
    print("No intersection found.")

    # t = np.dot(plane_point - line_start, plane_normal) / np.dot(line_direction, plane_normal)

    # if 0 <= t <= 1:
    #     intersection_point = line_parametric(t)
    #     if np.all(intersection_point == plane_point):
    #         return "The line lies on the plane."
    #     else:
    #         return "The line intersects the plane."
    # else:
    #     return "The line does not intersect the plane."

    # # Calculate the direction vector of the line segment
    # line_direction = [end - start for start, end in zip(line_start, line_end)]

    # # Calculate the normal vector of the plane
    # v1 = [plane_vertices[1][i] - plane_vertices[0][i] for i in range(3)]
    # v2 = [plane_vertices[2][i] - plane_vertices[0][i] for i in range(3)]
    # normal = [
    #     v1[1] * v2[2] - v1[2] * v2[1],
    #     v1[2] * v2[0] - v1[0] * v2[2],
    #     v1[0] * v2[1] - v1[1] * v2[0]
    # ]

    # # Calculate the denominator for the parameter t
    # denominator = sum(line_direction[i] * normal[i] for i in range(3))

    # # Check if the line and plane are not parallel
    # if abs(denominator) > 1e-6:
    #     # Calculate the parameter t for the intersection point
    #     t = sum((plane_vertices[0][i] - line_start[i])
    #             normal[i] for i in range(3)) / denominator

    #     # Calculate the intersection point
    #     intersection_point = [line_start[i] + t *
    #                           line_direction[i] for i in range(3)]

    #     return intersection_point

    # return None


# # plane Points
# a1 = Point3D(-5, 15, -5)
# a2 = Point3D(5, 15, -5)
# a3 = Point3D(5, 15, 5)
# # line Points
# p0 = Point3D(0, 3, 1)  # point in line
# v0 = [0, 1, 1]  # line direction as vector

# # create plane and line
# plane = Plane(a1, a2, a3)

# line = Line3D(p0, direction_ratio=v0)


# print(f"plane equation: {plane.equation()}")
# print(f"line equation: {line.equation()}")

# # find intersection:

# intr = plane.intersection(line)

# intersection = np.array(intr[0], dtype=float)
# print(f"intersection: {intersection}")


# Check if two points are equal within a given tolerance
# def are_points_equal(point1, point2, tolerance=1e-6):
#     return all(abs(p1 - p2) < tolerance for p1, p2 in zip(point1, point2))


# intr = plane.intersection(line)


# intersection = np.array(intr[0], dtype=float)
# print(f"intersection: {intersection}")

# # Check if the line and plane intersect
# if find_intersection_point(line_vertices[0], line_vertices[1], plane_vertices):
#     print("The line and the plane intersect.")
# else:
#     print("The line and the plane do not intersect.")
