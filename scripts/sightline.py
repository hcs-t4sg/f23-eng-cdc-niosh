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


def generateSightLineDirections(N=200, fov_angle=45, line_length=100):

    vectors = []
    inverseGoldenRatio = (5**0.5 - 1)/2

    for i in range(0, N):
        theta = 2 * math.pi * i * inverseGoldenRatio
        phi = math.acos(1 - 2 * (i+0.5) / N)

        direction = (math.cos(theta) * math.sin(phi) * line_length,
                     math.sin(theta) * math.sin(phi) * line_length,
                     math.cos(phi) * line_length)

        # May need further tinkering with positive and negatives to include elevation angle.
        angle = math.degrees(math.acos(direction[2] / line_length))

        # Check if the angle is within the specified field of view
        if angle <= fov_angle:
            vectors.append((round(direction[0], 6), round(
                direction[1], 6), round(direction[2], 6)))

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


# Function to create a transparent box with a specified midpoint
def create_transparent_box(length, width, height, transparency=80):
    # Calculate the half-lengths in each direction
    half_length = length / 2
    half_width = width / 2
    half_height = 0

    # Create a box object with a specified midpoint
    box = Part.makeBox(length, width, height)
    box.Placement.Base = App.Vector(-half_length, -half_width, -half_height)

    # Create a FreeCAD object to hold the box
    box_object = App.ActiveDocument.addObject(
        "Part::Feature", "TransparentBox")

    # Set the Shape property of the object to the box
    box_object.Shape = box

    # Set the transparency property of the object
    box_object.ViewObject.Transparency = transparency

    # Recompute the document to update the view
    App.ActiveDocument.recompute()


fov_angle = 90

# for i, vector in enumerate(generateSightLineDirections(N=400, fov_angle=fov_angle/2)):
#     my_create_line((0, 0, 0), vector, f"line_{i}")


def intersection_with_box(line_vector, box):
    bbox = box.BoundBox
    print(App.Vector(line_vector))
    line = Part.LineSegment(App.Vector(0, 0, 0), App.Vector(line_vector))
    intersection = bbox.getIntersectionPoint(
        App.Vector(0, 0, 0), App.Vector(line_vector))
    if intersection.x:
        return (intersection.x, intersection.y, intersection.z)
    return None


create_transparent_box(50, 30, 100, transparency=60)
box = App.ActiveDocument.getObject("TransparentBox")

fov_angle = 90
for i, vector in enumerate(generateSightLineDirections(N=400, fov_angle=fov_angle / 2)):
    intersection_point = intersection_with_box(vector, box.Shape)
    if intersection_point:
        my_create_line((0, 0, 0), intersection_point, f"line_{i}")
    else:
        my_create_line((0, 0, 0), vector, f"line_{i}")
