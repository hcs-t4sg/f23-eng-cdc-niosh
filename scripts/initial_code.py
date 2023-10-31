import FreeCAD as App
import FreeCADGui as Gui

# get the 3D model document
doc = App.ActiveDocument   
# get the visual representation model document
gui_doc = Gui.ActiveDocument

obj = doc.getObject("Fusion001")

# Example of Vertex
print(obj.Shape.Vertexes[0].X, obj.Shape.Vertexes[0].Y, obj.Shape.Vertexes[0].Z)

# Example of Face
print(obj.Shape.Faces[0].Area)

# Load Box and Print if They're Touching
intersectingBox = doc.getObject("Box002")
print(len(obj.Shape.common(intersectingBox.Shape.Shells).Vertexes)!=0)

outsideBox = doc.getObject("Box003")
print(len(obj.Shape.common(outsideBox.Shape.Shells).Vertexes)!=0)
