"""
----
file-name:      spool_holder.py
file-uuid:      8f2a1c3d-9e4b-4f6a-b1d2-5c7e8f9a0b1c
description:    Multiboard-based spool holder for Prusa MMU3 using click connectors and 100mm peg

project:
    name:       model123d
    uuid:       a0b40edb-6c25-41b9-878f-6bf97bfcf0a2
    url:        https://www.github.com/42sol-eu/model123d

author:         felix@42sol.eu
date:           2025-11-30
"""

# [Imports]
from pathlib import Path
from dataclasses import dataclass
from build123d import *
from ocp_vscode import *
from rich.console import Console

# [Setup]
console = Console()
objects = []

# [Constants]
no, yes = False, True
mm = 1

# [Helper Functions]
def debug(msg: str):
    """Print debug message if enabled"""
    if P.show_debug:
        console.print(f"[blue]DEBUG[/blue] {msg}")

def define(obj, color="#ff0000", name=""):
    """Define object properties for visualization"""
    if hasattr(obj, 'color'):
        obj.color = color
    if hasattr(obj, 'name'):
        obj.name = name
    objects.append(obj)

# [Parameters]
@dataclass
class P:
    """Parameters for the multiboard spool holder."""
    # Export settings
    do_export: bool = yes
    show_debug: bool = yes
    
    # Spool dimensions (standard filament spool)
    spool_inner_diameter: float = 53.0 * mm  # Inner hole diameter
    spool_outer_diameter: float = 200.0 * mm  # Outer spool diameter
    spool_width: float = 70.0 * mm  # Width of filament on spool
    
    # Holder arm dimensions
    arm_width: float = 30.0 * mm  # Width of the support arm
    arm_thickness: float = 8.0 * mm  # Thickness of support arm
    arm_length: float = 120.0 * mm  # Length from peg to spool center
    
    # Spindle dimensions (the rod the spool spins on)
    spindle_diameter: float = 50.0 * mm  # Diameter of spindle
    spindle_length: float = 80.0 * mm  # Length of spindle
    spindle_clearance: float = 2.0 * mm  # Clearance for smooth rotation
    
    # Bearing/washer dimensions
    bearing_diameter: float = 60.0 * mm
    bearing_thickness: float = 3.0 * mm
    
    # Connector positions
    num_pegs: int = 2  # Number of multiboard pegs
    peg_spacing: float = 50.0 * mm  # Distance between pegs
    
    # Aesthetic features
    do_fillet: bool = yes
    fillet_radius: float = 2.0 * mm

# [Model Creation]
class SpoolHolder:
    """Multiboard-based spool holder model"""
    
    def __init__(self, params: P = P()):
        self.params = params
        self.path = Path(__file__).parent
        
        # Load the multiboard components
        debug("Loading multiboard components...")
        importer = Mesher()
        
        # Load peg STL
        peg_file = self.path / "_inbox" / "multiboard_peg_l=100mm.stl"
        if peg_file.exists():
            self.peg_mesh = importer.read(peg_file)[0]
            debug(f"✓ Loaded peg from {peg_file.name}")
        else:
            console.print(f"[red]ERROR: Peg file not found: {peg_file}[/red]")
            self.peg_mesh = None
        
        # Load click connector STEP
        click_file = self.path / "_inbox" / "multiboard_click.step"
        if click_file.exists():
            self.click_solid = import_step(click_file)
            debug(f"✓ Loaded click connector from {click_file.name}")
        else:
            console.print(f"[red]ERROR: Click file not found: {click_file}[/red]")
            self.click_solid = None
    
    def build_mounting_plate(self) -> BuildPart:
        """Build the base mounting plate that holds the pegs and attaches to click connectors"""
        p = self.params
        debug("Building mounting plate...")
        
        with BuildPart() as plate:
            # Main mounting plate
            Box(
                length=150 * mm,
                width=100 * mm,
                height=10 * mm,
                align=(Align.CENTER, Align.CENTER, Align.MIN)
            )
            
            # Add mounting holes for click connectors (2 holes spaced apart)
            with BuildPart(mode=Mode.SUBTRACT):
                # Two mounting holes for orange click connectors
                with Locations([(-50 * mm, 0, 0), (50 * mm, 0, 0)]):
                    Cylinder(
                        radius=6 * mm,  # Hole for click connector
                        height=15 * mm,
                        align=(Align.CENTER, Align.CENTER, Align.MIN)
                    )
        
        return plate
    
    def build(self) -> list:
        """Build complete spool holder assembly"""
        p = self.params
        console.print("[bold green]Building multiboard spool holder...[/bold green]")
        
        parts = []
        
        # Build the mounting plate
        plate = self.build_mounting_plate()
        define(plate.part, "#cccccc", "Mounting Plate")
        parts.append(plate.part)
        
        # Add multiboard pegs pointing upward on the plate
        if self.peg_mesh:
            # Position two pegs upward on the plate
            # Rotate pegs to point up (Z direction) and place on plate surface
            peg1 = self.peg_mesh.rotate(Axis.Y, 90).translate((-25 * mm, 0, 10 * mm))
            peg2 = self.peg_mesh.rotate(Axis.Y, 90).translate((25 * mm, 0, 10 * mm))
            define(peg1, "#95a5a6", "Peg 1")
            define(peg2, "#95a5a6", "Peg 2")
            parts.extend([peg1, peg2])
        
        # Add click connectors for mounting (orange)
        if self.click_solid:
            # Two click connectors positioned at the mounting holes
            click1 = self.click_solid.translate((-50 * mm, 0, -10 * mm))
            click2 = self.click_solid.translate((50 * mm, 0, -10 * mm))
            define(click1, "#f39c12", "Click 1")
            define(click2, "#f39c12", "Click 2")
            parts.extend([click1, click2])
        
        console.print(f"[green]✓ Built {len(parts)} components[/green]")
        return parts

# [Main Execution]
if yes or __name__ == "__main__":
    holder = SpoolHolder(P())
    parts = holder.build()
    
    # [Visualization]
    set_port(3941)
    show(*objects)
    
    # [Export]
    if P.do_export:
        debug("Exporting models...")
        output_dir = Path(__file__).parent / "_output"
        output_dir.mkdir(exist_ok=True)
        
        # Export only the parts we built (not imported STL/STEP)
        export_parts = [p for p in parts if hasattr(p, 'wrapped') and p.wrapped is not None]
        
        for idx, part in enumerate(export_parts):
            if hasattr(part, 'label') and part.label:
                filename = f"spool_holder_{part.label.lower().replace(' ', '_')}.stl"
            else:
                filename = f"spool_holder_part_{idx}.stl"
            
            export_path = output_dir / filename
            
            try:
                exporter = Mesher()
                exporter.add_shape(part)
                exporter.write(export_path)
                console.log(f"[green]✓ Exported: {export_path.name}[/green]")
                del exporter
            except Exception as e:
                console.log(f"[yellow]⚠ Could not export {filename}: {e}[/yellow]")

# [End of file]