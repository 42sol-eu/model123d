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





P_belta_thickness: float = 5.0 * mm
P_belta_width: float = P.body_width + P_belta_thickness * 2 * mm
P_belta_height: float = P.body_height + P_belta_thickness * mm
P_belta_extrude: float = P.body_extrude + P.backplate_extrude + P_belta_thickness + 2 * mm
points_top = [
    (0.0, P_belta_height * 0.9),
    (0.0, P_belta_height * 1.2),
    (P_belta_width * 1.2, P_belta_height * 1.2),
    (P_belta_width * 1.2, P_belta_height * 0.5),
]
points_inner = [
    (P_belta_width * 0.0, P_belta_height * 0.1),
    (P_belta_width * 0.0, P_belta_height * 0.7),
    (P_belta_width * 1.0, P_belta_height * 0.4),
    (P_belta_width * 1.0, P_belta_height * 0.1),
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
    extrude(amount=P.body_extrude + P.backplate_extrude + 2.0, mode=Mode.SUBTRACT)

    with BuildSketch(Plane.XY.offset(P_belta_thickness / 2)) as top_right_cut:
        with Locations((P_belta_width * 0.5, P_belta_height * 0.75)):
            Polygon(*points_top)

    extrude(amount=P_belta_extrude, mode=Mode.SUBTRACT)

    with BuildSketch(
        Plane.XY.offset(P_belta_extrude / 2 + P_belta_thickness / 2)
    ) as top_inner_sketch:
        with Locations((P_belta_width * 0.5, P_belta_height * 0.35)):
            Polygon(*points_inner)

    extrude(amount=P_belta_extrude, mode=Mode.SUBTRACT)

    with BuildSketch(Plane.XY.offset(P_belta_extrude + 0)) as top_inner_sketch:
        with Locations((P_belta_width * 0.5, 10.0 + P_belta_height * 0.35)):
            Polygon(*points_inner)

    extrude(amount=P_belta_extrude, mode=Mode.SUBTRACT)

    with Locations((0, 8.8, 3.0)):
        Box(
            1.5,
            114.3,
            12.0,
            align=(Align.MIN, Align.MIN, Align.MIN),
            mode=Mode.SUBTRACT,
        )

    with Locations((P_belta_width - 1.5, 8.8, 3.0)):
        Box(
            1.5, 
            62.0, 
            12.0, 
            align=(Align.MIN, Align.MIN, Align.MIN), 
            mode=Mode.SUBTRACT
        )

    faces_X = case.part.faces().filter_by(Axis.X)
    left_l = faces_X[2]
    left_r = faces_X[1]
    faces_Y = case.part.faces().filter_by(Axis.Y)
    bottom = faces_Y[1]
    faces_Z = case.part.faces().filter_by(Axis.Z)
    up_b = faces_Z[4]
    up_t = faces_Z[7]

    # Vertical mole
    with BuildSketch(Plane.XY) as molle_xy:
        with Locations(
            (P_belta_width * 0.5, P_belta_height * 0.85),
            (P_belta_width * 0.5, P_belta_height * 0.15),
        ):
            with GridLocations(38.0, 25.0, 2, 2):
                RectangleRounded(30.0, 10.0, 2.0)
    extrude(amount=P_belta_thickness, mode=Mode.SUBTRACT)

    # Horizontal mole
    with BuildSketch(Plane.XY) as molle_xy:
        with Locations(
            (P_belta_width * 0.5, P_belta_height * 0.5),
        ):
            with GridLocations(2*25., 38.0, 2, 2):
                RectangleRounded(10.0, 30.0, 2.0)
    extrude(amount=P_belta_thickness, mode=Mode.SUBTRACT)
    
    with BuildSketch(bottom) as charger_hole:
        with Locations(
            (0, -2),
        ):
            RectangleRounded(10.5, 6.5, 3.2)
    extrude(amount=-P_belta_extrude, mode=Mode.SUBTRACT)
    define(charger_hole, "#f4f44b2c", "charger", alpha=0.8)
    edges_1 = case.part.edges().filter_by(lambda e: e.length > 10)
    # Stiches XZ
    with Locations(
        Location((0, P_belta_height * 0.06, P_belta_extrude / 2 - 0.5)),
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

    # Stiches XY
    with BuildSketch(Plane.XY.offset(P_belta_extrude / 2 - 0.5)) as stiches_xy:
        with Locations(
            Location((P_belta_width * 0.05, P_belta_height * 0.660)),
            Location((P_belta_width * 0.1, P_belta_height * 0.645)),
            Location((P_belta_width * 0.15, P_belta_height * 0.630)),
            Location((P_belta_width * 0.2, P_belta_height * 0.615)),
            Location((P_belta_width * 0.25, P_belta_height * 0.600)),
            Location((P_belta_width * 0.3, P_belta_height * 0.585)),
            Location((P_belta_width * 0.35, P_belta_height * 0.570)),
            Location((P_belta_width * 0.4, P_belta_height * 0.555)),
            Location((P_belta_width * 0.45, P_belta_height * 0.540)),
            Location((P_belta_width * 0.5, P_belta_height * 0.525)),
            Location((P_belta_width * 0.55, P_belta_height * 0.510)),
            Location((P_belta_width * 0.6, P_belta_height * 0.495)),
            Location((P_belta_width * 0.65, P_belta_height * 0.480)),
            Location((P_belta_width * 0.7, P_belta_height * 0.465)),
            Location((P_belta_width * 0.75, P_belta_height * 0.451)),
            Location((P_belta_width * 0.8, P_belta_height * 0.436)),
            Location((P_belta_width * 0.85, P_belta_height * 0.422)),
            Location((P_belta_width * 0.9, P_belta_height * 0.408)),
            Location((P_belta_width * 0.95, P_belta_height * 0.394)),
        ):
            Circle(0.75, align=(Align.CENTER, Align.MIN), mode=Mode.ADD)
    extrude(amount=2 * P_belta_extrude, mode=Mode.SUBTRACT)
    with BuildSketch(Plane.XY.offset(P_belta_extrude / 2 + 6)) as stiches_xy:
        with Locations(Location((P_belta_width * 0.5, P_belta_height * 0.06))):
            Rectangle(P_belta_width - P_belta_thickness * 2.5, P_belta_thickness)
    extrude(amount=P_belta_thickness / 2 - 1, mode=Mode.ADD)

    with BuildSketch(Plane.XY.offset(P_belta_extrude / 2 - 0.5)) as stiches_xy:
        y = P_belta_height * 0.06
        with Locations(
            Location((P_belta_width * 0.1, y)),
            Location((P_belta_width * 0.15, y)),
            Location((P_belta_width * 0.2, y)),
            Location((P_belta_width * 0.25, y)),
            Location((P_belta_width * 0.3, y)),
            Location((P_belta_width * 0.35, y)),
            Location((P_belta_width * 0.4, y)),
            Location((P_belta_width * 0.45, y)),
            Location((P_belta_width * 0.5, y)),
            Location((P_belta_width * 0.55, y)),
            Location((P_belta_width * 0.6, y)),
            Location((P_belta_width * 0.65, y)),
            Location((P_belta_width * 0.7, y)),
            Location((P_belta_width * 0.75, y)),
            Location((P_belta_width * 0.8, y)),
            Location((P_belta_width * 0.85, y)),
            Location((P_belta_width * 0.9, y)),
        ):
            Circle(0.75, align=(Align.CENTER, Align.MIN), mode=Mode.ADD)
    extrude(amount=P_belta_extrude, mode=Mode.SUBTRACT)

    edges = case.part.edges()
    if P.do_post_processing:
        fillet(edges[113], 2)
        fillet(edges[405], 2)
        
        fillet(edges_1[40], 1)
        
        fillet(edges_1[28], 1)
        fillet(edges_1[68], 1)
        
        fillet(edges_1[34], 1)
        fillet(edges_1[61], 1)

        fillet(edges_1[32], 1)
        fillet(edges_1[59], 1)

        fillet(edges_1[26], 1)
        fillet(edges_1[65], 1)
        
        fillet(edges_1[31], 1)
        fillet(edges_1[57], 1)
        
        fillet(edges_1[25], 1)
        fillet(edges_1[63], 1)        
        
        fillet(edges_1[23], 1)
        fillet(edges_1[49], 1)        
        
        fillet(edges_1[17], 1)
        fillet(edges_1[55], 1)          

        fillet(edges_1[20], 1)
        fillet(edges_1[47], 1)     
        
        fillet(edges_1[14], 1)
        fillet(edges_1[53], 1)          

        fillet(edges_1[18], 1)
        fillet(edges_1[45], 1)  

        fillet(edges_1[12], 1)
        fillet(edges_1[51], 1)  
        
        fillet(edges_1[7], 1)
        
        edges = case.part.faces().filter_by(lambda f: f.area_without_holes == 552.15) \
                        .edges().filter_by(lambda e: e.length>5.)
        for edge in edges:
            fillet(edge, .5)


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

objects = {
    "phone": get_phone_objects(),
    "backplate": get_backplate_objects(),
    "belta": {
        "case": case.part,
        #'left_l': left_l,
        #'left_r': left_r,
        #'bottom': bottom,
        #'up_t': up_t,
        #'up_b': up_b,
        "faces": colorize_named_faces(case),
        #'edges': colorize_edges(edges_1),
    },
}

# % % [show objects]
try:
    show(objects, port=3940)
except ImportError:
    print("ocp_vscode.show not available. Model built but not displayed.")

# %% [Export objects]

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
