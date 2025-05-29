"""
----
file-name:      frame_hanger_{identifier}.py
file-uuid:      fcaa3aba-387b-4a4e-93d4-b59b03243459
description:    {{description}}

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
    base_height: float       = 5.0 * mm
    base_diameter: float     = 12.5 * mm
    nose_length: float       = 12.0 + 12.5/2 - 5.0/2 * mm
    nose_width: float        = 5.0 * mm
    nose_height: float       = 2.5 * mm
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
        
    if P.show_nose:
        define(nose, "#00ff00ff", "nose")
    
    with BuildPart() as base:
        with BuildSketch(Plane.XY) as bottom_sketch:
            Circle(P.base_diameter/2)
        extrude(amount=P.base_height, mode=Mode.ADD)
        
        add(nose.part.rotate(Axis.Y, 180-15).rotate(Axis.X, 180).rotate(Axis.Z, 50))
        
        #TODO: add hole in the base
        
        edges = base.edges().filter_by(lambda e: e)
        for index, edge in enumerate(edges):
            if False:
                define(edge, "#00cc00ff", f"edges_{index}") 
        if P.do_fillet:
            fillet(edges[2],.6)
            fillet(edges[8],1.)
            fillet(edges[11],1.)
        
        Cylinder(radius=1.5 * mm, height=P.base_height + 5 * mm, mode=Mode.SUBTRACT)
        
        edges = base.edges().filter_by(lambda e: e)
        for index, edge in enumerate(edges):
            if index >= 0:
                define(edge, "#00cc00ff", f"edgesX_{index}") 
        if P.do_fillet:
            chamfer(edges[36], 2. * mm)
            
            
            
        
    define(base, "#0000aaff", "base")

    # Show the box
    show(*objects)
    
    # Export the box if do_export is True
    if P.do_export:
        debug("Exporting model")
        id = f'{P.base_diameter}x{P.base_height}mm_{P.nose_length}x{P.nose_width}x{P.nose_height}mm'

        export_name = __file__ \
                        .replace('{identifier}', id) \
                        .replace('.py', '.stl')
        export_path = Path(__file__).parent / export_name
        console.log(f"[green]Model exported to {export_path}[/green]")
        exporter = Mesher()
        exporter.add_shape(base.part)
        exporter.write(export_path)
        del exporter        