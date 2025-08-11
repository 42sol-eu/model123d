# -*- coding: utf-8 -*-
"""
This module provides functionality for generating and manipulating clip geometries for stampinup models.

## Features
- Defines default parameters for clip geometry (length, width, height)
- Provides a dataclass (`ClipParams`) for parameter management
- Contains a function (`make_clip`) to generate clip geometry based on parameters
- Includes a main function for testing and demonstration

----
file-name:       clip.py
file-uuid:       70ce686d-b09d-4dc5-8a9a-49a297da5fd7
description:    3D models for clip geometries in stampinup using default parameters
author:         felix@42sol.eu
project:
    name:       model123d
    uuid:       fe521ba0-4ad7-484d-9386-26de71379e15
    url:        https://www.github.com/42sol/model123d
"""

# %% [Imports]
from build123d import *
from ocp_vscode import show, set_defaults, set_port, Camera
from ocp_vscode.colors import ColorMap
from dataclasses import dataclass, fields
from rich import print
from pathlib import Path
from dataclasses import dataclass
from typing import Any
from math import radians, cos, sin

# %% [Constants]
no = False 
yes = True
mm = 1

# %% [Functions]
def debug(msg):
    """Print debug message if show_debug is True"""
    if Parameters.show_debug:
        print(f"[blue]DEBUG: {msg}[/blue]")

def file_path():
    """Return the path to the current file"""
    return Path(__file__).parent.resolve()

# %% [Parameters]
@dataclass
class Parameters:
    """Parameters for the procedural tree trunk"""
    show_debug:    bool =    yes
    do_show:       bool =    yes
    do_export:     bool =    no
    
    do_fillet:      bool =    yes
    export_folder: Path = file_path() / "_export"

    def __init__(self) -> Any:
        debug("Initializing core parameters")
        
    def __str__(self):
        """String representation of the parameters"""
        data = f"Parameters:\n"
        for field in fields(self):
            value = getattr(self, field.name)
            data += f"  {field.name}: {value}\n"
        return data

@dataclass
class ClipParameters(Parameters):
    """Parameters for the clip geometry."""
    length:         float = 20.0 * mm
    width_inner:    float =  6.0 * mm
    height_inner:   float =  4.0 * mm
    thickness:      float =  2.0 * mm
    fillet_radius:   float =  0.2 * mm

    def __init__(self) -> Any:
        super().__init__()
        debug("Initializing clip parameters")



# %% [Model]
class Clip:
    """Class to create clip geometry for stampinup models"""

    def __init__(self, params: ClipParameters = ClipParameters()):
        debug(f"Creating {__class__.__name__} instance")
        super().__init__()
        self.part = None
        self.params = params

    def build(self) -> "Clip":
        """
        Builds a "Clip" part by creating a partial ring with exact nested boundaries using two concentric arcs and connecting lines.
        The method constructs a 2D sketch of a partial ring (arc segment) defined by an outer and inner arc, then extrudes it to form a 3D part. The arcs are created using `JernArc`, which defines a circular arc by a start point, tangent, radius, and arc size. The resulting shape is filleted along its edges.
        Returns:
            Clip: The constructed Clip object with the generated part.
        Notes:
            - The outer and inner arcs are defined by their respective radii, start and end angles.
            - The arcs are connected by straight lines to form a closed profile.
            - The sketch is extruded by `P.height_inner` to create the 3D geometry.
            - All edges are filleted with a radius of `P.fillet_radius`.
        """
        debug(f"Creating part in {__class__.__name__}")
        P = self.params
        debug(f'{P}')

        with BuildPart() as _model:
            with BuildSketch() as sketch:
                Circle(radius=(P.width_inner + P.thickness) / 2)
                Circle(radius=P.width_inner / 2, mode=Mode.SUBTRACT)
                Rectangle(width=2*P.thickness, height=2*P.width_inner, mode=Mode.SUBTRACT, align=(Align.CENTER, Align.MIN))
            extrude(amount=P.height_inner/2, both=yes)
            
            if P.do_fillet: 
                fillet(_model.part.edges(), radius=P.fillet_radius)

            text_height = P.height_inner * 0.6

            # Create cut-out text in the center of the ring
            with BuildSketch(-Plane.ZX.offset(-(P.height_inner+P.thickness*1.8)/2)) as text_sketch:
                
                Rectangle(
                    width=1.2*text_height,
                    height=1.2*text_height,
                    align=(Align.CENTER, Align.CENTER)
                )
            extrude(text_sketch.sketch, amount=P.thickness, mode=Mode.SUBTRACT)

            # Create cut-out text in the center of the ring
            with BuildSketch(-Plane.ZX.offset(-(P.height_inner+0.85*P.thickness)/2)) as text_sketch:
                text_str = "12"
                
                Text(
                    text_str,
                    font_size=text_height,
                    font="Arial",
                    align=(Align.CENTER, Align.CENTER)
                )
            a = extrude(text_sketch.sketch, amount=P.thickness*0.55, mode=Mode.ADD)
            fillet(a.edges(), radius=P.fillet_radius/10.0)

        self.part = _model.part
        return self

    def export(self) -> "Clip":
        """Export the part to STL"""
        P = self.params
        export_path = P.export_folder / "clip.stl"
        debug(f"[green]Model exported to {export_path}[/green]")
        # Use Mesher to export all rings
        exporter = Mesher()
        exporter.add_shape(self.part)
        exporter.write(export_path)
        del exporter

        return self


            

# %% [Main]
if __name__ == "__main__":
    debug("Starting main execution")

    # Initialize ocp_vscode
    set_port(3939)
    set_defaults(reset_camera=Camera.KEEP)  # Keep camera position between updates

    # Initialize parameters
    P = ClipParameters()
    model = Clip(P)
    model.build()

    if P.do_show:
        debug("Showing the part")
        show(model.part)

    # Set up the export folder and export
    if P.do_export:
        P.export_folder.mkdir(parents=True, exist_ok=True)
        model.export()

    debug("Execution completed")