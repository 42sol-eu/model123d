# -*- coding: utf-8 -*-
"""
----
file-name:       tree_trunk_procedural.py
file-uuid:       70ce686d-b09d-4dc5-8a9a-49a297da5fd7
description:    3D models for tree trunk with procedural tree rings using 50% growth pattern
author:         felix@42sol.eu
project:
    name:       material123d
    uuid:       0a7cefda-00f0-4891-a077-8d1a0965f6d0
"""

# %% [Imports]
from build123d import *
from ocp_vscode import set_port, show_object, show_all, set_defaults, Camera
from ocp_vscode.colors import ColorMap
from dataclasses import dataclass, fields
from rich import print
from pathlib import Path
from math import sin, cos, pi, sqrt
import random
import numpy as np
from pythonperlin import perlin
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt

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

def generate_tree_ring_texture(size=512, num_rings=200, growth_rate=1.5, irregularity=0.1):
    """
    Generate tree ring cross-section texture using procedural approach
    
    Args:
        size: Size of the texture (size x size)
        num_rings: Number of rings to generate
        growth_rate: Growth rate between rings (1.5 = 50% increase)
        irregularity: Amount of random variation (0.0 to 1.0)
    
    Returns:
        2D numpy array representing the tree ring pattern
    """
    # Generate Perlin noise for irregularity
    p = perlin((8,8), dens=32, octaves=2, seed=0)
    
    # Create coordinate grid centered at origin
    idx = np.arange(size) - size / 2
    x, y = np.meshgrid(idx, idx)
    
    # Calculate radial distance from center
    phi = np.sqrt(x**2 + y**2)
    
    # Normalize phi to [0, 1] range
    max_radius = size / 2
    phi_normalized = phi / max_radius
    
    # Calculate ring positions with modified growth pattern for 200 rings
    # With 200 rings, exponential growth would be too extreme
    # Use a smaller base growth that scales down as we get more rings
    base_radius = 0.05  # Start smaller
    ring_positions = []
    current_radius = base_radius
    
    # Calculate a growth rate that will fit all rings
    # For 200 rings, we need much more conservative growth
    effective_growth_rate = pow(0.95 / base_radius, 1.0 / num_rings)  # Growth to reach 95% of max radius
    
    for i in range(num_rings):
        ring_positions.append(current_radius)
        current_radius *= effective_growth_rate
        
    debug(f"Effective growth rate: {effective_growth_rate:.6f} for {num_rings} rings")
    debug(f"Ring range: {ring_positions[0]:.4f} to {ring_positions[-1]:.4f}")
    
    # Create ring pattern using radial periodic function
    # Scale phi to create rings at specific positions
    ring_frequency = num_rings * pi / ring_positions[-1]  # Adjust frequency to fit all rings
    
    # Apply Perlin noise distortion for natural irregularity
    # Resize perlin noise to match texture size
    p_resized = np.repeat(np.repeat(p, size//p.shape[0], axis=0), size//p.shape[1], axis=1)
    
    # Create the ring pattern with distortion
    ring_pattern = np.sin(ring_frequency * phi_normalized + irregularity * 4 * p_resized)
    
    # Convert to ring values (0 = ring boundary, 1 = ring center)
    ring_pattern = (ring_pattern + 1) / 2  # Normalize to [0, 1]
    
    return ring_pattern, ring_positions

def create_ring_profile_from_texture(texture, ring_positions, ring_index, outer_radius, thickness_ratio=0.25):
    """
    Extract a ring profile from the procedural texture
    
    Args:
        texture: 2D numpy array of the tree ring texture
        ring_positions: List of normalized ring positions [0, 1]
        ring_index: Index of the ring to extract (0-based)
        outer_radius: Outer radius for this ring in world units
        thickness_ratio: Thickness as ratio of radius
    
    Returns:
        List of (x, y) points for the ring boundary
    """
    size = texture.shape[0]
    center = size // 2
    
    # Calculate the actual ring radius in texture coordinates
    ring_radius_normalized = ring_positions[ring_index]
    ring_radius_pixels = ring_radius_normalized * (size // 2)
    
    # Sample points around the ring
    num_points = 64
    points = []
    
    for i in range(num_points):
        angle = 2 * pi * i / num_points
        
        # Base position on circle
        base_x = ring_radius_pixels * cos(angle)
        base_y = ring_radius_pixels * sin(angle)
        
        # Sample texture at this position for distortion
        sample_x = int(center + base_x)
        sample_y = int(center + base_y)
        
        # Clamp to texture bounds
        sample_x = max(0, min(size-1, sample_x))
        sample_y = max(0, min(size-1, sample_y))
        
        # Get distortion from texture
        distortion = (texture[sample_y, sample_x] - 0.5) * 0.2  # Scale distortion
        
        # Apply distortion to radius
        distorted_radius = outer_radius * (1 + distortion)
        
        # Convert to world coordinates
        x = distorted_radius * cos(angle)
        y = distorted_radius * sin(angle)
        
        points.append((x, y))
    
    return points

def generate_sequential_ring_boundaries(params):
    """
    Generate ring boundaries sequentially where each outer ring becomes the next inner ring
    
    Args:
        params: Parameters object with all configuration
    
    Returns:
        List of (inner_boundary, outer_boundary) tuples for each ring
    """
    # Generate Perlin noise for distortion
    p = perlin((16,16), dens=64, octaves=3, seed=42)
    
    # Calculate parameters
    num_points = 128
    base_angles = [2 * pi * i / num_points for i in range(num_points)]
    
    # Sample noise for consistent distortion pattern
    noise_samples = []
    for i in range(num_points):
        angle = base_angles[i]
        # Sample noise based on angle
        nx = int((cos(angle * 3) * 0.5 + 0.5) * (p.shape[0] - 1))
        ny = int((sin(angle * 3) * 0.5 + 0.5) * (p.shape[1] - 1))
        nx = max(0, min(p.shape[0] - 1, nx))
        ny = max(0, min(p.shape[1] - 1, ny))
        noise_samples.append(p[nx, ny])
    
    # 1. Start with inner cylinder for the first ring (initial shoot)
    current_inner_boundary = []
    for i in range(num_points):
        angle = base_angles[i]
        x = params.base_radius * cos(angle)
        y = params.base_radius * sin(angle)
        current_inner_boundary.append((x, y))
    
    ring_pairs = []
    current_radius = params.base_radius
    
    debug(f"Starting sequential ring generation with {params.num_rings} rings")
    
    for ring_idx in range(params.num_rings):
        # Calculate growth rate for this ring (fast initial, slower later)
        if ring_idx < params.growth_transition_years:
            # Early years: fast growth
            t = ring_idx / params.growth_transition_years
            growth_rate = params.initial_growth_rate * (1 - t) + params.final_growth_rate * t
        else:
            # Later years: slower growth
            growth_rate = params.final_growth_rate
        
        # Calculate variation for this ring (small initial, larger later)
        if ring_idx < params.variation_transition_years:
            # Early years: small variation
            t = ring_idx / params.variation_transition_years
            ring_variation = params.initial_variation * (1 - t) + params.final_variation * t
        else:
            # Later years: full variation
            ring_variation = params.final_variation
        
        # Generate outer ring with calculated growth and distortion
        # For the first ring, use initial thickness parameter
        if ring_idx == 0:
            # First ring: use initial thickness to create proper cylinder
            current_radius = params.base_radius + params.initial_thickness
        else:
            # Subsequent rings: use growth rate
            current_radius *= growth_rate
        
        outer_boundary = []
        
        for i in range(num_points):
            angle = base_angles[i]
            
            # Apply noise-based distortion scaled by ring variation
            distortion = (noise_samples[i] - 0.5) * ring_variation
            
            # Add subtle ring-specific variation
            ring_specific_variation = sin(ring_idx * 0.15 + angle * 2) * ring_variation * 0.3
            
            # Calculate distorted radius
            total_distortion = distortion + ring_specific_variation
            distorted_radius = current_radius * (1 + total_distortion)
            
            # Convert to world coordinates
            x = distorted_radius * cos(angle)
            y = distorted_radius * sin(angle)
            outer_boundary.append((x, y))
        
        # Store the ring pair
        ring_pairs.append((current_inner_boundary.copy(), outer_boundary.copy()))
        
        # Calculate ring thickness for display
        inner_radius = sqrt(sum(x*x + y*y for x, y in current_inner_boundary) / len(current_inner_boundary))
        outer_radius = sqrt(sum(x*x + y*y for x, y in outer_boundary) / len(outer_boundary))
        ring_thickness = outer_radius - inner_radius
        
        debug(f"Ring {ring_idx + 1}: Inner {inner_radius:.4f}, Outer {outer_radius:.4f}, "
              f"Thickness {ring_thickness:.4f}, Growth {growth_rate:.3f}, Variation {ring_variation:.4f}")
        
        # 6. Use the outer ring as the new inner ring for next iteration
        current_inner_boundary = outer_boundary.copy()
    
    debug(f"Generated {len(ring_pairs)} sequential ring pairs")
    return ring_pairs

# %% [Parameters]
@dataclass
class Parameters:
    """Parameters for the procedural tree trunk"""
    show_debug:    bool =    yes
    do_show:       bool =    no
    do_export:     bool =    yes
    export_folder: Path = file_path() / "_export"
    
    # Tree trunk parameters
    num_rings: int = 10  # Number of rings for testing
    base_radius: float = 0.02  # Small initial shoot radius
    initial_thickness: float = 0.005  # Initial ring thickness (first cylinder)
    initial_growth_rate: float = 1.15  # Fast initial growth
    final_growth_rate: float = 1.02  # Slower growth in later years
    growth_transition_years: int = 5  # Years to transition from fast to slow growth
    
    # Distortion/variation parameters
    initial_variation: float = 0.001  # 0.1% variation for first years
    final_variation: float = 0.01  # 1% variation after 5 years
    variation_transition_years: int = 5  # Years to reach full variation
    
    # Trunk geometry parameters
    trunk_height: float = 2.0  # Short trunk
    trunk_curve: float = 0.05  # Very minimal curve
    trunk_steps: int = 30  # Path resolution
    trunk_offset: float = 0.01  # Offset from center axis
    
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
class ProceduralTreeTrunk:
    """Class to create procedural tree trunk with natural ring growth"""
    
    def __init__(self, params: Parameters = Parameters()):
        debug(f"Creating {__class__.__name__} instance")
        self.part = None
        self.params = params
        self._color_map = ColorMap.accent()
        self.ring_boundaries = None
        self.ring_radii = None

    def generate_boundaries(self):
        """Generate nested ring boundaries that fit exactly"""
        debug("Generating nested ring boundaries using sequential method")
        self.ring_pairs = generate_sequential_ring_boundaries(self.params)
        
        debug(f"Generated {len(self.ring_pairs)} sequential ring pairs")

    def build(self):
        """Create rings with exact nested boundaries"""
        debug(f"Creating part in {__class__.__name__}")
        P = self.params
        
        # Generate boundaries first
        self.generate_boundaries()
        
        # Create spline path for trunk (much straighter)
        points = []
        height = 2  # Short trunk
        turns = 0.05  # Very minimal curve
        steps = 30
        base_radius = 0.01  # Smaller offset for straighter trunk
        
        for i in range(steps + 1):
            t = i / steps
            angle = 2 * pi * turns * t
            x = base_radius * cos(angle)
            y = base_radius * sin(angle) 
            z = height * t
            points.append((x, y, z))

        path = Spline(points)
        start_plane = Plane.XY.move(Location(points[0]))
        
        all_rings = []
        ring_colors = []
        
        num_rings = len(self.ring_pairs)
        debug(f"Creating {num_rings} perfectly nested rings")
        
        # Create each ring using exact boundary pairs
        for i, (inner_boundary, outer_boundary) in enumerate(self.ring_pairs):
            # Calculate approximate radii for display
            inner_radius = sqrt(sum(x*x + y*y for x, y in inner_boundary) / len(inner_boundary))
            outer_radius = sqrt(sum(x*x + y*y for x, y in outer_boundary) / len(outer_boundary))
            ring_thickness = outer_radius - inner_radius
            
            debug(f"Ring {i+1}: Inner {inner_radius:.4f}, Outer {outer_radius:.4f}, Thickness {ring_thickness:.4f}")
            
            # Create ring profile using exact boundaries
            try:
                with BuildSketch(start_plane) as ring_profile:
                    # Create outer boundary spline
                    outer_points = [Vector(pt[0], pt[1]) for pt in outer_boundary]
                    outer_spline = Spline(*outer_points, periodic=True)
                    make_face(outer_spline)  # Outer boundary
                    
                    # Create inner boundary spline and subtract
                    inner_points = [Vector(pt[0], pt[1]) for pt in inner_boundary]
                    inner_spline = Spline(*inner_points, periodic=True)
                    
                    # Subtract inner from outer to create ring
                    with Locations((0, 0)):
                        make_face(inner_spline, mode=Mode.SUBTRACT)
                
                # Sweep the ring along the path
                ring_solid = sweep(ring_profile.sketch, path)
                
                # Display information
                ring_type = "Summer (wide)" if (i % 2) == 0 else "Winter (narrow)"
                year = (i // 2) + 1
                
                next_color = self._color_map.__next__()
                print(f"Ring {i+1}/{num_rings} ({ring_type}, Year {year}): "
                      f"Inner {inner_radius:.3f}, Outer {outer_radius:.3f}, "
                      f"Thickness {ring_thickness:.3f}")
                
                all_rings.append(ring_solid)
                ring_colors.append(next_color)
                
            except Exception as e:
                debug(f"Error creating ring {i+1}: {e}")
                continue
        
        # Display all rings
        for i, (ring_solid, color) in enumerate(zip(all_rings, ring_colors)):
            show_object(ring_solid, name=f"Ring {i+1}", 
                        options={"color": color})  # Removed alpha channel
        
        self.part = all_rings

    def export(self):
        """Export the part to STL"""
        P = self.params
        if P.do_export and self.part:
            export_path = P.export_folder / "procedural_tree_trunk.stl"
            debug(f"[green]Model exported to {export_path}[/green]")
            
            # Use Mesher to export all rings
            exporter = Mesher()
            for i, ring in enumerate(self.part):
                if i % 2 == 0:
                    debug(f"- Exporting ring {i+1}")
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
    set_defaults(reset_camera=Camera.KEEP)  # Keep camera position between updates
    
    # Initialize parameters
    P = Parameters()
    model = ProceduralTreeTrunk(P)
    model.build()
    
    if P.do_show:
        debug("Showing the part")
    
    # Set up the export folder and export
    if P.do_export:
        P.export_folder.mkdir(parents=True, exist_ok=True)
        model.export()

    debug("Execution completed")
