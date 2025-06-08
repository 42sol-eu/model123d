# %%

from ocp_vscode import *
from build123d import *

set_defaults(show_parent=False)

# %%

box = Box(1, 2, 3)
box = chamfer(box.edges(), 0.1)

# %%

push_object(
    box.faces().filter_by(Axis.X), name="green", color="green", alpha=0.2
)
push_object(
    box.faces().filter_by(Axis.Y), name="red", color="red", alpha=0.6
)
push_object(
    box.faces().filter_by(Axis.Z), name="blue", color="blue"
)
push_object(
    box.faces().sort_by(Axis.Z)[-2], name="default", alpha=0.5
)

# %%

push_object(
    box.wires().filter_by(Axis.X), name="green", color="green"
)
push_object(
    box.wires().filter_by(Axis.Y), name="red", color="red"
)
push_object(
    box.wires().filter_by(Axis.Z), name="blue", color="blue"
)

# %%

push_object(
    box.edges().filter_by(Axis.X), name="green", color="green"
)
push_object(
    box.edges().filter_by(Axis.Y), name="red", color="red"
)
push_object(
    box.edges().filter_by(Axis.Z), name="blue", color="blue"
)

# %%

push_object(
    box.vertices().filter_by(Axis.X), name="green", color="green"
)
push_object(
    box.vertices().filter_by(Axis.Y), name="red", color="red"
)
push_object(
    box.vertices().filter_by(Axis.Z), name="blue", color="blue"
)

# %%

push_object(box, name="green", color="green", alpha=0.2)
push_object(box.moved(Location((0, -4, 0))), name="red", color=(255, 0, 0, 0.6))
push_object(box.moved(Location((0, 4, 0))), name="blue", color="blue")
push_object(box.moved(Location((4, 0, 0))), name="default", alpha=0.5)

# %%

with BuildSketch() as s:
    Circle(2)

push_object(s, name="sketch1", color="green", alpha=0.2)
push_object(
    s.sketch.moved(Location((0, 0, -1))),
    name="sketch2",
    color="red", alpha=0.6,
)
push_object(
    s.sketch.moved(Location((0, 0, -2))).wrapped,
    name="sketch3",
    color="blue"
)

# %%

push_object(
    box, name="green", color="green", alpha=0.2
)
push_object(
    box.moved(Location((0, -4, 0))),
    name="red",
    color=(255, 0, 0, 0.6)
)

# %%

with BuildPart() as b:
    Box(1, 1, 2)
    with Locations((0, 2, 0)):
        Box(2, 2, 1)

if 1:
    a = {"name": "alpha",
        "color": (0, 1, 0, 0.2),
        "alpha": 0.2,
        "a": {"object": Vector(1, 2, 3), "name": "vector", "color": "red"},
        "b": {"c": Vector(5, 2, 3), "d": Pos(-3, 0, 0) * Box(1, 2, 3), "e": 123},
        
    }
    push_object(
        a, name="a"
    )
else:
    # You can pass a list of objects to push_object
    push_object(
        b.solids(),
        name="both_solids",
        color="purple", alpha=0.5,
    )
# %%

show_objects()

# %%