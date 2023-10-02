import FreeCAD as App
import FreeCADGui as Gui

obj_name = "Body"
obj2_name = "Box"
# get the 3D model document
doc = App.ActiveDocument   
# get the visual representation model document
gui_doc = Gui.ActiveDocument

print(doc)
obj = doc.getObject(obj_name)
print(obj)

box = doc.getObject(obj2_name)
print(box)

# v = obj.Shape.Vertexes
# v.y
# v.x

# box.Placement.
# box.Shape.BoundBox
# box.Shape.isInside (checks if a point is inside or outside a shape)
# box.Shape.isInside(box.placement.Base,1.0,True) (checks if a point is inside or outside a shape)

# space = box.Shape.BoundBox
# print(space)

# if (obj.Shape.isInside(box.Placement.Base,1.0,True)):
#     print("The box is touching the charger")

common_shape = obj.Shape.common(box.Shape)

if (common_shape.Volume > 0):
    print("The box is touching the charger.")
    obj.ViewObject.Transparency = 70
    gui_doc.getObject('Body').ShapeColor = (1.00,0.00,0.00)

else:
    print("The box is not touching the charger.")
    obj.ViewObject.Transparency = 70
    gui_doc.getObject('Body').ShapeColor = (0.00,1.00,0.00)

# Getting all the vertices in the main object
for vertex in obj.Shape.Vertexes:
    x = vertex.X
    y = vertex.Y
    z = vertex.Z
#    print(f"Vertex Coordinates: ({x}, {y}, {z})")