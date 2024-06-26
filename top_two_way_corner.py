"""
zeshoek.py -- Paul Cobbaut
2024-05-07
2024-06-17
Create a hexagon wall display for small figurines.
3D-printed hexagon, covered by a bought panel.
Corners for the hexagon and for the shelves.
Side for the hexagon.
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

# The directory to export the .stl files to
export_directory = "/home/paul/FreeCAD_generated/hexagon/"

#Dimensions in mm
center_radius   =  5
arm_length      = 20
arm_width       =  6
hole_width      =  2
cover_width     = arm_width/2 - hole_width/2
depth           = 21
gluepart_depth  =  1.90
gluepart_radius = 12
glass_mm        =  3

# Arms start as rectangles named a, b
# a goes down 270 degrees
# b goes up-right 30 degrees

a_deg = -90
b_deg = a_deg + 120


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

# Create document
doc = FreeCAD.newDocument("hexagon")

# Create body for regular corner part
# corner that connects three sides
BodyLabel   = 'regular_corner_body'
Body_obj    = doc.addObject("PartDesign::Body", BodyLabel)
# Create corner sketch
SketchLabel = 'regular_corner_sketch'
Sketch_obj  = doc.getObject(BodyLabel).newObject("Sketcher::SketchObject", SketchLabel)
Sketch_obj.Placement = FreeCAD.Placement(Vector(0,0,0),FreeCAD.Rotation(Vector(1,0,0),0))
Sketch_obj.ViewObject.hide()

# Create circle at origin = center of the corner piece
centerpoint = Vector(0,0,0)
radius = center_radius
direction = Vector(0,0,1)
Circle_obj = Sketch_obj.addGeometry(Part.Circle(centerpoint, direction, radius),True)

# mid points of the end lines
am = polar_to_vector(arm_length, a_deg)
bm = polar_to_vector(arm_length, b_deg)

# half points of the end lines
a_end_half = polar_to_vector(arm_width/2, a_deg + 90) 
b_end_half = polar_to_vector(arm_width/2, b_deg + 90) 

# end points of the three arms
a_end_for = am + a_end_half
a_end_bac = am - a_end_half
b_end_for = bm + b_end_half
b_end_bac = bm - b_end_half

# end lines = short lines furthest away from origin
a_end_line = Sketch_obj.addGeometry(Part.LineSegment(a_end_for, a_end_bac),False)
b_end_line = Sketch_obj.addGeometry(Part.LineSegment(b_end_for, b_end_bac),False)

# Find intersection point between center_circle and long edges of three rectangles
circle_center = (0, 0)

line_start   = (a_end_for.x, a_end_for.y)
line_end     = (a_end_half.x, a_end_half.y)
intersection = circle_line_segment_intersection(center_radius, line_start, line_end)
a_int_for    = Vector(intersection[0][0], intersection[0][1], 0)
a_for_inter  = Sketch_obj.addGeometry(Part.LineSegment(a_end_for, a_int_for),False)

line_start   = (a_end_bac.x, a_end_bac.y)
line_end     = (- a_end_half.x, - a_end_half.y)
intersection = circle_line_segment_intersection(center_radius, line_start, line_end)
a_int_bac    = Vector(intersection[0][0], intersection[0][1],0)
a_bac_inter  = Sketch_obj.addGeometry(Part.LineSegment(a_end_bac, a_int_bac),False)


line_end     = (b_end_for.x, b_end_for.y)
line_start   = (b_end_half.x, b_end_half.y)
intersection = circle_line_segment_intersection(center_radius, line_start, line_end)
b_int_for    = Vector(intersection[0][0], intersection[0][1],0)
b_for_inter  = Sketch_obj.addGeometry(Part.LineSegment(b_end_for, b_int_for),False)

line_end     = (b_end_bac.x, b_end_bac.y)
line_start   = (- b_end_half.x, - b_end_half.y)
intersection = circle_line_segment_intersection(center_radius, line_start, line_end)
b_int_bac    = Vector(intersection[0][0], intersection[0][1],0)
b_bac_inter  = Sketch_obj.addGeometry(Part.LineSegment(b_end_bac, b_int_bac),False)

# connect the arms 
a_to_b = Sketch_obj.addGeometry(Part.LineSegment(a_int_for, b_int_bac),False)
b_to_a = Sketch_obj.addGeometry(Part.LineSegment(b_int_for, a_int_bac),False)

# pad 
PadLabel  = 'Pad_main'
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
a_end_hole_bac = a_end_bac + polar_to_vector(cover_width, a_deg + 90) + polar_to_vector(0.1, a_deg)
b_end_hole_bac = b_end_bac + polar_to_vector(cover_width, b_deg + 90) + polar_to_vector(0.1, b_deg)

# hole points of the inner lines
a_inner_hole_for =   polar_to_vector(hole_width/2, a_deg + 90) + polar_to_vector(center_radius, a_deg )
b_inner_hole_for =   polar_to_vector(hole_width/2, b_deg + 90) + polar_to_vector(center_radius, b_deg )
a_inner_hole_bac = - polar_to_vector(hole_width/2, a_deg + 90) + polar_to_vector(center_radius, a_deg )
b_inner_hole_bac = - polar_to_vector(hole_width/2, b_deg + 90) + polar_to_vector(center_radius, b_deg )

# lines
a_end_hole   = Sketch_topface.addGeometry(Part.LineSegment(a_end_hole_for, a_end_hole_bac),False)
b_end_hole   = Sketch_topface.addGeometry(Part.LineSegment(b_end_hole_for, b_end_hole_bac),False)
a_inner_hole = Sketch_topface.addGeometry(Part.LineSegment(a_inner_hole_for, a_inner_hole_bac),False)
b_inner_hole = Sketch_topface.addGeometry(Part.LineSegment(b_inner_hole_for, b_inner_hole_bac),False)
a_for_hole   = Sketch_topface.addGeometry(Part.LineSegment(a_end_hole_for, a_inner_hole_for),False)
b_for_hole   = Sketch_topface.addGeometry(Part.LineSegment(b_end_hole_for, b_inner_hole_for),False)
a_bac_hole   = Sketch_topface.addGeometry(Part.LineSegment(a_end_hole_bac, a_inner_hole_bac),False)
b_bac_hole   = Sketch_topface.addGeometry(Part.LineSegment(b_end_hole_bac, b_inner_hole_bac),False)

# the hole
PocketLabel = 'Pocket_hole'
Pocket_hole = doc.getObject(BodyLabel).newObject('PartDesign::Pocket','Pocket')
Pocket_hole.Profile = Sketch_topface
Pocket_hole.Length = depth - 2



# bottom wall to against plexiglass
# sketch
SketchLabel = 'glass_sketch'
Sketch_bot  = doc.getObject(BodyLabel).newObject("Sketcher::SketchObject", SketchLabel)
Sketch_bot.Placement = FreeCAD.Placement(Vector(0,0,0),FreeCAD.Rotation(Vector(1,0,0),0))
Sketch_bot.ViewObject.hide()
# hole points of the end lines
a_end_hole_for = a_end_for - polar_to_vector(cover_width, a_deg + 90)
b_end_hole_for = b_end_for - polar_to_vector(cover_width, b_deg + 90)
a_end_hole_bac = a_end_bac + polar_to_vector(cover_width, a_deg + 90)
b_end_hole_bac = b_end_bac + polar_to_vector(cover_width, b_deg + 90)
# hole points of the inner lines
a_inner_hole_for =   polar_to_vector(hole_width/2, a_deg + 90) + polar_to_vector(5, a_deg )
b_inner_hole_for =   polar_to_vector(hole_width/2, b_deg + 90) + polar_to_vector(5, b_deg )
a_inner_hole_bac = - polar_to_vector(hole_width/2, a_deg + 90) + polar_to_vector(5, a_deg )
b_inner_hole_bac = - polar_to_vector(hole_width/2, b_deg + 90) + polar_to_vector(5, b_deg )
# lines
a_end_hole   = Sketch_bot.addGeometry(Part.LineSegment(a_end_hole_for, a_end_hole_bac),False)
b_end_hole   = Sketch_bot.addGeometry(Part.LineSegment(b_end_hole_for, b_end_hole_bac),False)
a_inner_hole = Sketch_bot.addGeometry(Part.LineSegment(a_inner_hole_for, a_inner_hole_bac),False)
b_inner_hole = Sketch_bot.addGeometry(Part.LineSegment(b_inner_hole_for, b_inner_hole_bac),False)
a_for_hole   = Sketch_bot.addGeometry(Part.LineSegment(a_end_hole_for, a_inner_hole_for),False)
b_for_hole   = Sketch_bot.addGeometry(Part.LineSegment(b_end_hole_for, b_inner_hole_for),False)
a_bac_hole   = Sketch_bot.addGeometry(Part.LineSegment(a_end_hole_bac, a_inner_hole_bac),False)
b_bac_hole   = Sketch_bot.addGeometry(Part.LineSegment(b_end_hole_bac, b_inner_hole_bac),False)
# pad 
PadLabel  = 'Pad_glass'
Pad_glass   = doc.getObject(BodyLabel).newObject('PartDesign::Pad',PadLabel)
Pad_glass.Profile = doc.getObject(SketchLabel)
Pad_glass.Length = glass_mm
Pad_glass.Reversed = 1
# refine
RefineGlassLabel = 'Refine_Glass'
Refine_Glass = doc.addObject('Part::Refine',RefineGlassLabel)
Refine_Glass.Source = Pad_glass
Refine_Glass.Label = RefineGlassLabel
Refine_Glass.ViewObject.hide()
doc.recompute()
# mesh
Mesh_Glass_Label = 'Mesh_Glass'
Mesh_Glass = doc.addObject("Mesh::Feature","Mesh_Glass")
Shape = Part.getShape(Refine_Glass,"")
Mesh_Glass.Mesh = MeshPart.meshFromShape(Shape=Shape, LinearDeflection=1, AngularDeflection=0.1, Relative=False)
Mesh_Glass.Label = Mesh_Glass_Label
# 3mf
export_list = []
export_list.append(Mesh_Glass)
Mesh.export(export_list, u"/home/paul/FreeCAD models/smurf/Top_two_way.3mf")

doc.recompute()
FreeCADGui.ActiveDocument.ActiveView.fitAll()

