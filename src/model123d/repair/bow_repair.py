
"""
Module: bow_repair
==================

This module provides classes and methods for managing and repairing bows.

Classes:
--------

- Bow:
    A dataclass representing a bow with an identifier, material, length, and repaired status.

- BowRepair:
    A class for managing a collection of Bow objects, providing functionality to add bows,
    repair them by ID, and retrieve lists of repaired and unrepaired bows.

Usage:
------

    bow_repair = BowRepair()
    bow = Bow(id=1, material="wood", length=1.5)
    bow_repair.add_bow(bow)
    bow_repair.repair_bow(1)
    repaired_bows = bow_repair.get_repaired_bows()
    unrepaired_bows = bow_repair.get_unrepaired_bows()
----
file-name:       bow_repair.py
file-uuid:       8e10ec12-af68-4871-8579-8185f95df489
description:    3D models for bow repair using build123d
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
from build123d import *
from dataclasses import dataclass
from rich import print
from pathlib import Path
from typing import List, Optional


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
    do_show:       bool =    yes
    do_export:     bool =    yes
    do_fillet:      bool =    yes
    export_folder: Path = file_path() / "_export"
    
    def __init__(self):
        debug("Initializing core parameters")

# %% [Parameters]
@dataclass
class BowParameters(Parameters):
    material:      str = "PLA_wood"
    length:        float = 60.0 * mm
    width:         float = 36.0 * mm
    width_inner:   float = 30.0 * mm
    height:        float = 12.0 * mm
    height_inner:  float =  6.5 * mm
    fillet_radius:  float =  2.5 * mm

class BowRepair:
    def __init__(self, params: BowParameters = BowParameters()):
        self.params = params
    
    def build(self) -> BuildPart:
        P = self.params
        debug(f"[bold green]Building bow parameters:[/bold green] {self.params}")
        cut_mode = Mode.SUBTRACT
        with BuildPart() as repair_part:
            Box(P.length, P.width, P.height)
            
                
            # Create two holes through the Plane.XY
            hole_radius = 2 * mm
            
            with GridLocations(P.length/4, P.width*0.35, 4, 2):
                Cylinder(   radius=hole_radius, height=P.height * 2, align=(Align.CENTER, Align.CENTER, Align.CENTER), 
                            mode=cut_mode)
                
            # Select the top and bottom faces (along Z axis)
            top_face = repair_part.faces().filter_by(Axis.Z).sort_by(Axis.Z)[-1]
            bottom_face = repair_part.faces().filter_by(Axis.Z).sort_by(Axis.Z)[0]
            debug(f"Selected top face: {top_face}")
            debug(f"Selected bottom face: {bottom_face}")
            # Create a lying cylinder on the center of the top face
            center = top_face.center()
            # Move and rotate the cylinder to lie along the X axis at the top face center
            with Locations(center):
                with GridLocations(0, P.width_inner*0.4, 1, 3):
                    Cylinder(radius=1.6*hole_radius, height=P.length, rotation=(0,90,0))
                # lying_cylinder.moved(center - lying_cylinder.center()).rotated(Axis.Y, 90)
            
            center = bottom_face.center()
            with Locations(center):
                with GridLocations(0, P.width_inner*0.4, 1, 3):
                    Cylinder(radius=hole_radius, height=P.length, rotation=(0,90,0))
                # lying_cylinder.moved(center - lying_cylinder.center()).rotated(Axis.Y, 90)
                
            Box(P.length + 2, P.width_inner, P.height_inner, mode=cut_mode)
            
            if P.do_fillet:
                # Add fillets to edges along the X axis
                edges_x = repair_part.edges().filter_by(Axis.X)
                for edge in edges_x:
                    fillet(edge, radius=P.fillet_radius)
                
            
        self.part = repair_part.part
        return self
    
    def export(self) -> BuildPart:
        P = self.params
        debug("[yellow]Exporting STL...[/yellow]")
        
        if not  P.export_folder.exists():
            P.export_folder.mkdir(parents=True, exist_ok=True)
            debug(f"Created export folder: {P.export_folder}")
        
        # Export using build123d's Mesher
        mesher = Mesher()
        mesher.add_shape(self.part.rotate(Axis.X, 90))  # Rotate to match the original orientation
        file_name = f"{__file__}.stl".replace(".py", "")
        mesher.write( P.export_folder / file_name )
        debug(f"Field model exported as {P.export_folder / file_name}")
        return self

    
# %% [Build Model]
debug("Creating Tak stone model")
P = BowParameters()

# %% [Display]
if P.do_show:
    try:
        from ocp_vscode import show, set_port
        set_port(3939)
        M1 = BowRepair(P)
        repair_part = M1.build().part
        show(repair_part, names=["repair_part"])
    except ImportError:
        print("ocp_vscode.show not available. Model built but not displayed.")

# %% [Export]
if P.do_export:
    debug("Exporting model")
    try:
        if "M1" not in locals():
            M1 = BowRepair(P)
            M1.build()
        M1.export()
    except Exception as e:
        print(f"Export failed: {e}")

# %% [End of file]