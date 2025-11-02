
"""
Module: lamp_adapter
====================

This module provides classes and methods for creating a circular lamp adapter.

Classes:
--------

- Adapter:
    A dataclass representing a ring with an identifier, material, length, and repaired status.

Usage:
------

    lamp_adapter = Adapter()
    
----
file
    name:       lamp_adapter.py
    uuid:       0fd60bf2-c132-434d-b8e0-c4aed6064897
    date:       2025-11-01
description:    3D models for Tak game stones using build123d
author:         felix@42sol.eu
project:
    name:       model123d
    uuid:       fe521ba0-4ad7-484d-9386-26de71379e15
    url:        https://www.github.com/42sol/model123d
"""

# %% [Constants]
no = False 
yes = True
mm = 1
# %% [Imports]
import os
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from build123d import *
from rich import print


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
    """Parameters for the stones.py"""
    show_debug:    bool =    yes
    do_cut:        bool =    no
    do_show:       bool =    yes
    do_export:     bool =    yes
    do_fillet:      bool =    no
    export_folder: Path = file_path() / "_export"
    
    def __init__(self):
        debug("Initializing core parameters")

# %% [Parameters]
@dataclass
class AdapterParameters(Parameters):
    """Parameters for the lamp adapter"""
    material:        str = "PETG_white"
    do_top_frame:    bool = no
    r_top_outer:     float = 153.5 / 2. * mm
    r_top_inner:     float = 149.5 / 2. * mm
    r_bottom_outer:  float = 147.0 / 2. * mm
    r_bottom_inner:  float = 143.0 / 2. * mm
    height_top    :  float =   8.0 * mm
    height_bottom:   float =  18.0 * mm
    thickness:       float =   2.0 * mm

class LampAdapter:
    """Class to build a lamp adapter model"""
    def __init__(self, params: AdapterParameters = AdapterParameters()):
        self.params = params
    
    def build(self) -> BuildPart:
        """Build the lamp adapter model"""
        P = self.params
        debug(f"[bold green]Building lamp adapter parameters:[/bold green] {self.params}")
        cut_mode = Mode.SUBTRACT
        with BuildPart() as full_part:
            Cylinder(P.r_bottom_outer, P.height_bottom)            
            # Select the top and bottom faces (along Z axis)
            top_face = full_part.faces().filter_by(Axis.Z).sort_by(Axis.Z)[-1]
            bottom_face = full_part.faces().filter_by(Axis.Z).sort_by(Axis.Z)[0]
            debug(f"Selected top face: {top_face}")
            debug(f"Selected bottom face: {bottom_face}")
            # Create a lying cylinder on the center of the top face
            center = top_face.center()
            
            full_height = P.height_bottom + P.height_top
            half_height = full_height / 2
            with Locations(Location((0, 0, half_height))) as top_part:
                Cylinder(P.r_top_outer, P.height_top, align=(Align.CENTER, Align.CENTER, Align.MAX))
            with Locations(Location((0, 0, half_height + P.thickness))) as top_part:
                Cylinder(P.r_top_inner, P.height_top, align=(Align.CENTER, Align.CENTER, Align.MAX), mode=cut_mode)
            
            
            if P.do_top_frame:
                # Create the top frame
                with Locations(Location((0, 0, P.height_bottom/2+P.height_top/2-P.thickness))) as top_frame:
                    Cylinder(P.r_top_outer, P.thickness, align=(Align.CENTER, Align.CENTER, Align.MIN))
            
            Cylinder(P.r_bottom_inner, 3*P.height_bottom, mode=cut_mode)    
            
            if P.do_cut:
                with Locations(Location((0, 0, -half_height))) as bottom_cut:
                    Box(3*P.r_bottom_outer, 1.2*P.r_bottom_outer, 2*full_height, align=(Align.CENTER, Align.MIN, Align.MIN), mode=cut_mode)
            
            if P.do_fillet:
                # Add fillets to edges along the X axis
                edges_x = full_part.edges().filter_by(Axis.X)
                for edge in edges_x:
                    fillet(edge, radius=P.fillet_radius)
                
            
        self.part = full_part.part
        return self
    
    def export(self) -> BuildPart:
        """Export the model as STL file"""
        P = self.params
        debug("[yellow]Exporting STL...[/yellow]")
        
        if not  P.export_folder.exists():
            P.export_folder.mkdir(parents=True, exist_ok=True)
            debug(f"Created export folder: {P.export_folder}")
        else:
            debug(f"Export folder already exists: {P.export_folder}")
        
        # Export using build123d's Mesher
        mesher = Mesher()
        mesher.add_shape(self.part.rotate(Axis.Y,180))  # Rotate to match the original orientation
        file_name = f"{Path(__file__).stem}.stl"
        path = os.getcwd()
        os.chdir(P.export_folder)
        mesher.write( P.export_folder / file_name )
        debug(f"Field model exported as {P.export_folder / file_name}")
        os.chdir(path)
        return self

    
# %% [Build Model]
debug("Creating Tak stone model")
P = AdapterParameters()

# %% [Display]
if P.do_show:
    try:
        from ocp_vscode import show, set_port
        set_port(3941)
        M1 = LampAdapter(P)
        part = M1.build().part
        show(part, names=["repair_part"])
    except ImportError:
        print("ocp_vscode.show not available. Model built but not displayed.")

# %% [Export]
if P.do_export:
    debug("Exporting model")
    try:
        if "M1" not in locals():
            M1 = LampAdapter(P)
            M1.build()
        M1.export()
    except Exception as e:
        print(f"Export failed: {e}")

# %% [End of file]