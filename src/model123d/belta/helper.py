# -*- coding: utf-8 -*-
"""
----
file-name:      helper.py
file-uuid:      1c704f51-9534-4931-ba71-2ee395e326d7
description:   Helper functions for the model123d project.
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
from ocp_vscode import ColorMap  # [docs](https://github.com/42sol/ocp-vscode)
import colorsys
import random

# [Local imports]
# none

# [Parameters]
# none

# [Global_Variables]
console = Console()

# [Code]
# [Imports]
from build123d import *
from rich.console import Console
from pathlib import Path

# [Local imports]
from parameter import Parameters


# [Constants]
from build123d import MM as mm

# [Functions]


def debug(msg: str):
    """Print debug message if show_debug is True.
    Args:
        msg (str): The message to print - use f-strings for more complex messages.
    Returns:
        None
    """
    if Parameters.show_debug:
        console.log(f"[blue]DEBUG: {msg}[/blue]")


def info(msg: str):
    """Print info message.
    Args:
        msg (str): The message to print - use f-strings for more complex messages.
    Returns:
        None
    """
    console.log(f"[green]INFO : {msg}[/green]")


def error(msg: str):
    """Print error message.
    Args:
        msg (str): The message to print - use f-strings for more complex messages.
    Returns:
        None
    """
    console.log(f"[red]ERROR: {msg}[/red]")


def create_name(base_path, suffix, extension="stl"):
    """Create a file name based on a base path, suffix, and extension.
    Args:
        base_path (str or Path): The base path for the file.
        suffix (str): The suffix to append to the base path.
        extension (str): The file extension to use (default is "stl").
    Returns:
        str: The constructed file name with the specified suffix and extension.
    """
    file_name = base_path.with_name(f"{base_path.stem}_{suffix}.{extension}")

    return str(file_name)


def define(object, color=None, name="", alpha=1.0):
    """Define an object with a name and color and alpha value.
    Args:
        object (Part or BuildPart): The object to define.
        color (str): The color of the object in hex format (e.g., "#ff0000").
        name (str): The name of the object.
        alpha (float): The transparency of the object, where 1.0 is fully opaque and 0.0 is fully transparent.
    Returns:
        None
    """

    # Catch if the object is a BuildPart, BuildSketch, or BuildLine
    if hasattr(object, "part"):
        debug(f"found BuildPart object: {object}")
        object.part.name = name
    elif hasattr(object, "sketch"):
        debug(f"found BuildSketch object: {object}")
        object.sketch.name = name
    elif hasattr(object, "line"):
        debug(f"found BuildLine object: {object}")
        object.line.name = name
    else:
        object.name = name

    object.color = color
    object.alpha = alpha
    debug(f"Defined object '{name}' with color {color} and alpha {alpha}")


def do_screw(x, y, z, diameter, name="screw", color="#C0C0C0"):
    """Create a screw with a head.
    Args:
        x (float): The x-coordinate of the screw's position.
        y (float): The y-coordinate of the screw's position.
        z (float): The z-coordinate of the screw's position.
        diameter (float): The diameter of the screw.
        name (str): The name to assign to the screw part (default is "screw").
        color (str): The color of the screw in hex format (default is "#C0C0C0").
    Returns:
        None
    """
    head_diameter = diameter * 2.5  # TODO: remove magic number head_diameter
    head_height = diameter * 0.5  # TODO: remove magic number head_diameter

    with BuildPart(Plane.XY.offset(z)) as screw_shaft:
        with Locations((x, y)):
            Cylinder(diameter / 2, head_height, mode=Mode.ADD)
    with BuildPart(Plane.XY.offset(z + head_height)) as screw_head:
        with Locations((x, y)):
            Cylinder(head_diameter / 2, 0.01, mode=Mode.ADD)
    screw = Compound([screw_shaft.part, screw_head.part], label=name)
    define(screw, color, f"{name}_screw")


# [Main]

if __name__ == "__main__":
    info("Testing info message")
    debug("Testing debug message")
    error("Testing error message")

    # Test create_name
    base = Path("/tmp/testfile.stl")
    print("Created name:", create_name(base, "v2", "3mf"))

    # Test define with a dummy object
    class Dummy:
        pass

    dummy_obj = Dummy()
    define(dummy_obj, color="#123456", name="dummy", alpha=0.5)
    print(
        f"Dummy object: name={dummy_obj.name}, color={dummy_obj.color}, alpha={dummy_obj.alpha}"
    )

    # Test do_screw (requires build123d)
    try:
        do_screw(0, 0, 0, 5, name="test_screw", color="#FFD700")
        print("do_screw executed successfully")
    except Exception as e:
        print(f"do_screw failed: {e}")

def get_marked_faces(part):
    """Returns a list of faces that are marked with a color."""
    faces = {}
    part_faces = part.faces()

    faces["top"] = part_faces.filter_by(Plane.XY)[0]
    faces["top"].color = "#ff0000aa"  # Mark the top face with a specific color
    faces["bottom"] = part_faces.filter_by(Plane.XY)[1]
    faces["bottom"].color = "#1a2ede75"  # Mark the top face with a specific color
    faces["left"] = part_faces.filter_by(Plane.YZ)[0]
    faces["left"].color = "#62babaff"  # Mark the left face with a specific color
    faces["right"] = part_faces.filter_by(Plane.YZ)[1]
    faces["right"].color = "#09ff0086"  # Mark the left face with a specific color
    faces["front"] = part_faces.filter_by(Plane.XZ)[0]
    faces["front"].color = "#eeff00"  # Mark the front face with a specific color
    faces["back"] = part_faces.filter_by(Plane.XZ)[1]
    faces["back"].color = "#ff00fba5"  # Mark the back face with a specific color

    return faces


def colorize_named_faces(part):
    """
    Colors all faces of a part that are named 'face_X_{counter}'.
    Each axis (X, Y, Z) gets a different color palette.
    """

    axis_colors = {
        "X": (0.0, 1.0, 1.0),  # Red
        "Y": (0.33, 1.0, 1.0),  # Green
        "Z": (0.66, 1.0, 1.0),  # Blue
    }
    colored_faces = {}
    colors = ColorMap.tab20()
    for axis, (h, s, v_base) in axis_colors.items():
        if axis == "X":
            faces = (
                part.faces()
                .filter_by(Axis.X)
                .filter_by(
                    lambda f: f.area_without_holes > 12.0 if type(f) == Face else False
                )
            )
        elif axis == "Y":
            faces = (
                part.faces()
                .filter_by(Axis.Y)
                .filter_by(
                    lambda f: f.area_without_holes > 12.0 if type(f) == Face else False
                )
            )
        elif axis == "Z":
            faces = (
                part.faces()
                .filter_by(Axis.Z)
                .filter_by(
                    lambda f: f.area_without_holes > 12.0 if type(f) == Face else False
                )
            )
        else:
            continue

        for idx, face in enumerate(faces):
            face.name = f"face_{axis}_{idx}"
            # Vary the value for each counter
            v = 0.5 + 0.5 * ((idx % 10) / 10)
            rgb = colorsys.hsv_to_rgb(h, s, v)
            hex_color = "#{:02x}{:02x}{:02x}ff".format(
                int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255)
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

# [End of file
