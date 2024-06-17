"""
Paul Cobbaut,
2024-05-10
2024-06-17
Create a hexagon wall display for small figurines.
3D-printed hexagon, covered by a bought panel.
Corners for the hexagon and for the shelves.
Side for the hexagon.
This --> top four way corner for mid shelve.
"""

import FreeCAD
from FreeCAD import Base, Vector
import PartDesign
import Sketcher
import Part
import Mesh
import MeshPart
import math

# Variables
#
#

#Dimensions in mm
glass_mm        =  3
center_radius   =  5
arm_length      = 20
arm_width       =  6
hole_width      =  2
cover_width     = arm_width/2 - hole_width/2
depth           = 21
gluepart_depth  =  1.90
gluepart_radius = 12
arm_d_length    = 42

# Arms start as rectangles named a, b, c
# a goes down 270 degrees
# b goes up-right 30 degrees
# c goes up-left 150 degrees

a_deg = -90
b_deg = a_deg + 120
c_deg = b_deg + 120
d_deg = a_deg + 180


# functions
#
#

def polar_to_vector(radius, angle_degrees):
    angle_radians = math.radians(angle_degrees)
    x = round(radius * math.cos(angle_radians),2)
    y = round(radius * math.sin(angle_radians),2)
    return Vector(x, y, 0)


def circle_line_segment_intersection(circle_radius, line_start, line_end):
    x1, y1 = line_start
    x2, y2 = line_end

    dx = x2 - x1
    dy = y2 - y1
    dr = math.sqrt(dx**2 + dy**2)
    D = x1*y2 - x2*y1
    discriminant = circle_radius**2 * dr**2 - D**2
    sqrt_discriminant = math.sqrt(discriminant)
    x1 = ( D * dy + math.copysign(dx * sqrt_discriminant, dy)) / (dr**2)
    x2 = ( D * dy - math.copysign(dx * sqrt_discriminant, dy)) / (dr**2)
    y1 = (-D * dx + math.copysign(dy * sqrt_discriminant, dx)) / (dr**2)
    y2 = (-D * dx - math.copysign(dy * sqrt_discriminant, dx)) / (dr**2)

    intersection_points = [(round(x1,2), round(y1,2)), (round(x2,2), round(y2,2))]
    valid_intersection_points = [point for point in intersection_points if is_point_on_line_segment(point, line_start, line_end)]
    return valid_intersection_points


def is_point_on_line_segment(point, line_start, line_end):
    x, y = point
    x1, y1 = line_start
    x2, y2 = line_end
    return min(x1, x2) <= x <= max(x1, x2) and min(y1, y2) <= y <= max(y1, y2)


def intersection_two_segments(line1_start, line1_end, line2_start, line2_end):
    x1, y1 = line1_start
    x2, y2 = line1_end
    x3, y3 = line2_start
    x4, y4 = line2_end
    x = ( (x1*y2 - y1*x2) * (x3-x4) - (x1-x2) * (x3*y4 - y3*x4) )  /  ( (x1-x2) * (y3-y4) - (y1-y2) * (x3-x4) )
    y = ( (x1*y2 - y1*x2) * (y3-y4) - (y1-y2) * (x3*y4 - y3*x4) )  /  ( (x1-x2) * (y3-y4) - (y1-y2) * (x3-x4) )
    return Vector(x,y,0)


# Create document
doc = FreeCAD.newDocument("four way corner mid shelve")

# Create body for regular corner part
# corner that connects three sides
BodyLabel   = 'fourway_corner_body'
Body_obj    = doc.addObject("PartDesign::Body", BodyLabel)
# Create corner sketch
SketchLabel = 'fourway_corner_sketch'
Sketch_obj  = doc.getObject(BodyLabel).newObject("Sketcher::SketchObject", SketchLabel)
Sketch_obj.Placement = FreeCAD.Placement(Vector(0,0,0),FreeCAD.Rotation(Vector(1,0,0),0))
Sketch_obj.ViewObject.hide()

# Create circle at origin = center of the corner piece
centerpoint = Vector(0,0,0)
radius = center_radius
direction = Vector(0,0,1)
Circle_obj = Sketch_obj.addGeometry(Part.Circle(centerpoint, direction, radius),True)

# mid points of the end lines
am = polar_to_vector(arm_length  , a_deg)
bm = polar_to_vector(arm_length  , b_deg)
cm = polar_to_vector(arm_length  , c_deg)
dm = polar_to_vector(arm_d_length, d_deg)

# half points of the end lines
a_end_half = polar_to_vector(arm_width/2, a_deg + 90) 
b_end_half = polar_to_vector(arm_width/2, b_deg + 90) 
c_end_half = polar_to_vector(arm_width/2, c_deg + 90) 
d_end_half = polar_to_vector(arm_width/2, d_deg + 90) 

# end points of the three arms
a_end_for = am + a_end_half
a_end_bac = am - a_end_half
b_end_for = bm + b_end_half
b_end_bac = bm - b_end_half
c_end_for = cm + c_end_half
c_end_bac = cm - c_end_half
d_end_for = dm + d_end_half
d_end_bac = dm - d_end_half

# end lines = short lines furthest away from origin
a_end_line = Sketch_obj.addGeometry(Part.LineSegment(a_end_for, a_end_bac),False)
b_end_line = Sketch_obj.addGeometry(Part.LineSegment(b_end_for, b_end_bac),False)
c_end_line = Sketch_obj.addGeometry(Part.LineSegment(c_end_for, c_end_bac),False)
d_end_line = Sketch_obj.addGeometry(Part.LineSegment(d_end_for, d_end_bac),False)

# Find intersection point between center_circle and long edges of three rectangles
lineaf_start = (a_end_for.x, a_end_for.y)
lineaf_end   = (a_end_half.x, a_end_half.y)
intersection = circle_line_segment_intersection(center_radius, lineaf_start, lineaf_end)
a_int_for    = Vector(intersection[0][0], intersection[0][1], 0)

lineab_start = (a_end_bac.x, a_end_bac.y)
lineab_end   = (- a_end_half.x, - a_end_half.y)
intersection = circle_line_segment_intersection(center_radius, lineab_start, lineab_end)
a_int_bac    = Vector(intersection[0][0], intersection[0][1],0)


linebf_start = (b_end_for.x, b_end_for.y)
linebf_end   = (b_end_half.x, b_end_half.y)
intersection = circle_line_segment_intersection(center_radius, linebf_start, linebf_end)
b_int_for    = Vector(intersection[0][0], intersection[0][1],0)

linebb_end   = (b_end_bac.x, b_end_bac.y)
linebb_start = (- b_end_half.x, - b_end_half.y)
intersection = circle_line_segment_intersection(center_radius, linebb_start, linebb_end)
b_int_bac    = Vector(intersection[0][0], intersection[0][1],0)


linecf_start = (c_end_for.x, c_end_for.y)
linecf_end   = (c_end_half.x, c_end_half.y)
intersection = circle_line_segment_intersection(center_radius, linecf_start, linecf_end)
c_int_for    = Vector(intersection[0][0], intersection[0][1],0)

linecb_start = (c_end_bac.x, c_end_bac.y)
linecb_end   = (- c_end_half.x, - c_end_half.y)
intersection = circle_line_segment_intersection(center_radius, linecb_start, linecb_end)
c_int_bac    = Vector(intersection[0][0], intersection[0][1],0)


linedf_start = (d_end_for.x, d_end_for.y)
linedf_end   = (d_end_half.x, d_end_half.y)
intersection = circle_line_segment_intersection(center_radius, linedf_start, linedf_end)
d_int_for    = Vector(intersection[0][0], intersection[0][1],0)

linedb_start = (d_end_bac.x, d_end_bac.y)
linedb_end   = (- d_end_half.x, - d_end_half.y)
intersection = circle_line_segment_intersection(center_radius, linedb_start, linedb_end)
d_int_bac    = Vector(intersection[0][0], intersection[0][1],0)

# draw lines, but not d or the intersecting ones with d
a_for_inter  = Sketch_obj.addGeometry(Part.LineSegment(a_end_for, a_int_for),False)
a_bac_inter  = Sketch_obj.addGeometry(Part.LineSegment(a_end_bac, a_int_bac),False)
#b_for_inter  = Sketch_obj.addGeometry(Part.LineSegment(b_end_for, b_int_for),False)
b_bac_inter  = Sketch_obj.addGeometry(Part.LineSegment(b_end_bac, b_int_bac),False)
c_for_inter  = Sketch_obj.addGeometry(Part.LineSegment(c_end_for, c_int_for),False)
#c_bac_inter  = Sketch_obj.addGeometry(Part.LineSegment(c_end_bac, c_int_bac),False)
#d_for_inter  = Sketch_obj.addGeometry(Part.LineSegment(d_end_for, d_int_for),False)
#d_bac_inter  = Sketch_obj.addGeometry(Part.LineSegment(d_end_bac, d_int_bac),False)

# find intersection between lines b_for and d_bac
line1_start = linebf_start
line1_end = linebf_end
line2_start = linedb_start
line2_end = linedb_end
i_bd = intersection_two_segments(line1_start, line1_end, line2_start, line2_end)

# find intersection between lines c_bac and d_for
line1_start = linecb_start
line1_end = linecb_end
line2_start = linedf_start
line2_end = linedf_end
i_dc = intersection_two_segments(line1_start, line1_end, line2_start, line2_end)

# draw the lines to the intersection points with d
bd_inter  = Sketch_obj.addGeometry(Part.LineSegment(i_bd, b_end_for),False)
db_inter  = Sketch_obj.addGeometry(Part.LineSegment(i_bd, d_end_bac),False)
dc_inter  = Sketch_obj.addGeometry(Part.LineSegment(i_dc, d_end_for),False)
cd_inter  = Sketch_obj.addGeometry(Part.LineSegment(i_dc, c_end_bac),False)

# connect the arms
a_to_b = Sketch_obj.addGeometry(Part.LineSegment(a_int_for, b_int_bac),False)
#b_to_c = Sketch_obj.addGeometry(Part.LineSegment(b_int_for, c_int_bac),False)
c_to_a = Sketch_obj.addGeometry(Part.LineSegment(c_int_for, a_int_bac),False)

# pad 
PadLabel  = 'Pad_four_corner'
Pad_obj   = doc.getObject(BodyLabel).newObject('PartDesign::Pad',PadLabel)
Pad_obj.Profile = doc.getObject(SketchLabel)
Pad_obj.Length = depth

doc.recompute()

# find top face
for i, fac in enumerate(Pad_obj.Shape.Faces): # Going through all faces of the object
  if fac.Surface.Position.z == depth:
      topface = 'Face{:d}'.format(i+1) # Building face name from its index

# Create sketch on topface of pad
SketchLabel = 'Sketch_topface'
Sketch_topface  = doc.getObject(BodyLabel).newObject("Sketcher::SketchObject", SketchLabel)
Sketch_topface.Support = doc.getObject(PadLabel),[topface,]
Sketch_topface.MapMode = 'FlatFace'
Sketch_topface.ViewObject.hide()

# hole points of the end lines
a_end_hole_for = a_end_for - polar_to_vector(cover_width, a_deg + 90) + polar_to_vector(0.1, a_deg)
b_end_hole_for = b_end_for - polar_to_vector(cover_width, b_deg + 90) + polar_to_vector(0.1, b_deg)
c_end_hole_for = c_end_for - polar_to_vector(cover_width, c_deg + 90) + polar_to_vector(0.1, c_deg)
a_end_hole_bac = a_end_bac + polar_to_vector(cover_width, a_deg + 90) + polar_to_vector(0.1, a_deg)
b_end_hole_bac = b_end_bac + polar_to_vector(cover_width, b_deg + 90) + polar_to_vector(0.1, b_deg)
c_end_hole_bac = c_end_bac + polar_to_vector(cover_width, c_deg + 90) + polar_to_vector(0.1, c_deg)

# hole points of the inner lines
a_inner_hole_for =   polar_to_vector(hole_width/2, a_deg + 90) + polar_to_vector(center_radius, a_deg )
b_inner_hole_for =   polar_to_vector(hole_width/2, b_deg + 90) + polar_to_vector(center_radius, b_deg )
c_inner_hole_for =   polar_to_vector(hole_width/2, c_deg + 90) + polar_to_vector(center_radius, c_deg )
a_inner_hole_bac = - polar_to_vector(hole_width/2, a_deg + 90) + polar_to_vector(center_radius, a_deg )
b_inner_hole_bac = - polar_to_vector(hole_width/2, b_deg + 90) + polar_to_vector(center_radius, b_deg )
c_inner_hole_bac = - polar_to_vector(hole_width/2, c_deg + 90) + polar_to_vector(center_radius, c_deg )

# lines
a_end_hole   = Sketch_topface.addGeometry(Part.LineSegment(a_end_hole_for, a_end_hole_bac),False)
b_end_hole   = Sketch_topface.addGeometry(Part.LineSegment(b_end_hole_for, b_end_hole_bac),False)
c_end_hole   = Sketch_topface.addGeometry(Part.LineSegment(c_end_hole_for, c_end_hole_bac),False)
a_inner_hole = Sketch_topface.addGeometry(Part.LineSegment(a_inner_hole_for, a_inner_hole_bac),False)
b_inner_hole = Sketch_topface.addGeometry(Part.LineSegment(b_inner_hole_for, b_inner_hole_bac),False)
c_inner_hole = Sketch_topface.addGeometry(Part.LineSegment(c_inner_hole_for, c_inner_hole_bac),False)
a_for_hole   = Sketch_topface.addGeometry(Part.LineSegment(a_end_hole_for, a_inner_hole_for),False)
b_for_hole   = Sketch_topface.addGeometry(Part.LineSegment(b_end_hole_for, b_inner_hole_for),False)
c_for_hole   = Sketch_topface.addGeometry(Part.LineSegment(c_end_hole_for, c_inner_hole_for),False)
a_bac_hole   = Sketch_topface.addGeometry(Part.LineSegment(a_end_hole_bac, a_inner_hole_bac),False)
b_bac_hole   = Sketch_topface.addGeometry(Part.LineSegment(b_end_hole_bac, b_inner_hole_bac),False)
c_bac_hole   = Sketch_topface.addGeometry(Part.LineSegment(c_end_hole_bac, c_inner_hole_bac),False)

# the hole
PocketLabel = 'Pocket_hole'
Pocket_hole = doc.getObject(BodyLabel).newObject('PartDesign::Pocket',PocketLabel)
Pocket_hole.Profile = Sketch_topface
Pocket_hole.Length = depth - gluepart_depth


# Create sketch on topface of cross for shelve
SketchCLabel = 'Sketch_cross'
Sketch_cross  = doc.getObject(BodyLabel).newObject("Sketcher::SketchObject", SketchCLabel)
Sketch_cross.Support = doc.getObject(PadLabel),[topface,]
Sketch_cross.MapMode = 'FlatFace'
Sketch_cross.ViewObject.hide()

d_end_hole_for = dm + d_end_half
d_end_hole_bac = dm
d_inner_hole_for =   dm + d_end_half - polar_to_vector(10, d_deg )
d_inner_hole_bac =   dm - polar_to_vector(10, d_deg )
d_end_hole   = Sketch_cross.addGeometry(Part.LineSegment(d_end_hole_for, d_end_hole_bac),False)
d_inner_hole = Sketch_cross.addGeometry(Part.LineSegment(d_inner_hole_for, d_inner_hole_bac),False)
d_for_hole   = Sketch_cross.addGeometry(Part.LineSegment(d_end_hole_for, d_inner_hole_for),False)
d_bac_hole   = Sketch_cross.addGeometry(Part.LineSegment(d_end_hole_bac, d_inner_hole_bac),False)

# the cross
PocketCLabel = 'Pocket_chole'
Pocket_chole = doc.getObject(BodyLabel).newObject('PartDesign::Pocket',PocketCLabel)
Pocket_chole.Profile = Sketch_cross
Pocket_chole.Length = depth 


# find bottom face
for i, fac in enumerate(Pad_obj.Shape.Faces): # Going through all faces of the object
  if fac.Surface.Position.z == 0:
      botface = 'Face{:d}'.format(i+1) # Building face name from its index

# Create sketch on topface of pad
SketchLabel = 'Sketch_botface'
Sketch_botface  = doc.getObject(BodyLabel).newObject("Sketcher::SketchObject", SketchLabel)
Sketch_botface.Support = doc.getObject(PadLabel),[botface,]
Sketch_botface.MapMode = 'FlatFace'
Sketch_botface.AttachmentOffset = FreeCAD.Placement(Vector(0,0,0),FreeCAD.Rotation(Vector(0,0,1),180))
Sketch_botface.ViewObject.hide()

# lines
a_end_hole   = Sketch_botface.addGeometry(Part.LineSegment(a_end_hole_for, a_end_hole_bac),False)
b_end_hole   = Sketch_botface.addGeometry(Part.LineSegment(b_end_hole_for, b_end_hole_bac),False)
c_end_hole   = Sketch_botface.addGeometry(Part.LineSegment(c_end_hole_for, c_end_hole_bac),False)
a_inner_hole = Sketch_botface.addGeometry(Part.LineSegment(a_inner_hole_for, a_inner_hole_bac),False)
b_inner_hole = Sketch_botface.addGeometry(Part.LineSegment(b_inner_hole_for, b_inner_hole_bac),False)
c_inner_hole = Sketch_botface.addGeometry(Part.LineSegment(c_inner_hole_for, c_inner_hole_bac),False)
a_for_hole   = Sketch_botface.addGeometry(Part.LineSegment(a_end_hole_for, a_inner_hole_for),False)
b_for_hole   = Sketch_botface.addGeometry(Part.LineSegment(b_end_hole_for, b_inner_hole_for),False)
c_for_hole   = Sketch_botface.addGeometry(Part.LineSegment(c_end_hole_for, c_inner_hole_for),False)
a_bac_hole   = Sketch_botface.addGeometry(Part.LineSegment(a_end_hole_bac, a_inner_hole_bac),False)
b_bac_hole   = Sketch_botface.addGeometry(Part.LineSegment(b_end_hole_bac, b_inner_hole_bac),False)
c_bac_hole   = Sketch_botface.addGeometry(Part.LineSegment(c_end_hole_bac, c_inner_hole_bac),False)

# the ridge
PadLabel = 'Pad_ridge'
Pad_ridge = doc.getObject(BodyLabel).newObject('PartDesign::Pad',PadLabel)
Pad_ridge.Profile = Sketch_botface
Pad_ridge.Length = glass_mm


doc.recompute()
# mesh
Mesh_Top_Label = 'Mesh_Top'
Mesh_Top = doc.addObject("Mesh::Feature",Mesh_Top_Label)
Shape = Part.getShape(Pad_ridge,"")
Mesh_Top.Mesh = MeshPart.meshFromShape(Shape=Shape, LinearDeflection=1, AngularDeflection=0.1, Relative=False)
Mesh_Top.Label = Mesh_Top_Label
# 3mf
export_list = []
export_list.append(Mesh_Top)
Mesh.export(export_list, u"/home/paul/FreeCAD models/smurf/Top_mid_shelve.3mf")

doc.recompute()
FreeCADGui.ActiveDocument.ActiveView.fitAll()

