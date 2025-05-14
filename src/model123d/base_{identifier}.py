"""
----
file-name:      recorder_{identifier}.py
file-uuid:      
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
    show_debug: bool      = yes
    show_selection: bool  = no
    do_export:  bool      = yes
    shape: str            = "round" # "round" | "hexagon"
    device_width: float   = 25.0 * mm
    
    shape: str            = "hexagon"
    device_width: float   = 45.0 * mm
    
    device_height: float  = 3.0 * mm
    magnet_diameter: float = 10.0 * mm
    magnet_height: float = 2.5 * mm
P = Parameters()
# [Main]    
if yes or __name__ == "main":
    debug("Running main")
    
    # [Model]
    debug("Creating model")            
    with BuildPart() as base:
        match P.shape:
            case "round":
                with BuildSketch(Plane.XY) as outer_sketch:
                    Circle(P.device_width/2)
                extrude(amount=P.device_height)
                edges = base.edges().sort_by(Axis.Z)[-1]
                define(edges, "#0000aaff", "outer_edges")
                fillet(edges, 0.5)
                
            
            case "hexagon":
                with BuildSketch(Plane.XY) as sketch:
                    RegularPolygon(P.device_width/2, 6)
                extrude(amount=P.device_height)
                
                edges = base.faces().sort_by(Axis.Z)[-1].edges()
                define(edges, "#0000aaff", "outer_edges")
                fillet(edges, 0.5)
                
                edges = base.edges().filter_by(Plane.YZ)
                define(edges, "#00aa00ff", "standing_edges")
                fillet(edges, 1.0)
            
            case _:
                console.log(f"[red]Unknown shape: {P.shape}[/red]")

        with BuildSketch(Plane.XY) as magnet_sketch:
            Circle(P.magnet_diameter/2)
        extrude(amount=P.magnet_height, mode=Mode.SUBTRACT)

        
    define(base, "#0000aaff", "base")

    # Show the box
    show(*objects)
    
    # Export the box if do_export is True
    if P.do_export:
        debug("Exporting model")
        match P.shape:
            case "round":
                id = f'round_{P.device_width}'
            case "hexagon":
                id = f'hexagon_{P.device_width}'
            case _:
                console.log(f"[red]Unknown shape: {P.shape}[/red]")
                id = f'unknown_{P.device_width}'

        export_name = __file__ \
                        .replace('{identifier}', id) \
                        .replace('.py', '.stl')
        export_path = Path(__file__).parent / export_name
        console.log(f"[green]Model exported to {export_path}[/green]")
        exporter = Mesher()
        exporter.add_shape(base.part)
        exporter.write(export_path)
        del exporter        