from build123d import *
from build123d import MM as mm
from ocp_vscode import show
from dataclasses import dataclass
from pathlib import Path
import sys
from math import sqrt

yes, no = True, False
@dataclass
class P:
    """Parameters for the Base Plate model."""
    do_export: bool = yes
    do_pattern : bool = no # NOT implemented yet
    do_magnet: bool = yes
    size: float = 42.0 * mm
    thickness: float = 4.5 * mm
    magnet_diameter: float = 10.0 * mm
    magnet_height: float = 3.0 * mm
    type : str = "Circular"  # Type of hole pattern: Hexagonal, Circular

with BuildPart() as base_plate:
    with BuildSketch() as sketch:
        # Create a rectangle for the base plate
        if P.type == "Hexagonal":
            # Create hexagonal holes
            hexagon = RegularPolygon(P.size / 2.0, 6)    
        else:
            Circle(P.size, align=(Align.CENTER, Align.CENTER))

    
    extrude(amount=P.thickness)
    fillet(base_plate.faces().sort_by(Axis.Z)[-1].edges(), radius=1.0)
    
if P.do_magnet:
    with BuildPart() as base_plate_with_hole:
        add(base_plate.part)
        with BuildSketch() as sketch:
            # Create circles for the holes
            with Locations((0.0, 0.0)):
                Circle(P.magnet_diameter / 2.0)
        extrude(amount=P.magnet_height, mode=Mode.SUBTRACT)
    
    base_plate = base_plate_with_hole

base_plate.color = "#FF0000aa"
base_plate.name = "Base Plate"



show(base_plate)

if P.do_export:
    exporter = Mesher()
    exporter.add_shape(base_plate.part)
    if P.do_pattern:
        sys.exit(1, "Patterning not implemented yet")
        exporter.add_shape(base_plate.part)
    parameters = f'{P.thickness}_{P.magnet_diameter}'
    file_name = __file__.replace(".py", ".stl") \
                .replace('{identifier}', P.type) \
                .replace('{size}', str(P.size)) \
                .replace('{parameters}', parameters)
    
    exporter.write(Path(__file__).parent / "_output" / file_name)