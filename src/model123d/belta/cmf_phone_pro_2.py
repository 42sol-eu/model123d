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

from ocp_vscode import show, show_object, set_defaults, Camera, set_colormap, ColorMap
from ocp_vscode.colors import ListedColorMap
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
import colorsys
import random

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

def colorize_named_faces(part):
    """
    Colors all faces of a part that are named 'face_X_{counter}'.
    Each axis (X, Y, Z) gets a different color palette.
    """

    axis_colors = {
        'X': (0.0, 1.0, 1.0),   # Red
        'Y': (0.33, 1.0, 1.0),  # Green
        'Z': (0.66, 1.0, 1.0),  # Blue
    }
    colored_faces = {}
    colors = ColorMap.tab20()
    for axis, (h, s, v_base) in axis_colors.items():
        if axis == 'X':
            faces = part.faces().filter_by(Axis.X)
        elif axis == 'Y':
            faces = part.faces().filter_by(Axis.Y)
        elif axis == 'Z':
            faces = part.faces().filter_by(Axis.Z)
        else:
            continue
        
        for idx, face in enumerate(faces):
            face.name = f"face_{axis}_{idx}"
            # Vary the value for each counter
            v = 0.5 + 0.5 * ((idx % 10) / 10)
            rgb = colorsys.hsv_to_rgb(h, s, v)
            hex_color = '#{:02x}{:02x}{:02x}ff'.format(
                int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255)
            )
            face.color = colors.__next__()
            colored_faces[face.name] = face
    return colored_faces

def colorize_edges_of_face(face):
    """
    Assigns a unique color to every edge in the given face.
    Returns a dictionary mapping edge names to edge objects.
    """

    colored_edges = {}
    for idx, edge in enumerate(face.edges()):
        # Generate a random color for each edge
        color = "#{:06x}ff".format(random.randint(0, 0xFFFFFF))
        edge.name = f"edge_{idx}"
        edge.color = color
        colored_edges[edge.name] = edge
    return colored_edges

P_belta_thickness: float = 5.0 * mm
P_belta_width: float = P.body_width + P_belta_thickness * 2 * mm
P_belta_height: float = P.body_height + P_belta_thickness * 2 * mm
P_belta_extrude: float =  P.body_extrude + P.backplate_extrude + P_belta_thickness * mm
points_top = [
    (0., P_belta_height * 0.9),
    (0., P_belta_height * 1.2),
    (P_belta_width * 1.2, P_belta_height * 1.2),  
    (P_belta_width * 1.2, P_belta_height * 0.5),
]
points_inner = [
    (P_belta_width * 0., P_belta_height * 0.1),
    (P_belta_width * 0., P_belta_height * 0.7),
    (P_belta_width * 1., P_belta_height * 0.4),  
    (P_belta_width * 1., P_belta_height * 0.1),
]

with BuildPart() as stitch:
    with BuildSketch() as sketch:
        Circle(0.75, align=(Align.CENTER, Align.MIN))
    extrude(amount=10*P_belta_extrude, mode=Mode.ADD)
stitch_x = stitch.part.rotate(Axis.Y, 90)

with BuildPart() as case:
    with BuildSketch(Plane.XY) as bottom_sketch:
        RectangleRounded(   P_belta_width, P_belta_height, P.body_radius,
                            align=(Align.MIN, Align.MIN))
    extrude(amount=P_belta_extrude+2.0, mode=Mode.ADD)
    
    with BuildSketch(Plane.XY.offset(P_belta_thickness/2)) as inner_cut:
        with Locations((P_belta_thickness-2, P_belta_thickness-2)):
            RectangleRounded(   P_belta_width-P_belta_thickness-2, 
                                P_belta_height,
                                P.body_radius,
                                align=(Align.MIN, Align.MIN))
    extrude(amount=P.body_extrude + P.backplate_extrude + 2.0, mode=Mode.SUBTRACT) 
    
    with BuildSketch(Plane.XY.offset(P_belta_thickness/2)) as top_right_cut:
        with Locations((P_belta_width * 0.5, P_belta_height * 0.75)):
            Polygon(*points_top)
            
    extrude(amount=P_belta_extrude, mode=Mode.SUBTRACT) 

    with BuildSketch(Plane.XY.offset(P_belta_extrude/2+P_belta_thickness/2)) as top_inner_sketch:
        with Locations((P_belta_width * 0.5, P_belta_height * 0.35)):
            Polygon(*points_inner)
            
    extrude(amount=P_belta_extrude, mode=Mode.SUBTRACT) 

    with BuildSketch(Plane.XY.offset(P_belta_extrude+0)) as top_inner_sketch:
        with Locations((P_belta_width * 0.5, 10.0 + P_belta_height * 0.35)):
            Polygon(*points_inner)
            
    extrude(amount=P_belta_extrude, mode=Mode.SUBTRACT) 
    
    
    with Locations( Location((0, 8.8, 3.0)) ):
        Box(1.5,114.3,10.0,align=(Align.MIN, Align.MIN, Align.MIN), mode=Mode.SUBTRACT)

    with Locations( Location((P_belta_width-1.5, 8.8, 3.0)) ):
        Box(1.5,62.0,10.0,align=(Align.MIN, Align.MIN, Align.MIN), mode=Mode.SUBTRACT)

    faces_X = case.part.faces().filter_by(Axis.X)
    left_l = faces_X[2]
    left_r = faces_X[1]
    faces_Y = case.part.faces().filter_by(Axis.Y)
    bottom = faces_Y[1]
    faces_Z = case.part.faces().filter_by(Axis.Z)
    up_b = faces_Z[4]
    up_t = faces_Z[7]
    edges = up_t.edges()
    fillet(edges[1], 1)
    fillet(edges[3], 1)
    
    with Locations( 
            Location((0, P_belta_height * 0.05, P_belta_extrude / 2 - 0.5)),
            Location((0, P_belta_height * 0.1, P_belta_extrude / 2 - 0.5)),
            Location((0, P_belta_height * 0.15, P_belta_extrude / 2 - 0.5)),
            Location((0, P_belta_height * 0.2, P_belta_extrude / 2 - 0.5)),
            Location((0, P_belta_height * 0.25, P_belta_extrude / 2 - 0.5)),
            Location((0, P_belta_height * 0.3, P_belta_extrude / 2 - 0.5)),
            Location((0, P_belta_height * 0.35, P_belta_extrude / 2 - 0.5)),
            Location((0, P_belta_height * 0.395, P_belta_extrude / 2 - 0.5)),
            Location((0, P_belta_height * 0.45, P_belta_extrude / 2 - 0.5)),
            Location((0, P_belta_height * 0.5, P_belta_extrude / 2 - 0.5)),
            Location((0, P_belta_height * 0.55, P_belta_extrude / 2 - 0.5)),
            Location((0, P_belta_height * 0.6, P_belta_extrude / 2 - 0.5)),
            Location((0, P_belta_height * 0.65, P_belta_extrude / 2 - 0.5)),
            Location((0, P_belta_height * 0.69, P_belta_extrude / 2 - 0.5)),
            
        ):
        add(stitch_x, mode=Mode.SUBTRACT)
    
        
    
case.part.move(Location((-P_belta_thickness, -P_belta_thickness, -2.2)))
define(case, "#f4f44b2c", "belta.case", alpha=0.8)
faces_X = case.part.faces().filter_by(Axis.X)
left_l = faces_X[2]
left_r = faces_X[1]
faces_Y = case.part.faces().filter_by(Axis.Y)
bottom = faces_Y[1]
faces_Z = case.part.faces().filter_by(Axis.Z)
up_b = faces_Z[4]
up_t = faces_Z[7]

objects = \
    {
            "phone": get_phone_objects(),
            "backplate": get_backplate_objects(),
            "belta": {
                'case': case.part,
                'left_l': left_l,
                'left_r': left_r,
                'bottom': bottom,
                'up_t': up_t,
                'up_b': up_b,
                'faces': colorize_named_faces(case),
                # 'edges': colorize_edges_of_face(case.part),
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
