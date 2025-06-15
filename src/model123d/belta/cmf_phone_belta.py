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

# %% [setup parameters]

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

# %% [Build case base]
with BuildPart() as top_case:
    with BuildSketch(Plane.XY) as top_sketch:
        with Locations((-P_belta_thickness, -P_belta_thickness)):
            RectangleRounded(
                P_belta_width + 2 * P_belta_thickness,
                P_belta_height * 0.775,
                P_belta_extrude * 1.05,
                align=(Align.MIN, Align.MIN, Align.MIN),
            )
    extrude(amount=P_belta_extrude + P_belta_thickness, 
            mode=Mode.ADD)

    with BuildSketch(Plane.XY) as bottom_sketch:
        with Locations(
            (-P_belta_thickness, P_belta_height * 0. - P_belta_thickness),
            (P_belta_width-21.8-P_belta_thickness, P_belta_height * 0. - P_belta_thickness)
        ):
            RectangleRounded(
                P_belta_extrude * 2.15,
                P_belta_height * 0.775,
                P_belta_extrude * 1.05,
                align=(Align.MIN, Align.MIN, Align.MIN),
            )
        with Locations(
            (+P_belta_thickness+6, -14)
        ):
            Rectangle(  66.0, P_belta_height*1.4, align=(Align.MIN, Align.MIN), 
                        mode=Mode.SUBTRACT)
    extrude(amount=-P_belta_thickness*0.5, 
            mode=Mode.ADD).move(Location((0,0, -P_belta_extrude)))

    with BuildSketch(Plane.XY) as bottom_sketch:
        RectangleRounded(
            P_belta_width, P_belta_height, P.body_radius, align=(Align.MIN, Align.MIN)
        )
    extrude(amount=P_belta_extrude + 2.0, mode=Mode.SUBTRACT)

    with BuildSketch(Plane.ZY.offset(P_belta_width/2)) as side_hole:
        with Locations(
            ((P_belta_extrude + P_belta_thickness/2.) * 0.5, 103.4),
            ((P_belta_extrude + P_belta_thickness/2.) * 0.5, 103.4-38.0),
            ((P_belta_extrude + P_belta_thickness/2.) * 0.5, 103.4-76.0),
        ):
            RectangleRounded(10.0, 30.0, 2.0)
    extrude(amount=-2*P_belta_width, mode=Mode.SUBTRACT)

    # Horizontal mole
    with BuildSketch(Plane.XY) as molle2_xy_top:
        with Locations(
            (P_belta_width * 0.5, P_belta_height * 0.5),
        ):
            with GridLocations(2*25.+25, 38.0, 2, 2):
                RectangleRounded(6.0, 30.0, 2.0)
    extrude(amount=P_belta_thickness*0.5, mode=Mode.ADD)



    with Locations(
        ((P_belta_width) * 0.5, (P_belta_height-2*P_belta_thickness) * 0.5, P_belta_extrude-2),
        ):
        spacer = Cylinder(
            radius=59./2.,
            height= 1.2*P_belta_thickness,
            mode=Mode.ADD,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        )



    long_molle_edges_top = top_case.part.edges().filter_by(lambda e: e.length == 26).sort_by(Axis.X)
    short_molle_edges_top = top_case.part.edges().filter_by(lambda e: e.length == 10.)
    other_edges = top_case.part.edges().filter_by(lambda e: e not in long_molle_edges_top and e not in short_molle_edges_top and e.length >10.)

    faces_Y = top_case.part.faces().filter_by(Axis.Y)
    with BuildSketch(faces_Y[0].offset(-P_belta_thickness)) as bottom_sketch:
        with GridLocations(23., 1, 3, 1):
            RectangleRounded(20.0, 10.0, 2.0)
    extrude(amount=2*P_belta_thickness, mode=Mode.SUBTRACT)
    
    P.do_post_processing = yes
    if P.do_post_processing:
        for index, edge in enumerate(long_molle_edges_top):
            if index <= 18 or index >= 22:
                if index % 2 == 1 and index not in [15,17]:
                    fillet(edge, 1.0)
                    
        chamfer(spacer.edges()[-1], 3.0)



    
    
    top_case.part.faces().filter_by(Axis.Z)[0].color = (1, 0, 0)
define(top_case, "#f4f44b2c", "belta.top_case", alpha=0.8)
# %% [Build case]

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
    faces_Y = case.part.faces().filter_by(Axis.Y)
    faces_Z = case.part.faces().filter_by(Axis.Z)
    
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
                    fillet(edge, 1.0)
                
        chamfer_tool = 2.0
        chamfer(other_edges[0], chamfer_tool)
        chamfer(other_edges[2], chamfer_tool)

    with Locations(
        ((P_belta_width) * 0.5, (P_belta_height-2*P_belta_thickness) * 0.5, -2),
        ):
        spacer = Cylinder(
            radius=59./2.,
            height= 2*P_belta_extrude,
            mode=Mode.SUBTRACT,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        )


    if P.do_post_processing:
        circle_edge = case.part.edges().filter_by(lambda e: e.length > 187 and e.length < 190)
    
        for index, edge in enumerate(circle_edge):
            fillet(edge, 1.0)

define(top_case, "#0000882c", "top", alpha=1.0)
    

addons = get_addon_objects()
location = Location((P_belta_thickness, P_belta_thickness, 4.2))
for element in [phone, display, backplate, screws, charger_frame] + list(addons.values()):
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

define(case, "#0000aa2c", "case", alpha=1.0)
faces_X = case.part.faces().filter_by(Axis.X)
faces_Y = case.part.faces().filter_by(Axis.Y)
faces_Z = case.part.faces().filter_by(Axis.Z)

objects = {
    "phone": get_phone_objects(),
    "backplate": get_backplate_objects(),
    "belta": {
        "case": case,
        "top": top_case,
        #"faces": colorize_named_faces(faces_Y),
        #"edges": colorize_edges(faces_Y),
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

        mesher = Mesher()
        mesher.add_shape(top_case.part)
        mesher.write(Path(__file__).parent / "belta_top_case.stl")

    except AttributeError:
        pass

# %% [End of file]
