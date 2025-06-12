# -*- coding: utf-8 -*-
"""
----
file-name:      cmf_phone_belta_{identifier}.py
file-uuid:      0f73bcdb-84d0-4426-b65e-39e6c87e3ffe
description:    Ideas for cmf phone pro
author:         felix@42sol.eu
project:
    name:       model123d
    uuid:       fe521ba0-4ad7-484d-9386-26de71379e15
    url:        https://www.github.com/42sol/model123d
"""


# %% [Imports]
from build123d import *

from ocp_vscode import show, set_defaults, Camera
from pathlib import Path
from math import sqrt
from copy import deepcopy as copy

# %% [Local imports]
from helper import *
from external import load_imports
from parameter import *
from phone_model import build_phone_model, get_phone_objects
from phone_addons import get_addon_objects
from phone_backplate import build_phone_backplate, get_backplate_objects
from export import export_all


P = Parameters()
# set_defaults(reset_camera=Camera.KEEP,)

# %% [Imports]
if P.do_imports:
    debug("Loading imports")
    objects = load_imports()

set_defaults(
    reset_camera=Camera.KEEP,)

# %% [Build phone model]
debug("Creating model")
display_cutout, display, phone, addons = build_phone_model(P)
screws, backplate, charger, charger_frame = build_phone_backplate(P)

# %% [build arm model]





P_belta_thickness: float = 4.8 * mm
P_belta_width: float = P.body_width + P_belta_thickness * 2 * mm
P_belta_height: float = P.body_height + P_belta_thickness * mm
P_belta_extrude: float = P.body_extrude + P.backplate_extrude + P_belta_thickness + 2 * mm
points_top = [
    (0.0,                 P_belta_height * 1.25),
    (0.0,                 P_belta_height * 1.8),
    (P_belta_width * 1.2, P_belta_height * 1.8),
    (P_belta_width * 1.2, P_belta_height * 1.25),
]
points_inner = [
    (P_belta_width * 0.0, P_belta_height * 0.1),
    (P_belta_width * 0.0, P_belta_height * 0.7),
    (P_belta_width * 1.0, P_belta_height * 0.6),
    (P_belta_width * 1.0, P_belta_height * 0.7),
]

with BuildPart() as stitch:
    with BuildSketch() as sketch:
        Circle(0.75, align=(Align.CENTER, Align.MIN))
    extrude(amount=10 * P_belta_extrude, mode=Mode.ADD)
stitch_x = stitch.part.rotate(Axis.Y, 90)

with BuildPart() as case:
    with BuildSketch(Plane.XY) as bottom_sketch:
        RectangleRounded(
            P_belta_width, P_belta_height, P.body_radius, align=(Align.MIN, Align.MIN)
        )
    extrude(amount=P_belta_extrude + 2.0, mode=Mode.ADD)

    with BuildSketch(Plane.XY.offset(P_belta_thickness / 2)) as inner_cut:
        with Locations((P_belta_thickness - 2, P_belta_thickness - 2)):
            RectangleRounded(
                P_belta_width - P_belta_thickness - 2,
                P_belta_height,
                P.body_radius,
                align=(Align.MIN, Align.MIN),
            )
    extrude(amount=P.body_extrude + P.backplate_extrude + 4.0, mode=Mode.SUBTRACT)

    with BuildSketch(Plane.XY.offset(P_belta_thickness / 2)) as top_right_cut:
        with Locations((P_belta_width * 0.5, P_belta_height)):
            Polygon(*points_top)

    extrude(amount=P_belta_extrude, mode=Mode.SUBTRACT)


    faces_X = case.part.faces().filter_by(Axis.X)
    # left_l = faces_X[2]
    # left_r = faces_X[1]
    faces_Y = case.part.faces().filter_by(Axis.Y)
    # bottom = faces_Y[1]
    faces_Z = case.part.faces().filter_by(Axis.Z)
    # up_b = faces_Z[4]
    # up_t = faces_Z[7]

    # Vertical mole
    with BuildSketch(Plane.XY) as molle1_xy:
        with Locations(
            (P_belta_width * 0.5, P_belta_height * 0.86),
            (P_belta_width * 0.5, P_belta_height * 0.14),
        ):
            with GridLocations(38.0, 25.0, 2, 2):
                RectangleRounded(30.0, 10.0, 2.0)
    extrude(amount=5*P_belta_thickness, mode=Mode.SUBTRACT)

    # Horizontal mole
    with BuildSketch(Plane.XY) as molle2_xy:
        with Locations(
            (P_belta_width * 0.5, P_belta_height * 0.5),
        ):
            with GridLocations(2*25.+25, 38.0, 2, 2):
                RectangleRounded(6.0, 30.0, 2.0)
    extrude(amount=4*P_belta_thickness, mode=Mode.SUBTRACT)

    with BuildSketch(Plane.ZY.offset(P_belta_width/2)) as side_hole:
        with Locations(
            ((P_belta_extrude + P_belta_thickness/2.) * 0.5, 103.4),
            ((P_belta_extrude + P_belta_thickness/2.) * 0.5, 103.4-38.0),
            ((P_belta_extrude + P_belta_thickness/2.) * 0.5, 103.4-76.0),
        ):
            RectangleRounded(10.0, 30.0, 2.0)
    extrude(amount=-2*P_belta_width, mode=Mode.SUBTRACT)
    
    
    with BuildSketch(faces_Y[1].offset(-P_belta_thickness)) as bottom_sketch:
        with GridLocations(23., 1, 3, 1):
            RectangleRounded(20.0, 10.0, 2.0)
    extrude(amount=2*P_belta_thickness, mode=Mode.SUBTRACT)
    
    edges = case.part.edges().filter_by(lambda e: e.length == 26.)

    long_molle_edges = case.part.edges().filter_by(lambda e: e.length == 26)
    short_molle_edges = case.part.edges().filter_by(lambda e: e.length == 10.)
    other_edges = case.part.edges().filter_by(lambda e: e not in long_molle_edges and e not in short_molle_edges and e.length >10.)
    P.do_post_processing = yes
    if P.do_post_processing:
        for index, edge in enumerate(long_molle_edges):
            if index < 89:
                if index % 2 == 1:
                    print(f"Filleting long molle edge {index}")
                    fillet(edge, 1.0)
                
        chamfer_tool = 2.0
        chamfer(other_edges[0], chamfer_tool)
        chamfer(other_edges[2], chamfer_tool)

    with BuildSketch(Plane.XY.offset(-2)) as patch:
        with Locations(
            (P_belta_width * 0.5, P_belta_height * 0.475),
        ):
            Circle(30.0, align=(Align.CENTER, Align.CENTER))
    extrude(amount=2*P_belta_extrude, mode=Mode.SUBTRACT)
    circle_edge = case.part.edges().filter_by(lambda e: e.length > 187 and e.length < 190)
    if P.do_post_processing:
        for index, edge in enumerate(circle_edge):
            print(f"Filleting circle edge {index}")
            fillet(edge, 1.0)
    

addons = get_addon_objects()
location = Location((P_belta_thickness, P_belta_thickness, 4.2))
for element in [phone, display, backplate, screws] + list(addons.values()):
    if isinstance(element, Part):
        element.move(location)
    elif type(element) is dict:
        for sub_element in element.values():
            if isinstance(sub_element, Part):
                sub_element.move(location)
            else:
                sub_element.part.move(location)
    else:
        element.part.move(location)

define(case, "#f4f44b2c", "belta.case", alpha=0.8)
faces_X = case.part.faces().filter_by(Axis.X)
# left_l = faces_X[2]
# left_r = faces_X[1]
faces_Y = case.part.faces().filter_by(Axis.Y)
# bottom = faces_Y[1]
faces_Z = case.part.faces().filter_by(Axis.Z)
# up_b = faces_Z[4]
# up_t = faces_Z[7]

objects = {
    "phone": get_phone_objects(),
    "backplate": get_backplate_objects(),
    "belta": {
        "case": case.part,
        #"patch": patch,
        #'left_l': left_l,
        #'left_r': left_r,
        #'bottom': bottom,
        #'up_t': up_t,
        #'up_b': up_b,
        "faces": colorize_named_faces(case),
        'edges': colorize_edges(long_molle_edges),
    }
}

# % % [show objects]
try:
    show(objects, port=3940)
except ImportError:
    print("ocp_vscode.show not available. Model built but not displayed.")

## %% [Export objects]

P.do_export = yes
if P.do_export:
    # export_all(P, __file__, objects, console)
    try:
        mesher = Mesher()
        mesher.add_shape(case.part)
        mesher.write(Path(__file__).parent / "belta_case.stl")
    except AttributeError:
        pass

# %% [End of file]
