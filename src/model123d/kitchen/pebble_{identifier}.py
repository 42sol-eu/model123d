"""
----
file-name:      pebble_{identifier}.py
file-uuid:      4e0d1190-2d81-418e-845a-d14dfe70202c
description:   A pebble shaped object with a button cutout and optional fillet and band cuts.

project:
    name:       model123d
    uuid:       fe521ba0-4ad7-484d-9386-26de71379e15
    url:        https://www.github.com/42sol/model123d
"""

# [Imports]
from build123d import *  # [docs](https://build123d.readthedocs.io/en/latest/cheat_sheet.html)
from build123d import MM as mm
from ocp_vscode import show
from dataclasses import dataclass
from pathlib import Path
import sys
from rich.console import Console
from math import sqrt

# [Constants]
no = False
yes = True

# [Setup]
console = Console()
objects = []


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
    show_debug: bool  = yes
    do_export:  bool  = no
    width:      float  = 20.0 * mm
    device_height:     float  = 76.5 * mm
    depth:      float  = 12.0 * mm
    
    def __init__(self):
        debug("Initializing parameters")

P = Parameters()

# [Pebble Shape]
with BuildPart() as pebble:
    # Create a base sphere
    length = P.device_height
    a = Sphere(radius=length / 2)
    define(a, color="#ff0000aa", name="Base Sphere")
    # Cut a button-like feature on the top
    with Locations(Location([0, 0, length / 4])):
        Cylinder(radius=length/2, height=length/2, mode=Mode.SUBTRACT)
    # Optionally add fillets to edges
    if P.device_height > 5 * mm:
        fillet(pebble.edges(), radius=length/5 * mm)
    with Locations(Location([0, 0, +2.0])):
        b = Cylinder(radius=length/2, height=length/4, mode=Mode.SUBTRACT)
    define(b, color="#00ffaa", name="Button Cutout")
    
define(pebble, color="#00ff00", name="Pebble Shape")

# Export or visualize the result
if P.do_export:
    pebble.part.export_step(Path(__file__).with_suffix(".stl"))
else:
    show(objects)
