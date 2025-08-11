#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
----
file-name:        center_stl.py
file-uuid:        fdd42084-db1c-430d-8510-d1a576b2c3f3
description:     Utility to center any STL mesh to the origin (0,0,0)
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
from rich.console import Console
from rich.table import Table
import argparse
import sys
from typing import Optional, Tuple

# %% [Constants]
console = Console()

# %% [Functions]
def get_mesh_info(mesh: trimesh.Trimesh) -> dict:
    """Get comprehensive information about a mesh"""
    bounds = mesh.bounds
    center = (bounds[0] + bounds[1]) / 2
    
    return {
        'vertices': mesh.vertices.shape[0],
        'faces': mesh.faces.shape[0],
        'bounds_min': bounds[0],
        'bounds_max': bounds[1],
        'center': center,
        'extents': mesh.extents,
        'volume': mesh.volume if mesh.is_watertight else None,
        'surface_area': mesh.area,
        'is_watertight': mesh.is_watertight,
        'is_centered': np.allclose(center, [0, 0, 0], atol=0.001)
    }

def display_mesh_info(info: dict, title: str = "Mesh Information"):
    """Display mesh information in a formatted table"""
    table = Table(title=title, show_header=True, header_style="bold magenta")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="white")
    
    table.add_row("Vertices", f"{info['vertices']:,}")
    table.add_row("Faces", f"{info['faces']:,}")
    table.add_row("Bounds (min)", f"[{info['bounds_min'][0]:.3f}, {info['bounds_min'][1]:.3f}, {info['bounds_min'][2]:.3f}]")
    table.add_row("Bounds (max)", f"[{info['bounds_max'][0]:.3f}, {info['bounds_max'][1]:.3f}, {info['bounds_max'][2]:.3f}]")
    table.add_row("Center", f"[{info['center'][0]:.3f}, {info['center'][1]:.3f}, {info['center'][2]:.3f}]")
    table.add_row("Extents", f"[{info['extents'][0]:.3f}, {info['extents'][1]:.3f}, {info['extents'][2]:.3f}]")
    table.add_row("Volume", f"{info['volume']:.3f}" if info['volume'] is not None else "N/A (not watertight)")
    table.add_row("Surface Area", f"{info['surface_area']:.3f}")
    table.add_row("Is Watertight", "✓" if info['is_watertight'] else "✗")
    table.add_row("Is Centered", "✓" if info['is_centered'] else "✗")
    
    console.print(table)

def center_mesh_to_origin(mesh: trimesh.Trimesh, method: str = 'geometric') -> Tuple[trimesh.Trimesh, np.ndarray]:
    """
    Center a mesh to the origin using different methods
    
    Args:
        mesh: Input trimesh object
        method: Centering method ('geometric', 'mass', 'bounds')
    
    Returns:
        Tuple of (centered_mesh, translation_vector)
    """
    # Make a copy to avoid modifying the original
    centered_mesh = mesh.copy()
    
    if method == 'geometric':
        # Center based on geometric center (midpoint of bounds)
        bounds = mesh.bounds
        center = (bounds[0] + bounds[1]) / 2
    elif method == 'mass':
        # Center based on center of mass (requires watertight mesh)
        if mesh.is_watertight:
            center = mesh.center_mass
        else:
            print("[yellow]Warning: Mesh is not watertight, falling back to geometric center[/yellow]")
            bounds = mesh.bounds
            center = (bounds[0] + bounds[1]) / 2
    elif method == 'bounds':
        # Center based on minimum bounds (align minimum corner to origin)
        center = mesh.bounds[0]
    else:
        raise ValueError(f"Unknown centering method: {method}")
    
    # Apply translation to center at origin
    translation_vector = -center
    centered_mesh.apply_translation(translation_vector)
    
    return centered_mesh, translation_vector

def center_stl_file(input_path: Path, output_path: Path = None, 
                   method: str = 'geometric', show_info: bool = True) -> bool:
    """
    Center an STL file and optionally save the result
    
    Args:
        input_path: Path to input STL file
        output_path: Path for output STL file (optional)
        method: Centering method
        show_info: Whether to display mesh information
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Load the mesh
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            task = progress.add_task(description=f"Loading {input_path.name}...", total=None)
            mesh = trimesh.load_mesh(str(input_path))
            progress.update(task, description=f"Loaded {input_path.name}")
        
        # Get original mesh info
        original_info = get_mesh_info(mesh)
        
        if show_info:
            display_mesh_info(original_info, f"Original Mesh: {input_path.name}")
        
        # Check if already centered
        if original_info['is_centered']:
            print(f"[green]✓ Mesh is already centered at origin![/green]")
            if output_path and output_path != input_path:
                mesh.export(str(output_path))
                print(f"[blue]Copied to: {output_path}[/blue]")
            return True
        
        # Center the mesh
        print(f"[blue]Centering mesh using '{method}' method...[/blue]")
        centered_mesh, translation = center_mesh_to_origin(mesh, method)
        
        # Get centered mesh info
        centered_info = get_mesh_info(centered_mesh)
        
        if show_info:
            display_mesh_info(centered_info, "Centered Mesh")
        
        # Display translation info
        print(f"[cyan]Translation applied: [{translation[0]:.3f}, {translation[1]:.3f}, {translation[2]:.3f}][/cyan]")
        
        # Verify centering
        center_distance = np.linalg.norm(centered_info['center'])
        if center_distance < 0.001:
            print(f"[green]✓ Successfully centered! Distance from origin: {center_distance:.6f}[/green]")
        else:
            print(f"[yellow]⚠ Close to center. Distance from origin: {center_distance:.6f}[/yellow]")
        
        # Save the result
        if output_path:
            centered_mesh.export(str(output_path))
            print(f"[green]✓ Saved centered mesh to: {output_path}[/green]")
        
        return True
        
    except Exception as e:
        print(f"[red]Error processing {input_path}: {e}[/red]")
        return False

def batch_center_stls(input_dir: Path, output_dir: Path = None, 
                        pattern: str = "*.stl", method: str = 'geometric') -> int:
    """
    Center multiple STL files in a directory
    
    Args:
        input_dir: Input directory containing STL files
        output_dir: Output directory (defaults to input_dir/_centered)
        pattern: File pattern to match
        method: Centering method
    
    Returns:
        Number of files successfully processed
    """
    if not input_dir.exists():
        print(f"[red]Input directory does not exist: {input_dir}[/red]")
        return 0
    
    # Find STL files
    stl_files = list(input_dir.glob(pattern))
    if not stl_files:
        print(f"[yellow]No STL files found matching pattern '{pattern}' in {input_dir}[/yellow]")
        return 0
    
    # Set up output directory
    if output_dir is None:
        output_dir = input_dir / "_centered"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"[blue]Found {len(stl_files)} STL files to process[/blue]")
    print(f"[blue]Output directory: {output_dir}[/blue]")
    
    successful = 0
    for stl_file in stl_files:
        print(f"\n[cyan]Processing: {stl_file.name}[/cyan]")
        output_file = output_dir / f"{stl_file.stem}_centered.stl"
        
        if center_stl_file(stl_file, output_file, method, show_info=False):
            successful += 1
    
    print(f"\n[green]✓ Successfully processed {successful}/{len(stl_files)} files[/green]")
    return successful

# %% [CLI Interface]
def main():
    """Command-line interface for the STL centering utility"""
    parser = argparse.ArgumentParser(
        description="Center STL meshes to the origin (0,0,0)",
        epilog= "Examples:\n"
                "  python center_stl.py input.stl\n"
                "  python center_stl.py input.stl -o centered.stl\n"
                "  python center_stl.py -d ./stl_files/\n"
                "  python center_stl.py input.stl -m mass",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Input options
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('input_file', nargs='?', type=Path, 
                        help='Input STL file to center')
    group.add_argument('-d', '--directory', type=Path,
                        help='Process all STL files in directory')
    
    # Output options
    parser.add_argument('-o', '--output', type=Path,
                        help='Output file path (for single file mode)')
    parser.add_argument('--output-dir', type=Path,
                        help='Output directory (for batch mode)')
    
    # Processing options
    parser.add_argument('-m', '--method', choices=['geometric', 'mass', 'bounds'],
                        default='geometric',
                        help='Centering method (default: geometric)')
    parser.add_argument('--pattern', default='*.stl',
                        help='File pattern for batch processing (default: *.stl)')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='Suppress detailed mesh information')
    
    args = parser.parse_args()
    
    # Single file mode
    if args.input_file:
        input_path = Path(args.input_file)
        if not input_path.exists():
            print(f"[red]Input file does not exist: {input_path}[/red]")
            sys.exit(1)
        
        # Determine output path
        if args.output:
            output_path = Path(args.output)
        else:
            output_path = input_path.parent / f"{input_path.stem}_centered.stl"
        
        success = center_stl_file(input_path, output_path, args.method, not args.quiet)
        sys.exit(0 if success else 1)
    
    # Batch mode
    elif args.directory:
        successful = batch_center_stls(
            input_dir=Path(args.directory),
            output_dir=args.output_dir,
            pattern=args.pattern,
            method=args.method
        )
        sys.exit(0 if successful > 0 else 1)

# %% [Module Usage]
if __name__ == "__main__":
    main()
else:
    # When imported as module, provide convenience functions
    __all__ = [
        'center_mesh_to_origin',
        'center_stl_file', 
        'batch_center_stls',
        'get_mesh_info',
        'display_mesh_info'
    ]
