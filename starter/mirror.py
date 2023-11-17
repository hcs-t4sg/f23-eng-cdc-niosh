import Points


class PointsFeature:
    def __init__(self, obj):
        obj.addProperty("App::PropertyColorList", "Colors",
                        "Points", "Ponts").Colors = []
        obj.Proxy = self

    def execute(self, fp):
        pass


def get_obj_vertices(object):
    vertices = len(object.Shape.Vertexes)
    if vertices != 0:
        obj_vertices = [[0 for i in range(3)] for j in range(vertices)]
        for i in range(vertices):
            obj_vertices[i][0] = object.Shape.Vertexes[i].X
            obj_vertices[i][1] = object.Shape.Vertexes[i].Y
            obj_vertices[i][2] = object.Shape.Vertexes[i].Z
        return obj_vertices
    else:
        return 0


doc = FreeCAD.newDocument()

cube = doc.addObject("Part::Box", "Cube")

cube.Length = 4.0
cube.Width = 4.0
cube.Height = 4.0

def mirror(name, objs):
    obj = doc.addObject("Part::Mirroring", name)
    obj.Source = objs
    doc.recompute()
    return obj


mirrored_cube = mirror("mirrored_obj", cube)
mirrored_cube.Placement = doc.Placement(doc.Vector(0, 0, 0), doc.Rotation(180, 0, 180), FreeCAD.Vector(0, 0, 0))
# do FreeCAD.Rotation(0, 0, 0) or FreeCAD.Rotation(180, 180, 180) to mirror in XY plane
# do FreeCAD.Rotation(0, 0, 180) or FreeCAD.Rotation(180, 180, 0) to mirror in XZ plane
# do FreeCAD.Rotation(0, 180, 0) or FreeCAD.Rotation(180, 0, 180) to mirror in YZ plane





# import FreeCAD as App
# import FreeCADGui as Gui

# obj_name = "Body001"
# doc = App.ActiveDocument
# original_object = doc.getObject("Shape")

# # create the feature
# mirror_feature = doc.getObject(obj_name)

# # set up feature's properties
# mirror_feature.Source=original_object
# mirror_feature.Label="Shape (Mirror #1)"
# mirror_feature.Normal=(0,1,0)
# mirror_feature.Base=(0,0,0)

# # copy colors from original
# mirror_feature.ViewObject.ShapeColor = original_object.ViewObject.ShapeColor
# mirror_feature.ViewObject.LineColor = original_object.ViewObject.LineColor
# mirror_feature.ViewObject.PointColor = original_object.ViewObject.PointColor



