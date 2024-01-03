import Points


class PointsFeature:
    def __init__(self, obj):
        obj.addProperty("App::PropertyColorList", "Colors",
                        "Points", "Ponts").Colors = []
        obj.Proxy = self

    def execute(self, fp):
        pass


def get_obj_vertices(object):
    print("hello")
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

vertices = get_obj_vertices(cube)
print(vertices)


a = doc.addObject("Points::FeaturePython", "Points")
PointsFeature(a)
a.ViewObject.Proxy = 0

p = Points.Points()

p.addPoints([FreeCAD.Vector(vertices[i][0], vertices[i][1], vertices[i][2])
            for i in range(len(vertices))])
a.Points = p

c = [(1.0, 0.0, 0.0)] * 100
a.Colors = c
a.ViewObject.DisplayMode = "Color"

doc.removeObject(cube.Name)
