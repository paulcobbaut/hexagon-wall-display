"""
glass.py -- Paul Cobbaut
2024-05-18
2024-05-27
2024-06-02
2024-06-12
Create a hexagon wall display for small figurines.
3D-printed hexagon, covered by a bought plexiglass panel.
This file ==> create svg and dxf for plexiglass panel
"""

import FreeCAD
from FreeCAD import Base, Vector
import PartDesign
import Sketcher
from ProfileLib import RegularPolygon 
import math
import importSVG
import importDXF

# Dimensions in mm
hexa           =   6
outer_radius   = 166
corner_radius  =  20
rounder_radius = outer_radius - corner_radius
hingecut       =  10
hingewidth     =  64
holeradius     =   1.50
hingeholedist  =  20

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

# draw the six arcs of the little circles, the top two only half
startangle = math.radians(-30)
endangle   = math.radians(30)
sketch.addGeometry(Part.ArcOfCircle(Part.Circle(center1, axis, corner_radius), startangle, endangle),False)
startangle = startangle + math.radians(60)
endangle   = endangle   + math.radians(60) - math.radians(30)  # top cut, top side is lower to use lid
sketch.addGeometry(Part.ArcOfCircle(Part.Circle(center2, axis, corner_radius), startangle, endangle),False)
startangle = startangle + math.radians(60) + math.radians(30)  # top cut, top side is lower to use lid
endangle   = endangle   + math.radians(60) + math.radians(30)  # top cut, top side is lower to use lid
sketch.addGeometry(Part.ArcOfCircle(Part.Circle(center3, axis, corner_radius), startangle, endangle),False)
startangle = startangle + math.radians(60) - math.radians(30)  # top cut, top side is lower to use lid
endangle   = endangle   + math.radians(60) 
sketch.addGeometry(Part.ArcOfCircle(Part.Circle(center4, axis, corner_radius), startangle, endangle),False)
startangle = startangle + math.radians(60)
endangle   = endangle   + math.radians(60)
sketch.addGeometry(Part.ArcOfCircle(Part.Circle(center5, axis, corner_radius), startangle, endangle),False)
startangle = startangle + math.radians(60)
endangle   = endangle   + math.radians(60)
sketch.addGeometry(Part.ArcOfCircle(Part.Circle(center6, axis, corner_radius), startangle, endangle),False)
doc.recompute()

# calculate the points for the top gap for the hinge
# edge8 is the top edge; hopefully :)
x = hingewidth/2  # half length of hinge cutout on either side of Y-axis
rightpoint     = Vector(x , sketch.Shape.Edges[8].Vertexes[0].Y   , 0)
rightpointdown = Vector(x , sketch.Shape.Edges[8].Vertexes[0].Y -5, 0)
leftpointdown  = Vector(-x, sketch.Shape.Edges[8].Vertexes[0].Y -5, 0)
leftpoint      = Vector(-x, sketch.Shape.Edges[8].Vertexes[0].Y   , 0)

# calculate start and endpoints of straight lines between arcs
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

# draw the line pieces between the end points of the arcs
line1 = sketch.addGeometry(Part.LineSegment(startpoint1, endpoint1),False)
line2a = sketch.addGeometry(Part.LineSegment(startpoint2, leftpoint),False)
lineh1 = sketch.addGeometry(Part.LineSegment(rightpoint    , rightpointdown), False) # hinge
lineh2 = sketch.addGeometry(Part.LineSegment(rightpointdown, leftpointdown ), False)
lineh3 = sketch.addGeometry(Part.LineSegment(leftpointdown , leftpoint     ), False)
line2b = sketch.addGeometry(Part.LineSegment(rightpoint, endpoint2),False)
line3 = sketch.addGeometry(Part.LineSegment(startpoint3, endpoint3),False)
line4 = sketch.addGeometry(Part.LineSegment(startpoint4, endpoint4),False)
line5 = sketch.addGeometry(Part.LineSegment(startpoint5, endpoint5),False)
line6 = sketch.addGeometry(Part.LineSegment(startpoint6, endpoint6),False)

# remove obsolete lines
sketch.delGeometries([0])
sketch.delGeometries([0])
sketch.delGeometries([0])
sketch.delGeometries([0])
sketch.delGeometries([0])
sketch.delGeometries([0])
sketch.delGeometries([0])
doc.recompute()

# draw holes, two at the top, one at the bottom
hole1center = Vector( hingeholedist/2,  leftpoint.y - 10, 0) # leftpoint.y == rightpoint.y
hole2center = Vector(-hingeholedist/2,  leftpoint.y - 10, 0)
hole3center = Vector(0               , -leftpoint.y + 10, 0)
sketch.addGeometry(Part.Circle(hole1center,axis,holeradius),False)
sketch.addGeometry(Part.Circle(hole2center,axis,holeradius),False)
sketch.addGeometry(Part.Circle(hole3center,axis,holeradius),False)
doc.recompute()

# export SVG and DXF
objs = []
objs.append(doc.getObject("Glass_Sketch"))
importSVG.export(objs, u"/home/paul/FreeCAD models/smurf/Hexagon Glass sketch.svg")
importDXF.export(objs, u"/home/paul/FreeCAD models/smurf/Hexagon Glass sketch.dxf")


FreeCADGui.ActiveDocument.ActiveView.fitAll()
