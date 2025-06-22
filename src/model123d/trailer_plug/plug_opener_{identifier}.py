"""
----
file-name:      plug_opener_{identifier}.py
file-uuid:      6f61bd14-e792-4294-909b-f624ac9334cd
description:   hanger plug opener

project:
    name:       model123d
    uuid:       fe521ba0-4ad7-484d-9386-26de71379e15
    url:        https://www.github.com/42sol/model123d
"""

# [Imports]
from build123d import *
from build123d import MM as mm
from ocp_vscode import show
from dataclasses import dataclass
from pathlib import Path
import sys
from rich.console import Console
from math import sqrt
from copy import deepcopy as copy
# [Setup]
console = Console()
objects = []

# [Constants]
no = False
yes = True

def debug(msg):
    """Print debug message if show_debug is True"""
    if Parameters.show_debug:
        console.log(f"[blue]DEBUG: {msg}[/blue]")

def define(object, color="#ff0000", name=""):
    """Define an object with a name and color"""
    if len(name) == 0:
        name = object.__name__
    else:
        object.name = name
    object.color = color
    objects.append(object)
    return object

# [Parameters]
@dataclass
class Parameters:
    """Parameters for the ${TM_FILENAME}"""
    show_debug: bool       = yes
    show_selection: bool   = yes
    show_nose:  bool       = no
    do_fillet: bool         = yes
    do_export:  bool       = yes
    # Device dimensions
    base_height: float       = 15.0 * mm
    base_diameter: float     = 30.0 * mm
    tool_grip: float         = 10.0 * mm
    grip_length: float       = 50.0 * mm
    base_thickness: float    = 2.0 * mm
    nose_length: float       = 30.0 * mm
    cut_length: float        = 15.0 * mm
    nose_width: float        = 5.0 * mm
    nose_height: float       = 15.0 * mm
P = Parameters()


def do_fillet(index, edge, radius):
    """Apply a fillet to the edges of an object"""
    define(edge, "#00c9ccff", f"edgeP{index}_{edge.length:.2f}mm") 
    fillet(edge, radius)

def do_chamfer(index, edge, radius):
    """Apply a fillet to the edges of an object"""
    define(edge, "#00c9ccff", f"edgeP{index}_{edge.length:.2f}mm") 
    chamfer(edge, radius)
        

# [Main]    
if __name__ == "__main__":
    debug("Running main")
    
    # [Model]
    debug("Creating model") 
    with BuildPart(Plane.XY.offset(P.tool_grip-P.nose_height)) as nose:
        Box(length=P.nose_length, width=P.nose_width, height=P.nose_height,
            align=(Align.MIN, Align.CENTER, Align.CENTER),
            mode=Mode.ADD)
    if P.show_nose:
        define(nose, "#00ff00ff", "nose")
        
            
    with BuildPart() as base:
        Cylinder(radius=P.base_diameter/2, height=P.base_height, mode=Mode.ADD)
        Cylinder(radius=P.base_diameter/2-P.base_thickness, height=P.nose_height, mode=Mode.SUBTRACT,)
        
        with BuildSketch(Plane.XY.offset(P.base_height/2-P.tool_grip/2)) as bottom_sketch:
            RectangleRounded(P.grip_length, P.base_diameter-P.base_thickness, 2*P.base_thickness)
        extrude(amount=P.tool_grip/2)
        add(nose.part.rotate(Axis.Z, 90), mode=Mode.SUBTRACT)

        edges = base.edges().filter_by(lambda e: e)
        if P.do_fillet:
            do_fillet(12, edges[12], 0.2)
            do_fillet(39, edges[39], 0.2)
            do_fillet(28, edges[28], 0.4)
            do_fillet(46, edges[46], 0.4)
            
            

    define(base, "#0000aaff", "tool")

    # Show the box
    
    show(*objects)
    
    # Export the box if do_export is True
    if P.do_export:
        debug("Exporting model")
        id = f'{P.base_diameter}x{P.base_height}mm'

        export_name = __file__ \
                        .replace('{identifier}', id) \
                        .replace('.py', '.stl')
        export_path = Path(__file__).parent / export_name
        console.log(f"[green]Model exported to {export_path}[/green]")
        exporter = Mesher()
        exporter.add_shape(base.part.rotate(Axis.Y, 180))
        exporter.write(export_path)
        del exporter        