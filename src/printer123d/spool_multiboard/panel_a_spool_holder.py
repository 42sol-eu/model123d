
    """
    Module: spool_panel
    ====================

    This module provides classes and methods for creating a spool holder on a multiboard panel using build123d.

    Classes:
    --------

    - Panel:
        A dataclass representing a ring with an identifier, material, length, and repaired status.

    Usage:
    ------

        spool_panel = Panel()
        spool_panel.build()
    ----
    file
        name:       spool_panel.py
        uuid:       b532dd30-e7d7-48c4-8b78-0bb29a1b8b2a
        date:       2025-11-08
    description:    3D models for Prusa MMU3 enclosures and parts
    author:         felix@42sol.eu
    project:
        name:       printer123d
        uuid:       7ad4ec3f-1ed5-4ff9-9a18-307b7b7237c1
        url:        https://www.github.com/42sol/printer123d
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
        do_export:     bool =    no
        do_fillet:      bool =    no
        export_folder: Path = file_path() / "_export"
        
        def __init__(self):
            debug("Initializing core parameters")

    # %% [Parameters]
    @dataclass
    class ModelParameters(Parameters):
        """Parameters for the lamp adapter"""
        material:              str = "PETG_white"
        spool_radius:          float =  12.5
        spool_height:          float = 120.0
        spool_move_on_grid:    Locations = Locations((-32,32,0))

    class SpoolHolder:
        """Class to build a spool holder model"""
        def __init__(self, params: ModelParameters = ModelParameters()):
            self.params = params
        
        def build(self) -> BuildPart:
            """Build the spool holder model"""
            P = self.params
            debug(f"[bold green]Building spool holder parameters:[/bold green] {self.params}")
            cut_mode = Mode.SUBTRACT
            with BuildPart() as full_part:
                debug("Building full part")
                # Import Panel_A.stl file
                panel_stl_path = file_path() / "Panel_A_simple.stl"
                if panel_stl_path.exists():
                    panel_mesh = Mesher().read(panel_stl_path)[0]
                    bbox = panel_mesh.bounding_box()
                    debug(f"Panel mesh bounding box: {bbox}")
                    # Center the panel at origin by translating it
                    panel_center = bbox.center()
                    panel_mesh = panel_mesh.translate(-panel_center)
                    add(panel_mesh)
                    debug(f"Imported Panel_A.stl from {panel_stl_path}")
                else:
                    debug(f"Panel_A.stl not found at {panel_stl_path}")
                
                debug("Adding spool holder cylinder")
                with Locations(P.spool_move_on_grid):
                    Cylinder(P.spool_radius, P.spool_height, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.ADD)
                # Select the top and bottom faces (along Z axis)
                top_face = full_part.faces().filter_by(Axis.Z).sort_by(Axis.Z)[-1]
                bottom_face = full_part.faces().filter_by(Axis.Z).sort_by(Axis.Z)[0]
                debug(f"Selected top face: {top_face}")
                debug(f"Selected bottom face: {bottom_face}")
                # Create a lying cylinder on the center of the top face
                center = top_face.center()    
                
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
    P = ModelParameters()

    # %% [Display]
    if P.do_show:
        try:
            from ocp_vscode import show, set_port
            set_port(3940)
            M1 = SpoolHolder(P)
            part = M1.build().part
            show(part, names=["repair_part"])
        except ImportError:
            print("ocp_vscode.show not available. Model built but not displayed.")

    # %% [Export]
    if P.do_export:
        debug("Exporting model")
        try:
            if "M1" not in locals():
                M1 = SpoolHolder(P)
                M1.build()
            M1.export()
        except Exception as e:
            print(f"Export failed: {e}")

    # %% [End of file]