"""
----
file-name:      frame_hanger_{identifier}.py
file-uuid:      fcaa3aba-387b-4a4e-93d4-b59b03243459
description:    A frame hanger for a special image frame.
author:         felix@42sol
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
    show_selection: bool   = no
    show_nose:  bool       = no
    do_fillet: bool         = yes
    do_export:  bool       = yes
    # Device dimensions
    base_height: float       = 8.0 * mm
    base_diameter: float     = 12.5 * mm
    base_width: float        = 130.0 * mm
    nose_length: float       = 10.0 - 5.0/2 * mm
    nose_width: float        = 5.0 * mm
    nose_height: float       = 2.5 * mm
    hole_diameter: float     = 2.0 * mm
    nose_angle: float        = -5
P = Parameters()

# [Main]    
if __name__ == "__main__":
    debug("Running main")
    
    # [Model]
    debug("Creating model") 
    with BuildPart() as nose:
        with BuildSketch(Plane.XY) as bottom_sketch:
            Rectangle(P.nose_length, P.nose_width, mode=Mode.ADD,
                align=(Align.MIN, Align.CENTER, Align.MIN))
            with Locations((P.nose_length, 0, 0)):
                Circle(P.nose_width/2)
        
        extrude(amount=P.nose_height, mode=Mode.ADD)
        fillet(nose.edges(), 1.2 * mm)
        
    if P.show_nose:
        define(nose, "#00ff00ff", "nose")
    
    with BuildPart() as base:
        with BuildSketch(Plane.XY) as bottom_sketch:
            Rectangle(P.base_diameter, P.base_width, align=(Align.CENTER, Align.MIN, Align.CENTER))
            with Locations((0, 0, 0), (0, P.base_width, 0)):
                Circle(P.base_diameter/2)
                Circle(P.hole_diameter,  mode=Mode.SUBTRACT)
            with Locations((0, P.base_width/4, 0), (0, P.base_width/4*3, P.base_height)):
                Circle(P.hole_diameter,  mode=Mode.SUBTRACT)
            with Locations((0, P.base_width/8, 0), (0, P.base_width/8*7, P.base_height)):    
                Rectangle(2*P.hole_diameter, P.base_width/4, mode=Mode.SUBTRACT)
                
                
        extrude(amount=P.base_height, mode=Mode.ADD)
        
        with Locations((0, 0, 0), (0, P.base_width, 0)):
            add(nose.part.locate(Location((2*P.hole_diameter,0,P.base_height*0.5))).rotate(Axis.Y, P.nose_angle))
        
        #TODO: add hole in the base
        
        edges = base.edges().filter_by(lambda e: e)
        for index in range(len(edges)):
            if P.show_selection:
                define(edges[index], "#ff0000ff", f"edges_{index}")
        if P.do_fillet:
            fillet(edges[3],.6)
            chamfer(edges[32],2.)
            chamfer(edges[36],2.)

    define(base, "#0000aaff", "base")

    # Show the box
    show(*objects)
    
    # Export the box if do_export is True
    if P.do_export:
        debug("Exporting model")
        id = f'{P.base_width}x{P.base_height}mm'

        export_name = __file__ \
                        .replace('{identifier}', id) \
                        .replace('.py', '.stl')
        export_path = Path(__file__).parent / export_name
        console.log(f"[green]Model exported to {export_path}[/green]")
        exporter = Mesher()
        exporter.add_shape(base.part)
        exporter.write(export_path)
        del exporter        