# -*- coding: utf-8 -*-
"""
----
file-name:       test_wood_grain.py
file-uuid:       8adad796-1764-4a44-8ed0-f8e18ed8478d
description:    3D models for Tak game stones and extendable board using build123d
author:         felix@42sol.eu
project:
    name:       material123d
    uuid:       0a7cefda-00f0-4891-a077-8d1a0965f6d0
    url:        https://www.github.com/42sol/material123d
"""

# %% [Imports]
from build123d import *
from ocp_vscode import show, set_port
from dataclasses import dataclass, fields
from rich import print
from pathlib import Path

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
    """Parameters for the test_wood_grain.py"""
    show_debug:    bool =    yes
    do_show:       bool =    yes
    do_export:     bool =    no
    export_folder: Path = file_path() / "_export"
    
    def __init__(self):
        debug("Initializing core parameters")

    def __str__(self):
        """String representation of the parameters"""
        data = f"Parameters:\n"
        for field in fields(self):
            value = getattr(self, field.name)
            data += f"  {field.name}: {value}\n"

        return data
# %% [Model]

class TestWoodGrain:
    """Class to test wood grain generation"""
    
    def __init__(self, params: Parameters = Parameters()):
        debug("Creating TestWoodGrain instance")
        self.part = None  # Placeholder for the part to be created
        self.params = params
        
        # Load STL model 'wood_grain_modifier.stl' from the same directory as this script
        stl_path = file_path() / "_output" / "wood_plank_200x200x15.stl"
        
        
        importer = Mesher()
        if not stl_path.exists():
            debug(f"Error: {stl_path} not found!")
            raise FileNotFoundError(f"STL file {stl_path} does not exist.")
        self.wood_grain = importer.read(stl_path)  # Assuming the STL file contains one mesh
        debug(f"Loaded wood grain mesh from {stl_path}")
        
    def build(self):
        """Create a simple box to test the setup"""
        debug("Creating part in TestWoodGrain")
        P = self.params
        debug(f"# {P}")

        with BuildPart() as _model:
            Box(400, 400, 100)
            add(self.wood_grain, mode=Mode.INTERSECT)
            #add(self.wood_grain, mode=Mode.INTERSECT)
        self.part = _model.part
# %% [Main]
if __name__ == "__main__":
    debug("Starting main execution")
    
    # Initialize parameters
    P = Parameters()
    model = TestWoodGrain(P)
    model.build()
    
    if P.do_show:
        debug("Showing the part")
        show(model.part, model.wood_grain, names=["Test Wood Grain", "Wood Grain Modifier"], colors=["#1f4fefee", "#4f1fefee"])
    # Set up the export folder
    if P.do_export:
        P.export_folder.mkdir(parents=True, exist_ok=True)
        # TODO: export the model to the specified folder
    
    debug("Execution completed")
    