# -*- coding: utf-8 -*-
"""
----
file-name:      trash_bin_foot_{identifier}.py
file-uuid:      c5b63eba-ea13-460c-a5e3-7fdc1f8ff0ee
description:   IKEA HÖLASS trash bin foot.
author:        felix@42sol.eu
project:
    name:       model123d
    uuid:       fe521ba0-4ad7-484d-9386-26de71379e15
    url:        https://www.github.com/42sol/model123d
"""


# %% [Imports]
from build123d import * # docs: https://build123d.readthedocs.io/en/latest/

from ocp_vscode import show, set_defaults, Camera
from pathlib import Path
from math import sqrt
from copy import deepcopy as copy

# %% [Local imports]
from helper import *
from parameter import *
from export import export_all


P = Parameters()

# %% [Imports]
set_defaults(
    reset_camera=Camera.KEEP,)

# %% [Build phone model]
debug("Creating model")

# %% [setup parameters]


# %% [Build foot base]
with BuildPart() as foot:
    # Create the base box for the foot
    with BuildSketch() as foot_sketch:
        RectangleRounded(
            P.body_width+P.thicken, P.body_height+P.thicken,
            radius=P.outer_radius,
            align=C.CCC
        )
        RectangleRounded(
            P.body_width, P.body_height,
            radius=P.body_radius,
            align=C.CCC,
            mode=C.SUBTRACT
        )
    extrude(amount=P.body_extrude)

    add(foot.part.moved(Location((0, 0, P.body_extrude*4))))
    faces_Z = foot.faces().filter_by(Axis.Z)

with BuildPart() as foot_clamp:
    with BuildSketch(faces_Z[0]) as foot_sketch_hanger:
        with Locations(
            (110.,0,0),
        ):
            RectangleRounded(
                P.clamp+P.thicken, P.clamp+P.thicken,
                radius=P.thicken/10.0,
                align=(Align.CENTER, Align.CENTER, Align.MAX),
            )
            RectangleRounded(
                P.clamp+1, P.clamp+1,
                1.0,
                align=(Align.CENTER, Align.CENTER, Align.MAX),
                mode=C.SUBTRACT
            )
    extrude(amount=P.body_extrude*5, both=True)
    faces_X = foot.faces().filter_by(Axis.X)
    add(foot.part, mode=C.SUBTRACT)
    add(foot.part.moved(Location((P.body_width+P.thicken+P.clamp+3, 0, 0))),mode=C.SUBTRACT)

define(foot.part,"#ff0000ff", "IKEA HÖLASS foot")
define(foot_clamp.part,"#0000aaff", "IKEA HÖLASS clamp")


objects = {
    "foot": foot,
    "clamp": foot_clamp,
    #"backplate": get_backplate_objects(),
    "details": {
        #"case": case,
        #"top": top_case,
        "faces": colorize_named_faces(faces_X),
        #"edges": colorize_edges(faces_Y),
    }
}

# % % [show objects]
try:
    show(objects, port=3939)
except ImportError:
    print("ocp_vscode.show not available. Model built but not displayed.")

## %% [Export objects]

if P.do_export:
    # export_all(P, __file__, objects, console)
    try:
        mesher = Mesher()
        mesher.add_shape(foot.part)
        mesher.write(Path(__file__).parent / "IKEA_HÖLASS_foot.stl")
        
        mesher = Mesher()
        mesher.add_shape(foot_clamp.part)
        mesher.write(Path(__file__).parent / "IKEA_HÖLASS_foot_clamp.stl")

    except AttributeError:
        pass

# %% [End of file]
