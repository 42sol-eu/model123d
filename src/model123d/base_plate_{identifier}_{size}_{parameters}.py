from build123d import *
from build123d import MM as mm
from ocp_vscode import show
from dataclasses import dataclass
from pathlib import Path
import sys
from math import sqrt

@dataclass
class P:
    """Parameters for the Base Plate model."""
    do_export: bool = True
    do_pattern : bool = False
    do_hole: bool = False
    do_extra: bool = False
    size: float = 42.0 * mm
    thickness: float = 1.5 * mm
    hole_diameter: float = 10.0 * mm
    hole_offset: float = 3.0 * mm
    type : str = "Hexagonal"  # Type of hole pattern

with BuildPart() as base_plate:
    with BuildSketch() as sketch:
        # Create a rectangle for the base plate
        if P.type == "Hexagonal":
            # Create hexagonal holes
            hexagon = RegularPolygon(P.size / 2.0, 6)
            
        else:
            Rectangle(P.size, P.size, align=(Align.CENTER, Align.CENTER))

    
    extrude(amount=P.thickness)
    fillet(base_plate.faces().sort_by(Axis.Z)[-1].edges(), radius=1.0)
    
if P.do_hole:
    with BuildPart() as base_plate_with_hole:
        add(base_plate.part)
        with BuildSketch() as sketch:
            # Create circles for the holes
            with Locations((0.0, 0.0)):
                Circle(P.hole_diameter / 2.0)
            if P.do_extra:
                with Locations((P.hole_offset, P.hole_offset)):
                    Circle(P.hole_diameter / 2.0)
        extrude(amount=P.thickness, mode=Mode.SUBTRACT)
    
    base_plate = base_plate_with_hole

base_plate.color = "#FF0000"
base_plate.name = "Base Plate"



show(base_plate)

if P.do_export:
    exporter = Mesher()
    exporter.add_shape(base_plate.part)
    if P.do_pattern:
        sys.exit(1, "Patterning not implemented yet")
        exporter.add_shape(base_plate.part)
    parameters = f'{P.thickness}_{P.hole_diameter}'
    file_name = __file__.replace(".py", ".stl") \
                .replace('{identifier}', P.type) \
                .replace('{size}', str(P.size)) \
                .replace('{parameters}', parameters)
    
    exporter.write(Path(__file__).parent / "_output" / file_name)