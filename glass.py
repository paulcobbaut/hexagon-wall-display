"""
glass.py -- Paul Cobbaut, 2024-05-18
2024-05-27
2024-06-02
Create a hexagon wall display for small figurines.
3D-printed hexagon, covered by a bought plexiglass panel.
This file ==> svg and dxf for plexiglass panel
"""

import FreeCAD
from FreeCAD import Base, Vector
import PartDesign
import Sketcher
from ProfileLib import RegularPolygon 
import math
import importSVG

# Dimensions in mm
hexa = 6
outer_radius   = 166
corner_radius  =  20
rounder_radius = outer_radius - corner_radius
topcut         =   2
hingecut       =  10
hingewidth     =  64

# labels
DocLabel    = 'Hexagon Glass Panel'
BodyLabel   = 'Glass_Body'
SketchLabel = 'Glass_Sketch'
OuterLabel  = 'Outer_Hexagon'

# start
doc    = FreeCAD.newDocument(DocLabel)
body   = doc.addObject("PartDesign::Body", BodyLabel)
sketch = doc.getObject(BodyLabel).newObject("Sketcher::SketchObject", SketchLabel)
sketch.Placement = FreeCAD.Placement(Vector(0,0,0),FreeCAD.Rotation(Vector(1,0,0),0))

# calculate the points needed
# six rounded corners = six center points + twelve

# rounded corners
# calculate the six centers of the arcs that serve as corners
center = Vector(0,0,0)
rounder = RegularPolygon.makeRegularPolygon(sketch, hexa, center, Vector(rounder_radius,0,0),False)

doc.recompute()

center1 = sketch.Shape.Vertex1.Point
center2 = sketch.Shape.Vertex2.Point
center3 = sketch.Shape.Vertex3.Point
center4 = sketch.Shape.Vertex4.Point
center5 = sketch.Shape.Vertex5.Point
center6 = sketch.Shape.Vertex6.Point

# axis
axis = Vector(0,0,1)

# little circles
startangle = math.radians(-30)
endangle   = math.radians(30)
sketch.addGeometry(Part.ArcOfCircle(Part.Circle(center1, axis, corner_radius), startangle, endangle),False)
startangle = startangle + math.radians(60)
endangle   = endangle   + math.radians(60)
sketch.addGeometry(Part.ArcOfCircle(Part.Circle(center2, axis, corner_radius), startangle, endangle),False)
startangle = startangle + math.radians(60)
endangle   = endangle   + math.radians(60)
sketch.addGeometry(Part.ArcOfCircle(Part.Circle(center3, axis, corner_radius), startangle, endangle),False)
startangle = startangle + math.radians(60)
endangle   = endangle   + math.radians(60)
sketch.addGeometry(Part.ArcOfCircle(Part.Circle(center4, axis, corner_radius), startangle, endangle),False)
startangle = startangle + math.radians(60)
endangle   = endangle   + math.radians(60)
sketch.addGeometry(Part.ArcOfCircle(Part.Circle(center5, axis, corner_radius), startangle, endangle),False)
startangle = startangle + math.radians(60)
endangle   = endangle   + math.radians(60)
sketch.addGeometry(Part.ArcOfCircle(Part.Circle(center6, axis, corner_radius), startangle, endangle),False)

doc.recompute()


e = sketch.Shape.Edges[6]
#startpoint6 = e.Vertexes[0].Point
endpoint1   = e.Vertexes[1].Point
e = sketch.Shape.Edges[7]
startpoint1 = e.Vertexes[0].Point
endpoint2   = e.Vertexes[1].Point
e = sketch.Shape.Edges[8]
startpoint2 = e.Vertexes[0].Point
endpoint3   = e.Vertexes[1].Point
e = sketch.Shape.Edges[9]
startpoint3 = e.Vertexes[0].Point
endpoint4   = e.Vertexes[1].Point
e = sketch.Shape.Edges[10]
startpoint4 = e.Vertexes[0].Point
endpoint5   = e.Vertexes[1].Point
e = sketch.Shape.Edges[11]
startpoint5 = e.Vertexes[0].Point
endpoint6   = e.Vertexes[1].Point
e = sketch.Shape.Edges[6]
startpoint6 = e.Vertexes[0].Point
#endpoint1   = e.Vertexes[1].Point


line1 = sketch.addGeometry(Part.LineSegment(startpoint1, endpoint1),False)
line2 = sketch.addGeometry(Part.LineSegment(startpoint2, endpoint2),False)
line3 = sketch.addGeometry(Part.LineSegment(startpoint3, endpoint3),False)
line4 = sketch.addGeometry(Part.LineSegment(startpoint4, endpoint4),False)
line5 = sketch.addGeometry(Part.LineSegment(startpoint5, endpoint5),False)
line6 = sketch.addGeometry(Part.LineSegment(startpoint6, endpoint6),False)

#doc.removeObject('rounder')
sketch.delGeometries([0])
sketch.delGeometries([0])
sketch.delGeometries([0])
sketch.delGeometries([0])
sketch.delGeometries([0])
sketch.delGeometries([0])
sketch.delGeometries([0])

doc.recompute()

#### line to cut off from the top, so the lid can open and close
# first find highest point (y value)

highest_y = 0
for i, e in enumerate(sketch.Shape.Edges): # Going through all edges of the other ridge
  #print("Edgename: Edge" + str(i+1) + " XYZ: " + str(e.Vertexes[0].Point) + str(e.Vertexes[1].Point) )
  if e.Vertexes[0].Y > highest_y:
      highest_y = e.Vertexes[0].Y
      #print(highest_y)

# draw line just below highest point
topcutstart = Vector(- outer_radius * 1.5, highest_y - topcut, 0)
topcutend   = Vector(+ outer_radius * 1.5, highest_y - topcut, 0)
topcutline  = sketch.addGeometry(Part.LineSegment(topcutstart, topcutend),False)


doc.recompute()

objs = []
objs.append(doc.getObject("Glass_Sketch"))
importSVG.export(objs, u"/home/paul/FreeCAD models/smurf/Hexagon Glass sketch.svg")



doc.recompute()
FreeCADGui.ActiveDocument.ActiveView.fitAll()
