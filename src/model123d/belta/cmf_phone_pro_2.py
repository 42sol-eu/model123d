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
from ocp_vscode import show, show_object, set_defaults, Camera
from dataclasses import dataclass
from pathlib import Path
import sys
from rich.console import Console
from math import sqrt
from copy import deepcopy as copy

# [Setup]
console = Console()

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
        exporter.add_shape(part.part)
    exporter.write(file_path)
    del exporter

def define(object, color=None, name="", alpha=1.0):
    """Define an object with a name and color"""
    if hasattr(object, 'part'):
        # If the object has a part, use that
        object.part.name = name
        object.color = color
        object.alpha = alpha
    else:
        object.name = name
        object.color = color
        object.alpha = alpha


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
    do_export: bool          = no
    
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
    screw_y2: float               =  18.1 + 98.43 * mm
    screw_x2: float               =   3.9 * mm
    screw_y1: float               =  18.1 * mm
    screw_x1: float               =   3.9 * mm
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
    camera1_x: float          =  3.9 + 23.96 * mm
    camera1_y: float          =  143.0 * mm
    camera1_w: float          =  10.6 * mm
    camera1_h: float          =  22.0 * mm
    camera1_r: float          =   5.0 * mm
    camera1_frame: float = 1.0
    camera1_extrude: float = 1.0
    
    camera2_x: float          =  11. * mm
    camera2_y: float          =  152.5 * mm
    camera2_diameter: float   =  19. * mm
    camera2_frame: float = 5.0
    camera2_extrude: float = 2.0

    camera3_x: float          =  11. * mm
    camera3_y: float          =  153.5 - 22. * mm
    camera3_diameter: float   =  19. * mm
    camera3_frame: float = 5.0
    camera3_extrude: float = 2.0
    
    cameraF_x: float          =  11. * mm
    cameraF_y: float          =  142.5 * mm
    cameraF_w: float          =  20. * mm
    cameraF_h: float          =  22. + 19. * mm
    cameraF_r: float          =   9.5 * mm
    
    # Plugs dimensions
    usbc_width: float         =  0.1 + 8.4 * mm
    usbc_height: float        =  0.1 + 2.6 * mm
    usbc_extrude: float       =   8.0 * mm
    usbc_radius: float        =   1.25 * mm
    usbc_inside_width: float  =   6.65 * mm
    usbc_inside_height: float =   1.6 * mm

objects = []


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
    define (lense,  "#f4f44b2c", f'{name}_lens', alpha=0.2)
    
    compound = Compound([frame.part, bottom.part, outer.part, inner.part, lense.part], label=name)
    define(compound, name=f'{name}')
    return compound, frame, bottom, outer, inner, lense, bottom

def do_led(x, y, z, diameter, name="led"):
    with BuildPart(Plane.XY.offset(z+0.01)) as outer:
        with Locations((x, y)):
            Cylinder(diameter, 0.01, mode=Mode.ADD)

    with BuildPart(Plane.XY.offset(z+0.02)) as inner:
        with Locations((x, y)):
            Cylinder(diameter*0.5, 0.01, mode=Mode.ADD)

    define(outer,  "#bbbdbbff", f'{name}_outer')
    define(inner,  "#f4f44b2c", f'{name}_inner')
    led = Compound([outer.part, inner.part], label=name)
    define(led, "#f4f44b2c", f'{name}_led')
    return led, outer, inner

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
            
            if 0: # Do not make the inside part
                RectangleRounded(   P.usbc_inside_width, P.usbc_inside_height, 
                                    P.usbc_inside_height/4, mode=Mode.SUBTRACT)
            
        extrude(amount=-P.usbc_extrude, mode=Mode.SUBTRACT)
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

    define(phone,   "#ccccd3ff", "phone.body")
    define(display, "#000000ff", "phone.display")


    
    camera1, camera1_frame, camera1_lense, camera1_inner, camera1_outer, camera1_lense, camera1_back = do_camera(P.camera1_x, P.camera1_y+P.camera1_h/4, P.body_extrude, P.camera1_r*2-0.1, P.camera1_frame, P.camera1_extrude,      'camera1')
    led, outer, inner = do_led(P.camera1_x, P.camera1_y-P.camera1_h/4, P.body_extrude, P.camera1_r*0.6, 'led')
    camera2, camera2_frame, camera2_lense, camera2_inner, camera2_outer, camera2_lense, camera2_back = do_camera(P.camera2_x, P.camera2_y, P.body_extrude, P.camera3_diameter-0.1, P.camera2_frame, P.camera2_extrude, 'camera2')
    camera3, camera3_frame, camera3_lense, camera3_inner, camera3_outer, camera3_lense, camera3_back = do_camera(P.camera3_x, P.camera3_y, P.body_extrude, P.camera3_diameter-0.1, P.camera3_frame, P.camera3_extrude, 'camera3')
                    


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

    with BuildPart(Plane.XY.offset(P.body_extrude)) as charger_frame:
        with BuildSketch(Plane.XY.offset(P.body_extrude)) as cuts:
            with Locations(
                (P.charger_position_x, P.charger_position_y)):
                Circle(P.charger_outer_diameter/2-0.1, mode=Mode.ADD)
                Circle(P.charger_inner_diameter/2, mode=Mode.SUBTRACT)
        extrude(amount=P.backplate_extrude, mode=Mode.ADD)

    define(backplate, "#18e162ff", "phone.backplate")
    define(charger_frame, "#5cd10eff", "charger")

    P_arm_width: float = 10.0 * mm
    P_arm1_y_height: float = P.screw_y2 - P.screw_y1 
    P_arm2_x_height: float = P.screw_x4 - P.screw_x1
    P_arm_extrude: float = 5.0 * mm
    with BuildPart(Plane.XY.offset(P.body_extrude+P.backplate_extrude)) as arm1:
        with Locations(
                Location((P.screw_x1, P.screw_y2)),
            ):
            Box(P_arm_width, P_arm1_y_height, P_arm_extrude, align=(Align.CENTER, Align.MAX), mode=Mode.ADD)   
            Box(P_arm2_x_height, P_arm_width, P_arm_extrude, align=(Align.MIN, Align.CENTER), mode=Mode.ADD)
    define(arm1, "#0000ffff", "belta.arm1")

    objects = \
            { "phone": {
                "body": phone,
                "display": display,
                "back": {
                    "backplate": backplate,
                    "charger": charger_frame,
                    "camera1": {
                        "frame": camera1_frame,
                        "lense": camera1_lense,
                        "inner": camera1_inner,
                        "outer": camera1_outer,
                        "back":  camera1_back,
                        
                    },
                    "camera2": {
                        "frame": camera2_frame,
                        "lense": camera2_lense,
                        "inner": camera2_inner,
                        "outer": camera2_outer,
                        "back":  camera2_back,
                    },
                    "camera3": {
                        "frame": camera3_frame,
                        "lense": camera3_lense,
                        "inner": camera3_inner,
                        "outer": camera3_outer,
                        "back":  camera3_back,
                    },
                    "led": {
                        "outer": outer,
                        "inner": inner,
                    }
                },
                
            },
            "belta": {
                "arm1": arm1,
            },
    }

    show(objects, glass=no)

    # Export the box if do_export is True
    if P.do_export:
        debug("Exporting model")
        id = f'1'

        export_name = __file__ \
                        .replace('{identifier}', id) \
                        .replace('.py', '.stl')
        export_path = Path(__file__).parent / export_name
        console.log(f"[green]Model exported to {export_path}[/green]")
        

        # Full model:
        export_parts_to_stl(export_path, [display, phone, backplate, charger, camera1_frame, camera2_frame, camera3_frame])
        
        # Individual parts:
        export_parts_to_stl((export_path, "display", "1"), [display])
        export_parts_to_stl((export_path, "phone", "1"), [phone])
        export_parts_to_stl((export_path, "backplate", "1"), [backplate])
        export_parts_to_stl([export_path, "addons", "1"], [camera1_frame, camera2_frame, camera3_frame, charger_frame])
        export_parts_to_stl((export_path, "lenses", "1"), [camera1_lense, camera2_lense, camera3_lense])
        # 3mf export
        export_name = export_name.replace('.stl', '.3mf')
        export_path = Path(__file__).parent / export_name
        