"""
sides_and_shelves.py -- Paul Cobbaut, 2024-05-14
Create a hexagon wall display for small figurines.
3D-printed hexagon, covered by a bought plexiglass panel.
This file ==> Sides and shelves
1. short shelve
2. long shelve
3. side
4. side with hinges
5. hinge leaf to hold plexiglass panel
"""

import FreeCAD
from FreeCAD import Base, Vector
import PartDesign
import Sketcher
import Part
import Mesh
import MeshPart
import math

#Dimensions in mm
common_height = 42.00
common_width  =  6.00
insert_width_shelve  =  1.60 # shelves loosely in hexagon sides MK3 print
insert_width_side    =  2.10 # sides firmly in hexagon corners MK4 print
insert_length = 10.00 # insert in corner or side
ridge_width  = 2
ridge_height = 3

short_length = 207  # short shelve
long_length  = 288  # long shelve

side_length  = 130  # side of hexagon

hinge_length = 20
hinge_outer  = 3.0  # radius
hinge_inner  = 1.1  # radius

hole_mm      = 1.5  # radius

leaf_thickness = 3

# Create document
doc = FreeCAD.newDocument("hexagon sides")

def makebox(label, length, width, height):
  obj        = doc.addObject("Part::Box", label)
  obj.Label  = label
  obj.Length = length
  obj.Width  = width
  obj.Height = height
  return obj

# 1. short shelve --> main part and two insert parts
short_shelve_main  = makebox('short_shelve_main' , short_length , common_width       , common_height)
short_shelve_left  = makebox('short_shelve_left' , insert_length, insert_width_shelve, common_height)
short_shelve_right = makebox('short_shelve_right', insert_length, insert_width_shelve, common_height)
short_shelve_left.Placement  = FreeCAD.Placement(Vector(-insert_length, (common_width - insert_width_shelve)/2, 0),FreeCAD.Rotation(Vector(1,0,0),0))
short_shelve_right.Placement = FreeCAD.Placement(Vector(short_length  , (common_width - insert_width_shelve)/2, 0),FreeCAD.Rotation(Vector(1,0,0),0))
short_shelve_compound        = doc.addObject("Part::Compound","short_shelve_compound")
short_shelve_compound.Links  = [short_shelve_main, short_shelve_left, short_shelve_right,]
#short_shelve_compound.ViewObject.hide()

# 2. long shelve --> main part and two insert parts
long_shelve_main  = makebox('long_shelve_main' , long_length  , common_width  , common_height)
long_shelve_left  = makebox('long_shelve_left' , insert_length, common_width/2, common_height-2)
long_shelve_right = makebox('long_shelve_right', insert_length, common_width/2, common_height-2)
long_shelve_left.Placement  = FreeCAD.Placement(Vector(-insert_length, 0, 0),FreeCAD.Rotation(Vector(1,0,0),0))
long_shelve_right.Placement = FreeCAD.Placement(Vector(long_length   , 0, 0),FreeCAD.Rotation(Vector(1,0,0),0))
long_shelve_compound        = doc.addObject("Part::Compound","long_shelve_compound")
long_shelve_compound.Links  = [long_shelve_main, long_shelve_left, long_shelve_right,]
#long_shelve_compound.ViewObject.hide()

# 3. side --> main part and two smaller insert parts and a ridge on top that holds the plexiglass
side_main  = makebox('side_main' , side_length  , common_width     , common_height    )
side_left  = makebox('side_left' , insert_length, insert_width_side, common_height - 4)
side_right = makebox('side_right', insert_length, insert_width_side, common_height - 4)
side_ridge = makebox('side_ridge', side_length  , ridge_width      , ridge_height     )
side_left.Placement  = FreeCAD.Placement(Vector(-insert_length, (common_width - insert_width_side)/2, 2            ), FreeCAD.Rotation(Vector(1,0,0), 0))
side_right.Placement = FreeCAD.Placement(Vector(side_length   , (common_width - insert_width_side)/2, 2            ), FreeCAD.Rotation(Vector(1,0,0), 0))
side_ridge.Placement = FreeCAD.Placement(Vector(0             , (common_width - ridge_width)/2      , common_height), FreeCAD.Rotation(Vector(1,0,0), 0))
side_compound        = doc.addObject("Part::Compound","side_compound")
side_compound.Links  = [side_main, side_left, side_right,side_ridge]
#side_compound.ViewObject.hide()

# 4. side with hinge --> identical to short side, plus two hinge parts
side_hinge_main  = makebox('side_hinge_main' , side_length  , common_width     , common_height)
side_hinge_left  = makebox('side_hinge_left' , insert_length, insert_width_side, common_height - 4)
side_hinge_right = makebox('side_hinge_right', insert_length, insert_width_side, common_height - 4)
side_hinge_ridg1 = makebox('side_hinge_ridg1', side_length/2 - hinge_length/2 -1 , ridge_width      , ridge_height) ## gap in ridge to open glass!
side_hinge_ridg2 = makebox('side_hinge_ridg2', side_length/2 - hinge_length/2 -1 , ridge_width      , ridge_height)
side_hinge_left.Placement  = FreeCAD.Placement(Vector(-insert_length, (common_width - insert_width_side)/2, 2            ), FreeCAD.Rotation(Vector(1,0,0), 0))
side_hinge_right.Placement = FreeCAD.Placement(Vector(side_length   , (common_width - insert_width_side)/2, 2            ), FreeCAD.Rotation(Vector(1,0,0), 0))
side_hinge_ridg1.Placement = FreeCAD.Placement(Vector(0             , (common_width - ridge_width)/2      , common_height), FreeCAD.Rotation(Vector(1,0,0), 0))
side_hinge_ridg2.Placement = FreeCAD.Placement(Vector(side_length/2 + hinge_length/2 +1 , (common_width - ridge_width)/2      , common_height), FreeCAD.Rotation(Vector(1,0,0), 0))
# these two chamfers allow for wider opening of the plexiglass door
# find ridge edges to chamfer
for i, e in enumerate(side_hinge_ridg1.Shape.Edges): # Going through all edges of the left ridge
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
for i, e in enumerate(side_hinge_ridg2.Shape.Edges): # Going through all edges of the other ridge
  #print("Edgename: Edge" + str(i+1) + " XYZ: " + str(e.Vertexes[0].Point) + str(e.Vertexes[1].Point) )
  if -0.1 < e.Vertexes[0].X - (side_length/2 + hinge_length/2 +1) < 0.1:
    if -0.1 < e.Vertexes[1].X - (side_length/2 + hinge_length/2 +1) < 0.1:
      if -0.1 < e.Vertexes[0].Z - (common_height + ridge_height) < 0.1:
        if -0.1 < e.Vertexes[1].Z - (common_height + ridge_height) < 0.1:
          chamferlist = []
          chamferlist.append((i+1,2.99,2))
          chamfer_ridg2 = doc.addObject("Part::Chamfer","Chamfer_ridg2")
          chamfer_ridg2.Base = side_hinge_ridg2
          chamfer_ridg2.Edges = chamferlist
# left hinge is two tubes; outer and inner
hinge_cyllo = doc.addObject("Part::Cylinder","hinge_cyllo")
hinge_cyllo.Radius = hinge_outer
hinge_cyllo.Height = hinge_length
hinge_cyllo.Placement  = FreeCAD.Placement(Vector(side_length/2 - hinge_length - hinge_length/2 -0.1, -1, common_height + 1),FreeCAD.Rotation(Vector(0,1,0),90))
hinge_cylli = doc.addObject("Part::Cylinder","hinge_cylli")
hinge_cylli.Radius = hinge_inner
hinge_cylli.Height = hinge_length
hinge_cylli.Placement  = FreeCAD.Placement(Vector(side_length/2 - hinge_length - hinge_length/2 -0.1, -1, common_height + 1),FreeCAD.Rotation(Vector(0,1,0),90))
hinge_left = doc.addObject("Part::Cut","hinge_left")
hinge_left.Base = hinge_cyllo
hinge_left.Tool = hinge_cylli
# right hinge is two tubes; outer and inner
hinge_cylro = doc.addObject("Part::Cylinder","hinge_cylro")
hinge_cylro.Radius = hinge_outer
hinge_cylro.Height = hinge_length
hinge_cylro.Placement  = FreeCAD.Placement(Vector(side_length/2 + hinge_length/2 +0.1, -1, common_height + 1),FreeCAD.Rotation(Vector(0,1,0),90))
hinge_cylri = doc.addObject("Part::Cylinder","hinge_cylri")
hinge_cylri.Radius = hinge_inner
hinge_cylri.Height = hinge_length
hinge_cylri.Placement  = FreeCAD.Placement(Vector(side_length/2 + hinge_length/2 +0.1, -1, common_height + 1),FreeCAD.Rotation(Vector(0,1,0),90))
hinge_right = doc.addObject("Part::Cut","hinge_right")
hinge_right.Base = hinge_cylro
hinge_right.Tool = hinge_cylri
# cut middle hinge from main side body, otherwise the leaf-hinge does not fit
hinge_cut = doc.addObject("Part::Cylinder","hinge_cut")
hinge_cut.Radius = hinge_outer + 0.1
hinge_cut.Height = hinge_length + 0.2
hinge_cut.Placement  = FreeCAD.Placement(Vector(side_length/2 - hinge_length/2 -0.1, -1, common_height + 1),FreeCAD.Rotation(Vector(0,1,0),90))
side_main_cut = doc.addObject("Part::Cut","side_main_cut")
side_main_cut.Base = side_hinge_main
side_main_cut.Tool = hinge_cut
# hinge compound
side_hinge_compound        = doc.addObject("Part::Compound","side_hinge_compound")
side_hinge_compound.Links  = [side_main_cut, side_hinge_left, side_hinge_right, chamfer_ridg1, chamfer_ridg2, hinge_right, hinge_left,]
#side_hinge_compound.ViewObject.hide()

# 5. hinge leaf
# middle hinge is two tubes; outer and inner
hinge_cylmo = doc.addObject("Part::Cylinder","hinge_cylmo")
hinge_cylmo.Radius = hinge_outer
hinge_cylmo.Height = hinge_length
hinge_cylmo.Placement  = FreeCAD.Placement(Vector(side_length/2 - hinge_length/2, -1, common_height + 1),FreeCAD.Rotation(Vector(0,1,0),90))
hinge_cylmi = doc.addObject("Part::Cylinder","hinge_cylmi")
hinge_cylmi.Radius = hinge_inner
hinge_cylmi.Height = hinge_length
hinge_cylmi.Placement  = FreeCAD.Placement(Vector(side_length/2 - hinge_length/2, -1, common_height + 1),FreeCAD.Rotation(Vector(0,1,0),90))
hinge_middle = doc.addObject("Part::Cut","hinge_middle")
hinge_middle.Base = hinge_cylmo
hinge_middle.Tool = hinge_cylmi
# hinge leaf is extruded hexagon
hexleaf = doc.addObject("Part::RegularPolygon","hexleaf")
hexleaf.Label='hexleaf'
hexleaf.Polygon=6
hexleaf.Circumradius='20.00 mm'
hexleaf.Placement=App.Placement(Vector(side_length/2, -17, common_height + 3),App.Rotation(App.Vector(0.00,0.00,1.00),0.00))
extleaf = doc.addObject('Part::Extrusion','extleaf')
extleaf.Base = hexleaf
extleaf.LengthFwd = leaf_thickness
extleaf.Solid = True
# remove overlap with side hinges from hexleaf
over_left  = makebox('side_hinge_left' , 7, 4, 1)
over_right = makebox('side_hinge_right', 7, 4, 1)
over_left.Placement  = FreeCAD.Placement(Vector(side_length/2 - hinge_length/2 -7, -3.5, common_height +3), FreeCAD.Rotation(Vector(1,0,0), 0))
over_right.Placement = FreeCAD.Placement(Vector(side_length/2 + hinge_length/2, -3.5, common_height +3), FreeCAD.Rotation(Vector(1,0,0), 0))
# cut the overlaps from the leaf
cutover1 = doc.addObject("Part::Cut","cutover1")
cutover1.Base = extleaf
cutover1.Tool = over_left
cutover2 = doc.addObject("Part::Cut","cutover2")
cutover2.Base = cutover1
cutover2.Tool = over_right
# holes in extleaf (to screw the plexiglass)
hole1 = doc.addObject("Part::Cylinder","hole1")
hole1.Radius = hole_mm
hole1.Height = 10
hole1.Placement  = FreeCAD.Placement(Vector(side_length/2 - hinge_length/2, -17, common_height),FreeCAD.Rotation(Vector(1,0,0),0))
hole2 = doc.addObject("Part::Cylinder","hole2")
hole2.Radius = hole_mm
hole2.Height = 10
hole2.Placement  = FreeCAD.Placement(Vector(side_length/2 + hinge_length/2, -17, common_height),FreeCAD.Rotation(Vector(1,0,0),0))
# cut the holes
cuthole1 = doc.addObject("Part::Cut","cuthole1")
cuthole1.Base = cutover2
cuthole1.Tool = hole1
cuthole2 = doc.addObject("Part::Cut","cuthole2")
cuthole2.Base = cuthole1
cuthole2.Tool = hole2
# leaf compound
leaf_compound        = doc.addObject("Part::Compound","leaf_compound")
leaf_compound.Links  = [cuthole2, hinge_middle,]
#leaf_compound.ViewObject.hide()

doc.recompute()
FreeCADGui.ActiveDocument.ActiveView.fitAll()
