"""
glass.py -- Paul Cobbaut, 2024-05-18
Create a hexagon wall display for small figurines.
3D-printed hexagon, covered by a bought plexiglass panel.
This file ==> svg and dxf for plexiglass panel
"""

import FreeCAD
from FreeCAD import Base, Vector
import PartDesign
import Sketcher


# Dimensions in mm
hexagon_radius = 170

# labels
DocLabel    = 'Hexagon Glass Panel'
BodyLabel   = 'glass_body'
SketchLabel = 'glass_sketch'


doc    = FreeCAD.newDocument(DocLabel)
body   = doc.addObject("PartDesign::Body", BodyLabel)
sketch = doc.getObject(BodyLabel).newObject("Sketcher::SketchObject", SketchLabel)
sketch.Placement = FreeCAD.Placement(Vector(0,0,0),FreeCAD.Rotation(Vector(1,0,0),0))



doc.recompute()
FreeCADGui.ActiveDocument.ActiveView.fitAll()
