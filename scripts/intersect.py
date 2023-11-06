import FreeCAD as App
import FreeCADGui as Gui
import numpy as np

obj_name = "Sketch"
line_name = "Sketch001"
plane_name = "Sketch"

# get the 3D model document
doc = App.ActiveDocument
# get the visual representation model document
gui_doc = Gui.ActiveDocument

obj = doc.getObject(obj_name)
line = doc.getObject(line_name)
plane = doc.getObject(plane_name)


# Check if two points are equal within a given tolerance
# def are_points_equal(point1, point2, tolerance=1e-6):
#     return all(abs(p1 - p2) < tolerance for p1, p2 in zip(point1, point2))


def find_intersection_point(line_vertices, plane_vertices):
    # Convert line to parametric form
    line_direction = line_vertices[0] - line_vertices[1]
    line_parametric(t): return line_start + t * line_direction

    # Find two vectors in the plane
    vector1 = plane_vertices[2] - plane_vertices[1]
    vector2 = plane_vertices[3] - plane_vertices[1]

    # Find the normal vector
    normal_vector = np.cross(vector1, vector2)

    constant = normal_vector[]

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
    #             * normal[i] for i in range(3)) / denominator

    #     # Calculate the intersection point
    #     intersection_point = [line_start[i] + t *
    #                           line_direction[i] for i in range(3)]

    #     return intersection_point

    # return None


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


print("\nvertices of the obj:")
line_vertices = get_line_vetices(line)
print(line_vertices)
print("\nvertices of the obj:")
plane_vertices = get_plane_vertices(obj)
print(plane_vertices)


# Define the vertices of the plane as [x, y, z]
plane_vertices = [
    [0, 0, 0],
    [1, 0, 0],
    [1, 1, 0],
]

# Define the start and end points of the line segment
line_start = [0.5, 0.5, -1]
line_end = [0.5, 0.5, 1]




# # Check if the line and plane intersect
# if find_intersection_point(line_vertices[0], line_vertices[1], plane_vertices):
#     print("The line and the plane intersect.")
# else:
#     print("The line and the plane do not intersect.")
