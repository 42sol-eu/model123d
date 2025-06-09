# -*- coding: utf-8 -*-
"""
----
file-name:      phone_addons.py
file-uuid:      211e9bb6-847b-41df-ab07-7c23357b597b
description:   Load and manage phone addons for the cmf_phone_2_pro model.

project:
    name:       model123d
    uuid:       a0b40edb-6c25-41b9-878f-6bf97bfcf0a2
    url:        https://www.github.com/42sol/model123d
"""

# [Imports]
from build123d import *
from rich import print  # [docs](https://rich.readthedocs.io)
from rich.console import Console
from pathlib import Path  # [docs](https://docs.python.org/3/library/pathlib.html)

# [Local Imports]
from parameter import Parameters
from helper import define

# [Parameters]

# [Global_Variables]
console = Console()
camera1 = camera2 = camera3 = led = None

# [Classes]


class Camera:
    """A class to create a camera object with a frame, lense, and inner parts."""

    def __init__(self, x, y, z, diameter, frame, height, name="camera") -> "Camera":
        """Initialize a camera object with its parameters
        Args:
            x (float): X coordinate of the camera center.
            y (float): Y coordinate of the camera center.
            z (float): Z coordinate of the camera center.
            diameter (float): Diameter of the camera.
            frame (float): Width of the camera frame.
            height (float): Height of the camera.
            name (str): Name of the camera object (default is "camera").
        Returns:
            Camera: An instance of the Camera class.
        """
        self.create(x, y, z, diameter, frame, height, name)

    def create(self, x, y, z, diameter, frame, height, name="camera") -> "Camera":
        """Create a camera with a frame, internally used.

        Args:
            self (Camera): The camera object instance.
            x (float): X coordinate of the camera center.
            y (float): Y coordinate of the camera center.
            z (float): Z coordinate of the camera center.
            diameter (float): Diameter of the camera.
            frame (float): Width of the camera frame.
            height (float): Height of the camera.
            name (str): Name of the camera object (default is "camera").
        Returns:
            Camera: An instance of the Camera class with defined parts.
        """

        self.name = name
        self.x = x
        self.y = y
        self.z = z

        outer_radius = diameter / 2
        inner_radius = (diameter - frame) / 2

        with BuildPart(Plane.XY.offset(z)) as bottom:
            with Locations((x, y)):
                Cylinder(inner_radius, 0.01, mode=Mode.ADD)

        with BuildPart(Plane.XY.offset(z + 0.01)) as outer:
            with Locations((x, y)):
                Cylinder(inner_radius * 0.4, 0.01, mode=Mode.ADD)

        with BuildPart(Plane.XY.offset(z + 0.02)) as inner:
            with Locations((x, y)):
                Cylinder(inner_radius * 0.3, 0.01, mode=Mode.ADD)

        with BuildPart(Plane.XY.offset(z)) as frame:
            with BuildSketch(Plane.XY.offset(z)) as frame_sketch:
                with Locations((x, y)):
                    Circle(outer_radius, mode=Mode.ADD)
                    Circle(inner_radius, mode=Mode.SUBTRACT)
            extrude(amount=height, mode=Mode.ADD)

        with BuildPart(Plane.XY.offset(z + height / 2)) as lense:
            with Locations((x, y)):
                Cylinder(inner_radius, height - 0.05, mode=Mode.ADD)

        self.bottom = bottom
        define(bottom, "#000000ff", f"{name}_bottom")

        self.outer = outer
        define(outer, "#444343bb", f"{name}_outer")

        self.inner = inner
        define(inner, "#282877ff", f"{name}_inner")

        self.frame = frame
        define(frame, "#bbbdbbff", f"{name}_frame")

        self.lense = lense
        define(lense, "#f4f44b2c", f"{name}_lens", alpha=0.2)

        self.compound = Compound(
            [frame.part, bottom.part, outer.part, inner.part, lense.part], label=name
        )
        define(self.compound, name=f"{name}")

        return self

    def to_dict(self) -> dict:
        """Convert the camera object to a dictionary representation.
        Args:
            self (Camera): The camera object instance.
        Returns:
            dict: A dictionary containing the camera's parts.
        """
        return {
            "frame": self.frame,
            "lense": self.lense,
            "inner": self.inner,
            "outer": self.outer,
            "bottom": self.bottom,
        }


class Led:
    """Generate a LED object with an outer and inner part.
    This class creates a simple LED model with an outer and inner cylinder.
    """

    def __init__(self, x, y, z, diameter, name="led") -> "Led":
        """Initialize a LED object with its parameters.
        Args:
            self (Led): The LED object instance.
            x (float): X coordinate of the LED center.
            y (float): Y coordinate of the LED center.
            z (float): Z coordinate of the LED center.
            diameter (float): Diameter of the LED.
            name (str): Name of the LED object (default is "led").
        """
        self.create(x, y, z, diameter, name)

    def create(self, x, y, z, diameter, name="led") -> "Led":
        """Create a LED with an outer and inner part, internally used.
        Args:
            self (Led): The LED object instance.
            x (float): X coordinate of the LED center.
            y (float): Y coordinate of the LED center.
            z (float): Z coordinate of the LED center.
            diameter (float): Diameter of the LED.
            name (str): Name of the LED object (default is "led").
        Returns:
            Led: An instance of the Led class with defined parts.
        """
        with BuildPart(Plane.XY.offset(z + 0.01)) as outer:
            with Locations((x, y)):
                Cylinder(diameter, 0.01, mode=Mode.ADD)
        with BuildPart(Plane.XY.offset(z + 0.02)) as inner:
            with Locations((x, y)):
                Cylinder(diameter * 0.5, 0.01, mode=Mode.ADD)

        self.outer = outer
        define(outer, "#bbbdbbff", f"{name}_outer")

        self.inner = inner
        define(inner, "#f4f44b2c", f"{name}_inner")
        led = Compound([outer.part, inner.part], label=name)

        self.led = led
        define(led, "#f4f44b2c", f"{name}_led")

        return self

    def to_dict(self) -> dict:
        """Convert the LED object to a dictionary representation.
        Args:
            self (Led): The LED object instance.
        Returns:
            dict: A dictionary containing the LED's parts.
        """
        return {"outer": self.outer, "inner": self.inner}


# [Functions]


def build_phone_addons(P: Parameters) -> tuple:
    """Builds the 3 cameras and the led, returns a dict with all parts
    Args:
        P (Parameters): The parameters object containing configuration for the phone addons.
    Returns:
        tuple: A tuple containing the objects from this module.
    """
    global camera1, camera2, camera3, led

    camera1 = Camera(
        P.camera1_x,
        P.camera1_y + P.camera1_h / 4,
        P.body_extrude,
        P.camera1_r * 2 - 0.1,
        P.camera1_frame,
        P.camera1_extrude,
        "camera1",
    )
    camera2 = Camera(
        P.camera2_x,
        P.camera2_y,
        P.body_extrude,
        P.camera3_diameter - 0.1,
        P.camera2_frame,
        P.camera2_extrude,
        "camera2",
    )
    camera3 = Camera(
        P.camera3_x,
        P.camera3_y,
        P.body_extrude,
        P.camera3_diameter - 0.1,
        P.camera3_frame,
        P.camera3_extrude,
        "camera3",
    )
    led = Led(
        P.camera1_x,
        P.camera1_y - P.camera1_h / 4,
        P.body_extrude,
        P.camera1_r * 0.6,
        "led",
    )

    return camera1, camera2, camera3, led


def get_addon_objects() -> dict:
    """Returns a dictionary of all addon objects.
    Returns:
        dict: A dictionary containing the addon objects from this module.
    """
    return {
        "camera1": camera1.to_dict(),
        "camera2": camera2.to_dict(),
        "camera3": camera3.to_dict(),
        "led": led.to_dict(),
    }


if __name__ == "__main__":
    P = Parameters()
    build_phone_addons(P)

    # Optionally show the model (if ocp_vscode/show is available)
    try:
        from ocp_vscode import show

        objects = {"addons": get_addon_objects()}
        show(objects)

    except ImportError:
        print("ocp_vscode not available, skipping show.")

# [End of file]
