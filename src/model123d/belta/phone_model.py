# -*- coding: utf-8 -*-
"""
----
file-name:      phone_model.py
file-uuid:      039917f8-70a4-40fb-b268-7b5a7bd95b55
description:   Generate a phone model with a display, body, and addons.
author:        felix@42sol.eu

project:
    name:       model123d
    uuid:       a0b40edb-6c25-41b9-878f-6bf97bfcf0a2
    url:        https://www.github.com/42sol/model123d
"""

# [Imports]
from rich import print  # [docs](https://rich.readthedocs.io)
from rich.console import Console
from pathlib import Path  # [docs](https://docs.python.org/3/library/pathlib.html)
from build123d import *

# [Local Imports]
from helper import *
from parameter import Parameters
from phone_addons import build_phone_addons, get_addon_objects
from phone_backplate import build_phone_backplate, get_backplate_objects


# [Parameters]

# [Global Variables]
display_cutout = display = body = addons = None


# [Code]

# [Functions]


def build_phone_model(P):
    """Builds the phone body and display, 
    Args:
        P (Parameters): Parameters for the phone model
    Returns:
        tuple: A tuple containing (display_cutout, display, body)
    """
    global display_cutout, display, body, addons

    with BuildPart() as display_cutout:
        with BuildSketch(Plane.XY) as bottom_sketch:
            RectangleRounded(
                P.body_width, P.body_height, P.body_radius, align=(Align.MIN, Align.MIN)
            )
        extrude(amount=P.display_extrude, mode=Mode.ADD)

    with BuildPart() as display:
        with BuildSketch(Plane.XY) as bottom_sketch:
            RectangleRounded(
                P.body_width, P.body_height, P.body_radius, align=(Align.MIN, Align.MIN)
            )
        extrude(amount=P.display_extrude, mode=Mode.ADD)
        bottom_face = display.faces().filter_by(Plane.XY)[0]
        edge = bottom_face.edges()[-1]
        fillet(edge, P.display_extrude / 2)

    with BuildPart() as body:
        with BuildSketch(Plane.XY) as bottom_sketch:
            RectangleRounded(
                P.body_width, P.body_height, P.body_radius, align=(Align.MIN, Align.MIN)
            )
            if P.do_screw_holes:
                with Locations(
                    (P.screw_x1, P.screw_y1),
                    (P.screw_x2, P.screw_y2),
                    (P.screw_x3, P.screw_y3),
                    (P.screw_x4, P.screw_y4),
                ):
                    Circle(P.screw_diameter / 2, mode=Mode.SUBTRACT)
                with Locations((P.ext_position_x, P.ext_position_y)):
                    Circle(P.ext_diameter / 2, mode=Mode.SUBTRACT)
        extrude(amount=P.body_extrude, mode=Mode.ADD)
        active = body.faces().filter_by(Plane.XZ)
        bottom_face = active[0]
        top_face = active[1]
        active = body.faces().filter_by(Plane.YZ).filter_by(lambda f: f)
        left_face = active[0]
        right_face = active[1]
        active = body.faces().filter_by(Plane.XY).filter_by(lambda f: f)
        display_face = active[0]
        back_face = active[1]
        if P.show_debug:
            define(bottom_face, "#ff0000aa", "bottom_face")
            define(top_face, "#00ff00aa", "top_face")
            define(left_face, "#00ffffff", "left_face")
            define(right_face, "#ff00ffff", "right_face")
            define(display_face, "#eeff00ff", "display_face")
            define(back_face, "#f90404", "back_face")
        with BuildSketch(bottom_face) as bottom_sketch:
            RectangleRounded(P.usbc_width, P.usbc_height, P.usbc_radius)
            if 0:  # Do not make the inside part
                RectangleRounded(
                    P.usbc_inside_width,
                    P.usbc_inside_height,
                    P.usbc_inside_height / 4,
                    mode=Mode.SUBTRACT,
                )
        extrude(amount=-P.usbc_extrude, mode=Mode.SUBTRACT)
        add(display_cutout.part, mode=Mode.SUBTRACT)
        edges = body.edges().filter_by(lambda e: e)
        for index in range(len(edges)):
            if P.show_selection:
                define(edges[index], "#ff0000ff", f"edges_{index}")
        if P.do_post_processing:
            pass
            # fillet(edges[3],.6)
            # chamfer(edges[32],2.)
            # chamfer(edges[36],2.)
    define(body, "#ccccd3ff", "body")
    define(display, "#000000ff", "display")
    addons = build_phone_addons(P)
    return display_cutout, display, body, addons


def get_phone_objects():
    global display, body, addons

    return {"body": body, "display": display, "addons": get_addon_objects()}


if __name__ == "__main__":
    P = Parameters()
    display_cutout, display, body, addons = build_phone_model(P)
    screws, backplate, charger, charger_frame = build_phone_backplate(P)
    # Optionally show the model (if ocp_vscode/show is available)
    try:
        from ocp_vscode import show

        objects = {
            "body": get_phone_objects(),
            "backplate": get_backplate_objects(),
        }

        show(objects, glass=yes)
    except ImportError:
        print("ocp_vscode.show not available. Model built but not displayed.")
