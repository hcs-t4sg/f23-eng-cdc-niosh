import FreeCAD as App
import FreeCADGui as Gui

obj_name = "Body001"
# get the 3D model document
doc = App.ActiveDocument   
# get the visual representation model document
gui_doc = Gui.ActiveDocument

print(doc)
obj = doc.getObject(obj_name)
print(obj)