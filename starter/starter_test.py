import Points

class PointsFeature:
    def __init__(self, obj):
        obj.addProperty("App::PropertyColorList","Colors","Points","Ponts").Colors=[]
        obj.Proxy = self

    def execute(self, fp):
        pass

FreeCAD.newDocument()
a=FreeCAD.ActiveDocument.addObject("Points::FeaturePython","Points")
PointsFeature(a)
a.ViewObject.Proxy=0

p=Points.Points()
p.addPoints([App.Vector(i/100,0,0) for i in range(100)])
a.Points=p

c=[(1.0,0.0,0.0)] * 100
a.Colors=c
a.ViewObject.DisplayMode="Color"

for i in range(3):
    print("THIS IS A LOOP ON STEP: " + str(i))
