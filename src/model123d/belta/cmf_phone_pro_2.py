"""
----
file-name:      cmf_phone_pro_{identifier}.py
file-uuid:      0f73bcdb-84d0-4426-b65e-39e6c87e3ffe
description:    Ideas for cmf phone pro
author:         felix@42sol.eu
project:
    name:       model123d
    uuid:       fe521ba0-4ad7-484d-9386-26de71379e15
    url:        https://www.github.com/42sol/model123d
"""

# [Imports]
from build123d import *
from build123d import MM as mm
from ocp_vscode import show, set_defaults, Camera
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
false = False
true = True

# [Helpers]
def debug(msg):
    """Print debug message if show_debug is True"""
    if Parameters.show_debug:
        console.log(f"[blue]DEBUG: {msg}[/blue]")

def define(object, color="#ff0000", name=""):
    """Define an object with a name and color"""
    if len(name) == 0:
        if hasattr(object, '__name__'):
            name = object.__name__
        else:
            name = [k for k, v in globals().items() if v is object and not k.startswith("__")]
            name = name[0] if name else "unnamed"
    else:
        object.name = name
    object.color = color
    objects.append(object)
    return object

# [Parameters]
@dataclass
class Parameters:
    """Parameters for the ${TM_FILENAME}"""
    show_debug: bool         = no
    show_selection: bool     = no
    show_nose: bool          = no
    do_details: bool         = no
    do_screws: bool          = yes
    do_charger: bool         = yes
    do_post_processing: bool = no
    do_export: bool          = yes
    
    # Device dimensions
    body_height: float            = 164.0 * mm # TODO: fix height
    body_radius: float            =   9. * mm
    body_width: float             =  78.0 * mm
    body_extrude: float           =   7.8 - 1.5 + 0.2 * mm
    display_extrude: float        =   1.0 * mm
    backplate_extrude: float      =   1.3 * mm
    hole_diameter: float          =   2.0 * mm

    # Screw dimensions
    screw_diameter: float         =   2.20 * mm
    screw_head_diameter: float   =    5.85 * mm
    screw_y1: float               =  18.1 + 98.43 * mm
    screw_x1: float               =   3.9 * mm
    screw_y2: float               =  18.1 * mm
    screw_x2: float               =   3.9 * mm
    screw_y3: float               =  18.1 + 98.43 * mm
    screw_x3: float               =  78.0 - 3.9 * mm
    screw_y4: float               =  18.1 + 43.58 + 98.43 * mm
    screw_x4: float               =  3.9 + 23.96 * mm
    
    # Extension dimensions
    ext_position_y: float         =  10. * mm
    ext_position_x: float         =  78. - 10. * mm
    ext_diameter: float           =  2.5 * mm
    ext_radius: float             = 19.52/2 * mm
    
    # Charger dimensions
    charger_position_x: float     =  78. / 2. * mm
    charger_position_y: float     =  75. * mm
    charger_inner_diameter: float =  46. * mm
    charger_outer_diameter: float =  54. * mm
    
    # Camera dimensions
    camera1_x: float         =  3.9 + 23.96 * mm
    camera1_y: float         =  143.0 * mm
    camera1_w: float         =  10.6 * mm
    camera1_h: float         =  22.0 * mm
    camera1_r: float         =   5.0 * mm

    camera2_x: float         =  11. * mm
    camera2_y: float         =  152.5 * mm
    camera2_diameter: float  =  19. * mm

    camera3_x: float         =  11. * mm
    camera3_y: float         =  153.5 - 22. * mm
    camera3_diameter: float  =  19. * mm

    cameraF_x: float         =  11. * mm
    cameraF_y: float         =  142.5 * mm
    cameraF_w: float         =  20. * mm
    cameraF_h: float         =  22. + 19. * mm
    cameraF_r: float         =   9.5 * mm
    
    # Plugs dimensions
    usbc_width: float         =   8.4 * mm
    usbc_height: float        =   2.6 * mm
    usbc_radius: float        =   1.25 * mm
    usbc_inside_width: float  =   6.65 * mm
    usbc_inside_height: float =   1.6 * mm



P = Parameters()
set_defaults(reset_camera=Camera.KEEP,)


# [Helper models]

def do_camera(x, y, z, diameter, frame, height, name="camera"):
    """Create a camera with a frame"""
    outer_radius = diameter / 2
    inner_radius = (diameter - frame) / 2
    
    with BuildPart(Plane.XY.offset(z)) as bottom:
        with Locations((x, y)):
            Cylinder(inner_radius, 0.01, mode=Mode.ADD)

    with BuildPart(Plane.XY.offset(z+0.01)) as outer:
        with Locations((x, y)):
            Cylinder(inner_radius*0.4, 0.01, mode=Mode.ADD)

    with BuildPart(Plane.XY.offset(z+0.02)) as inner:
        with Locations((x, y)):
            Cylinder(inner_radius*0.3, 0.01, mode=Mode.ADD)
    
    with BuildPart(Plane.XY.offset(z)) as frame:
        with BuildSketch(Plane.XY.offset(z)) as frame_sketch:
            with Locations((x, y)):
                Circle(outer_radius, mode=Mode.ADD)
                Circle(inner_radius, mode=Mode.SUBTRACT)
        extrude(amount=height, mode=Mode.ADD)
    
    with BuildPart(Plane.XY.offset(z+height/2)) as lense:
        with Locations((x, y)):
            Cylinder(inner_radius, height-0.05, mode=Mode.ADD)
        
    
    define (bottom, "#000000ff", f'{name}_bottom')
    define (outer, "#444343bb", f'{name}_outer')
    define (inner, "#282877ff", f'{name}_inner')
    define (frame,  "#bbbdbbff", f'{name}_frame')
    define (lense,  "#f4f44b2c", f'{name}_lens')
    return frame

def do_led(x, y, z, diameter, name="led"):
    with BuildPart(Plane.XY.offset(z+0.01)) as outer:
        with Locations((x, y)):
            Cylinder(diameter, 0.01, mode=Mode.ADD)

    with BuildPart(Plane.XY.offset(z+0.02)) as inner:
        with Locations((x, y)):
            Cylinder(diameter*0.5, 0.01, mode=Mode.ADD)

    define (outer,  "#bbbdbbff", f'{name}_outer')
    define (inner,  "#f4f44b2c", f'{name}_inner')

def do_screw(x, y, z, diameter, name="screw"):
    """Create a screw with a head"""
    head_diameter = diameter * 2.5
    head_height = diameter * 0.5
    # TODO: implement and add this 
    with BuildPart(Plane.XY.offset(z)) as screw:
        with Locations((x, y)):
            Cylinder(diameter/2, head_height, mode=Mode.ADD)
    
    with BuildPart(Plane.XY.offset(z+head_height)) as head:
        with Locations((x, y)):
            Cylinder(head_diameter/2, 0.01, mode=Mode.ADD)
    
    define (screw, "#ccccd3ff", f'{name}_screw')

# [Main]    
if __name__ == "__main__":    
    # [Model]
    
    debug("Loading backplate")
    # Import an STL part (replace with your STL file path)
    stl_path = Path(__file__).parent / "cmf_phone_2_pro_universal_cover_2.stl"
    try:
        importer = Mesher()
        backplate = import_stl(stl_path)
        backplate.move(loc=Location((-P.body_width-8,-23.35,P.body_extrude-0.8)))
        # .rotate(Axis.Z, 45)  # Rotate the backplate to match the orientation
        if yes or P.show_debug:
            define(backplate, "#ffffffdd", "backplate_imported")
            debug(f"Imported STL part from {stl_path}. {type(backplate)}")
    except Exception as e:
        debug(f"Failed to import STL: {e}")
    
    
    debug("Creating model") 

    with BuildPart() as display_cutout:
        with BuildSketch(Plane.XY) as bottom_sketch:
            RectangleRounded(P.body_width, P.body_height, P.body_radius,
                            align=(Align.MIN, Align.MIN))
        extrude(amount=P.display_extrude, mode=Mode.ADD)        
    
    with BuildPart() as display:
        with BuildSketch(Plane.XY) as bottom_sketch:
            RectangleRounded(P.body_width, P.body_height, P.body_radius,
                            align=(Align.MIN, Align.MIN))
        extrude(amount=P.display_extrude, mode=Mode.ADD)        
        bottom_face = display.faces().filter_by(Plane.XY)[0]
        edge = bottom_face.edges()[-1]
        fillet(edge, P.display_extrude/2)
        
            
    with BuildPart() as phone:
        with BuildSketch(Plane.XY) as bottom_sketch:
            RectangleRounded(P.body_width, P.body_height, P.body_radius,
                            align=(Align.MIN, Align.MIN))

            if P.do_screws:
                with Locations(
                    (P.screw_x1, P.screw_y1),
                    (P.screw_x2, P.screw_y2),
                    (P.screw_x3, P.screw_y3),
                    (P.screw_x4, P.screw_y4),
                    ):
                    Circle(P.screw_diameter/2, mode=Mode.SUBTRACT)
                    
                with Locations(
                    (P.ext_position_x, P.ext_position_y)):
                    Circle(P.ext_diameter/2, mode=Mode.SUBTRACT)
        
        extrude(amount=P.body_extrude, mode=Mode.ADD)
        
        active = phone.faces().filter_by(Plane.XZ)
        bottom_face = active[0]
        top_face    = active[1]
        
        active = phone.faces().filter_by(Plane.YZ).filter_by(lambda f: f)
        left_face  = active[0]
        right_face = active[1]
        
        active = phone.faces().filter_by(Plane.XY).filter_by(lambda f: f)
        display_face  = active[0]
        back_face = active[1]
        
        if P.show_debug:
            define(bottom_face, "#ff0000aa", "bottom_face")
            define(top_face, "#00ff00aa", "top_face")
            define(left_face, "#00ffffff", "left_face")
            define(right_face, "#ff00ffff", "right_face")
            define(display_face, "#eeff00ff", "display_face")
            define(back_face, "#f90404", "back_face")
        
        with BuildSketch(bottom_face) as bottom_sketch:
            # Define the sketch on the bottom face
            RectangleRounded(P.usbc_width, P.usbc_height, P.usbc_radius)
            RectangleRounded(   P.usbc_inside_width, P.usbc_inside_height, 
                                P.usbc_inside_height/4, mode=Mode.SUBTRACT)
            
        extrude(amount=-P.usbc_height, mode=Mode.SUBTRACT)
        add(display_cutout.part, mode=Mode.SUBTRACT)
        edges = phone.edges().filter_by(lambda e: e)
        for index in range(len(edges)):
            if P.show_selection:
                define(edges[index], "#ff0000ff", f"edges_{index}")
        if P.do_post_processing:
            pass
            # fillet(edges[3],.6)
            # chamfer(edges[32],2.)
            # chamfer(edges[36],2.)

    define(phone,   "#ccccd3ff", "phone")
    define(display, "#000000ff", "display")

    P.camera1_frame = 1.0
    P.camera2_frame = 5.0
    P.camera3_frame = 5.0
    P.camera1_extrude = 1.0
    P.camera2_extrude = 2.0
    P.camera3_extrude = 2.0
    
    camera1_frame = do_camera(P.camera1_x, P.camera1_y+P.camera1_h/4, P.body_extrude, P.camera1_r*2-0.1, P.camera1_frame, P.camera1_extrude,      'camera1')
    do_led(P.camera1_x, P.camera1_y-P.camera1_h/4, P.body_extrude, P.camera1_r*0.6, 'led')
    camera2_frame = do_camera(P.camera2_x, P.camera2_y, P.body_extrude, P.camera3_diameter-0.1, P.camera2_frame, P.camera2_extrude, 'camera2')
    camera3_frame = do_camera(P.camera3_x, P.camera3_y, P.body_extrude, P.camera3_diameter-0.1, P.camera3_frame, P.camera3_extrude, 'camera3')
                    


    with BuildPart(Plane.XY.offset(P.body_extrude)) as backplate_screws:
        with BuildSketch() as cuts:
            with Locations(
                (P.camera1_x, P.camera1_y)):
                RectangleRounded(P.camera1_w, P.camera1_h, P.camera1_r, mode=Mode.ADD)

            
            with Locations(
                (P.camera2_x, P.camera2_y)):
                Circle(P.camera2_diameter/2, mode=Mode.ADD)

            with Locations(
                (P.camera3_x, P.camera3_y)):
                Circle(P.camera3_diameter/2, mode=Mode.ADD)
            
        with BuildSketch() as screws:
            if P.do_screws:
                with Locations(
                    (P.screw_x1, P.screw_y1),
                    (P.screw_x2, P.screw_y2),
                    (P.screw_x3, P.screw_y3),
                    (P.screw_x4, P.screw_y4),
                    ):
                    Circle(P.screw_diameter/2, mode=Mode.ADD)
                    
                with Locations(
                    (P.ext_position_x, P.ext_position_y)):
                    Circle(P.ext_diameter/2, mode=Mode.ADD)
        extrude(amount=P.backplate_extrude, mode=Mode.ADD)

        if P.do_charger:
            with BuildSketch() as cuts:
                with Locations(
                    (P.charger_position_x, P.charger_position_y)):
                    Circle(P.charger_outer_diameter/2, mode=Mode.ADD)
                    Circle(P.charger_inner_diameter/2, mode=Mode.SUBTRACT)
            extrude(amount=P.backplate_extrude*2, mode=Mode.ADD)
        


    with BuildPart(Plane.XY.offset(P.body_extrude)) as backplate:
        with BuildSketch(Plane.XY.offset(P.body_extrude)) as back_sketch:
            RectangleRounded(   P.body_width, P.body_height, P.body_radius,
                                align=(Align.MIN, Align.MIN))
                
        extrude(amount=P.backplate_extrude, mode=Mode.ADD)
        
        top_face = backplate.faces().filter_by(Plane.XY)[-1]
        edge = top_face.edges()[0]
        fillet(edge, P.backplate_extrude-.11)
        
        if P.do_screws:
            with Locations(
                (P.screw_x1,       P.screw_y1, P.backplate_extrude),
                (P.screw_x2,       P.screw_y2, P.backplate_extrude),
                (P.screw_x3,       P.screw_y3, P.backplate_extrude),
                (P.screw_x4,       P.screw_y4, P.backplate_extrude),
                (P.ext_position_x, P.ext_position_y, P.backplate_extrude/2+0.1),
                ):
                Cylinder(P.screw_head_diameter/2, P.backplate_extrude, mode=Mode.SUBTRACT)

            with Locations(
                (P.ext_position_x, P.ext_position_y, P.backplate_extrude),
                ):
                Cylinder(P.ext_radius, P.backplate_extrude, mode=Mode.SUBTRACT)

            with Locations(
                (P.ext_position_x+P.ext_radius/2, P.ext_position_y-P.ext_radius/2, P.backplate_extrude),
                ):
                Box(P.ext_radius*2, P.ext_radius*2, P.backplate_extrude, 
                    mode=Mode.SUBTRACT)
        
        add(backplate_screws.part, mode=Mode.SUBTRACT)

    with BuildPart(Plane.XY.offset(P.body_extrude)) as charger:
        if P.do_charger:
            with BuildSketch(Plane.XY.offset(P.body_extrude)) as cuts:
                with Locations(
                    (P.charger_position_x, P.charger_position_y)):
                    Circle(P.charger_outer_diameter/2, mode=Mode.ADD)
                    Circle(P.charger_inner_diameter/2, mode=Mode.SUBTRACT)
            extrude(amount=P.backplate_extrude*2, mode=Mode.ADD)

        
    define(backplate, "#e19e18ff", "backplate_2")
    define(charger, "#7c5b18ff", "charger")
    # Show the box
    show(*objects)
    
    # Export the box if do_export is True
    if P.do_export:
        debug("Exporting model")
        id = f'1'

        export_name = __file__ \
                        .replace('{identifier}', id) \
                        .replace('.py', '.stl')
        export_path = Path(__file__).parent / export_name
        console.log(f"[green]Model exported to {export_path}[/green]")
        exporter = Mesher()
        exporter.add_shape(display.part)
        exporter.add_shape(phone.part)
        exporter.add_shape(backplate.part)
        exporter.write(export_path)
        
        exporter = Mesher()
        exporter.add_shape(display.part)
        exporter.write(export_path.with_name(export_path.stem + "_display.stl"))
        
        exporter = Mesher()
        exporter.add_shape(phone.part)
        exporter.write(export_path.with_name(export_path.stem + "_phone.stl"))
        
        exporter = Mesher()
        exporter.add_shape(backplate.part)
        exporter.write(export_path.with_name(export_path.stem + "_backplate.stl"))

        exporter = Mesher()
        exporter.add_shape(camera1_frame.part)
        exporter.add_shape(camera2_frame.part)
        exporter.add_shape(camera3_frame.part)
        exporter.add_shape(charger.part)
        exporter.write(export_path.with_name(export_path.stem + "_addons.stl"))
        
        del exporter        