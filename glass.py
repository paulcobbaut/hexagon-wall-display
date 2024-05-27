"""
glass.py -- Paul Cobbaut, 2024-05-18
2024-05-27
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

# Dimensions in mm
hexa = 6
outer_radius   = 170
corner_radius  =  10
rounder_radius = outer_radius - corner_radius

# labels
DocLabel    = 'Hexagon Glass Panel'
BodyLabel   = 'Glass_Body'
SketchLabel = 'Glass_Sketch'
OuterLabel  = 'Outer_Hexagon'

# functions

def create_arc_from_points(Center, StartPoint, EndPoint):
  #Center = App.Vector(0,0,0)
  #StartPoint = App.Vector(0, 1, 0)
  #EndPoint = App.Vector(0.707, 0.707, 0)   #almost on the arc
  Normal = (StartPoint - Center).cross(EndPoint - Center)
  circ = Part.Circle(Center, Normal, (StartPoint - Center).Length)
  up1 =  circ.parameter(StartPoint) #closest point - 'exact'
  up2 = circ.parameter(EndPoint) # closest point 'approximate'
  arc = Part.Arc(circ, up1, up2)
  #print(f'arc start at {arc.StartPoint} ends at {arc.EndPoint}\n center {arc.centerOfCurvature(up1)}')
  Part.show(arc.toShape())
  print("In: ", StartPoint, " ", EndPoint)
  print("Ui: ", up1, " ", up2)
  return arc



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

#print('center1 =' , center1.X, ' ', center1.Y, ' ', center1.Z)
#print('center2 =' , center2.X, ' ', center2.Y, ' ', center2.Z)
#print('center3 =' , center3.X, ' ', center3.Y, ' ', center3.Z)
#print('center4 =' , center4.X, ' ', center4.Y, ' ', center4.Z)
#print('center5 =' , center5.X, ' ', center5.Y, ' ', center5.Z)
#print('center6 =' , center6.X, ' ', center6.Y, ' ', center6.Z)

# axis
axis = Vector(0,0,1)


# little circles
startangle = math.radians(-45)
endangle   = math.radians(45)
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



'''
# construction: the outer limit of the hexagon
outer = RegularPolygon.makeRegularPolygon(sketch,hexa,Vector(0,0,0),Vector(outer_radius,0,0),True)


doc.recompute()

# create small circles at the six vertexes of the rounder
for i, v in enumerate(doc.getObject(SketchLabel).Shape.Edges):
    #print("i:", i+1, " v:", v)
    X = v.Vertexes[0].X
    Y = v.Vertexes[0].Y
    Z = v.Vertexes[0].Z
    #print("Edge" + str(i+1) +" x = " + str(round(X,2)) + " y = " + str(round(Y,2)) + " z = " + str(round(Z,2)))
    centerpoint = Vector(X,Y,0)
    radius = corner_radius
    direction = Vector(0,0,1)
    sketch.addGeometry(Part.Circle(centerpoint, direction, radius),False)


  #print("Edgename: Edge" + str(i+1) + " XYZ: " + str(e.Vertexes[0].Point) + str(e.Vertexes[1].Point) )
  if -0.1 < e.Vertexes[0].X - (side_length/2 - hinge_length/2 -1) < 0.1:
    if -0.1 < e.Vertexes[1].X - (side_length/2 - hinge_length/2 -1) < 0.1:
      if -0.1 < e.Vertexes[0].Z - (common_height + ridge_height) < 0.1:
        if -0.1 < e.Vertexes[1].Z - (common_height + ridge_height) < 0.1:
          chamferlist = []
          chamferlist.append((i+1,2.99,2))
          chamfer_ridg1 = doc.addObject("Part::Chamfer","Chamfer_ridg1")
          chamfer_ridg1.Base = side_hinge_ridg1
          chamfer_ridg1.Edges = chamferlist
'''




doc.recompute()
FreeCADGui.ActiveDocument.ActiveView.fitAll()
