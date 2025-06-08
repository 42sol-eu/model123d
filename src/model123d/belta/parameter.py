from dataclasses import dataclass
from helper import *

@dataclass
class Parameters:
    """Parameters for the ${TM_FILENAME}"""
    show_debug: bool          = no
    show_selection: bool      = no
    show_nose: bool           = no
    do_imports: bool          = no
    do_details: bool          = no
    do_screw_holes: bool      = yes
    do_backplate_screws: bool = yes
    do_charger: bool          = yes
    do_post_processing: bool  = no
    do_export: bool           = no
    
    # Device dimensions
    body_height: float            = 164.0
    body_radius: float            =   9.0
    body_width: float             =  78.0
    body_extrude: float           =   7.8 - 1.5 + 0.2
    display_extrude: float        =   1.0
    backplate_extrude: float      =   1.3
    hole_diameter: float          =   2.0

    # Screw dimensions
    
    screw_diameter: float         =   2.20
    screw_head_diameter1: float   =   5.2
    screw_head_extrude: float     =   0.3
    screw_head_diameter: float    =   5.85
    screw_y1: float               =  18.1
    screw_x1: float               =   3.9
    screw_y2: float               =  18.1 + 98.43
    screw_x2: float               =   3.9
    screw_y3: float               =  18.1 + 43.58 + 98.43
    screw_x3: float               =  3.9 + 23.96
    screw_y4: float               =  18.1 + 98.43
    screw_x4: float               =  78.0 - 3.9
    
    # Extension dimensions
    ext_position_y: float         =  10.0
    ext_position_x: float         =  78.0 - 10.0
    ext_diameter: float           =  2.5
    ext_radius: float             = 19.52/2
    
    # Charger dimensions
    charger_position_x: float     =  78.0 / 2.0
    charger_position_y: float     =  75.0
    charger_inner_diameter: float =  46.0
    charger_outer_diameter: float =  54.0
    
    # Camera dimensions
    camera1_x: float          =  3.9 + 23.96
    camera1_y: float          =  143.0
    camera1_w: float          =  10.6
    camera1_h: float          =  22.0
    camera1_r: float          =   5.0
    camera1_frame: float = 1.0
    camera1_extrude: float = 1.0
    
    camera2_x: float          =  11.0
    camera2_y: float          =  152.5
    camera2_diameter: float   =  19.0
    camera2_frame: float = 5.0
    camera2_extrude: float = 2.0

    camera3_x: float          =  11.0
    camera3_y: float          =  153.5 - 22.0
    camera3_diameter: float   =  19.0
    camera3_frame: float = 5.0
    camera3_extrude: float = 2.0
    
    cameraF_x: float          =  11.0
    cameraF_y: float          =  142.5
    cameraF_w: float          =  20.0
    cameraF_h: float          =  22.0 + 19.0
    cameraF_r: float          =   9.5
    
    # Plugs dimensions
    usbc_width: float         =  0.1 + 8.4
    usbc_height: float        =  0.1 + 2.6
    usbc_extrude: float       =   8.0
    usbc_radius: float        =   1.25
    usbc_inside_width: float  =   6.65
    usbc_inside_height: float =   1.6
