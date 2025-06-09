"""
----
file-name:      roof_{identifier}_{size}_{parameters}.py
file-uuid:      cc490682-f9bb-49df-979b-e77f51a9f7ac
description:   Generate a roof with a chimney and holes

project:
    name:       model123d
    uuid:       a0b40edb-6c25-41b9-878f-6bf97bfcf0a2
    url:        https://www.github.com/42sol/model123d
"""

# [Imports]
from build123d import *
from build123d import MM as mm
from ocp_vscode import show
from dataclasses import dataclass
import sys
from rich.console import Console
from pathlib import Path                                   # [docs](https://docs.python.org/3/library/pathlib.html)

# [Parameters]

# [Constants]
no, yes = False, True

# [Global_Variables]
console = Console()

# [Code]
# [Imports]


# [Parameters]
@dataclass
class P:
    """Parameters for the Base Plate model."""
    do_export: bool = yes
    do_pattern : bool = no
    do_chimney: bool = no
    do_extra: bool = yes
    do_show_cuts: bool = no# yes #  
    do_show_lines: bool = no
    
    size: float = 100.0 * mm
    height: float = 24.0 * mm
    depth: float = 130.0 * mm 
    
    size_2: float = 52.0 * mm
    width_2: float = 42.0 * mm
    height_2: float = 14.0 * mm
    depth_2: float = 52.0 * mm
    
    thickness: float = 1.8 * mm
    hole_diameter: float = 10.0 * mm
    hole_offset: float = 3.0 * mm

objects = []

P.height_diff = P.height - P.height_2
e1 = ((P.depth-P.width_2)/2,   -P.thickness)
e2 = ((P.depth-P.width_2)/2,    P.height_diff)
e3 = (P.depth/2-P.size_2/2,     P.height_diff)
e4 = (P.depth/2,                P.height_2-P.thickness+P.height_diff)
points2 = [e1, e2, e3, e4]
with BuildPart() as roof_cut_2:
    with BuildSketch(-Plane.ZY) as roof_cut_sketch_2:   
        with BuildLine(Plane.ZY) as roof_cut_line_2:
            Polyline(points2)
            mirror(roof_cut_line_2.line, about=Plane.XY.offset(P.depth/2))
        make_face()
    extrude(amount=P.depth_2)
if P.do_show_cuts:
    objects.append(roof_cut_2)
    if P.do_show_lines:
        objects.append(roof_cut_line_2)     
        roof_cut_line_2.color = "#0000FF"
        roof_cut_line_2.name = "Roof Cut Line 2"

a1 = (0-P.size/2,0)
a2 = (0-P.size/2,-P.thickness)
b1 = (0, P.height)
b2 = (0, P.height-P.thickness)
points = [b2, a2, a1, b1]
with BuildPart() as roof:
    with BuildSketch() as sketch:
        with BuildLine() as roof_line:
            Polyline(points)
            mirror(roof_line.line, about=Plane.ZY)
        make_face()
    extrude(amount=P.depth)
    if P.do_extra:
        add(roof_cut_2.part, mode=Mode.SUBTRACT)
    # fillet(roof.faces().sort_by(Axis.Z)[-1].edges(), radius=1.0)

objects.append(roof)

f1 = (0,0)
f2 = (0-P.size/2,-P.thickness)
f3 = (0, P.height-P.thickness)
points2 = [f1, f2, f3]
with BuildPart() as roof_cut_1:
    with BuildSketch() as roof_cut_sketch_1:
        with BuildLine() as roof_cut_line_1:
            Polyline(points2)
            mirror(roof_cut_line_1.line, about=Plane.ZY)
        make_face()
    extrude(amount=P.depth)
    
    # fillet(roof.faces().sort_by(Axis.Z)[-1].edges(), radius=1.0)
if P.do_show_cuts:
    objects.append(roof_cut_1)
    if P.do_show_lines:
        objects.append(roof_cut_line_1)    
        roof_cut_line_1.color = "#0000FFAA"
        roof_cut_line_1.name = "Roof Cut Line 1"
    

c1 = (-P.depth/2-P.size_2/2,P.height_diff)
c2 = (-P.depth/2-P.size_2/2-P.thickness,P.height_diff)
d2 = (-P.depth/2, P.height_2+P.height_diff)
d3 = (-P.depth/2, P.height_2-P.thickness+P.height_diff)
points = [d2, c2, c1, d3]

if P.do_extra:
    with BuildPart() as roof_2:
        with BuildSketch(-Plane.ZY) as sketch_2:   
            with BuildLine(Plane.ZY) as roof_line_2:
                Polyline(points)
                mirror(roof_line_2.line, about=Plane.XY.offset(-P.depth/2))
            make_face()
        extrude(amount=P.depth_2)
        add(roof_cut_1.part, mode=Mode.SUBTRACT)   
    objects.append(roof_2)
    roof_2.name = "Roof 2"
    roof_2.color = "#AA0000"
    if P.do_show_cuts:
        objects.append(roof_line_2)
        roof_line_2.color = "#0000FFAA"
        roof_line_2.name = "Roof Line 2"





if P.do_chimney:
    with BuildPart() as roof_with_hole:
        add(roof.part)
        with BuildSketch() as sketch:
            # Create circles for the holes
            with Locations((0.0, 0.0)):
                Circle(P.hole_diameter / 2.0)
            if P.do_extra:
                with Locations((P.hole_offset, P.hole_offset)):
                    Circle(P.hole_diameter / 2.0)
        extrude(amount=P.thickness, mode=Mode.SUBTRACT)
    
    roof = roof_with_hole

roof.color = "#FF0000"
roof.name = "Main"



show(objects)

with BuildPart() as roof_export:
    add(roof.part)
    if P.do_extra:
        add(roof_2.part)

if P.do_export:
    exporter = Mesher()
    exporter.add_shape(roof_export.part)
    if P.do_pattern:
        sys.exit(1, "Patterning not implemented yet")
        exporter.add_shape(roof.part)
    parameters = f'{P.thickness}'
    file_name = __file__.replace(".py", ".stl") \
                .replace('{identifier}', 'test') \
                .replace('{size}', str(P.size)) \
                .replace('{parameters}', parameters)
    
    exporter.write(Path(__file__).parent / "_output" / file_name)