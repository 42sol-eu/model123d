"""
----
file-name:      recorder_{identifier}.py
file-uuid:      c5e2823a-ebb0-44e0-a35f-cdc51494fb06
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
    show_selection: bool   = no
    do_fillet: bool         = yes
    do_export:  bool       = yes
    device_bottom_width: float     = 76.0 * mm
    device_top_width: float = 45.0 * mm
    
    device_height: float   = 14.0 * mm
    hole_diameter: float   = 12.0 * mm
P = Parameters()

# [Main]    
if yes or __name__ == "main":
    debug("Running main")
    
    # [Model]
    debug("Creating model")            
    with BuildPart() as base:
        with BuildSketch(Plane.XY) as bottom_sketch:
            Circle(P.device_bottom_width/2)
        with BuildSketch(Plane.XY.offset(P.device_height-1)) as top_sketch:
            Circle(P.device_top_width/2) 
        loft()

        with BuildSketch(Plane.XY.offset(P.device_height-1)) as top_sketch:
            Circle(P.device_top_width/2-4)
        extrude(amount=2, mode=Mode.ADD)

        with BuildSketch(Plane.XY) as bottom_cut_sketch:
            Circle(P.device_bottom_width/2-3)
        with BuildSketch(Plane.XY.offset(P.device_height-4)) as top_cut_sketch:
            Circle(P.device_top_width/2-3) 
        loft(mode=Mode.SUBTRACT)
        
        with BuildPart(Plane.XY.offset(P.device_height-4)) as strenght:
            Box(P.device_top_width, 8, 4)
            Box(8, P.device_top_width, 4)
            Cylinder(P.hole_diameter/2+4, 4)

        edges = base.edges().filter_by(lambda e: e.length > 50)
        for index, edge in enumerate(edges):
            define(edge, "#0000aaff", f"edges_{index}") 
        if P.do_fillet:
            fillet(edges[0],.5)
            fillet(edges[1],.5)
            fillet(edges[2],1)
            fillet(edges[4],1)
                
    
        with BuildSketch(Plane.XY) as magnet_sketch:
            Circle(P.hole_diameter/2)
        extrude(amount=P.device_height*2, mode=Mode.SUBTRACT)

        
    define(base, "#0000aaff", "base")

    # Show the box
    show(*objects)
    
    # Export the box if do_export is True
    if P.do_export:
        debug("Exporting model")
        id = f'{P.device_bottom_width}'

        export_name = __file__ \
                        .replace('{identifier}', id) \
                        .replace('.py', '.stl')
        export_path = Path(__file__).parent / export_name
        console.log(f"[green]Model exported to {export_path}[/green]")
        exporter = Mesher()
        exporter.add_shape(base.part)
        exporter.write(export_path)
        
# [End of file]      