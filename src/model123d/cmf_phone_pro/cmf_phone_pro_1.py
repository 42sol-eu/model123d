"""
----
file-name:      cmf_phone_pro_{identifier}.py
file-uuid:      0f73bcdb-84d0-4426-b65e-39e6c87e3ffe
description:    Ideas for cmf phone pro
author:         felix@42sol.eu
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
false = False
true = True

# [Helpers]
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
    show_nose: bool        = no
    do_fillet: bool        = no
    do_export: bool        = yes
    
    # Device dimensions
    body_height: float            = 163.78 * mm # TODO: fix height
    body_radius: float            =   9. * mm
    body_width: float             =  78.0 * mm
    body_extrude: float           =   7.8 * mm
    hole_diameter: float          =   2.0 * mm

    # Screw dimensions
    screw_diameter: float         =   2.2 * mm
    screw_y1: float               =  18.1 + 98.43 * mm
    screw_x1: float               =   3.9 * mm
    screw_y2: float               =  18.1 * mm
    screw_x2: float               =   3.9 * mm
    screw_y3: float               =  98.43 * mm
    screw_x3: float               =  78.0 - 3.9 * mm
    screw_y4: float               =  18.1 + 43.58 + 98.43 * mm
    screw_x4: float               =  3.9 + 23.96 * mm
    
    # Extension dimensions
    ext_position_y: float         =  10. * mm
    ext_position_x: float         =  78. - 10. * mm
    ext_diameter: float           =  2.5 * mm
    
    # Charger dimensions
    charger_position_x: float     =  78. / 2. * mm
    charger_position_y: float     =  75. * mm
    charger_inner_diameter: float =  50. * mm
    charger_outer_diameter: float =  54. * mm
    
    # Camera dimensions
    camera1_x: float         =  3.9 + 23.96 * mm
    camera1_y: float         =  142.5 * mm
    camera1_w: float         =  10.6 * mm
    camera1_h: float         =  22.0 * mm
    camera1_r: float         =   5.0 * mm

    camera2_x: float         =  11. * mm
    camera2_y: float         =  153.5 * mm
    camera2_diameter: float  =  19. * mm

    camera3_x: float         =  11. * mm
    camera3_y: float         =  153.5 - 22. * mm
    camera3_diameter: float  =  19. * mm

    camera4_x: float         =  11. * mm
    camera4_y: float         =  142.5 * mm
    camera4_w: float         =  20. * mm
    camera4_h: float         =  22. + 19. * mm
    camera4_r: float         =   9.5 * mm



P = Parameters()

# [Calculate parameters]


# [Main]    
if __name__ == "__main__":    
    # [Model]
    debug("Creating model") 
    with BuildPart() as phone:
        with BuildSketch(Plane.XY) as bottom_sketch:
            RectangleRounded(P.body_width, P.body_height, P.body_radius,
                            align=(Align.MIN, Align.MIN))

            with Locations(
                (P.screw_x1, P.screw_y1),
                (P.screw_x2, P.screw_y2),
                (P.screw_x3, P.screw_y3),
                (P.screw_x4, P.screw_y4),
                ):
                Circle(P.screw_diameter/2, mode=Mode.SUBTRACT)
                
            with Locations(
                (P.ext_position_x, P.ext_position_y)):
                Circle(P.ext_diameter/2, mode=Mode.SUBTRACT)

            with Locations(
                (P.charger_position_x, P.charger_position_y)):
                Circle(P.charger_outer_diameter/2, mode=Mode.SUBTRACT)
                Circle(P.charger_inner_diameter/2, mode=Mode.ADD)
        
            with Locations(
                (P.camera1_x, P.camera1_y)):
                RectangleRounded(P.camera1_w, P.camera1_h, P.camera1_r, mode=Mode.SUBTRACT)
            with Locations(
                (P.camera1_x, P.camera1_y+P.camera1_h/4)):
                Circle(P.camera1_r-0.5, mode=Mode.ADD)
            with Locations(
                (P.camera1_x, P.camera1_y-P.camera1_h/4)):
                Circle(P.camera1_r/2, mode=Mode.ADD)

            with Locations(
                (P.camera4_x, P.camera4_y)):
                RectangleRounded(P.camera4_w, P.camera4_h, P.camera4_r, mode=Mode.SUBTRACT)
                
            with Locations(
                (P.camera2_x, P.camera2_y)):
                Circle(P.camera2_diameter/2, mode=Mode.ADD)
                Circle((P.camera2_diameter-5)/2, mode=Mode.SUBTRACT)

            with Locations(
                (P.camera3_x, P.camera3_y)):
                Circle(P.camera3_diameter/2, mode=Mode.ADD)
                Circle((P.camera3_diameter-5)/2, mode=Mode.SUBTRACT)
        
        extrude(amount=P.body_extrude, mode=Mode.ADD)

    if 0:    
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
        
        
        edges = base.edges().filter_by(lambda e: e)
        for index in range(len(edges)):
            if P.show_selection:
                define(edges[index], "#ff0000ff", f"edges_{index}")
        if P.do_fillet:
            pass
            # fillet(edges[3],.6)
            # chamfer(edges[32],2.)
            # chamfer(edges[36],2.)

    define(phone, "#0000aaff", "phone")

    # Show the box
    show(*objects)
    
    # Export the box if do_export is True
    if P.do_export:
        debug("Exporting model")
        id = f'1'

        export_name = __file__ \
                        .replace('{identifier}', id) \
                        .replace('.py', '.stl')
        export_path = Path(__file__).parent / export_name
        console.log(f"[green]Model exported to {export_path}[/green]")
        exporter = Mesher()
        exporter.add_shape(phone.part)
        exporter.write(export_path)
        del exporter        