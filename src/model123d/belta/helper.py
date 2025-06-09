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

# [Parameters]

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

console = Console()


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

# [End of file
