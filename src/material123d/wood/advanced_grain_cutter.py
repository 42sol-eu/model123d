# -*- coding: utf-8 -*-
"""
----
file-name:       advanced_grain_cutter.py
file-uuid:       generated
description:     Advanced wood grain cutting with multiple options using trimesh
author:          felix@42sol.eu
project:
    name:        material123d
    uuid:        0a7cefda-00f0-4891-a077-8d1a0965f6d0
    url:         https://www.github.com/42sol/material123d
"""

# %% [Imports]
import trimesh
import numpy as np
from pathlib import Path
from dataclasses import dataclass
from rich import print
from rich.progress import Progress, SpinnerColumn, TextColumn
from typing import Optional, Tuple, List
import time
import click

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

# %% [Parameters]
@dataclass
class Parameters:
    """Parameters for the advanced grain cutter"""
    show_debug:    bool = yes
    do_export:     bool = yes
    export_folder: Path = file_path() / "_output"
    
    # Performance settings
    simplify_mesh: bool = yes  # Simplify mesh for faster processing
    target_faces: int = 50000  # Target face count for simplification
    
    def __init__(self):
        debug("Initializing advanced parameters")

# %% [Model]
class AdvancedGrainCutter:
    """Advanced wood grain cutter with performance optimizations"""
    
    def __init__(self, params: Parameters = Parameters()):
        debug("Creating AdvancedGrainCutter instance")
        self.params = params
        self.original_mesh = None
        self.working_mesh = None  # Simplified version for operations
        
        # Load the wood grain modifier STL
        stl_path = file_path() / "wood_grain_modifier.stl"
        self._load_mesh(stl_path)
    
    def _load_mesh(self, stl_path: Path):
        """Load and optionally simplify the mesh for better performance"""
        if not stl_path.exists():
            raise FileNotFoundError(f"STL file not found: {stl_path}")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            task = progress.add_task(description="Loading STL file...", total=None)
            
            self.original_mesh = trimesh.load_mesh(str(stl_path))
            debug(f"Original mesh: {self.original_mesh.vertices.shape[0]} vertices, {self.original_mesh.faces.shape[0]} faces")
            
            # Simplify mesh if requested and if it's too complex
            if (self.params.simplify_mesh and 
                self.original_mesh.faces.shape[0] > self.params.target_faces):
                
                progress.update(task, description="Simplifying mesh for better performance...")
                try:
                    self.working_mesh = self.original_mesh.simplify_quadric_decimation(self.params.target_faces)
                    debug(f"Simplified mesh: {self.working_mesh.vertices.shape[0]} vertices, {self.working_mesh.faces.shape[0]} faces")
                except ImportError as e:
                    debug(f"Mesh simplification not available ({e}), using original mesh")
                    progress.update(task, description="Simplification not available, using original mesh...")
                    self.working_mesh = self.original_mesh
                except Exception as e:
                    debug(f"Mesh simplification failed ({e}), using original mesh")
                    progress.update(task, description="Simplification failed, using original mesh...")
                    self.working_mesh = self.original_mesh
            else:
                self.working_mesh = self.original_mesh
            
            progress.update(task, description="Mesh loaded successfully!")
    
    def _apply_rotation(self, mesh: trimesh.Trimesh, rotation: Tuple[float, float, float]) -> trimesh.Trimesh:
        """
        Apply rotation to a mesh
        
        Args:
            mesh: The mesh to rotate
            rotation: Rotation angles in degrees (rx, ry, rz)
        
        Returns:
            Rotated mesh
        """
        rx, ry, rz = rotation
        
        if rx != 0:
            rotation_x = trimesh.transformations.rotation_matrix(np.radians(rx), [1, 0, 0])
            mesh.apply_transform(rotation_x)
        
        if ry != 0:
            rotation_y = trimesh.transformations.rotation_matrix(np.radians(ry), [0, 1, 0])
            mesh.apply_transform(rotation_y)
        
        if rz != 0:
            rotation_z = trimesh.transformations.rotation_matrix(np.radians(rz), [0, 0, 1])
            mesh.apply_transform(rotation_z)
        
        return mesh

    def create_planar_cut(  self, plane_origin: Tuple[float, float, float], 
                            plane_normal: Tuple[float, float, float],
                            keep_positive: bool = True) -> Optional[trimesh.Trimesh]:
        """
        Create a planar cut through the mesh
        
        Args:
            plane_origin: Point on the cutting plane
            plane_normal: Normal vector of the cutting plane
            keep_positive: If True, keep the positive side of the plane
        
        Returns:
            Cut mesh centered at origin or None if empty
        """
        debug(f"Creating planar cut at {plane_origin} with normal {plane_normal}")
        
        try:
            plane_normal_arr = np.array(plane_normal)
            if not keep_positive:
                plane_normal_arr = -plane_normal_arr
                
            cut_mesh = self.working_mesh.slice_plane(
                plane_origin=np.array(plane_origin),
                plane_normal=plane_normal_arr
            )
            
            if cut_mesh and cut_mesh.vertices.shape[0] > 0:
                # Center the result at origin
                cut_bounds = cut_mesh.bounds
                cut_center = (cut_bounds[0] + cut_bounds[1]) / 2
                cut_mesh.apply_translation(-cut_center)
                debug(f"Cut successful: {cut_mesh.vertices.shape[0]} vertices, centered at origin")
                return cut_mesh
            else:
                debug("Cut resulted in empty mesh")
                return None
                
        except ImportError as e:
            debug(f"Planar cut not available (missing dependency: {e})")
            return None
        except Exception as e:
            debug(f"Error during planar cut: {e}")
            return None

    def create_cylindrical_cut( self, center: Tuple[float, float, float], 
                                radius: float, height: float,
                                axis: str = 'z',
                                rotation: Tuple[float, float, float] = (0, 0, 0)) -> Optional[trimesh.Trimesh]:
        """
        Create a cylindrical intersection with the mesh
        
        Args:
            center: Center of the cylinder
            radius: Radius of the cylinder
            height: Height of the cylinder
            axis: Axis along which the cylinder extends ('x', 'y', or 'z')
            rotation: Rotation angles in degrees (rx, ry, rz)
        
        Returns:
            Intersection mesh or None if empty
        """
        debug(f"Creating cylindrical cut: center={center}, radius={radius}, height={height}, rotation={rotation}")
        
        try:
            # Create cylinder mesh
            if axis == 'z':
                cylinder = trimesh.creation.cylinder(radius=radius, height=height)
                transform = trimesh.transformations.translation_matrix(center)
            elif axis == 'x':
                cylinder = trimesh.creation.cylinder(radius=radius, height=height)
                # Rotate 90 degrees around Y axis to align with X
                rotation_matrix = trimesh.transformations.rotation_matrix(np.pi/2, [0, 1, 0])
                translation = trimesh.transformations.translation_matrix(center)
                transform = np.dot(translation, rotation_matrix)
            elif axis == 'y':
                cylinder = trimesh.creation.cylinder(radius=radius, height=height)
                # Rotate 90 degrees around X axis to align with Y
                rotation_matrix = trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0])
                translation = trimesh.transformations.translation_matrix(center)
                transform = np.dot(translation, rotation_matrix)
            else:
                raise ValueError(f"Invalid axis: {axis}. Must be 'x', 'y', or 'z'")
            
            cylinder.apply_transform(transform)
            
            # Apply additional rotation if specified
            if rotation != (0, 0, 0):
                cylinder = self._apply_rotation(cylinder, rotation)
            
            # Perform intersection
            intersection = self.working_mesh.intersection(cylinder)
            
            if intersection and intersection.vertices.shape[0] > 0:
                # Center the result at origin
                intersection_bounds = intersection.bounds
                intersection_center = (intersection_bounds[0] + intersection_bounds[1]) / 2
                intersection.apply_translation(-intersection_center)
                debug(f"Cylindrical intersection successful: {intersection.vertices.shape[0]} vertices, centered at origin")
                return intersection
            else:
                debug("Cylindrical intersection resulted in empty mesh")
                return None
                
        except Exception as e:
            debug(f"Error during cylindrical cut: {e}")
            return None

    def create_spherical_cut(   self, center: Tuple[float, float, float], 
                                radius: float,
                                rotation: Tuple[float, float, float] = (0, 0, 0)) -> Optional[trimesh.Trimesh]:
        """
        Create a spherical intersection with the mesh
        
        Args:
            center: Center of the sphere
            radius: Radius of the sphere
            rotation: Rotation angles in degrees (rx, ry, rz) - for consistency, though spheres are symmetric
        
        Returns:
            Intersection mesh or None if empty
        """
        debug(f"Creating spherical cut: center={center}, radius={radius}, rotation={rotation}")
        
        try:
            # Create sphere mesh
            sphere = trimesh.creation.icosphere(subdivisions=3, radius=radius)
            sphere.apply_translation(center)
            
            # Apply rotation if specified (mainly for consistency with other shapes)
            if rotation != (0, 0, 0):
                sphere = self._apply_rotation(sphere, rotation)
            
            # Perform intersection
            intersection = self.working_mesh.intersection(sphere)
            
            if intersection and intersection.vertices.shape[0] > 0:
                # Center the result at origin
                intersection_bounds = intersection.bounds
                intersection_center = (intersection_bounds[0] + intersection_bounds[1]) / 2
                intersection.apply_translation(-intersection_center)
                debug(f"Spherical intersection successful: {intersection.vertices.shape[0]} vertices, centered at origin")
                return intersection
            else:
                debug("Spherical intersection resulted in empty mesh")
                return None
                
        except Exception as e:
            debug(f"Error during spherical cut: {e}")
            return None
    
    def create_wood_plank_cut(  self, plank_size: Tuple[float, float, float],
                                plank_center: Tuple[float, float, float] = None,
                                rotation: Tuple[float, float, float] = (0, 0, 0)) -> Optional[trimesh.Trimesh]:
        """
        Create a wood plank-shaped cut (rectangular box intersection)
        
        Args:
            plank_size: (width, depth, height) of the plank
            plank_center: Center position of the plank (default: mesh center)
            rotation: Rotation angles in degrees (rx, ry, rz)
        
        Returns:
            Plank-shaped intersection or None if empty
        """
        if plank_center is None:
            bounds = self.working_mesh.bounds
            plank_center = ((bounds[0] + bounds[1]) / 2).tolist()
        
        debug(f"Creating wood plank cut: size={plank_size}, center={plank_center}, rotation={rotation}")
        
        try:
            # Create box mesh
            box = trimesh.creation.box(extents=plank_size)
            box.apply_translation(plank_center)
            
            # Apply rotation if specified
            if rotation != (0, 0, 0):
                box = self._apply_rotation(box, rotation)
            
            # Perform intersection
            intersection = self.working_mesh.intersection(box)
            
            if intersection and intersection.vertices.shape[0] > 0:
                # Center the result at origin
                intersection_bounds = intersection.bounds
                intersection_center = (intersection_bounds[0] + intersection_bounds[1]) / 2
                intersection.apply_translation(-intersection_center)
                debug(f"Plank intersection successful: {intersection.vertices.shape[0]} vertices, centered at origin")
                return intersection
            else:
                debug("Plank intersection resulted in empty mesh")
                return None
                
        except Exception as e:
            debug(f"Error during plank cut: {e}")
            return None
    
    def export_mesh(self, mesh: trimesh.Trimesh, filename: str) -> bool:
        """Export a mesh to STL file"""
        if not self.params.do_export:
            debug("Export disabled in parameters")
            return False
            
        self.params.export_folder.mkdir(parents=True, exist_ok=True)
        output_path = self.params.export_folder / f"{filename}.stl"
        
        try:
            mesh.export(str(output_path))
            debug(f"Exported mesh to {output_path}")
            print(f"[green]✓ Exported: {output_path.name} ({mesh.vertices.shape[0]} vertices)[/green]")
            return True
        except Exception as e:
            debug(f"Export failed: {e}")
            return False
    
    def get_mesh_info(self) -> dict:
        """Get information about the loaded mesh"""
        if not self.working_mesh:
            return {}
        
        bounds = self.working_mesh.bounds
        return {
            'vertices': self.working_mesh.vertices.shape[0],
            'faces': self.working_mesh.faces.shape[0],
            'bounds': bounds,
            'extents': self.working_mesh.extents,
            'volume': self.working_mesh.volume if self.working_mesh.is_watertight else 'N/A',
            'surface_area': self.working_mesh.area,
            'is_watertight': self.working_mesh.is_watertight
        }

# %% [CLI Commands]
@click.group()
@click.option('--debug/--no-debug', default=True, help='Enable debug output')
@click.option('--export/--no-export', default=True, help='Enable exporting cut meshes')
@click.option('--export-folder', type=click.Path(), default=None, help='Output folder for exported files')
@click.pass_context
def cli(ctx, debug, export, export_folder):
    """Advanced Wood Grain Cutter - Create various cuts from wood grain STL files"""
    ctx.ensure_object(dict)
    
    # Initialize parameters
    params = Parameters()
    params.show_debug = debug
    params.do_export = export
    if export_folder:
        params.export_folder = Path(export_folder)
    
    ctx.obj['params'] = params
    
    # Initialize cutter
    try:
        ctx.obj['cutter'] = AdvancedGrainCutter(params)
        
        if debug:
            info = ctx.obj['cutter'].get_mesh_info()
            print(f"[blue]Loaded mesh info:[/blue]")
            print(f"  Vertices: {info['vertices']:,}")
            print(f"  Faces: {info['faces']:,}")
            print(f"  Extents: [{info['extents'][0]:.1f}, {info['extents'][1]:.1f}, {info['extents'][2]:.1f}]")
            print(f"  Is watertight: {info['is_watertight']}")
    except Exception as e:
        print(f"[red]Error initializing cutter: {e}[/red]")
        raise click.Abort()

@cli.command()
@click.option('--width', '-w', type=float, required=True, help='Plank width')
@click.option('--depth', '-d', type=float, required=True, help='Plank depth')
@click.option('--height', '-h', type=float, required=True, help='Plank height')
@click.option('--offset-x', type=float, default=0.0, help='X offset from mesh center')
@click.option('--offset-y', type=float, default=0.0, help='Y offset from mesh center')
@click.option('--offset-z', type=float, default=0.0, help='Z offset from mesh center')
@click.option('--rotate-x', type=float, default=0.0, help='Rotation around X axis (degrees)')
@click.option('--rotate-y', type=float, default=0.0, help='Rotation around Y axis (degrees)')
@click.option('--rotate-z', type=float, default=0.0, help='Rotation around Z axis (degrees)')
@click.option('--output', '-o', type=str, default=None, help='Output filename (without extension)')
@click.pass_context
def plank(ctx, width, depth, height, offset_x, offset_y, offset_z, rotate_x, rotate_y, rotate_z, output):
    """Create a rectangular plank cut from the wood grain"""
    cutter = ctx.obj['cutter']
    
    # Calculate center position
    bounds = cutter.working_mesh.bounds
    mesh_center = (bounds[0] + bounds[1]) / 2
    center = (
        mesh_center[0] + offset_x,
        mesh_center[1] + offset_y, 
        mesh_center[2] + offset_z
    )
    
    print(f"[yellow]Creating plank cut: {width}×{depth}×{height} at offset ({offset_x}, {offset_y}, {offset_z})[/yellow]")
    
    plank_cut = cutter.create_wood_plank_cut(
        plank_size=(width, depth, height),
        plank_center=center,
        rotation=(rotate_x, rotate_y, rotate_z)
    )
    
    if plank_cut:
        if output is None:
            output = f"wood_plank_{width}x{depth}x{height}"
        cutter.export_mesh(plank_cut, output)
        print(f"[green]✓ Plank cut created successfully![/green]")
    else:
        print(f"[red]✗ Plank cut resulted in empty mesh[/red]")

@cli.command()
@click.option('--radius', '-r', type=float, required=True, help='Cylinder radius')
@click.option('--height', '-h', type=float, required=True, help='Cylinder height')
@click.option('--axis', type=click.Choice(['x', 'y', 'z']), default='z', help='Cylinder axis')
@click.option('--offset-x', type=float, default=0.0, help='X offset from mesh center')
@click.option('--offset-y', type=float, default=0.0, help='Y offset from mesh center')
@click.option('--offset-z', type=float, default=0.0, help='Z offset from mesh center')
@click.option('--rotate-x', type=float, default=0.0, help='Rotation around X axis (degrees)')
@click.option('--rotate-y', type=float, default=0.0, help='Rotation around Y axis (degrees)')
@click.option('--rotate-z', type=float, default=0.0, help='Rotation around Z axis (degrees)')
@click.option('--output', '-o', type=str, default=None, help='Output filename (without extension)')
@click.pass_context
def cylinder(ctx, radius, height, axis, offset_x, offset_y, offset_z, rotate_x, rotate_y, rotate_z, output):
    """Create a cylindrical cut from the wood grain"""
    cutter = ctx.obj['cutter']
    
    # Calculate center position
    bounds = cutter.working_mesh.bounds
    mesh_center = (bounds[0] + bounds[1]) / 2
    center = (
        mesh_center[0] + offset_x,
        mesh_center[1] + offset_y, 
        mesh_center[2] + offset_z
    )
    
    print(f"[yellow]Creating cylinder cut: r={radius}, h={height}, axis={axis} at offset ({offset_x}, {offset_y}, {offset_z})[/yellow]")
    
    cylinder_cut = cutter.create_cylindrical_cut(
        center=center,
        radius=radius,
        height=height,
        axis=axis,
        rotation=(rotate_x, rotate_y, rotate_z)
    )
    
    if cylinder_cut:
        if output is None:
            output = f"wood_cylinder_r{radius}_h{height}_{axis}"
        cutter.export_mesh(cylinder_cut, output)
        print(f"[green]✓ Cylinder cut created successfully![/green]")
    else:
        print(f"[red]✗ Cylinder cut resulted in empty mesh[/red]")

@cli.command()
@click.option('--radius', '-r', type=float, required=True, help='Sphere radius')
@click.option('--offset-x', type=float, default=0.0, help='X offset from mesh center')
@click.option('--offset-y', type=float, default=0.0, help='Y offset from mesh center')
@click.option('--offset-z', type=float, default=0.0, help='Z offset from mesh center')
@click.option('--rotate-x', type=float, default=0.0, help='Rotation around X axis (degrees)')
@click.option('--rotate-y', type=float, default=0.0, help='Rotation around Y axis (degrees)')
@click.option('--rotate-z', type=float, default=0.0, help='Rotation around Z axis (degrees)')
@click.option('--output', '-o', type=str, default=None, help='Output filename (without extension)')
@click.pass_context
def sphere(ctx, radius, offset_x, offset_y, offset_z, rotate_x, rotate_y, rotate_z, output):
    """Create a spherical cut from the wood grain"""
    cutter = ctx.obj['cutter']
    
    # Calculate center position
    bounds = cutter.working_mesh.bounds
    mesh_center = (bounds[0] + bounds[1]) / 2
    center = (
        mesh_center[0] + offset_x,
        mesh_center[1] + offset_y, 
        mesh_center[2] + offset_z
    )
    
    print(f"[yellow]Creating sphere cut: r={radius} at offset ({offset_x}, {offset_y}, {offset_z})[/yellow]")
    
    sphere_cut = cutter.create_spherical_cut(
        center=center,
        radius=radius,
        rotation=(rotate_x, rotate_y, rotate_z)
    )
    
    if sphere_cut:
        if output is None:
            output = f"wood_sphere_r{radius}"
        cutter.export_mesh(sphere_cut, output)
        print(f"[green]✓ Sphere cut created successfully![/green]")
    else:
        print(f"[red]✗ Sphere cut resulted in empty mesh[/red]")

@cli.command()
@click.pass_context
def info(ctx):
    """Show information about the loaded wood grain mesh"""
    cutter = ctx.obj['cutter']
    info = cutter.get_mesh_info()
    
    print(f"[blue]Wood Grain Mesh Information:[/blue]")
    print(f"  Vertices: {info['vertices']:,}")
    print(f"  Faces: {info['faces']:,}")
    print(f"  Bounds: [{info['bounds'][0][0]:.1f}, {info['bounds'][0][1]:.1f}, {info['bounds'][0][2]:.1f}] to [{info['bounds'][1][0]:.1f}, {info['bounds'][1][1]:.1f}, {info['bounds'][1][2]:.1f}]")
    print(f"  Extents: [{info['extents'][0]:.1f}, {info['extents'][1]:.1f}, {info['extents'][2]:.1f}]")
    print(f"  Volume: {info['volume']}")
    print(f"  Surface Area: {info['surface_area']:.1f}")
    print(f"  Is watertight: {info['is_watertight']}")

# %% [Main]
if __name__ == "__main__":
    cli()
