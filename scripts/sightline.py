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
                     math.sin(theta) * math.sin(phi) * line_length, math.cos(phi) * line_length)

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


fov_angle = 90

for i, vector in enumerate(generateSightLineDirections(N=400, fov_angle=fov_angle/2)):
    my_create_line((0, 0, 0), vector, f"line_{i}")


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
                     math.sin(theta) * math.sin(phi) * line_length, math.cos(phi) * line_length)

        # May need further tinkering with positive and negatives to include elevation angle.
        angle = math.degrees(math.acos(direction[2] / line_length))

        # Check if the angle is within the specified field of view
        if direction[2] >= 0:
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


fov_angle = 90

for i, vector in enumerate(generateSightLineDirections(N=400, fov_angle=fov_angle/2, line_length=200)):
    my_create_line((0, 0, -100), vector, f"line_{i}")
