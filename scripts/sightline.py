import math
import FreeCAD as App
import Part
import pandas as pd

sensors = pd.DataFrame({'Name': ['Sentry ST87 Series'], 'Angle': [150], 'Width':[3], 'Height':[3], 'Range':[10]})

'''
generateSightLines():
Parameters: 
- N, the number of sightlines
- fov_angle, angle of sensor (cone shape)
- line_length, length of the line generated
Returns: a list of n sightlines, each a vector from the given origin

Sources: 
- https://arxiv.org/pdf/0912.4540.pdf
- https://extremelearning.com.au/how-to-evenly-distribute-points-on-a-sphere-more-effectively-than-the-canonical-fibonacci-lattice/
'''




def generateSightLineDirections(N=200, fov_angle=45, line_length=100, origin=(0, 0, 0)):
    vectors = []
    inverseGoldenRatio = (5**0.5 - 1) / 2

    for i in range(N):
        theta = 2 * math.pi * i * inverseGoldenRatio
        phi = math.acos(1 - 2 * (i + 0.5) / N)

        direction = (math.cos(theta) * math.sin(phi) * line_length,
                     math.sin(theta) * math.sin(phi) * line_length,
                     math.cos(phi) * line_length)

        # Shift direction by origin
        shifted_direction = (origin[0] + direction[0],
                             origin[1] + direction[1],
                             origin[2] + direction[2])

        angle = math.degrees(math.acos(direction[2] / line_length))

        if angle <= fov_angle:
            # print(shifted_direction)
            vectors.append((round(shifted_direction[0], 6),
                            round(shifted_direction[1], 6),
                            round(shifted_direction[2], 6)))

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
def create_transparent_box(length, width, height, midpoint, number, transparency=80):
    half_length = length / 2
    half_width = width / 2

    box = Part.makeBox(length, width, height)
    box.Placement.Base = App.Vector(midpoint[0] - half_length,
                                    midpoint[1] - half_width,
                                    midpoint[2])

    # Create a FreeCAD object to hold the box
    box_object = App.ActiveDocument.addObject(
        "Part::Feature", f"TransparentBox{number}")

    # Set the Shape property of the object to the box
    box_object.Shape = box

    # Set the transparency property of the object
    box_object.ViewObject.Transparency = transparency

    # Recompute the document to update the view
    App.ActiveDocument.recompute()

    box_object.recompute()


def intersection_with_box(line_vector, box, origin):
    bbox = box.BoundBox
    line = Part.LineSegment(App.Vector(origin), App.Vector(line_vector))
    intersection = bbox.getIntersectionPoint(
        App.Vector(origin), App.Vector(line_vector))
    if intersection.x:
        return (intersection.x, intersection.y, intersection.z)
    return None


# Set the midpoint of the box
# origin = (-100, 0, 0)
# create_transparent_box(40, 40, 40, midpoint=origin, transparency=60)
# box = App.ActiveDocument.getObject("TransparentBox001")

fov_angle = 90
# for i, vector in enumerate(generateSightLineDirections(N=400, fov_angle=fov_angle / 2, line_length=100, origin=origin)):
#     print(vector)
#     intersection_point = intersection_with_box(vector, box.Shape, origin)
#     if intersection_point:
#         my_create_line(origin, intersection_point, f"line_{i}")
#     else:
#         my_create_line(origin, vector, f"line_{i}")


def create_multiple(origins, sensor_specs):
    # App.Console.PrintMessage(sensor_specs)
    # App.Console.PrintMessage(int(sensor_specs.iloc[type_of_sensor, 0]))
    for i in range(len(origins)):
        create_transparent_box((sensor_specs.loc['Height'])*100, (sensor_specs.loc['Width'])*100, (sensor_specs.loc['Range'])*100, origins[i], i, transparency=60)
        box = App.ActiveDocument.getObject(f"TransparentBox{i}")
        for j, vector in enumerate(generateSightLineDirections(N=400, fov_angle=sensor_specs.loc['Angle'] / 2, line_length=1000, origin=origins[i])):
            intersection_point = intersection_with_box(
                vector, box.Shape, origins[i])
            if intersection_point:
                my_create_line(
                    origins[i], intersection_point, f"set_{i}_line_{j}")
            else:
                my_create_line(origins[i], vector, f"set_{i}_line_{j}")


number_of_sensors = int(input("How many sensors do you want to add? \n"))
App.Console.PrintMessage("Sensor options: \n")
for index, row in sensors.iterrows():
    App.Console.PrintMessage(f"({index}) {row['Name']} \n")   
type_of_sensor = int(input("Choose a sensor: "))

App.Console.PrintMessage(f"{sensors.at[type_of_sensor, 'Name']} \n")
origins = []
for i in range(number_of_sensors):
    x_coor = int(input(f"sensor {i} x-coor: "))
    App.Console.PrintMessage(f"{x_coor}\n")
    y_coor = int(input(f"sensor {i} y-coor: "))
    App.Console.PrintMessage(f"{y_coor}\n")
    z_coor = int(input(f"sensor {i} z-coor: "))
    App.Console.PrintMessage(f"{z_coor}\n")
    origin = (x_coor, y_coor, z_coor)
    origins.append(origin)

create_multiple(origins, sensors.iloc[type_of_sensor, :])

