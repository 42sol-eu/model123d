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
    
    def build_spindle(self) -> BuildPart:
        """Build the spindle that the spool rotates on"""
        p = self.params
        debug("Building spindle assembly...")
        
        with BuildPart() as spindle_assy:
            # Main spindle rod
            with BuildPart() as spindle:
                Cylinder(
                    radius=p.spindle_diameter / 2,
                    height=p.spindle_length,
                    align=(Align.CENTER, Align.CENTER, Align.MIN)
                )
            
            # Bearing/washer on each side to keep spool centered
            with BuildPart(mode=Mode.ADD) as bearings:
                # Left washer
                with Locations((0, 0, -p.bearing_thickness)):
                    Cylinder(
                        radius=p.bearing_diameter / 2,
                        height=p.bearing_thickness,
                        align=(Align.CENTER, Align.CENTER, Align.MIN)
                    )
                # Right washer
                with Locations((0, 0, p.spindle_length)):
                    Cylinder(
                        radius=p.bearing_diameter / 2,
                        height=p.bearing_thickness,
                        align=(Align.CENTER, Align.CENTER, Align.MIN)
                    )
            
            # Add chamfers for easier spool insertion
            if p.do_fillet:
                chamfer(spindle_assy.edges().filter_by(Axis.Z).group_by(Axis.Z)[-1], 
                       length=p.fillet_radius)
        
        return spindle_assy
    
    def build_support_arm(self) -> BuildPart:
        """Build the arm connecting the peg to the spindle"""
        p = self.params
        debug("Building support arm...")
        
        with BuildPart() as arm:
            # Main arm body - horizontal beam
            with BuildPart():
                Box(
                    length=p.arm_length,
                    width=p.arm_width,
                    height=p.arm_thickness,
                    align=(Align.MIN, Align.CENTER, Align.CENTER)
                )
            
            # Mounting plate at peg end
            with BuildPart(mode=Mode.ADD):
                with Locations((0, 0, 0)):
                    Box(
                        length=20 * mm,
                        width=p.arm_width + 10 * mm,
                        height=p.arm_thickness + 10 * mm,
                        align=(Align.MAX, Align.CENTER, Align.CENTER)
                    )
            
            # Spindle mount at far end
            with BuildPart(mode=Mode.ADD):
                with Locations((p.arm_length, 0, 0)):
                    Cylinder(
                        radius=p.spindle_diameter / 2 + 10 * mm,
                        height=p.arm_thickness + 10 * mm,
                        align=(Align.CENTER, Align.CENTER, Align.CENTER),
                        rotation=(90, 0, 0)
                    )
            
            # Cutout for spindle
            with BuildPart(mode=Mode.SUBTRACT):
                with Locations((p.arm_length, 0, 0)):
                    Cylinder(
                        radius=p.spindle_diameter / 2 + p.spindle_clearance,
                        height=p.arm_width + 20 * mm,
                        align=(Align.CENTER, Align.CENTER, Align.CENTER),
                        rotation=(90, 0, 0)
                    )
            
            # Add fillets for strength
            if p.do_fillet:
                fillet(arm.edges().filter_by(GeomType.CIRCLE), radius=p.fillet_radius)
        
        return arm
    
    def build(self) -> list:
        """Build complete spool holder assembly"""
        p = self.params
        console.print("[bold green]Building multiboard spool holder...[/bold green]")
        
        parts = []
        
        # Build main components
        spindle = self.build_spindle()
        define(spindle.part, "#3498db", "Spindle")
        parts.append(spindle.part)
        
        support_arm = self.build_support_arm()
        define(support_arm.part, "#e74c3c", "Support Arm")
        parts.append(support_arm.part)
        
        # Position spindle on arm
        spindle_positioned = spindle.part.rotate(Axis.X, 90).translate((p.arm_length, 0, p.spindle_length / 2))
        
        # Add multiboard peg connectors
        if self.peg_mesh:
            # Position pegs at mounting end
            peg1 = self.peg_mesh.translate((0, -p.peg_spacing / 2, 0))
            peg2 = self.peg_mesh.translate((0, p.peg_spacing / 2, 0))
            define(peg1, "#95a5a6", "Peg 1")
            define(peg2, "#95a5a6", "Peg 2")
            parts.extend([peg1, peg2])
        
        # Add click connector if available
        if self.click_solid:
            click_positioned = self.click_solid.translate((0, 0, -20 * mm))
            define(click_positioned, "#f39c12", "Click Connector")
            parts.append(click_positioned)
        
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
        
        for idx, part in enumerate(parts):
            if hasattr(part, 'name') and part.name:
                filename = f"spool_holder_{part.name.lower().replace(' ', '_')}.stl"
            else:
                filename = f"spool_holder_part_{idx}.stl"
            
            export_path = output_dir / filename
            
            exporter = Mesher()
            exporter.add_shape(part)
            exporter.write(export_path)
            console.log(f"[green]✓ Exported: {export_path.name}[/green]")
            del exporter

# [End of file]