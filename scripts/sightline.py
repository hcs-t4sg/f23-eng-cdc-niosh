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

def generateSightLineDirectionsGridded(theta_angles = 30, phi_angles = 30):
    
    vectors = []

    for i in range(0, theta_angles):
        for j in range(0, phi_angles):
            theta = 2 * math.pi * i / theta_angles
            phi = math.pi * j / phi_angles

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

for i, vector in enumerate(generateSightLineDirectionsGridded()):
    my_create_line((0,0,0), vector, f"line_{i}")