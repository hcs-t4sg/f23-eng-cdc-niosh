import FreeCAD as App
import FreeCADGui as Gui


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


def rayTracing():
    if obj.Shape.isInside(x.Placement.Base, 1.0, True):
        FreeCADGui.getDocument("starter_test").getObject(
            "Body").ShapeColor = (1.0, 0.0, 0.0)
        print("intersecting")
    else:
        FreeCADGui.getDocument("starter_test").getObject(
            "Body").ShapeColor = (0.0, 1.0, 0.0)
        print("not intersecting")
    # FreeCADGui.getDocument("starter_test").getObject("Body").ShapeColor = (204, 204, 204)


def are_points_equal(point1, point2, tolerance=1e-6):
    # Check if two points are equal within a given tolerance
    return all(abs(p1 - p2) < tolerance for p1, p2 in zip(point1, point2))


def find_intersection_point(line_start, line_end, plane_vertices):
    # Calculate the direction vector of the line segment
    line_direction = [end - start for start, end in zip(line_start, line_end)]

    # Calculate the normal vector of the plane
    v1 = [plane_vertices[1][i] - plane_vertices[0][i] for i in range(3)]
    v2 = [plane_vertices[2][i] - plane_vertices[0][i] for i in range(3)]
    normal = [
        v1[1] * v2[2] - v1[2] * v2[1],
        v1[2] * v2[0] - v1[0] * v2[2],
        v1[0] * v2[1] - v1[1] * v2[0]
    ]

    # Calculate the denominator for the parameter t
    denominator = sum(line_direction[i] * normal[i] for i in range(3))

    # Check if the line and plane are not parallel
    if abs(denominator) > 1e-6:
        # Calculate the parameter t for the intersection point
        t = sum((plane_vertices[0][i] - line_start[i])
                * normal[i] for i in range(3)) / denominator

        # Calculate the intersection point
        intersection_point = [line_start[i] + t *
                              line_direction[i] for i in range(3)]

        return intersection_point

    return None


def get_line_vetices(line):
    line_vertices = [[0 for i in range(3)] for j in range(2)]
    for i in range(2):
        line_vertices[i][0] = line.Shape.Vertexes[i].X
        line_vertices[i][1] = line.Shape.Vertexes[i].Y
        line_vertices[i][2] = line.Shape.Vertexes[i].Z
        # print(line.Shape.Vertexes[i].X)
        # print(line.Shape.Vertexes[i].Y)
    return line_vertices


def get_plane_vertices(plane):
    plane_vertices = [[0 for i in range(3)] for j in range(4)]
    for i in range(4):
        plane_vertices[i][0] = plane.Shape.Vertexes[i].X
        plane_vertices[i][1] = plane.Shape.Vertexes[i].Y
        plane_vertices[i][2] = plane.Shape.Vertexes[i].Z
        # print(plane.Shape.Vertexes[i].X)
        # print(plane.Shape.Vertexes[i].Y)
    return plane_vertices


print("\nvertices of the obj:")
line_vertices = get_line_vetices(line)
print(line_vertices)
print("\nvertices of the obj:")
plane_vertices = get_plane_vertices(obj)
print(plane_vertices)


# Find the intersection point of the line segment with the plane
intersection_point = find_intersection_point(
    line_vertices[0], line_vertices[1], plane_vertices)

if intersection_point is not None:
    # Check if the intersection point is within the boundaries of the plane
    min_x = min(vertex[0] for vertex in plane_vertices)
    max_x = max(vertex[0] for vertex in plane_vertices)
    min_y = min(vertex[1] for vertex in plane_vertices)
    max_y = max(vertex[1] for vertex in plane_vertices)

    if (
        min_x <= intersection_point[0] <= max_x and
        min_y <= intersection_point[1] <= max_y
    ):
        print("The line segment intersects the space within the plane.")
    else:
        print("The line segment does not intersect the space within the plane.")
else:
    print("The line segment is parallel to the plane and does not intersect.")
