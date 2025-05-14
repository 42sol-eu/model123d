"""
----
file-name:      recorder_{identifier}.py
file-uuid:      
description:    {{description}}

project:
    name:       model123d
    uuid:       fe521ba0-4ad7-484d-9386-26de71379e15
    url:        https://www.github.com/42sol/model123d
"""

# [Imports]
from build123d import *
from build123d import MM as mm
from ocp_vscode import show
from dataclasses import dataclass
from pathlib import Path
import sys
from rich.console import Console
from math import sqrt
from copy import deepcopy as copy
# [Setup]
console = Console()
objects = []

# [Constants]
no = False
yes = True

def debug(msg):
    """Print debug message if show_debug is True"""
    if Parameters.show_debug:
        console.log(f"[blue]DEBUG: {msg}[/blue]")

def define(object, color="#ff0000", name=""):
    """Define an object with a name and color"""
    if len(name) == 0:
        name = object.__name__
    else:
        object.name = name
    object.color = color
    objects.append(object)
    return object

# [Parameters]
@dataclass
class Parameters:
    """Parameters for the ${TM_FILENAME}"""
    show_debug: bool  = yes
    show_selection: bool  = no
    do_export:  bool  = yes
    do_fillet_cut: bool  = no
    do_fillet_recorder: bool  = no
    do_band_cut:  bool  = no
    do_pebble:   bool  = no
    
    do_main_fillet: bool  = yes
    
    fillet_radius: float  = 1.8 * mm
    width:      float  = 20.5 * mm 
    height:     float  = 76.5 * mm 
    depth:      float  = 12.0 * mm 
    thickness:  float  =  2.5 * mm
    top_cut:    float  = 48.0 * mm
    button_x:   float  =  1.25 * mm
    button_z:   float  =  7.0 * mm
    tighten_r:  float  =  0.25 * mm
    bottom_r:   float  =  6.0 * mm
    cut_radius: float  =  2.0 * mm #[1.2..2.0]
    
    device_height: float  =  76.5 * mm
    device_width:  float  =  20.5 * mm
    device_depth:  float  =  12.0 * mm
    
    def __init__(self):
        debug("Initializing parameters")
        self.width += self.thickness

    @property
    def sleeve_width(self) -> float:
        """Calculate sleeve width"""
        return self.width + 2 * self.thickness

    @property
    def sleeve_height(self) -> float:
        """Calculate sleeve height"""
        return self.device_height + self.thickness

    @property
    def sleeve_depth(self) -> float:
        """Calculate sleeve depth"""
        return self.depth + 2 * self.thickness
    
    def id(self):
        """Return a unique identifier for the parameters"""
        params = [self.width, self.height, self.depth]
        param_str = "_".join(str(param) for param in params[:5]).replace(".", "-")
        return param_str

P = Parameters()

# [Functions]
def create_box(width, height, depth, location=Location([.0, .0, .0])):
    """Create a box with the given dimensions"""
    debug(f"Creating box with width={width}, height={height}, depth={depth}")
    return Box(width, height, depth).move(location)

# [Main]    
if yes or __name__ == "main":
    debug("Running main")
    
    # [Model]
    debug("Creating model")
    
    body           = create_box(P.device_width, P.device_height, P.device_depth)
    button         = create_box(P.device_width+2*P.button_x, P.device_height, P.button_z)
    P.button_cut_x = -P.device_width*0.2
    P.button_len_x = P.device_width*2.0
    button_right_1 = create_box(P.button_len_x, P.device_height*0.5, P.device_depth+2*P.thickness, 
                                    Location([P.button_cut_x, +P.height/2, 2*P.thickness])) 
    
    front_cut_box  = create_box(P.device_width, P.top_cut,             P.device_depth, 
                                    Location([.0, P.top_cut/2-2.5, 2*P.thickness]))
    band_cut       = create_box(4*P.thickness,         4*P.thickness,          4*P.thickness, 
                                    Location([P.width/2, -P.height/2, .0]))
    # Create a box
    with BuildPart() as recorder:
        add(body)
        add(button)
        if P.do_fillet_recorder:
            fillet(objects=recorder.part.edges(),radius=.3*mm)
    define(recorder, "#fff000aa", "Recorder")

    with BuildPart() as button_cut:
        add(button_right_1)
        if P.do_main_fillet:
            fillet(objects=button_cut.edges(), radius=P.fillet_radius)
        
    define(button_cut, "#00ffffaa", "Side Cut Box")
    
    with BuildPart() as front_cut:
        add(front_cut_box) 
        if P.do_main_fillet:
            fillet(objects=front_cut.edges(), radius=P.fillet_radius)
    
    
        
    with BuildPart() as bottom_cut:
        with BuildSketch(Plane.XZ) as sketch:
            RegularPolygon(P.bottom_r, 6)
        extrude(amount=P.device_height)
        bottom_cut.part.move(Location([.0, -2*P.thickness, .0])) 
        fillet(objects=bottom_cut.edges(), radius=.5)

    with BuildPart() as recorder_tightener:
        with BuildSketch(Plane.XZ) as sketch:
            RegularPolygon(P.tighten_r, 6)
        extrude(amount=P.device_height)
    
    with BuildPart() as recorder_tighteners:
        add(copy(recorder_tightener.part).move(Location([+P.device_width*1/8,P.device_height/2,+P.device_depth/2])))
        add(copy(recorder_tightener.part).move(Location([-P.device_width*1/8,P.device_height/2,+P.device_depth/2])))
        add(copy(recorder_tightener.part).move(Location([+P.device_width*3/8,P.device_height/2,-P.device_depth/2])))
        add(copy(recorder_tightener.part).move(Location([-P.device_width*3/8,P.device_height/2,-P.device_depth/2])))
    
    with BuildPart() as recorder_w_cuts:
        add(recorder)
        add(recorder.part.move(Location([.0, 3*P.thickness,.0])))
        add(bottom_cut)
        add(recorder_tighteners, mode=Mode.SUBTRACT)
        if P.do_band_cut:
            add(band_cut)
        

        
        if P.do_fillet_cut:
            fillet(objects=recorder.part.edges(),radius=.3*mm)
    define(recorder_w_cuts, "#00ff00aa", "Cuts")
            
    with BuildPart() as sleeve:
        # Create a box with the given dimensions
        create_box(P.sleeve_width, P.sleeve_height, P.sleeve_depth)
        
        
        # Add fillets to the edges of the cut
        item = -1
        select_edge =[0,1,5,8,9,]
        select_addon=[14,19,20,24,]
        select_all = select_edge + select_addon
        fillet_edges = []
        fillet_addon = []
        for edge in sleeve.edges() \
                        .filter_by(lambda e: e.length>P.thickness and e.length<65.0) \
                        .filter_by(lambda e: e.distance_to((0,-P.device_height/2,0)) >P.device_height*0.4) \
                        .sort_by(Axis.Y) \
                        .sort_by(lambda e: e.length, reverse=yes):
                        
            
            item += 1
            if item in select_edge:
                fillet_edges.append(edge)
                if P.show_selection:
                    define(edge, color="#ff0000", name=f"Edge_{item} len: {edge.length}")
            elif item in select_addon:
                fillet_addon.append(edge)
                if P.show_selection:
                    define(edge, color="#00ff00", name=f"Edge_{item} len: {edge.length}")
        print(f"Number of edges: {len(fillet_edges)}")
        
        add(front_cut, mode=Mode.SUBTRACT)
        add(button_cut, mode=Mode.SUBTRACT)
        
        
        # Find edges that touch the bounding box
        bounding_box = sleeve.part.bounding_box()
        touching_edges = sleeve.edges().filter_by(
            lambda e: any(
            abs(coord - bound) < 1e-6
            for coord, bound in zip(e.bounding_box().min, bounding_box.min)
            ) or any(
            abs(coord - bound) < 1e-6
            for coord, bound in zip(e.bounding_box().max, bounding_box.max)
            )
        ).filter_by(
            lambda e: e.length > P.thickness+0.1)
        for edge in touching_edges:
            if P.show_selection:
                define(edge, color="#ff00ff", name="Bounding Box Edge")
        # Add fillets to the edges
        if P.do_main_fillet:
            fillet(objects=touching_edges, radius=P.fillet_radius)
        cut = recorder_w_cuts.part
        add(cut, mode=Mode.SUBTRACT)
        
        faces = []
        for index, face in enumerate(sleeve.faces() \
                    .filter_by(lambda f: f.area > 403.0 and not (1517 <= f.area <= 1518)) \
                    .sort_by(lambda f: f.area, reverse=yes) ):
            faces.append(face)
            if P.show_selection:                
                define(face, color="#0000ff", name=f"Face_{index} area: {face.area}")
        
        rotate = 30
        for index, face in enumerate(faces):
            if index in [1,2]:
                continue
            elif index == 0:
                x_range = range(-1, 2)
                y_range = range(-7, 8)
                x_dist = 6 * mm
                y_dist = 5 * mm
                x_skip = []
                y_skip = [1]
            else:
                x_range = range(-1, 2)
                y_range = range(-4, 6)
                x_dist = 5 * mm
                y_dist = 5 * mm
                x_skip = []
                y_skip = []
            
            with BuildSketch(face) as hex_pattern:
                for x in x_range:
                    for y in y_range:
                        hex_center = Location([x * x_dist, y * y_dist])
                        with Locations(hex_center):
                            if x in x_skip or y in y_skip:
                                continue
                            RegularPolygon(P.cut_radius, 6,rotation=rotate)
        extrude(amount=-P.device_height, mode=Mode.SUBTRACT)
        
        
    define(sleeve, "#0000aaff", "Sleeve")

    
        
    # [Pebble Shape]
    if P.do_pebble:
        with BuildPart() as pebble:
            # Create a base sphere
            length = P.device_height + 40.0
            a = Sphere(radius=length / 2)
            # Cut a button-like feature on the top
            with Locations(Location([0, 0, length / 4])):
                Cylinder(radius=length/2, height=length/2, mode=Mode.SUBTRACT)
            # Optionally add fillets to edges
            fillet(pebble.edges(), radius=length/5 * mm)
            with Locations(Location([0, 0, +6.5])):
                b = Cylinder(radius=length/2, height=length/4, mode=Mode.SUBTRACT)
            top_circle = pebble.edges().filter_by(GeomType.CIRCLE).sort_by(Axis.Z)
            fillet(pebble.edges(), radius=2* mm)
            scale(pebble.part, by=(.7,.9,.5))
            
        with BuildPart() as pebble_sleeve:
            add(pebble.part.move(Location([.0, .0, P.device_depth])))
            add(recorder_w_cuts, mode=Mode.SUBTRACT)
        define(pebble_sleeve, color="#00ff00aa", name="Pebble Shape")

    # Show the box
    show(*objects)
    
    # Export the box if do_export is True
    if P.do_export:
        debug("Exporting model")
        if P.do_pebble:
            id = 'pebble'
        else:
            id = 'sleeve_cut'
        export_name = __file__ \
                        .replace('{identifier}', id) \
                        .replace('.py', '.stl')
        export_path = Path(__file__).parent / export_name
        console.log(f"[green]Model exported to {export_path}[/green]")
        exporter = Mesher()
        if P.do_pebble:
            exporter.add_shape(pebble_sleeve.part)
        else:
            exporter.add_shape(sleeve.part)
        exporter.write(export_path)
        del exporter        