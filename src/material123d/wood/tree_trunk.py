# -*- coding: utf-8 -*-
"""
----
file-name:       tree_trunk.py
file-uuid:       70ce686d-b09d-4dc5-8a9a-49a297da5fd7
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
    """Parameters for the tree_trunk.py"""
    show_debug:    bool =    yes
    do_show:       bool =    yes
    do_export:     bool =    no  # Disabled due to export issues
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
        # Start with the innermost ring at a base radius
        base_inner_radius = 0.12  # Increased from 0.08 for better proportions
        
        # Growth rate: each ring's inner radius is 50% larger than the previous ring's inner radius
        growth_rate = 1.5  # 50% increase = multiply by 1.5
        
        # Calculate all ring inner radii using exponential growth
        ring_inner_radii = []
        ring_outer_radii = []
        current_inner = base_inner_radius
        
        for i in range(num_rings):
            ring_inner_radii.append(current_inner)
            # Ring thickness is proportional to the inner radius to maintain similar proportions
            ring_thickness = current_inner * 0.3  # Increased from 0.25 to 0.3 for better thickness
            ring_outer_radii.append(current_inner + ring_thickness)
            # Next ring's inner radius is 50% larger
            current_inner = current_inner * growth_rate
            
        # Verify that the outermost ring fits within our desired outer boundary
        max_outer = max(ring_outer_radii)
        if max_outer > outer_radius:
            # Scale down all radii proportionally to fit
            scale_factor = outer_radius / max_outer
            ring_inner_radii = [r * scale_factor for r in ring_inner_radii]
            ring_outer_radii = [r * scale_factor for r in ring_outer_radii]
        
        all_rings = []
        ring_colors = []
        
        # Create and sweep each ring separately to get 6 tubes
        for n in range(num_rings):
    
            with BuildPart() as _model:
                # Create a twisted spline path for the trunk with variations for each ring

                # Define points along a helical/twisted path with ring-specific variations
                points = []
                height = 20
                turns = 2
                steps = 30
                base_radius = 0.5
                
                # Create ring-specific path variations
                # Each ring has slightly different environmental pressures
                ring_lean_x = 0.05 * sin(n * 0.7)  # Slight lean in X direction based on ring
                ring_lean_y = 0.03 * cos(n * 0.9)  # Slight lean in Y direction based on ring
                twist_variation = 1.0 + 0.15 * sin(n * 0.5)  # Vary the twist amount per ring
                radius_drift = 0.02 * cos(n * 1.2)  # Small radius changes per ring
                
                # Store original random state
                original_state = random.getstate()
                
                for i in range(steps + 1):
                    t = i / steps
                    angle = 0.5 * pi * turns * twist_variation * t
                    
                    # Base helical path
                    radius = base_radius + radius_drift
                    
                    # Add ring-specific environmental effects
                    # Simulate wind lean that affects each ring differently
                    wind_effect_x = ring_lean_x * t  # Increases with height
                    wind_effect_y = ring_lean_y * t
                    
                    # Add small random variations that are consistent per ring
                    # Use ring index as seed for reproducible but different patterns
                    random.seed(n * 100 + i)  # Deterministic but different per ring and point
                    jitter_x = 0.01 * random.uniform(-1, 1)
                    jitter_y = 0.01 * random.uniform(-1, 1)
                    
                    x = radius * cos(angle) + wind_effect_x + jitter_x
                    y = radius * sin(angle) + wind_effect_y + jitter_y
                    z = height * t
                    points.append((x, y, z))

                # Restore original random state
                random.setstate(original_state)
                
                # Create a spline from the points
                path = Spline(points)

                z_dir = (points[1][0] - points[0][0], points[1][1] - points[0][1], points[1][2] - points[0][2])
                
                # Use pre-calculated ring radii based on 50% growth pattern
                r1 = ring_inner_radii[n]  # Inner radius of this ring
                r2 = ring_outer_radii[n]  # Outer radius of this ring
                ring_thickness = r2 - r1
                
                # Create natural tree ring profile instead of perfect circles
                # Pass ring index for seasonal variation and reduce irregularity
                outer_points, inner_points = create_tree_ring_profile(r2, r1, irregularity=0.08, num_points=48, ring_index=n)
                
                # Determine ring type for debug output
                ring_type = "Summer (wide)" if (n % 2) == 0 else "Winter (narrow)"
                
                # Calculate gap to next ring (if exists)
                gap_to_next_ring = 0
                gap_percentage = 0
                if n < num_rings - 1:
                    gap_to_next_ring = ring_inner_radii[n + 1] - r2
                    gap_percentage = (gap_to_next_ring / ring_thickness * 100) if ring_thickness > 0 else 0
                
                # Create a simple plane at the start point
                start_plane = Plane.XY.move(Location((points[0][0], points[0][1], points[0][2])))
                
                debug(f"Creating ring {n+1}: r1={r1:.4f}, r2={r2:.4f}, thickness={ring_thickness:.4f}")
                
                # Create outer tube
                with BuildSketch(start_plane) as outer_profile:
                    Circle(r2)
                outer_tube = sweep(outer_profile.sketch, path)
                
                # Create inner tube (for subtraction)
                with BuildSketch(start_plane) as inner_profile:
                    Circle(r1)
                inner_tube = sweep(inner_profile.sketch, path)
                
                # Subtract inner from outer to create ring
                ring_solid = outer_tube - inner_tube
                
                next_color = self._color_map.__next__()
                print(f"Ring {n+1} ({ring_type}): Inner {r1:.3f}, Outer {r2:.3f}, Thickness {ring_thickness:.3f}, Gap {gap_percentage:.1f}%")
            
            # Collect all rings
            all_rings.append(ring_solid)
            ring_colors.append(next_color)
        
        # Display all rings together using individual show_object calls
        for i, (ring_solid, color) in enumerate(zip(all_rings, ring_colors)):
            show_object(ring_solid, name=f"Ring {i+1}", options={"color": color, "alpha": 0.7})
            
        self.part = all_rings
        
    def export(self):
        """Export the part to the specified folder"""
        P = self.params
        if P.do_export and self.part:
            export_path = P.export_folder / "tree_trunk.stl"
            debug(f"[green]Model exported to {export_path}[/green]")
            exporter = Mesher()
            # Add all rings to the exporter
            for i, ring in enumerate(self.part):
                if i % 2 == 0:
                    exporter.add_shape(ring)
            exporter.write(export_path)
            del exporter 
        else:
            debug("Exporting is disabled in parameters or no part created")

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
        model.export()

    debug("Execution completed")
