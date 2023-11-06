from sympy import Point3D, Plane, Line3D
import numpy as np
# import FreeCAD as App
# import FreeCADGui as Gui
import sympy as sp

t = sp.symbols('t')

u, v, s = sp.symbols('u, v, s')

a1x, a1y, a1z = -26.551074, 29.194627000000004, 0.0
a12x, a12y, a12z = 45.091893, 29.194627000000004, 0.0
a13x, a13y, a13z = 45.091893, -34.722119000000006, 0.0
p0x, p0y, p0z = -112.944015, -52.98405, 0.0
p01x, p01y, p01z = 47.203128, -43.33413, 0.

eq1 = sp.Eq(a1x + u * a12x + v * a13x - p0x - s * p01x, 0)
eq2 = sp.Eq(a1y + u * a12y + v * a13y - p0y - s * p01y, 0)
eq3 = sp.Eq(a1z + u * a12z + v * a13z - p0y - s * p01y, 0)
ans = sp.solve((eq1, eq2, eq3), (u, v, s))
print(ans)

# a1x, a1y, a1z = 1, 0, 0
# a12x, a12y, a12z = -1, 1, 0
# a13x, a13y, a13z = -1, 0, 1
# p0x, p0y, p0z = 0, 0, 0
# p01x, p01y, p01z = 2, 2, 2

# eq1 = sp.Eq(a1x + u * a12x + v * a13x - p0x - t * p01x, 0)
# eq2 = sp.Eq(a1y + u * a12y + v * a13y - p0y - t * p01y, 0)
# eq3 = sp.Eq(a1z + u * a12z + v * a13z - p0y - t * p01y, 0)
# ans = sp.solve((eq1, eq2, eq3), (u, v, t))
# print(ans)


# # # get the 3D model document
# doc = App.ActiveDocument
# # # get the visual representation model document
# gui_doc = Gui.ActiveDocument


# Check if two points are equal within a given tolerance
# def are_points_equal(point1, point2, tolerance=1e-6):
#     return all(abs(p1 - p2) < tolerance for p1, p2 in zip(point1, point2))​

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

    eq1 = sp.Eq((coeff1 * (line_vertices[0][0] + line_direction[0] * t)) + (coeff2 * (
        line_vertices[0][1] + line_direction[1] * t)) + (coeff3 * (line_vertices[0][2] + line_direction[2] * t)), sum)
    print(eq1)
    ans = sp.solve(eq1, t)
    print("answer", ans)

    x = sp.symbols('x')

    equation = sp.Eq(x**2 - 4.32345324, 0)

    # Solve the equation
    solutions = sp.solve(equation, x)

    # Print the solutions
    print("Solutions:", solutions)

# print("normal vector: ", normal_vector)
# constant = 0
# for i in range(3):
#     constant += normal_vector[i] * plane_vertices[0][i]
#     print(plane_vertices[0][i])

# print(constant)


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


# obj_name = "Body"
# obj = doc.getObject(obj_name)
# rect_vert = get_plane_vertices(obj)
# print("Rectangle vertexes:")
# print(rect_vert)


# line_name = "Sketch"
# line = doc.getObject(line_name)
# line_vert = get_line_vertices(line)
# print("Line vertexes:")
# print(line_vert)

# find_intersection_point(line_vert, rect_vert)


# if find_intersection_point(line_vert, rect_vert):
#     print("The line and the plane intersect.")
# else:
#     print("The line and the plane do not intersect.")

plane_vertices = np.array([
    [-26.551074, 29.194627, 0.0],
    [45.091893, 29.1946270, 0.0],
    [45.091893, -34.7221190, 0.0],
    [-26.551074, -34.7221190, 0.0]
])

# [-26.551074, 29.194627000000004, 0.0],
# [45.091893, 29.194627000000004, 0.0],
# [45.091893, -34.722119000000006, 0.0],
# [-26.551074, -34.722119000000006, 0.0]

line_vertices = np.array([
    [-112.944015, -52.98405, -2],
    [82.760554, -41.767499, 2.]
])

find_intersection_point(line_vertices, plane_vertices)
