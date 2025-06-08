from build123d import *
from ocp_vscode import show
from ocp_vscode.colors import ListedColorMap
with BuildPart() as p:
    Box(0.1, 0.1, 2)

a = {
    "a": Vector(1, 2, 3),
    "b": [
        Pos(2, 2, 2) * Cylinder(1, 1),
        (1, 2, 3),
        p,
        p.part,
        {"c": Vector(5, 2, 3), "d": Pos(-3, 0, 0) * Box(1, 2, 3), "e": 123},
    ],
}
x = 0
b = [
    Pos(2, 4, 2) * Sphere(1),
    "wert",
    p,
    p.part,
    {"x": Pos(-5, -5, 0) * Box(2, 1, 0.5), "y": 123},
]

show(p, a, b, names=["p", "a", "b"])