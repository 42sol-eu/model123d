"""
Docstring for model123d.sports.inset_pipe
"""
from build123d import *
from ocp_vscode import *

outer_diameter = 33.7 + 1 * MM
thickness = 2.5 * MM
inner_diameter = outer_diameter - 2 * thickness
height = 10 * MM

print(f"outer_diameter: {outer_diameter}")
print(f"inner_diameter: {inner_diameter}")

with BuildPart() as pipe:
    Cylinder(outer_diameter / 2, height)
    Cylinder(outer_diameter / 2 + 2, height/2)
    Cylinder(inner_diameter / 2, height, mode=Mode.SUBTRACT)



with BuildPart() as main:
    Cylinder(outer_diameter / 2 + 1 * MM, height + 5 * MM)
    Cylinder((outer_diameter - 3 * thickness)/ 2 * MM, height + 5 * MM, mode=Mode.SUBTRACT)
    add(pipe.part.move(Location((0, 0, 2.5 * MM))), mode=Mode.SUBTRACT)
    add(pipe.part.move(Location((0, 0, 2.5 * MM))), mode=Mode.SUBTRACT)
    
    # edges = main.part.edges().filter_by(lambda edge: edge.length > outer_diameter * 3.14)
    edges = main.part.edges().filter_by(GeomType.CIRCLE)
    fillet(edges, radius=0.4 * MM)
    
show(main,edges)

from pathlib import Path

exporter = Mesher()
exporter.add_shape(main.part)
exporter.write(Path(__file__).parent / "pipe_insets.stl")