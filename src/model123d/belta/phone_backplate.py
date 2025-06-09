# -*- coding: utf-8 -*-
"""
----
file-name:      phone_backplate.py
file-uuid:      46e23b19-7c4f-4d93-8a92-d889022feccf
description:   Generate the backplate for a phone model, including screw holes and charger cutout.
author:         42sol

project:
    name:       model123d
    uuid:       a0b40edb-6c25-41b9-878f-6bf97bfcf0a2
    url:        https://www.github.com/42sol/model123d
"""

# [Imports]
from rich import print                                     # [docs](https://rich.readthedocs.io)
from rich.console import Console
from pathlib import Path                                   # [docs](https://docs.python.org/3/library/pathlib.html)

# [Parameters]

# [Global_Variables]
console = Console()

# [Code]
# [Imports]
from build123d import *

# [Local Imports]
from helper import define

# [Global Variables]
screws, backplate, charger, charger_frame = None, None, None, None

# [Functions]


def build_phone_backplate(P) -> tuple:
    """Builds the backplate and charger frame, returns (backplate_screws, backplate, charger, charger_frame)
    Args:
        P (Parameters): Parameters for the phone backplate
    Returns:
        tuple: A tuple containing the screws, backplate, charger, and charger frame objects

    """
    global screws, backplate, charger, charger_frame

    with BuildPart(Plane.XY.offset(P.body_extrude)) as backplate_screws:
        with BuildSketch() as cuts:
            with Locations((P.camera1_x, P.camera1_y)):
                RectangleRounded(P.camera1_w, P.camera1_h, P.camera1_r, mode=Mode.ADD)
            with Locations((P.camera2_x, P.camera2_y)):
                Circle(P.camera2_diameter / 2, mode=Mode.ADD)
            with Locations((P.camera3_x, P.camera3_y)):
                Circle(P.camera3_diameter / 2, mode=Mode.ADD)
        with BuildSketch() as screws:
            if P.do_screw_holes:
                with Locations(
                    (P.screw_x1, P.screw_y1),
                    (P.screw_x2, P.screw_y2),
                    (P.screw_x3, P.screw_y3),
                    (P.screw_x4, P.screw_y4),
                ):
                    Circle(P.screw_diameter / 2, mode=Mode.ADD)
                with Locations((P.ext_position_x, P.ext_position_y)):
                    Circle(P.ext_diameter / 2, mode=Mode.ADD)
        extrude(amount=P.backplate_extrude, mode=Mode.ADD)
        if P.do_charger:
            with BuildSketch() as cuts:
                with Locations((P.charger_position_x, P.charger_position_y)):
                    Circle(P.charger_outer_diameter / 2, mode=Mode.ADD)
                    Circle(P.charger_inner_diameter / 2, mode=Mode.SUBTRACT)
            extrude(amount=P.backplate_extrude * 2, mode=Mode.ADD)

    with BuildPart(Plane.XY.offset(P.body_extrude)) as backplate:
        with BuildSketch(Plane.XY.offset(P.body_extrude)) as back_sketch:
            RectangleRounded(
                P.body_width, P.body_height, P.body_radius, align=(Align.MIN, Align.MIN)
            )
        extrude(amount=P.backplate_extrude, mode=Mode.ADD)
        top_face = backplate.faces().filter_by(Plane.XY)[-1]
        edge = top_face.edges()[0]
        fillet(edge, P.backplate_extrude - 0.11)
        if P.do_screw_holes:
            with Locations(
                (P.screw_x1, P.screw_y1, P.backplate_extrude),
                (P.screw_x2, P.screw_y2, P.backplate_extrude),
                (P.screw_x3, P.screw_y3, P.backplate_extrude),
                (P.screw_x4, P.screw_y4, P.backplate_extrude),
                (P.ext_position_x, P.ext_position_y, P.backplate_extrude / 2 + 0.1),
            ):
                Cylinder(
                    P.screw_head_diameter / 2, P.backplate_extrude, mode=Mode.SUBTRACT
                )
            with Locations((P.ext_position_x, P.ext_position_y, P.backplate_extrude)):
                Cylinder(P.ext_radius, P.backplate_extrude, mode=Mode.SUBTRACT)
            with Locations(
                (
                    P.ext_position_x + P.ext_radius / 2,
                    P.ext_position_y - P.ext_radius / 2,
                    P.backplate_extrude,
                )
            ):
                Box(
                    P.ext_radius * 2,
                    P.ext_radius * 2,
                    P.backplate_extrude,
                    mode=Mode.SUBTRACT,
                )
        add(backplate_screws.part, mode=Mode.SUBTRACT)

    with BuildPart(Plane.XY.offset(P.body_extrude)) as charger:
        if P.do_charger:
            with BuildSketch(Plane.XY.offset(P.body_extrude)) as cuts:
                with Locations((P.charger_position_x, P.charger_position_y)):
                    Circle(P.charger_outer_diameter / 2, mode=Mode.ADD)
                    Circle(P.charger_inner_diameter / 2, mode=Mode.SUBTRACT)
            extrude(amount=P.backplate_extrude * 2, mode=Mode.ADD)

    with BuildPart(Plane.XY.offset(P.body_extrude)) as charger_frame:
        with BuildSketch(Plane.XY.offset(P.body_extrude)) as cuts:
            with Locations((P.charger_position_x, P.charger_position_y)):
                Circle(P.charger_outer_diameter / 2 - 0.1, mode=Mode.ADD)
                Circle(P.charger_inner_diameter / 2, mode=Mode.SUBTRACT)
        extrude(amount=P.backplate_extrude, mode=Mode.ADD)

    define(backplate, "#18e162ff", "phone.backplate")
    define(charger_frame, "#5cd10eff", "charger")

    # Create silver screws to fit into the holes of the backplate
    screws = {}
    if P.do_backplate_screws:
        screw_positions = [
            (P.screw_x1, P.screw_y1, P.backplate_extrude),
            (P.screw_x2, P.screw_y2, P.backplate_extrude),
            (P.screw_x3, P.screw_y3, P.backplate_extrude),
            (P.screw_x4, P.screw_y4, P.backplate_extrude),
            (P.ext_position_x, P.ext_position_y, P.backplate_extrude / 2 + 0.1),
        ]
        count = 1
        for pos in screw_positions:
            with BuildPart(Plane.XY.offset(P.body_extrude)) as screw:
                with Locations(pos):
                    Cylinder(P.screw_head_diameter1 / 2, P.screw_head_extrude)

                pos1 = list(pos)
                pos1[2] += P.screw_head_extrude / 2
                with Locations(Location(pos1)):
                    Box(
                        P.screw_diameter * 2,
                        1.0,
                        P.screw_head_extrude / 4,
                        mode=Mode.SUBTRACT,
                    )
                    Box(
                        1.0,
                        P.screw_diameter * 2,
                        P.screw_head_extrude / 4,
                        mode=Mode.SUBTRACT,
                    )
                name = f"screw_{count}"
                define(screw, "#C0C0C0", name, alpha=1.0)  # Silver color
                screws[name] = screw
                count += 1
    else:
        pass

    return screws, backplate, charger, charger_frame


def get_backplate_objects() -> dict:
    """Returns the objects that are part of the backplate
    Returns:
        dict: A dictionary containing the screws, backplate, charger frame, and charger objects
    """
    return {"screws": screws, "backplate": backplate, "charger_frame": charger_frame}


# [Main]


if __name__ == "__main__":
    from parameter import Parameters

    P = Parameters()
    screws, backplate, charger, charger_frame = build_phone_backplate(P)

    try:
        from ocp_vscode import show

        show(get_backplate_objects(), glass=False)
    except ImportError:
        print("ocp_vscode.show not available. Model built but not displayed.")

# [End of file]
