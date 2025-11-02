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

def tool(plane, point : Vector, direction=0):
    """A tool function that can be used to create a point."""
    with BuildSketch(plane) as tool_1:
        if plane == Plane.XY:
            if direction == 0:
                point_1 = point + (0, 1, 0)
                point_2 = point + (0, 0, 0) 
                point_3 = point + (1, 0, 0)
            else:
                point_1 = point + (0, -1, 0)
                point_2 = point + (0, 0, 0) 
                point_3 = point + (1, 0, 0)
        elif plane == Plane.XZ:
            if direction == 0:
                point_1 = point + (1, 0, 0)
                point_2 = point + (0, 0, 0) 
                point_3 = point + (0, 0, 1)
            else:
                point_1 = point + (1, 0, 0)
                point_2 = point + (0, 0, 0) 
                point_3 = point + (0, 0, -1)
                
        elif plane == Plane.YZ:
            if direction == 0:
                point_1 = point + (0, 0, -1)
                point_2 = point + (0, 0, 0) 
                point_3 = point + (0, -1, 0)
            else:
                point_1 = point + (0, 0, 1)
                point_2 = point + (0, 0, 0) 
                point_3 = point + (0, 1, 0)
        
        with BuildLine():
            Polyline([point_1, point_2, point_3])
            Bezier([point_1, point_2, point_3], weights=wts)
        make_face()

    r_tool = tool_1.sketch
    return r_tool

with BuildPart() as part:
    # Create a box
    box = Box(10, 10, 10)

    edge_0 = part.part.edges()[0]
    point_0_0 = edge_0.vertices()[0]
    point_0_1 = edge_0.vertices()[1]
    
    edge_1 = part.part.edges()[1]
    point_1_0 = edge_1.vertices()[0]
    point_1_1 = edge_1.vertices()[1]

    edge_2 = part.part.edges()[2]
    point_2_0 = edge_2.vertices()[0]
    point_2_1 = edge_2.vertices()[1]
    
    edge_3 = part.part.edges()[3]
    point_3_0 = edge_3.vertices()[0]
    point_3_1 = edge_3.vertices()[1]
    edge_4 = part.part.edges()[4]
    point_4_0 = edge_4.vertices()[0]
    point_4_1 = edge_4.vertices()[1]
    
    edge_5 = part.part.edges()[5]
    point_5_0 = edge_5.vertices()[0]
    point_5_1 = edge_5.vertices()[1]
    edge_6 = part.part.edges()[6]
    point_6_0 = edge_6.vertices()[0]
    point_6_1 = edge_6.vertices()[1]

    sweep(tool(Plane.XY, point_0_0, 0), edge_0, mode=Mode.SUBTRACT)
    sweep(tool(Plane.XZ, point_1_0, 1), edge_1, mode=Mode.SUBTRACT)
    sweep(tool(Plane.XY, point_2_0, 1), edge_2, mode=Mode.SUBTRACT)
    
    # sweep(tool(Plane.XZ, point_3_1, 0), edge_3, mode=Mode.ADD)
    
objects['part'] = part.part
part.name = "Box"
objects['edge_0'] = edge_0
objects['edge_1'] = edge_1
objects['edge_2'] = edge_2
objects['edge_3'] = edge_3
objects['edge_4'] = edge_4
objects['edge_5'] = edge_5
objects['edge_6'] = edge_6
objects['point_0_0'] = point_0_0
objects['point_0_1'] = point_0_1
objects['point_1_0'] = point_1_0
objects['point_1_1'] = point_1_1
objects['point_2_0'] = point_2_0
objects['point_2_1'] = point_2_1
objects['tool_0'] = tool(Plane.XY, point_0_0, 0)
objects['tool_1'] = tool(Plane.XZ, point_1_0, 1)
objects['tool_2'] = tool(Plane.XY, point_2_0, 1)
objects['tool_3'] = tool(Plane.XZ, point_3_0, 0)

# part.part.color = "#aa0000"  # Dark red color for the box
show_object(objects)