# -*- coding: utf-8 -*-
"""
----
file-name:       tree_trunk.py
file-uuid:       70ce686d-b09d-4dc5-8a9a-49a2@dataclass
class Parameters:
    """Parameters for the test_wood_grain.py"""
    show_debug:    bool =    yes
    do_show:       bool =    yes
    do_export:     bool =    no  # Disabled due to export issues
    export_folder: Path = file_path() / "_export"7
description:    3D models for Tak game stones and extendable board using build123d
author:         felix@42sol.eu
project:
    name:       material123d
    uuid:       0a7cefda-00f0-4891-a077-8d1a0965f6d0
    url:        https://www.github.com/42sol/material123d
"""

# %% [Imports]
from build123d import *
from ocp_vscode import set_port, show_object, show_all
from ocp_vscode.colors import ColorMap
from dataclasses import dataclass, fields
from rich import print
from pathlib import Path
from math import sin, cos, pi
import random

# %% [Constants]
no = False 
yes = True
mm = 1

# %% [Functions]
def debug(msg):
    """Print debug message if show_debug is True"""
    if Parameters.show_debug:
        print(f"[blue]DEBUG: {msg}[/blue]")

def file_path():
    """Return the path to the current file"""
    return Path(__file__).parent.resolve()

def create_tree_ring_profile(outer_radius, inner_radius, irregularity=0.1, num_points=64, ring_index=0):
    """
    Create a more natural tree ring profile with irregular edges
    
    Args:
        outer_radius: Outer radius of the ring
        inner_radius: Inner radius of the ring  
        irregularity: Amount of random variation (0.0 to 1.0)
        num_points: Number of points to create the irregular shape
        ring_index: Index of the ring to determine growth pattern
    
    Returns:
        Tuple of (outer_points, inner_points) for creating the ring profile
    """
    outer_points = []
    inner_points = []
    
    # Determine if this is a summer (wide) or winter (narrow) ring
    is_summer_ring = (ring_index % 2) == 0  # Alternate between summer and winter
    growth_variation = 1.2 if is_summer_ring else 0.8  # Summer rings are wider
    
    # Create a base pattern that both inner and outer rings will follow
    # This ensures they have similar shape variations
    base_pattern = []
    for i in range(num_points):
        angle = 2 * pi * i / num_points
        
        # Create base irregular pattern using multiple sine waves
        base_variation = (
            0.4 * sin(2 * angle) +           # Main growth direction variation
            0.25 * sin(5 * angle) +          # Medium frequency bumps
            0.15 * sin(8 * angle) +          # Fine detail variations
            0.1 * sin(12 * angle) +          # Very fine details
            random.uniform(-0.3, 0.3)        # Small random variations
        ) * irregularity
        
        # Add seasonal growth pattern - some parts grow more/less in different seasons
        seasonal_angle_effect = 0.3 * sin(angle + ring_index * 0.5) * growth_variation
        base_variation += seasonal_angle_effect * irregularity
        
        base_pattern.append(base_variation)
    
    # Apply the base pattern to both inner and outer rings with slight differences
    for i in range(num_points):
        angle = 2 * pi * i / num_points
        
        # Outer ring follows the base pattern more strongly
        outer_variation = base_pattern[i] * outer_radius
        # Inner ring follows the same pattern but with slightly less variation
        inner_variation = base_pattern[i] * inner_radius * 0.7  # 70% of outer variation
        
        # Calculate actual radii with variations
        r_outer = outer_radius + outer_variation
        r_inner = inner_radius + inner_variation
        
        # Ensure inner radius is always smaller than outer, with minimum thickness
        min_thickness = (outer_radius - inner_radius) * 0.3  # Minimum 30% of nominal thickness
        r_inner = min(r_inner, r_outer - min_thickness)
        
        # Convert to cartesian coordinates
        x_outer = r_outer * cos(angle)
        y_outer = r_outer * sin(angle)
        x_inner = r_inner * cos(angle)
        y_inner = r_inner * sin(angle)
        
        outer_points.append((x_outer, y_outer))
        inner_points.append((x_inner, y_inner))
    
    return outer_points, inner_points

# %% [Parameters]
@dataclass
class Parameters:
    """Parameters for the test_wood_grain.py"""
    show_debug:    bool =    yes
    do_show:       bool =    yes
    do_export:     bool =    yes
    export_folder: Path = file_path() / "_export"
    
    def __init__(self):
        debug("Initializing core parameters")

    def __str__(self):
        """String representation of the parameters"""
        data = f"Parameters:\n"
        for field in fields(self):
            value = getattr(self, field.name)
            data += f"  {field.name}: {value}\n"

        return data
# %% [Model]

class TreeTrunk:
    """Class to test wood grain generation"""
    
    def __init__(self, params: Parameters = Parameters()):
        debug(f"Creating {__class__.__name__} instance")
        self.part = None  # Placeholder for the part to be created
        self.params = params
        self._color_map = ColorMap.accent()

    def build(self):
        """Create rings and show them all"""
        debug(f"Creating part in {__class__.__name__}")
        P = self.params

        # Sweep a circle profile along the spline to form the trunk
        num_rings = 6
        outer_radius = 0.4
        inner_radius = 0.2
        total_radial_space = outer_radius - inner_radius  # 0.2 total space
        
        # Calculate ring spacing to ensure 20% minimum gap between rings
        # Each ring needs: ring_thickness + gap
        # We want: gap >= 0.2 * ring_thickness
        # So: ring_thickness + 0.2 * ring_thickness = 1.2 * ring_thickness per ring
        available_space_per_ring = total_radial_space / num_rings
        ring_thickness = available_space_per_ring * 0.6  # 60% for the ring itself
        ring_gap = available_space_per_ring * 0.4        # 40% for the gap (> 20% requirement)
        
        all_rings = []
        ring_colors = []
        
        # Create and sweep each ring separately to get 6 tubes
        for n in range(num_rings):
    
            with BuildPart() as _model:
                # Create a twisted spline path for the trunk

                # Define points along a helical/twisted path
                points = []
                height = 20
                turns = 2
                steps = 30
                radius = 0.5
                for i in range(steps + 1):
                    t = i / steps
                    angle = .5 * pi * turns * t
                    # Add jitter: up to 20% of radius
                    jitter = radius * 0.2
                    dx = 0 # random.uniform(-jitter, jitter)
                    dy = 0 # random.uniform(-jitter, jitter)
                    x = radius * cos(angle) + dx
                    y = radius * sin(angle) + dy
                    z = height * t
                    points.append((x, y, z))

                # Create a spline from the points
                path = Spline(points)


                z_dir = (points[1][0] - points[0][0], points[1][1] - points[0][1], points[1][2] - points[0][2])
                
                # Calculate ring radii with proper spacing
                # Each ring is positioned at: inner_radius + n * (ring_thickness + ring_gap)
                ring_start_radius = inner_radius + n * (ring_thickness + ring_gap)
                r1 = ring_start_radius  # Inner radius of this ring
                r2 = ring_start_radius + ring_thickness  # Outer radius of this ring
                
                # Create natural tree ring profile instead of perfect circles
                # Pass ring index for seasonal variation and reduce irregularity
                outer_points, inner_points = create_tree_ring_profile(r2, r1, irregularity=0.08, num_points=48, ring_index=n)
                
                # Determine ring type for debug output
                ring_type = "Summer (wide)" if (n % 2) == 0 else "Winter (narrow)"
                gap_to_next_ring = ring_gap if n < num_rings - 1 else 0
                gap_percentage = (gap_to_next_ring / ring_thickness * 100) if ring_thickness > 0 else 0
                
                with BuildSketch(Plane(origin=points[0], z_dir=z_dir)) as ring_profile:
                    # Create outer boundary using spline through irregular points
                    outer_spline = Spline(*outer_points, periodic=True)
                    make_face(outer_spline)
                    
                    # Create inner boundary (hole) using spline through irregular points  
                    inner_spline = Spline(*inner_points, periodic=True)
                    make_face(inner_spline, mode=Mode.SUBTRACT)
                    
                    next_color = self._color_map.__next__()
                    print(f"Ring {n+1} ({ring_type}): Inner {r1:.3f}, Outer {r2:.3f}, Thickness {ring_thickness:.3f}, Gap {gap_percentage:.1f}%")
                a = sweep(ring_profile.sketch, path)
                #add(a)
            
            # Collect all rings
            all_rings.append(_model.solids()[0])
            ring_colors.append(next_color)
        
        # Display all rings together using individual show_object calls
        for i, (ring_solid, color) in enumerate(zip(all_rings, ring_colors)):
            show_object(ring_solid, name=f"Ring {i+1}", options={"color": color, "alpha": 0.7})
            
        self.part = all_rings
        
    def export(self):
        """Export the part to the specified folder"""
        P = self.params
        if P.do_export:
            export_path = P.export_folder / "tree_trunk"
            debug(f"[green]Model exported to {export_path}[/green]")
            exporter = Mesher()
            exporter.add_shape(self.part)
            exporter.write(export_path)
            del exporter 
        else:
            debug("Exporting is disabled in parameters")

# %% [Main]
if __name__ == "__main__":
    debug("Starting main execution")
    
    # Initialize ocp_vscode
    set_port(3939)
    
    # Initialize parameters
    P = Parameters()
    model = TreeTrunk(P)
    model.build()
    
    if P.do_show:
        debug("Showing the part")
        # Objects are already shown individually in build() method
    # Set up the export folder
    if P.do_export:
        P.export_folder.mkdir(parents=True, exist_ok=True)
        model.export()

    debug("Execution completed")
    