# -*- coding: utf-8 -*-
"""
----
file-name:      algorithms.py
file-uuid:      d36b3eb7-8f1a-4bd4-8428-1df71a85ea36
description:   more complex algorithms for the phone belta

project:
    name:       model123d
    uuid:       fe521ba0-4ad7-484d-9386-26de71379e15
    url:        https://www.github.com/42sol/model123d
"""

# [Imports]
from rich import print                                     # [docs](https://rich.readthedocs.io)
from rich.console import Console
from pathlib import Path                                   # [docs](https://docs.python.org/3/library/pathlib.html)
from build123d import *                                    # [docs](https://build123d.readthedocs.io)
from build123d import MM as mm                           

# [Local imports]
from parameter import Parameters, PageSize
from helper import *


# [Code]


def create_moles(P_belta_width, P_belta_height, P_belta_thickness, P_belta_extrude, case):
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
    
def create_stitches(P_belta_width, P_belta_height, P_belta_thickness, P_belta_extrude):
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
