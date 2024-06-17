"""
sides_and_shelves.py -- Paul Cobbaut
2024-05-14
2024-06-15 no longer going for inserts, instead gravity will do it
Create a hexagon wall display for small figurines.
3D-printed hexagon, covered by a bought plexiglass panel.
This file ==> Sides and shelves
1. short shelve
2. long shelve
3. side
4. side with hinges
5. hinge leaf to hold plexiglass panel
6. side with quartershelve
7. side with double quartershelve
"""

import FreeCAD
from FreeCAD import Base, Vector
import PartDesign
import Sketcher
import Part
import Mesh
import MeshPart
import math

# math
cos30 = 0.866 # approximate cosine of 30 degree angle
sin30 = 0.500 # exact

# dimensions are in mm

# sides and shelves
common_height = 42
common_width  =  6

# shelves
short_length = 211 # short shelve (was 207 with previous)
long_length  = 288 # long shelve
cross_length =  10 # where shelves rest on
cross_cut    =   2 # no overlap at the back
cross_height = common_height - cross_cut
cross_width  = common_width/2

# sides
side_length   = 130  # side of hexagon
insert_length =  10
insert_gap    =   2
insert_height = common_height - (2*insert_gap)
insert_width  =   2.10 # sides firmly in hexagon corners MK4 print
insert_Y      = (common_width - insert_width)/2
ridge_width   =   2
ridge_Y       = (common_width - ridge_width)/2
ridge_height  =   3

# holders
holder_length = 20
groove_length = 10

# hinge
hinge_length = 20
hinge_outer  = 3.0  # radius
hinge_inner  = 1.1  # radius

# leaf
leaf_thickness = 3
hole_mm      = 1.5  # radius

# Create document
doc = FreeCAD.newDocument("hexagon sides")

def makebox(label, length, width, height):
  obj        = doc.addObject("Part::Box", label)
  obj.Label  = label
  obj.Length = length
  obj.Width  = width
  obj.Height = height
  return obj



# 1. short shelve --> main part and two cross parts
short_shelve_main  = makebox('short_shelve_main' , short_length, common_width, common_height)
short_shelve_left  = makebox('short_shelve_left' , cross_length, cross_width , cross_height )
short_shelve_right = makebox('short_shelve_right', cross_length, cross_width , cross_height )
short_shelve_left.Placement  = FreeCAD.Placement(Vector(-cross_length, 0, 0),FreeCAD.Rotation(Vector(1,0,0),0))
short_shelve_right.Placement = FreeCAD.Placement(Vector(short_length , 0, 0),FreeCAD.Rotation(Vector(1,0,0),0))
short_shelve_compound        = doc.addObject("Part::Compound","short_shelve_compound")
short_shelve_compound.Links  = [short_shelve_main, short_shelve_left, short_shelve_right,]
short_shelve_compound.ViewObject.hide()

# 2. long shelve --> main part and two cross parts
long_shelve_main  = makebox('long_shelve_main' , long_length , common_width, common_height)
long_shelve_left  = makebox('long_shelve_left' , cross_length, cross_width , cross_height )
long_shelve_right = makebox('long_shelve_right', cross_length, cross_width , cross_height )
long_shelve_left.Placement  = FreeCAD.Placement(Vector(-cross_length, 0, 0),FreeCAD.Rotation(Vector(1,0,0),0))
long_shelve_right.Placement = FreeCAD.Placement(Vector(long_length  , 0, 0),FreeCAD.Rotation(Vector(1,0,0),0))
long_shelve_compound        = doc.addObject("Part::Compound","long_shelve_compound")
long_shelve_compound.Links  = [long_shelve_main, long_shelve_left, long_shelve_right,]
long_shelve_compound.ViewObject.hide()

# 3. side --> main part and two smaller insert parts and a ridge on top that holds the plexiglass
side_main  = makebox('side_main' , side_length  , common_width, common_height)
side_left  = makebox('side_left' , insert_length, insert_width, insert_height)
side_right = makebox('side_right', insert_length, insert_width, insert_height)
side_ridge = makebox('side_ridge', side_length  , ridge_width , ridge_height )
side_left.Placement  = FreeCAD.Placement(Vector(-insert_length, insert_Y, 2            ), FreeCAD.Rotation(Vector(1,0,0), 0))
side_right.Placement = FreeCAD.Placement(Vector(side_length   , insert_Y, 2            ), FreeCAD.Rotation(Vector(1,0,0), 0))
side_ridge.Placement = FreeCAD.Placement(Vector(0             , ridge_Y , common_height), FreeCAD.Rotation(Vector(1,0,0), 0))
side_compound        = doc.addObject("Part::Compound","side_compound")
side_compound.Links  = [side_main, side_left, side_right,side_ridge]
side_compound.ViewObject.hide()


# 6. side --> normal side with half-extension for quartershelve
sideq_main  = makebox('sideq_main' , side_length  , common_width, common_height)
sideq_left  = makebox('sideq_left' , insert_length, insert_width, insert_height)
sideq_right = makebox('sideq_right', insert_length, insert_width, insert_height)
sideq_ridge = makebox('sideq_ridge', side_length  , ridge_width , ridge_height )
sideq_left.Placement  = FreeCAD.Placement(Vector(-insert_length, insert_Y, 2            ), FreeCAD.Rotation(Vector(1,0,0), 0))
sideq_right.Placement = FreeCAD.Placement(Vector(side_length   , insert_Y, 2            ), FreeCAD.Rotation(Vector(1,0,0), 0))
sideq_ridge.Placement = FreeCAD.Placement(Vector(0             , ridge_Y , common_height), FreeCAD.Rotation(Vector(1,0,0), 0))
# holders for shelve on the side, midway
# Pythagoras helps a bit, 0.866 = cos30
hypo   = common_width / cos30
# main for the solid part
holder1_main = makebox('holder1_main', common_width  , holder_length/2, common_height)
holder2_main = makebox('holder2_main', common_width  , holder_length/2, common_height)
holder1_main.Placement = FreeCAD.Placement(Vector(side_length/2 - hypo/2, common_width/2, 0),App.Rotation(App.Vector(0,0,1),30))
holder2_main.Placement = FreeCAD.Placement(Vector(side_length/2 + hypo/2, common_width/2, 0),App.Rotation(App.Vector(0,0,1),210))
# extr for the extrusion on which the shelve rests
holder1_extr = makebox('holder1_extr', common_width/2, holder_length/2, common_height)
holder2_extr = makebox('holder2_extr', common_width/2, holder_length/2, common_height)
X1 = (side_length / 2) - (hypo / 2) - (insert_length * sin30)
X2 = (side_length / 2) + (hypo / 2) + (insert_length * sin30) - ((common_width / 2) * cos30)
Y1 = (common_width / 2) + (insert_length * cos30)
Y2 = (common_width / 2) - (insert_length * cos30) - ((common_width / 2) * sin30)
holder1_extr.Placement = FreeCAD.Placement(Vector(X1, Y1, 0),App.Rotation(App.Vector(0,0,1),30))
holder2_extr.Placement = FreeCAD.Placement(Vector(X2, Y2, 0),App.Rotation(App.Vector(0,0,1),210))
# edge for the back to push the shelve against
holder1_edge = makebox('holder1_edge', common_width/2, holder_length/2, cross_cut)
holder2_edge = makebox('holder2_edge', common_width/2, holder_length/2, cross_cut )
X3 = (side_length / 2) - (hypo / 2) - (insert_length * sin30) + ((common_width / 2) * cos30)
X4 = (side_length / 2) + (hypo / 2) + (insert_length * sin30)
Y3 = (common_width / 2) + (insert_length * cos30) + ((common_width / 2) * sin30)
Y4 = (common_width / 2) - (insert_length * cos30)   
holder1_edge.Placement = FreeCAD.Placement(Vector(X3, Y3, 0),App.Rotation(App.Vector(0,0,1),30))
holder2_edge.Placement = FreeCAD.Placement(Vector(X4, Y4, 0),App.Rotation(App.Vector(0,0,1),210))

sideq_compound        = doc.addObject("Part::Compound","sideq_compound")
sideq_compound.Links  = [sideq_main, sideq_left, sideq_right,sideq_ridge, holder1_main, holder1_extr, holder1_edge, holder2_main, holder2_extr, holder2_edge]
#sideq_compound.ViewObject.hide()

# refine
Refine_sideq = doc.addObject('Part::Refine','Refine_sideq')
Refine_sideq.Source = sideq_compound
Refine_sideq.Label = 'Refine_sideq'
Refine_sideq.ViewObject.hide()
doc.recompute()
# mesh
Mesh_sideq = doc.addObject("Mesh::Feature","Mesh_sideq")
Shape = Part.getShape(Refine_sideq,"")
Mesh_sideq.Mesh = MeshPart.meshFromShape(Shape=Shape, LinearDeflection=1, AngularDeflection=0.1, Relative=False)
Mesh_sideq.Label = "Mesh_sideq"
# 3mf
export_list = []
export_list.append(Mesh_sideq)
Mesh.export(export_list, u"/home/paul/FreeCAD models/smurf/sideq.3mf")



sideq2_compound        = doc.addObject("Part::Compound","sideq2_compound")
sideq2_compound.Links  = [sideq_main, sideq_left, sideq_right,sideq_ridge, holder1_main, holder1_extr, holder1_edge]
#sideq_compound.ViewObject.hide()

# refine
Refine_sideq2 = doc.addObject('Part::Refine','Refine_sideq2')
Refine_sideq2.Source = sideq2_compound
Refine_sideq2.Label = 'Refine_sideq2'
Refine_sideq2.ViewObject.hide()
doc.recompute()
# mesh
Mesh_sideq2 = doc.addObject("Mesh::Feature","Mesh_sideq2")
Shape = Part.getShape(Refine_sideq2,"")
Mesh_sideq2.Mesh = MeshPart.meshFromShape(Shape=Shape, LinearDeflection=1, AngularDeflection=0.1, Relative=False)
Mesh_sideq2.Label = "Mesh_sideq2"
# 3mf
export_list = []
export_list.append(Mesh_sideq2)
Mesh.export(export_list, u"/home/paul/FreeCAD models/smurf/sideq2.3mf")



sideq3_compound        = doc.addObject("Part::Compound","sideq3_compound")
sideq3_compound.Links  = [sideq_main, sideq_left, sideq_right,sideq_ridge, holder2_main, holder2_extr, holder2_edge]
#sideq_compound.ViewObject.hide()

# refine
Refine_sideq3 = doc.addObject('Part::Refine','Refine_sideq3')
Refine_sideq3.Source = sideq3_compound
Refine_sideq3.Label = 'Refine_sideq3'
Refine_sideq3.ViewObject.hide()
doc.recompute()
# mesh
Mesh_sideq3 = doc.addObject("Mesh::Feature","Mesh_sideq3")
Shape = Part.getShape(Refine_sideq3,"")
Mesh_sideq3.Mesh = MeshPart.meshFromShape(Shape=Shape, LinearDeflection=1, AngularDeflection=0.1, Relative=False)
Mesh_sideq3.Label = "Mesh_sideq3"
# 3mf
export_list = []
export_list.append(Mesh_sideq3)
Mesh.export(export_list, u"/home/paul/FreeCAD models/smurf/sideq3.3mf")





'''
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
side_hinge_ridg1.ViewObject.hide()
side_hinge_ridg2.ViewObject.hide()
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
side_hinge_compound.ViewObject.hide()

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
hexleaf.ViewObject.hide()
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
leaf_compound.ViewObject.hide()

'''

doc.recompute()
FreeCADGui.ActiveDocument.ActiveView.fitAll()
