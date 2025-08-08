# -*- coding: utf-8 -*-
"""
----
file-name:       stones.py
file-uuid:       edc816e2-341f-4bb8-b986-9f22ff345e76
description:    3D models for Tak game stones and extendable board using build123d
author:         felix@42sol.eu
project:
    name:       model123d
    uuid:       fe521ba0-4ad7-484d-9386-26de71379e15
    url:        https://www.github.com/42sol/model123d
"""
# %% [Constants]
no = False 
yes = True
mm = 1
# %% [Imports]
from build123d import *
from dataclasses import dataclass
from rich import print
from pathlib import Path

def debug(msg):
    """Print debug message if show_debug is True"""
    if Parameters.show_debug:
        print(f"[blue]DEBUG: {msg}[/blue]")

def file_path():
    """Return the path to the current file"""
    return Path(__file__).parent.resolve()

# %% [Parameters]
@dataclass
class Parameters:
    """Parameters for the stones.py"""
    show_debug:    bool =    yes
    do_show:       bool =    yes
    do_export:     bool =    yes
    export_folder: Path = file_path() / "_export"
    
    def __init__(self):
        debug("Initializing core parameters")

# %% [Stone Parameters]
@dataclass
class StoneParameters(Parameters):
    height:           float   = 21.0 * mm
    width:            float   = 21.0 * mm
    field_xy:          float   = 32.0 * mm
    depth:            float   =  8.5 * mm
    field_height:      float   =  6.0 * mm
    bevel:            float   =  0.5 * mm
    mod_b:            float   = 10.0 * mm  # modifier for bevel
    font:             str    = "Arial"     # TODO: implement a font inset
    do_rounded:       bool   = yes
    do_chamfer:       bool   = yes
    do_inset_t:       bool   = no
    do_inset_b:       bool   = no
    do_corner_stone:  bool   = yes
    stack_height: int    = 1
    def __init__(self):
        debug("Initializing stone parameters")
        super().__init__()

# %% [Tak Stone Model]
class TakStone:
    """3D model for a Tak stone using build123d."""

    def __init__(self, params: StoneParameters = StoneParameters()):
        self.params = params


    def build(self) -> BuildPart:
        P = self.params
        debug(f"[bold green]Building TakStone with parameters:[/bold green] {self.params}")
        
        with BuildPart() as stone:
            
            if P.do_rounded:
                with BuildSketch() as sketch:
                    P = self.params
                    mod_b = P.mod_b 
                    RectangleRounded(
                                P.height, P.width,
                                radius=P.bevel * mod_b
                            )
                extrude(sketch.sketch,amount= P.depth)
            else:
                Box(P.height, P.width, P.depth)
            if P.do_chamfer:
                debug(f"Applying chamfer with radius {P.bevel} mm")
                # Apply chamfer to edges
                chamfer(stone.edges(), length=P.bevel)
            else:
                debug(f"Applying fillet with radius {P.bevel} mm")
                # Apply fillet to edges
                fillet(stone.edges(), radius=P.bevel)
                
            faces = stone.faces().filter_by(Axis.Z, 0)
                
            if P.do_inset_b:
                debug("Applying inset for stone decoration")
                # Create an inset for decoration
                inset_part = self._create_inset(faces[0], modifier_z=1.0)
                add(inset_part, mode=Mode.SUBTRACT)
            if P.do_inset_t:
                upset_part = self._create_inset(faces[-1], modifier_xy=1.0)
                add(upset_part, mode=Mode.ADD)
                
            if P.do_corner_stone:
                debug("Creating corner stone")
                # Create a corner stone
                corner_part = self._create_corner_stone(faces[-1])
                add(corner_part, mode=Mode.ADD)

        self.part = stone.part
        
        return self

    def _create_corner_stone(self, face: Face) -> BuildPart:
        """
        Create a corner stone by applying a rounded rectangle inset.
        """
        P = self.params
        width = 0.8 * min(P.height, P.width)/2
        height = 2.0 * width
        
        pts = [
            (-0.5*width, height),
            (-0.7*width, 0.90*height),
            (-0.6*width, 0.85*height),
            (-0.7*width, 0.80*height),
            (-0.6*width, 0.75*height),
            (-0.7*width, 0.70*height),
            (-0.6*width, 0.65*height),
            (-0.9*width, 0.5*height),
            (-0.8*width, 0),
            (-0.5*width, 0),
            (-0.5*width, 0.1 * height),
            (-0.4*width, 0.5 * height),
            (-0.4*width, height),
        ]

        with BuildPart() as figure:
            with BuildSketch(Plane.XZ) as sketch:
                with BuildLine() as line:
                    l1 = Polyline(pts)
                    l2 = Line(l1 @ 1, l1 @ 0)
                make_face()
            revolve(axis=Axis.Z)
            fillet(figure.edges(), radius=0.5*P.bevel)
        # Move the figure to the center of the given face
        center = face.center()
        return figure.part.move(Location(center))

    def _create_corner_stone_spline(self, face: Face) -> BuildPart:
        """
        Create a corner stone by applying a rounded rectangle inset.
        """
        P = self.params
        width = 0.8 * min(P.height, P.width)/2
        height = 2.0 * width
        
        pts = [
            (-0.41*width, height),
            (-0.65*width, 0.85*height),
            (-0.6*width, 0.80*height),
            (-0.6*width, 0.75*height),
            (-0.55*width, 0.725*height),
            (-0.6*width, 0.70*height),
            (-0.55*width, 0.675*height),
            (-0.6*width, 0.65*height),
            (-0.55*width, 0.625*height),
            (-0.7*width, 0.5*height),
            (-0.75*width, 0.4*height),
            (-0.8*width, 0.2*height),
            (-0.7*width, 0.05*height),
            (-0.6*width, -2*P.bevel),
            (-0.5*width, 0.1 * height),
            (-0.4*width, 0.5 * height),
            (-0.4*width, height),
        ]

        with BuildPart() as figure:
            with BuildSketch(Plane.XZ) as sketch:
                with BuildLine() as line:
                    l1 = Spline(pts)
                    l2 = Line(l1 @ 1, l1 @ 0)
                make_face()
            revolve(axis=Axis.Z)
            # fillet(figure.edges(), radius=P.bevel)
        # Move the figure to the center of the given face
        center = face.center()
        return figure.part.move(Location(center))
    
    def _create_inset(self, face: Face, modifier_xy=0.0, modifier_z=0.0) -> BuildPart:
        """ Create an inset for decoration on the given face.
        """
        with BuildPart(face) as inset:
            P = self.params
            mod_b = P.mod_b
            if P.do_rounded:
                with BuildSketch(face) as sketch:
                    RectangleRounded(
                        P.height - mod_b * P.bevel - modifier_xy, 
                        P.width  - mod_b * P.bevel - modifier_xy,
                        radius=P.bevel * mod_b 
                    )
                extrude(sketch.sketch, amount= P.bevel * mod_b/2 + modifier_z,
                        both=yes)
            else:
                Box(P.height - mod_b * P.bevel - modifier_xy, 
                    P.width  - mod_b * P.bevel - modifier_xy, 
                    P.bevel * mod_b            + modifier_z)
                
            if P.do_chamfer:
                chamfer(inset.edges(), length=P.bevel)
            else:
                fillet(inset.edges(), radius=P.bevel)
        return inset.part
        
    
    def export(self) -> BuildPart:        
        P = self.params
        debug("[yellow]Exporting STL...[/yellow]")
        
        if not  P.export_folder.exists():
            P.export_folder.mkdir(parents=True, exist_ok=True)
            debug(f"Created export folder: {P.export_folder}")
        
        # Export using build123d's Mesher
        mesher = Mesher()
        export_part = self.part
        # set type_str based on inset and rotate part based on inset
        if P.do_inset_b and P.do_inset_t    :
            type_str = "_inset_both" 
            if P.stack_height == 1:
                export_part = self.part.rotate(Axis.X, 90)

        elif P.do_inset_t:
            type_str = "_inset_top"
            if P.stack_height == 1:
                export_part = self.part.rotate(Axis.X, 0)

        elif P.do_inset_b:
            type_str = "_inset_bottom"
            if P.stack_height == 1:
                export_part = self.part.rotate(Axis.X, 180)
        else:
            type_str = "_plain"
            if P.stack_height == 1:
                export_part = self.part.rotate(Axis.X, 90)

        if P.stack_height > 1:
            pass
        
        if P.do_rounded:
            type_str += "_rounded"
        if P.do_corner_stone:
            type_str += "_corner"

        mesher.add_shape(export_part)
        
        mesher.write( P.export_folder/ f"tak_stone{type_str}.stl" )
        debug(f"Model exported as {P.export_folder / f'tak_stone{type_str}.stl'}")
        return self
            

class Field4by4:
    """3D model for a 4x4 Tak game field using build123d."""
    
    def __init__(self, params: StoneParameters = StoneParameters()):
        self.params = params
        self.stones = []
    
    def build(self) -> BuildPart:
        P = self.params
        debug(f"[bold green]Building Field4by4 with parameters:[/bold green] {self.params}")
        length = P.field_xy
        with BuildPart() as field:
            Box(4*length+2, 4*length+2, P.field_height)
            
            with Locations((0, 0, P.field_height/2)):
                with GridLocations(length, length, 4, 4):
                    stone = Box(length-2, length-2, P.field_height*0.4, mode=Mode.ADD)
                with GridLocations(length, length, 5,5):
                    spacer = Box( 8, 8, P.field_height, rotation=(0,0,45.),mode=Mode.SUBTRACT)
            
            with GridLocations(length, length, 5,5):
                spacer = Box( 8, 8, P.field_height, rotation=(0,0,45.))
            # Cut the outer edges to make spacers flat

            with BuildPart() as frame:
                Box(4*length+12, 4*length+12, P.field_height)
                Box(4*length+2, 4*length+2, P.field_height, mode=Mode.SUBTRACT)
            add(frame, mode=Mode.SUBTRACT)

            with GridLocations(4*length+3, 4*length+3, 2,2):
                Box( 8, 8, 2*P.field_height, rotation=(0,0,45.), mode=Mode.SUBTRACT)

            with GridLocations(4*length+3, 4*length+3, 1, 2):
                with GridLocations(length, length, 3,1):
                    Box( 6, 6, 2*P.field_height, rotation=(0,0,45.), mode=Mode.SUBTRACT)

            with GridLocations(4*length+3, 4*length+3, 2, 1):
                with GridLocations(length, length, 1,3):
                    Box( 6, 6, 2*P.field_height, rotation=(0,0,45.), mode=Mode.SUBTRACT)
            
            # Add magnet openings (5mm diameter, 2mm deep) at the center of each field cell
            magnet_diameter = 5 * mm
            magnet_depth = 1.5 * mm
            # Place magnets on the outside faces, 4 per side
            magnet_offset = (4*length+2)/2 - magnet_depth/2 - 0.8
            magnet_z = 0
            
            # Move magnet slots to be accessed from below, 1 layer below the outer frame
            magnet_slot_z = magnet_z  # below the field base
            magnet_modes = Mode.SUBTRACT
            # Left and right sides (Y varies, X fixed)
            for i in range(4):
                y = -1.5 * length + i * length
                # Left side (X-)
                with Locations((-magnet_offset, y, magnet_slot_z)):
                    Cylinder(radius=magnet_diameter / 2, height=magnet_depth, rotation=(0, 90., 0), mode=magnet_modes)
                    Box(magnet_diameter/2, magnet_diameter, magnet_depth, rotation=(0, 90., 0), mode=magnet_modes, align=(Align.MAX, Align.CENTER, Align.CENTER))
                    
                # Right side (X+)
                with Locations((magnet_offset, y, magnet_slot_z)):
                    Cylinder(radius=magnet_diameter / 2, height=magnet_depth, rotation=(0, 90., 0), mode=magnet_modes)
                    Box(magnet_diameter/2, magnet_diameter, magnet_depth, rotation=(0, 90., 0), mode=magnet_modes, align=(Align.MAX, Align.CENTER, Align.CENTER))
                    
                    
            # Top and bottom sides (X varies, Y fixed)
            for i in range(4):
                x = -1.5 * length + i * length
                # Bottom side (Y-)
                with Locations((x, -magnet_offset, magnet_slot_z)):
                    Cylinder(radius=magnet_diameter / 2, height=magnet_depth, rotation=(90., 0, 0), mode=magnet_modes)
                    Box(magnet_diameter/2, magnet_depth, magnet_diameter, rotation=(0, 90., 0), mode=magnet_modes, align=(Align.MAX, Align.CENTER, Align.CENTER))
                # Top side (Y+)
                with Locations((x, magnet_offset, magnet_slot_z)):
                    Cylinder(radius=magnet_diameter / 2, height=magnet_depth, rotation=(90., 0, 0), mode=magnet_modes)
                    Box(magnet_diameter/2, magnet_depth, magnet_diameter, rotation=(0, 90., 0), mode=magnet_modes, align=(Align.MAX, Align.CENTER, Align.CENTER))

            # Add a triangle on top of each field cell
            triangle_height = P.field_height * 0.08
            triangle_base = 1.
            triangle_offset_z = P.field_height * 0.34

            with BuildSketch(Plane.XY.offset(triangle_offset_z)) as tri_sketch:
                with GridLocations(4*length+3, 4*length-5, 1, 2):
                    with GridLocations(length, length, 4,1):
                        Triangle(   a=triangle_base, b=triangle_base+1, c=triangle_base+1,
                                    rotation=0.0)

            extrude(tri_sketch.sketch, amount=triangle_height, mode=Mode.SUBTRACT)

            with BuildSketch(Plane.XY.offset(triangle_offset_z)) as tri_sketch:

                with GridLocations(4*length-5, 4*length+3, 2, 1):
                    with GridLocations(length, length, 1,4):
                        Triangle(   a=triangle_base, b=triangle_base+1, c=triangle_base+1,
                                    rotation=90.0)

            extrude(tri_sketch.sketch, amount=triangle_height, mode=Mode.SUBTRACT)



        self.part = field.part
        return self 
    
    def export(self) -> BuildPart:
        P = self.params
        debug("[yellow]Exporting Field4by4 STL...[/yellow]")
        
        if not  P.export_folder.exists():
            P.export_folder.mkdir(parents=True, exist_ok=True)
            debug(f"Created export folder: {P.export_folder}")
        
        # Export using build123d's Mesher
        mesher = Mesher()
        mesher.add_shape(self.part)
        mesher.write( P.export_folder / "tak_field_4x4.stl" )
        debug(f"Field model exported as {P.export_folder / 'tak_field_4x4.stl'}")
        return self

# %% [Setup]
debug("Creating Tak stone model")
P = StoneParameters()

# %% [Display]
if P.do_show:
    try:
        from ocp_vscode import show, set_port
        set_port(3939)
        M1 = TakStone(P)
        M1.params.do_corner_stone = yes 
        corner_stone = M1.build().part.move(Location((P.field_xy, 0, 0)))
        M1.params.do_corner_stone = no
        stone_model = M1.build().part.move(Location((P.field_xy, P.field_xy, 0)))
        M2 = Field4by4(P)
        field_4x4 = M2.build().part.move(Location((0, 0, -10)))
        show(field_4x4, corner_stone, stone_model, names=["field_4x4","corner_stone", "stone_model"])
    except ImportError:
        print("ocp_vscode.show not available. Model built but not displayed.")

# %% [Export]
if P.do_export:
    debug("Exporting model")
    try:
        M1.params.do_corner_stone = yes
        M1.export()
        M1.params.do_corner_stone = no
        M1.export()
        M2.export()
    except Exception as e:
        print(f"Export failed: {e}")

# %% [End of file]