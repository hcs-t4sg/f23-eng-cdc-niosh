from sympy import Point3D, Plane, Line3D
import numpy as np
# import FreeCAD as App
# import FreeCADGui as Gui
import sympy as sp

t = sp.symbols('t')


def find_intersection_point(line_vertices, plane_vertices):

    # Get direction
    line_direction = line_vertices[1] - line_vertices[0]
    # line_parametric(t): return line_start + t * line_direction

    print("ld:", line_direction)

    # Find two vectors in the plane
    vector1 = plane_vertices[1] - plane_vertices[0]
    vector2 = plane_vertices[2] - plane_vertices[0]

    print("v1:", vector1)
    print("v2:", vector2)

    # Find the normal vector
    normal_vector = np.cross(vector1, vector2)

    t_numerator = np.dot(normal_vector, (plane_vertices[0] - line_vertices[0]))
    t_denominator = np.dot(normal_vector, line_direction)

    if t_denominator == 0:
        if t_numerator == 0:
            return "The line lies in the plane."
        else:
            return "The line is parallel to the plane and does not intersect."

    t = t_numerator / t_denominator

    intersection_point = line_vertices[0] + t * line_direction

    return intersection_point

    # coeff1 = normal_vector[0]
    # coeff2 = normal_vector[1]
    # coeff3 = normal_vector[2]

    # sum = coeff1 * plane_vertices[0][0] + coeff2 * \
    #     plane_vertices[0][1] + coeff3 * plane_vertices[0][2]

    # print(normal_vector)
    # print("sum: ", sum)

    # eq1 = sp.Eq(coeff1 * (line_vertices[0][0] + line_direction[0] * t) + coeff2 * (
    #     line_vertices[0][1] + line_direction[1] * t) + coeff3 * (line_vertices[0][2] + line_direction[2] * t), sum)
    # ans = sp.solve(eq1, t)
    # print("answer", ans)


plane_vertices = np.array([
    [-26.551074, 29.194627000000004, 0.0],
    [45.091893, 29.194627000000004, 0.0],
    [45.091893, -34.722119000000006, 0.0],
    [-26.551074, -34.722119000000006, 0.0]
])

line_vertices = np.array([
    [-112.944015, -52.98405, 0.],
    [82.760554, -41.767499, 0.]
])

# [82.760554, -41.767499, 0.]
# [68.944415, 10.509815, 0.]
# [76.077611, -47.58556, 2.]

print(find_intersection_point(line_vertices, plane_vertices))


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
