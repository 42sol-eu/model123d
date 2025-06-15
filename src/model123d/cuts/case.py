from build123d import *
from ocp_vscode import *

with BuildPart() as not_phone_case:
    with BuildSketch(Plane.XY):
        RectangleRounded(80 * MM, 150 * MM, 10 * MM)
        RectangleRounded(70 * MM, 140 * MM, 2 * MM, mode=Mode.SUBTRACT)
    extrude(amount=2 * MM)
    with BuildSketch(Plane.XZ):
        RectangleRounded(80 * MM, 150 * MM, 10 * MM)
        RectangleRounded(70 * MM, 140 * MM, 2 * MM, mode=Mode.SUBTRACT)
    extrude(amount=2 * MM)

    to_fillet_inner = not_phone_case.faces().sort_by(Axis.Z)[-1].inner_wires().edges()
    #fillet(to_fillet[0], 1)
    to_fillet_outer = not_phone_case.faces().sort_by(Axis.Z)[-1].outer_wire().edges()
    # fillet(to_fillet, 1)

show(not_phone_case, to_fillet_inner, names=["not_phone_case", "to_fillet_inner"],)