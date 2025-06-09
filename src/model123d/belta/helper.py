from build123d import *
from rich.console import Console

console = Console()

# [Constants]
from build123d import MM as mm
no = False
yes = True
false = False
true = True

def debug(msg):
    """Print debug message if show_debug is True"""
    from parameter import Parameters
    if Parameters.show_debug:
        console.log(f"[blue]DEBUG: {msg}[/blue]")


def create_name(base_path, suffix, extension="stl"):
    return base_path.with_name(f"{base_path.stem}_{suffix}.{extension}")


def export_parts_to_stl(file_path, parts):
    if type(file_path) is list or type(file_path) is tuple:
        base_path = file_path[0]
        suffix = '_'.join(file_path[1:])
        file_path = create_name(base_path, suffix, "stl")
        print(f"Exporting to {file_path}")
    exporter = Mesher()
    for part in parts:
        # Check if part is a Part or has a 'part' attribute
        if hasattr(part, 'part'):
            exporter.add_shape(part.part)
        else:
            exporter.add_shape(part)
    exporter.write(file_path)
    del exporter


def define(object, color=None, name="", alpha=1.0):
    """Define an object with a name and color"""
    if hasattr(object, 'part'):
        object.part.name = name
        object.color = color
        object.alpha = alpha
    else:
        object.name = name
        object.color = color
        object.alpha = alpha



def do_screw(x, y, z, diameter, name="screw"):
    """Create a screw with a head"""
    head_diameter = diameter * 2.5
    head_height = diameter * 0.5
    with BuildPart(Plane.XY.offset(z)) as screw:
        with Locations((x, y)):
            Cylinder(diameter/2, head_height, mode=Mode.ADD)
    with BuildPart(Plane.XY.offset(z+head_height)) as head:
        with Locations((x, y)):
            Cylinder(head_diameter/2, 0.01, mode=Mode.ADD)
    define (screw, "#ccccd3ff", f'{name}_screw')
