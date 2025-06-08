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

#%% [Imports]
from build123d import *

from ocp_vscode import show, show_object, set_defaults, Camera
from pathlib import Path
from rich.console import Console
from math import sqrt
from copy import deepcopy as copy

#%% [Local imports]
from helper import *
from external import load_imports
from parameter import Parameters  # Absolute import for direct script execution
from phone_model import build_phone_model, get_phone_objects
from phone_backplate import build_phone_backplate, get_backplate_objects
from export import export_all

P = Parameters()
set_defaults(reset_camera=Camera.KEEP,)

#%% [Imports]
if P.do_imports:
    debug("Loading imports")
    objects = load_imports()

#%% [Build phone model]
debug("Creating model") 
display_cutout, display, phone, addons = build_phone_model(P)
screws, backplate, charger, charger_frame = build_phone_backplate(P)

#%% [build arm model]
P_arm1_width: float = 4.0 * mm
P_arm2_width: float = 10.0 * mm
P_x_offset: float = 8.0 * mm
P_arm1_y_height: float = P.screw_y2 - P.screw_y1 + 10
P_arm2_x_height: float = P.screw_x4 - P.screw_x1 + 15
P_arm_extrude: float = 3.0 * mm

P_arm_z: float = P.body_extrude + P.backplate_extrude + 2

with BuildPart() as arm1_part:
    with BuildSketch(Plane.XZ) as sketch:
        with BuildLine() as arm1_line:
            l1 = Line( (P.screw_x1, P.screw_y1), (P.screw_x2, P.screw_y2))
            l2 = Line( (P.screw_x2, P.screw_y2), (P.screw_x4, P.screw_y4))
            l3 = Line( (P.screw_x4, P.screw_y4), (P.screw_x4, P.screw_y3))
            l4 = Line( (P.screw_x4, P.screw_y3), (P.screw_x3, P.screw_y3))
        a = Rectangle(3,2)
    sweep(transition=Transition.TRANSFORMED)
    

    
with BuildPart(Plane.XY.offset(P.body_extrude +  P.backplate_extrude)) as arm1:
    with Locations(
            Location((P.screw_x1-P_x_offset, P.screw_y2)),
        ):
        arm2 = Box(P_arm2_x_height, P_arm2_width, P_arm_extrude, align=(Align.MIN, Align.CENTER), mode=Mode.ADD)


front, back = arm2.faces().filter_by(Plane.XZ)


with BuildPart() as arm2:
    with BuildSketch(front) as sketch:
        RectangleRounded(3, 10, 1, align=(Align.CENTER, Align.CENTER), mode=Mode.ADD)
    extrude(amount=P_arm_extrude, mode=Mode.ADD)

define(arm1, "#ffa200ff", "belta.arm1")
define(arm2, "#33c043ff", "belta.arm2")

def get_marked_faces(part):
    """Returns a list of faces that are marked with a color."""
    faces = {}
    part_faces = part.faces()
    
    faces['top'] = part_faces.filter_by(Plane.XY)[0]
    faces['top'].color = "#ff0000aa"  # Mark the top face with a specific color
    faces['bottom'] = part_faces.filter_by(Plane.XY)[1]
    faces['bottom'].color = "#1a2ede75"  # Mark the top face with a specific color
    faces['left'] = part_faces.filter_by(Plane.YZ)[0]
    faces['left'].color = "#62babaff"  # Mark the left face with a specific color
    faces['right'] = part_faces.filter_by(Plane.YZ)[1]
    faces['right'].color = "#09ff0086"  # Mark the left face with a specific color
    faces['front'] = part_faces.filter_by(Plane.XZ)[0]
    faces['front'].color = "#eeff00"  # Mark the front face with a specific color
    faces['back'] = part_faces.filter_by(Plane.XZ)[1]
    faces['back'].color = "#ff00fba5"  # Mark the back face with a specific color
    
    return faces

objects = \
    {
            "phone": get_phone_objects(),
            "backplate": get_backplate_objects(),
            "belta": {
                'arm1_line': arm1_line,
                #'arm2_line': arm2_line,
                #'arm3_line': arm3_line,
                #'arm4_line': arm4_line,
                'arm1': arm1_part,
                #'arm2': arm2_part,
                #'arm3': arm3_part,
                #'arm4': arm4_part,
                'faces': get_marked_faces(arm1)
            },
    }

#% % [show objects]
try:
    show(objects, glass=yes)
except ImportError:
    print("ocp_vscode.show not available. Model built but not displayed.")
#%% [Export objects]

export_all(P, objects, console)

# %%
