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

# %% [Imports]
from build123d import *
from dataclasses import dataclass
from rich import print
from pathlib import Path
from ocp_vscode import show, set_port, set_defaults, Camera
from ocp_vscode import ColorMap, set_colormap
import inspect

# %% [Constants]
no = False
yes = True
mm = 1

# %% [Functions]

def debug(msg):
    """Print debug message if show_debug is True"""
    if Parameters.show_debug:
        frame = inspect.currentframe().f_back
        line_no = frame.f_lineno
        print(f"[blue]DEBUG: {msg}[/blue] {__file__}:{line_no}")


def file_path():
    """Return the path to the current file"""
    return Path(__file__).parent.resolve()


def setup_colormap(colormap_type: str = "tab20") -> None:
    """Setup the OCP colormap for automatic coloring."""
    try:
        # Try using built-in OCP colormaps first
        if colormap_type == "tab20":
            colormap = ColorMap.tab20(alpha=0.8)
        elif colormap_type == "segmented":
            colormap = ColorMap.segmented(["red", "green", "blue", "yellow", "magenta", "cyan"], alpha=0.8)
        else:
            # Try golden_ratio with the specified colormap
            colormap = ColorMap.golden_ratio(colormap_type, alpha=0.8)
        
        set_colormap(colormap)
        debug(f"Colormap setup successful: {colormap_type}")
    except Exception as e:
        debug(f"Colormap setup failed: {e}")
        # Fallback to default segmented colormap
        colormap = ColorMap.segmented(["red", "green", "blue", "yellow", "magenta", "cyan"])
        set_colormap(colormap)
        debug("Using fallback segmented colormap")


def get_colormap_colors(n_colors, colormap_name='viridis', alpha=1.0):
    """Generate n_colors using manual color generation (fallback method)
    
    Args:
        n_colors (int): Number of colors to generate
        colormap_name (str): Name of the colormap (unused, kept for compatibility)
        alpha (float): Alpha transparency (0.0-1.0)
    
    Returns:
        list: List of color strings in hex format with alpha
    """
    # Fallback to default colors when not using set_colormap approach
    default_colors = ["#FF0000ff", "#00FF00ff", "#0000FFff", "#FFFF00ff", "#FF00FFff", "#00FFFFff"]
    return (default_colors * ((n_colors // len(default_colors)) + 1))[:n_colors]


# %% [Parameters]
@dataclass
class Parameters:
    """Parameters for the stones.py"""

    show_debug: bool = yes
    do_show: bool = yes
    do_export: bool = yes
    do_copyrights: bool = no
    use_colormap: bool = yes  # Use OCP colormap for colors
    export_folder: Path = file_path() / "_export"

    def __init__(self):
        debug("Initializing core parameters")


# %% [Stone Parameters]
@dataclass
class StoneParameters(Parameters):
    """Parameters for the Tak game stones and field."""

    height: float = 21.0 * mm
    width: float = 21.0 * mm
    depth: float = 8.5 * mm
    bevel: float = 0.5 * mm
    mod_b: float = 10.0 * mm  # modifier for bevel
    font: str = "Arial"  # TODO: implement a font inset
    do_rounded: bool = yes
    do_chamfer: bool = yes
    do_inset_t: bool = no
    do_inset_b: bool = no
    do_corner_stone: bool = yes
    stack_height: int = 1

    def __init__(self):
        debug("Initializing stone parameters")
        super().__init__()


@dataclass
class FieldParameters(StoneParameters):
    """Parameters for the Tak game board fields."""

    fields: int = 3
    fields_x: int = 3
    fields_y: int = 3
    field_xy: float = 32.0 * mm
    field_height: float = 6.0 * mm
    nozzle_diameter: float = 0.8 * mm
    min_fields: int = 3
    max_fields: int = 8
    do_outer_cuts: bool = yes
    do_magnet_guide: bool = no
    debug_magnets: bool = no

    def __init__(self, stone_params: StoneParameters = StoneParameters()):
        """Initialize field parameters based on stone parameters."""
        debug("Initializing field parameters")
        super().__init__()
        # Use stone parameters to set field dimensions
        if self.nozzle_diameter >= 0.8 * mm:
            self.field_height = self.field_height / 0.4 * 0.8
        self.height = stone_params.height
        self.width = stone_params.width
        self.depth = stone_params.depth
        self.bevel = stone_params.bevel


class MagnetSlots:
    """Parameters for the magnet slots in the Tak game board.
    TODO: complete this model and move it to noah123d
    """

    diameter: float = 5.0 * mm
    depth: float = 1.5 * mm
    offset_x: float = 0.8 * mm
    offset_y: float = 0.8 * mm
    z: float = 0.0

    def __init__(self, nozzle_size: float = 0.8 * mm, layer_height: float = 0.4 * mm):
        """Initialize magnet slot parameters.
        - includes its own parameters.
        """
        debug("Initializing magnet slot parameters")
        self.nozzle_size = nozzle_size
        self.layer_height = layer_height
        if self.nozzle_size >= 0.8 * mm:
            self.addon = 0.8 * mm
        else:
            self.addon = 0.4 * mm

    def build(
        self,
        position: Location = Location((0, 0, 0)),
        rotation: RotationLike = (0, 0, 0),
        do_marker: bool = False,
    ) -> BuildPart:
        """Build the magnet slots based on parameters."""
        debug("Building magnet slots")

        with BuildPart(position) as slots:
            # Create a cylinder for the magnet slot
            Cylinder(radius=(self.diameter + self.addon) / 2, height=self.depth)
            # Create a box for the magnet slot
            Box(
                self.diameter / 2 + self.addon,
                self.diameter + self.addon,
                self.depth - 0.1,
                align=(Align.MAX, Align.CENTER, Align.CENTER),
            )

            if do_marker:
                # orientation guide
                Box(
                    self.diameter / 2 + self.addon,
                    2 * self.addon,
                    1.6 * self.depth + self.addon - 0.2,
                    align=(Align.MAX, Align.CENTER, Align.MAX),
                )

        slots.part = slots.part.rotate(Axis.X, rotation[0])
        slots.part = slots.part.rotate(Axis.Y, rotation[1])
        slots.part = slots.part.rotate(Axis.Z, rotation[2])

        return slots.part


# %% [Tak Stone Model]
class TakStone:
    """3D model for a Tak stone using build123d."""

    def __init__(self, params: StoneParameters = StoneParameters()):
        self.params = params
        self._part = None
        self._name = "Tak_stone_unspecified"

    @property
    def name(self) -> str:
        """Return the name of the stone."""
        return self._name

    @property
    def part(self) -> Part:
        """Return the part of the stone."""
        if self._part is None:
            raise ValueError("Stone part not built yet. Call build() first.")
        return self._part

    def build(self) -> BuildPart:
        """Build the Tak stone model based on parameters."""
        P = self.params
        debug(
            f"[bold green]Building TakStone with parameters:[/bold green] {self.params}"
        )

        with BuildPart() as stone:

            if P.do_rounded:
                with BuildSketch() as sketch:
                    P = self.params
                    mod_b = P.mod_b
                    RectangleRounded(P.height, P.width, radius=P.bevel * mod_b)
                extrude(sketch.sketch, amount=P.depth)
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

        self._part = stone.part

        return self

    def _create_corner_stone(self, face: Face) -> BuildPart:
        """Create a corner stone by applying a rounded rectangle inset."""
        P = self.params
        width = 0.8 * min(P.height, P.width) / 2
        height = 2.0 * width

        pts = [
            (-0.5 * width, height),
            (-0.7 * width, 0.90 * height),
            (-0.6 * width, 0.85 * height),
            (-0.7 * width, 0.80 * height),
            (-0.6 * width, 0.75 * height),
            (-0.7 * width, 0.70 * height),
            (-0.6 * width, 0.65 * height),
            (-0.9 * width, 0.5 * height),
            (-0.8 * width, 0),
            (-0.5 * width, 0),
            (-0.5 * width, 0.1 * height),
            (-0.4 * width, 0.5 * height),
            (-0.4 * width, height),
        ]

        with BuildPart() as figure:
            with BuildSketch(Plane.XZ) as sketch:
                with BuildLine() as line:
                    l1 = Polyline(pts)
                    l2 = Line(l1 @ 1, l1 @ 0)
                make_face()
            revolve(axis=Axis.Z)
            fillet(figure.edges(), radius=0.5 * P.bevel)
        # Move the figure to the center of the given face
        center = face.center()
        return figure.part.move(Location(center))

    def _create_corner_stone_spline(self, face: Face) -> BuildPart:
        """
        Create a corner stone by applying a rounded rectangle inset.
        """
        P = self.params
        width = 0.8 * min(P.height, P.width) / 2
        height = 2.0 * width

        pts = [
            (-0.41 * width, height),
            (-0.65 * width, 0.85 * height),
            (-0.6 * width, 0.80 * height),
            (-0.6 * width, 0.75 * height),
            (-0.55 * width, 0.725 * height),
            (-0.6 * width, 0.70 * height),
            (-0.55 * width, 0.675 * height),
            (-0.6 * width, 0.65 * height),
            (-0.55 * width, 0.625 * height),
            (-0.7 * width, 0.5 * height),
            (-0.75 * width, 0.4 * height),
            (-0.8 * width, 0.2 * height),
            (-0.7 * width, 0.05 * height),
            (-0.6 * width, -2 * P.bevel),
            (-0.5 * width, 0.1 * height),
            (-0.4 * width, 0.5 * height),
            (-0.4 * width, height),
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
        """Create an inset for decoration on the given face."""
        with BuildPart(face) as inset:
            P = self.params
            mod_b = P.mod_b
            if P.do_rounded:
                with BuildSketch(face) as sketch:
                    RectangleRounded(
                        P.height - mod_b * P.bevel - modifier_xy,
                        P.width - mod_b * P.bevel - modifier_xy,
                        radius=P.bevel * mod_b,
                    )
                extrude(
                    sketch.sketch, amount=P.bevel * mod_b / 2 + modifier_z, both=yes
                )
            else:
                Box(
                    P.height - mod_b * P.bevel - modifier_xy,
                    P.width - mod_b * P.bevel - modifier_xy,
                    P.bevel * mod_b + modifier_z,
                )

            if P.do_chamfer:
                chamfer(inset.edges(), length=P.bevel)
            else:
                fillet(inset.edges(), radius=P.bevel)
        return inset.part

    def export(self) -> BuildPart:
        """Export the Tak stone model as an STL file."""
        P = self.params
        debug("[yellow]Exporting STL...[/yellow]")

        if not P.export_folder.exists():
            P.export_folder.mkdir(parents=True, exist_ok=True)
            debug(f"Created export folder: {P.export_folder}")

        # Export using build123d's Mesher
        mesher = Mesher()
        export_part = self._part
        # set type_str based on inset and rotate part based on inset
        if P.do_inset_b and P.do_inset_t:
            type_str = "_inset_both"
            if P.stack_height == 1:
                export_part = self._part.rotate(Axis.X, 90)

        elif P.do_inset_t:
            type_str = "_inset_top"
            if P.stack_height == 1:
                export_part = self._part.rotate(Axis.X, 0)

        elif P.do_inset_b:
            type_str = "_inset_bottom"
            if P.stack_height == 1:
                export_part = self._part.rotate(Axis.X, 180)
        else:
            type_str = "_plain"
            if P.stack_height == 1:
                export_part = self._part.rotate(Axis.X, 90)

        if P.stack_height > 1:
            pass

        if P.do_rounded:
            type_str += "_rounded"
        if P.do_corner_stone:
            type_str += "_corner"

        mesher.add_shape(export_part)

        mesher.write(P.export_folder / f"tak_stone{type_str}.stl")
        debug(f"Model exported as {P.export_folder / f'tak_stone{type_str}.stl'}")
        return self


class Field:
    """3D model for a Tak game field using build123d."""

    def __init__(self, params: FieldParameters = FieldParameters()):
        self.params = params
        self._name = "Tak_field_unspecified"

    @property
    def name(self) -> str:
        """Return the name of the field."""
        return self._name

    @property
    def part(self) -> Part:
        """Return the part of the field."""
        if self._part is None:
            raise ValueError("Field part not built yet. Call build() first.")
        return self._part

    def _do_name(self) -> str:
        """Generate a name for the field based on parameters."""
        name = f"tak_field_{self.params.fields_x}x{self.params.fields_y}"
        if self.params.do_outer_cuts:
            name += "_outer_cuts"
        if self.params.do_magnet_guide:
            name += "_magnet_guide"
        self._name = name
        self._part = None

    def build(self) -> BuildPart:
        """
        Build the Tak game field.
        """

        P = self.params
        self._do_name()
        debug(
            f"[bold green]Building {self.name} with parameters:[/bold green] {self.params}"
        )
        length = P.field_xy
        full_length_x = P.fields_x * P.field_xy
        full_length_y = P.fields_y * P.field_xy
        with BuildPart() as field:
            Box(full_length_x + 2, full_length_y + 2, P.field_height)

            with Locations((0, 0, P.field_height / 2)):
                with GridLocations(length, length, P.fields_x, P.fields_y):
                    Box(length - 2, length - 2, P.field_height * 0.4, mode=Mode.ADD)
                with GridLocations(length, length, P.fields_x + 1, P.fields_y + 1):
                    Box(8, 8, P.field_height, rotation=(0, 0, 45.0), mode=Mode.SUBTRACT)
            with GridLocations(length, length, P.fields_x + 1, P.fields_y + 1):
                Box(8, 8, P.field_height, rotation=(0, 0, 45.0))

            # Cut the outer edges to make spacers flat
            with BuildPart() as frame:
                Box(full_length_x + 12, full_length_y + 12, P.field_height)
                Box(
                    full_length_x + 2,
                    full_length_y + 2,
                    P.field_height,
                    mode=Mode.SUBTRACT,
                )
            add(frame, mode=Mode.SUBTRACT)

            if P.do_outer_cuts:
                with GridLocations(full_length_x + 3, full_length_y + 3, 2, 2):
                    Box(
                        8,
                        8,
                        2 * P.field_height,
                        rotation=(0, 0, 45.0),
                        mode=Mode.SUBTRACT,
                    )

                if P.fields_x > 1:
                    with GridLocations(full_length_x + 3, full_length_y + 3, 1, 2):
                        with GridLocations(length, length, P.fields_x - 1, 1):
                            Box(
                                6,
                                6,
                                2 * P.field_height,
                                rotation=(0, 0, 45.0),
                                mode=Mode.SUBTRACT,
                            )

                if P.fields_y > 1:
                    with GridLocations(full_length_x + 3, full_length_y + 3, 2, 1):
                        with GridLocations(length, length, 1, P.fields_y - 1):
                            Box(
                                6,
                                6,
                                2 * P.field_height,
                                rotation=(0, 0, 45.0),
                                mode=Mode.SUBTRACT,
                            )

            # Add magnet openings (5mm diameter, 2mm deep) at the center of each field cell
            magnet_diameter = 5 * mm
            magnet_depth = 1.5 * mm
            # Place magnets on the outside faces, 4 per side
            magnet_offset_x = (full_length_x + 2) / 2 - magnet_depth / 2 - 0.8
            magnet_offset_y = (full_length_y + 2) / 2 - magnet_depth / 2 - 0.8
            magnet_z = 0

            # Move magnet slots to be accessed from below, 1 layer below the outer frame
            magnet_slot_z = magnet_z  # below the field base
            magnet_modes = Mode.SUBTRACT
            if P.debug_magnets:
                magnet_offset_x += 20  # move the magnets out of the board
                magnet_offset_y += 20
                magnet_modes = Mode.ADD
            # Left and right sides (Y varies, X fixed)
            for i in range(P.fields_y):
                y = i * length - full_length_y / 2 + length / 2
                # Left side (X-)
                with Locations((-magnet_offset_x, y, magnet_slot_z)):
                    Cylinder(
                        radius=magnet_diameter / 2,
                        height=magnet_depth,
                        rotation=(0, 90.0, 0),
                        mode=magnet_modes,
                    )
                    Box(
                        magnet_diameter / 2,
                        magnet_diameter,
                        magnet_depth,
                        rotation=(0, 90.0, 0),
                        mode=magnet_modes,
                        align=(Align.MAX, Align.CENTER, Align.CENTER),
                    )

                # Right side (X+)
                with Locations((magnet_offset_x, y, magnet_slot_z)):
                    Cylinder(
                        radius=magnet_diameter / 2,
                        height=magnet_depth,
                        rotation=(0, 90.0, 0),
                        mode=magnet_modes,
                    )
                    Box(
                        magnet_diameter / 2,
                        magnet_diameter,
                        magnet_depth,
                        rotation=(0, 90.0, 0),
                        mode=magnet_modes,
                        align=(Align.MAX, Align.CENTER, Align.CENTER),
                    )

            # Top and bottom sides (X varies, Y fixed)
            for i in range(P.fields_x):
                x = i * length - full_length_x / 2 + length / 2
                # Bottom side (Y-)
                with Locations((x, -magnet_offset_y, magnet_slot_z)):
                    Cylinder(
                        radius=magnet_diameter / 2,
                        height=magnet_depth,
                        rotation=(90.0, 0, 0),
                        mode=magnet_modes,
                    )
                    Box(
                        magnet_diameter / 2,
                        magnet_depth,
                        magnet_diameter,
                        rotation=(0, 90.0, 0),
                        mode=magnet_modes,
                        align=(Align.MAX, Align.CENTER, Align.CENTER),
                    )
                # Top side (Y+)
                with Locations((x, magnet_offset_y, magnet_slot_z)):
                    Cylinder(
                        radius=magnet_diameter / 2,
                        height=magnet_depth,
                        rotation=(90.0, 0, 0),
                        mode=magnet_modes,
                    )
                    Box(
                        magnet_diameter / 2,
                        magnet_depth,
                        magnet_diameter,
                        rotation=(0, 90.0, 0),
                        mode=magnet_modes,
                        align=(Align.MAX, Align.CENTER, Align.CENTER),
                    )

            if P.do_magnet_guide:
                # Add a triangle on top of each field cell
                triangle_height = P.field_height * 0.08
                triangle_base = 1.0
                triangle_offset_z = P.field_height * 0.34

                with BuildSketch(Plane.XY.offset(triangle_offset_z)) as tri_sketch:
                    with GridLocations(full_length_x + 3, full_length_y - 5, 1, 2):
                        with GridLocations(length, length, P.fields_x, 1):
                            Triangle(
                                a=triangle_base,
                                b=triangle_base + 1,
                                c=triangle_base + 1,
                                rotation=0.0,
                            )

                extrude(tri_sketch.sketch, amount=triangle_height, mode=Mode.SUBTRACT)

                with BuildSketch(Plane.XY.offset(triangle_offset_z)) as tri_sketch:

                    with GridLocations(full_length_x - 5, full_length_y + 3, 2, 1):
                        with GridLocations(length, length, 1, P.fields_y):
                            Triangle(
                                a=triangle_base,
                                b=triangle_base + 1,
                                c=triangle_base + 1,
                                rotation=90.0,
                            )

                extrude(
                    tri_sketch.sketch,
                    amount=triangle_height,
                    both=yes,
                    mode=Mode.SUBTRACT,
                )

            if P.do_copyrights:
                try:
                    # add a creators text "Created by 42sol.eu" on the bottom face
                    text_depth = min(1.0, P.field_height * 0.15)  # Conservative text depth
                    # Position text on the bottom face of the field
                    text_z_offset = -P.field_height / 4
                    # TODO: copyright text is not working ... and needs to be fixed
                    with BuildSketch(Plane.XY.offset(text_z_offset)) as text_sketch:
                        Text(
                            "42sol.eu",  # Shorter text to avoid mesh complexity
                            font_size=21.0,  # Smaller font to reduce complexity
                            font="Arial",
                            rotation=90.0,  # No rotation to reduce complexity
                        )
                    # Use a shallow extrusion to avoid mesh issues
                    extrude(text_sketch.sketch, amount=text_depth, mode=Mode.SUBTRACT)
                except Exception as e:
                    debug(f"Copyright text creation failed: {e}. Skipping copyright text.")
                    # If text creation fails, continue without it

        self._part = field.part
        return self

    def export(self) -> BuildPart:
        """Export the Tak game field model as an STL file."""
        P = self.params

        debug(f"[yellow]Exporting Field {self._name} STL...[/yellow]")

        if not P.export_folder.exists():
            P.export_folder.mkdir(parents=True, exist_ok=True)
            debug(f"Created export folder: {P.export_folder}")

        # Export using build123d's Mesher
        mesher = Mesher()
        mesher.add_shape(self._part)

        mesher.write(P.export_folder / f"{self._name}.stl")
        debug(f"Field model exported as {P.export_folder / f'{self._name}.stl'}")
        return self


# %% [Setup]
debug("Creating Tak stone model")
P = StoneParameters()

# %% [Display]
if False:
    set_port(3939)
    set_defaults(reset_camera=Camera.KEEP)
    FP = FieldParameters(P)
    with BuildPart() as magnet_test:
        Box(30, 30, 20)
        add(
            MagnetSlots(nozzle_size=0.8, layer_height=0.4).build(
                position=Location((-3, 0, 3 - 1.5 * FP.nozzle_diameter)), do_marker=True
            ),
            mode=Mode.SUBTRACT,
        )
        add(
            MagnetSlots(nozzle_size=0.8, layer_height=0.4).build(
                position=Location((-3, 6, 3 - 1.5 * FP.nozzle_diameter)),
                rotation=(180, 0, 0),
                do_marker=True,
            ),
            mode=Mode.SUBTRACT,
        )
        # add(MagnetSlots(nozzle_size=.8, layer_height=.4).build(position=Location((-3, 0, 3-1.5*FP.nozzle_diameter)),  rotation=( 0,  90, 0), do_marker=True), mode=Mode.SUBTRACT)
        # add(MagnetSlots(nozzle_size=.8, layer_height=.4).build(position=Location((-3, 0, 3-1.5*FP.nozzle_diameter)),  rotation=( 0, 180, 0), do_marker=True), mode=Mode.SUBTRACT)
        # add(MagnetSlots(nozzle_size=.8, layer_height=.4).build(position=Location((-3, 10, 3-1.5*FP.nozzle_diameter)), rotation=(0, 0, 180), do_marker=True), mode=Mode.SUBTRACT)
        # add(MagnetSlots(nozzle_size=.8, layer_height=.4).build(position=Location((-3, 10, 3-1.5*FP.nozzle_diameter)), rotation=(0, 180, 0), do_marker=True), mode=Mode.SUBTRACT)

    show(magnet_test.part, names=["Magnet Test"], colors=["#1f4fefee"])
    # export magnet_test.part as stl
    m = Mesher()
    m.add_shape(magnet_test.part)
    m.write(P.export_folder / "magnet_test.stl")


if P.do_show:
    try:
        set_port(3939)
        set_defaults(reset_camera=Camera.KEEP)
        FP = FieldParameters(P)
        M1 = TakStone(P)
        M1.params.do_corner_stone = yes
        corner_stone = M1.build().part.move(Location((FP.field_xy, 0, 0)))
        M1.params.do_corner_stone = no
        stone_model = M1.build().part.move(Location((FP.field_xy, FP.field_xy, 0)))

        # TODO: play with field parameters to test
        # MAYBE: Improve positioning of magnet guides (integrate magnet guide into slot cut)
        # NEW: field extensions with 5x1, 4x1
        FP.do_outer_cuts = yes
        FP.do_magnet_guide = yes

        objects = [corner_stone, stone_model]
        names = ["corner_stone", "stone_model"]
        
        # Setup colormap if enabled
        if P.use_colormap:
            setup_colormap("tab20")  # Use built-in tab20 colormap
            colors = None  # Let set_colormap handle the coloring automatically
        else:
            colors = ["#000000ff", "#FFFFFFff"]

        if True:
            M_fields = {}

            for i in range(FP.min_fields, FP.max_fields + 1):
                
                # 1xN fields
                FP.fields_x = 1
                FP.fields_y = i
                key = f"{FP.fields_x}x{FP.fields_y}"
                M_fields[key] = Field(FP)
                field = (
                    M_fields[key]
                    .build()
                    .part.move(Location(((i - 3) * 4 * FP.field_xy * 2, 0, -20)))
                )
                objects.append(field)
                names.append(M_fields[key].name)

                # 2xN fields
                FP.fields_x = 2
                FP.fields_y = i
                key = f"{FP.fields_x}x{FP.fields_y}"
                M_fields[key] = Field(FP)
                field = (
                    M_fields[key]
                    .build()
                    .part.move(Location(((i - 3) * 4 * FP.field_xy * 2, 0, -40)))
                )
                objects.append(field)
                names.append(M_fields[key].name)

                # 3xN fields
                FP.fields_x = 3
                FP.fields_y = i
                key = f"{FP.fields_x}x{FP.fields_y}"
                M_fields[key] = Field(FP)
                field = (
                    M_fields[key]
                    .build()
                    .part.move(Location(((i - 3) * 4 * FP.field_xy * 2, 0, -60)))
                )
                objects.append(field)
                names.append(M_fields[key].name)

                # NxN fields
                FP.fields_x = i
                FP.fields_y = i
                key = f"{FP.fields_x}x{FP.fields_y}"
                M_fields[key] = Field(FP)
                field = (
                    M_fields[key]
                    .build()
                    .part.move(
                        Location(((i - 3) * 4 * FP.field_xy * 2 + FP.field_xy * 2, 0, -70))
                    )
                )
                objects.append(field)
                names.append(M_fields[key].name)
                
            # Handle colors: if using colormap, let set_colormap handle it, otherwise use fallback colors
            if not P.use_colormap or colors is not None:
                # Generate fallback colors for all objects
                field_count = len(objects) - 2  # Subtract the 2 stone objects
                field_colors = get_colormap_colors(field_count, 'default', 0.8)
                if colors is not None:
                    colors.extend(field_colors)
                else:
                    colors = ["#000000ff", "#FFFFFFff"] + field_colors
        else:
            FP.fields_x = 4
            FP.fields_y = 4
            key = f"{FP.fields_x}x{FP.fields_y}"
            M_fields[key] = Field(FP)
            field = M_fields[key].build().part.move(Location((0, 0, -10)))
            objects.append(field)
            names.append(M_fields[key].name)
            # Handle single field color
            if not P.use_colormap or colors is not None:
                if colors is not None:
                    colors.append("#EEEE00aa")
                else:
                    colors = ["#000000ff", "#FFFFFFff", "#EEEE00aa"]

        # Show with or without colors based on colormap setup
        if P.use_colormap and colors is None:
            show(*objects, names=names)  # Let set_colormap handle colors automatically
        else:
            show(*objects, names=names, colors=colors)
    except ImportError:
        print("ocp_vscode.show not available. Model built but not displayed.")

# %% [Export]
if P.do_export:
    debug("Exporting model")
    try:
        print("Exporting Tak stone model...")
        M1.params.do_corner_stone = yes
        M1.export()
        print("Exporting Tak field model...")
        M1.params.do_corner_stone = no
        M1.export()
        FP.fields_x = 8
        FP.fields_y = 8
        for key, field in M_fields.items():
            print(f"Exporting {field.name}...")
            field.export()
    except Exception as e:
        print(f"Export failed: {e}")

# %% [End of file]
