from build123d import *
from ocp_vscode import *
objects= {} 
set_port(3939)

pts = [
    (0, 0),
    (0, 1),
    (1, 1),
]

wts = [
    1.0,
    1.0,
    1.0,
]

with BuildPart() as ex30:
    with BuildSketch() as ex30_sk:
        with BuildLine() as ex30_ln:
            l0 = Polyline(pts)
            l1 = Bezier(pts, weights=wts)
        make_face()
    extrude(amount=10)
    
show_all()