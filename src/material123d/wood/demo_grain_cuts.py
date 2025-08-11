#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick     try:
        # 1. Box intersection (wood plank) - centered at origin
        print("1. Creating wood plank cut (200×200×1.5mm) centered at origin...")
        # Use mesh center for cutting, but result will be centered at origin
        bounds = mesh.bounds
        mesh_center = (bounds[0] + bounds[1]) / 2
        
        box = trimesh.creation.box(extents=[200, 200, 1.5])
        box.apply_translation(mesh_center)
        plank = mesh.intersection(box)
        if plank and plank.vertices.shape[0] > 0:
            # Center the result at origin
            plank_bounds = plank.bounds
            plank_center = (plank_bounds[0] + plank_bounds[1]) / 2
            plank.apply_translation(-plank_center)

            output_file = output_dir / "wood_plank_200x200x1.5_centered.stl"
            plank.export(str(output_file))
            print(f"   [green]✓ Saved: {output_file.name} (centered at origin)[/green]")
            cuts_created += 1
        else:
            print("   [yellow]⚠ Empty result[/yellow]")

    except Exception as e:
        print(f"   [red]✗ Error: {e}[/red]") wood grain cutting techniques using trimesh
"""

import trimesh
import numpy as np
from pathlib import Path
from rich import print
from rich.console import Console
from rich.table import Table

console = Console()

def demo_wood_grain_cuts():
    """Demonstrate various cutting techniques on the wood grain STL"""
    
    # Load the wood grain STL
    stl_path = Path(__file__).parent / "wood_grain_modifier.stl"
    
    if not stl_path.exists():
        print(f"[red]Error: {stl_path} not found![/red]")
        return
    
    print("[blue]Loading wood grain STL...[/blue]")
    mesh = trimesh.load_mesh(str(stl_path))
    
    # Create output directory
    output_dir = Path(__file__).parent / "_output" / "demo_cuts"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Get mesh info
    bounds = mesh.bounds
    center = (bounds[0] + bounds[1]) / 2
    extents = mesh.extents
    
    # Display mesh info in a table
    table = Table(title="Wood Grain Mesh Information", show_header=True, header_style="bold magenta")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="white")
    
    table.add_row("Vertices", f"{mesh.vertices.shape[0]:,}")
    table.add_row("Faces", f"{mesh.faces.shape[0]:,}")
    table.add_row("Bounds (min)", f"[{bounds[0][0]:.1f}, {bounds[0][1]:.1f}, {bounds[0][2]:.1f}]")
    table.add_row("Bounds (max)", f"[{bounds[1][0]:.1f}, {bounds[1][1]:.1f}, {bounds[1][2]:.1f}]")
    table.add_row("Extents", f"[{extents[0]:.1f}, {extents[1]:.1f}, {extents[2]:.1f}]")
    table.add_row("Volume", f"{mesh.volume:.2f}" if mesh.is_watertight else "N/A (not watertight)")
    table.add_row("Surface Area", f"{mesh.area:.2f}")
    table.add_row("Is Watertight", "✓" if mesh.is_watertight else "✗")
    
    console.print(table)
    
    cuts_created = 0
    
    print(f"\n[yellow]Creating demonstration cuts...[/yellow]")
    
    try:
        # 1. Box intersection (wood plank)
        print("1. Creating wood plank cut (200×200×1.2mm)...")
        box = trimesh.creation.box(extents=[200, 200, 1.2])
        box.apply_translation(center)
        plank = mesh.intersection(box)
        if plank and plank.vertices.shape[0] > 0:
            output_file = output_dir / "wood_plank_200x200x1.2.stl"
            plank.export(str(output_file))
            print(f"   [green]✓ Saved: {output_file.name}[/green]")
            cuts_created += 1
        else:
            print("   [yellow]⚠ Empty result[/yellow]")
    
    except Exception as e:
        print(f"   [red]✗ Error: {e}[/red]")
    
    try:
        # 2. Cylindrical cut (dowel) - centered at origin
        print("2. Creating cylindrical dowel cut (r=8mm, h=40mm) centered at origin...")
        bounds = mesh.bounds
        mesh_center = (bounds[0] + bounds[1]) / 2
        
        cylinder = trimesh.creation.cylinder(radius=8, height=40)
        cylinder.apply_translation(mesh_center)
        dowel = mesh.intersection(cylinder)
        if dowel and dowel.vertices.shape[0] > 0:
            # Center the result at origin
            dowel_bounds = dowel.bounds
            dowel_center = (dowel_bounds[0] + dowel_bounds[1]) / 2
            dowel.apply_translation(-dowel_center)
            
            output_file = output_dir / "wood_dowel_r8_h40_centered.stl"
            dowel.export(str(output_file))
            print(f"   [green]✓ Saved: {output_file.name} (centered at origin)[/green]")
            cuts_created += 1
        else:
            print("   [yellow]⚠ Empty result[/yellow]")

    except Exception as e:
        print(f"   [red]✗ Error: {e}[/red]")
    
    try:
        # 3. Planar slice - centered at origin
        print("3. Creating planar slice (middle Z section) centered at origin...")
        bounds = mesh.bounds
        mesh_center = (bounds[0] + bounds[1]) / 2
        z_mid = mesh_center[2]
        
        # First cut: keep everything above z_mid - 5
        upper_cut = mesh.slice_plane(plane_origin=[0, 0, z_mid - 5], plane_normal=[0, 0, 1])
        if upper_cut:
            # Second cut: keep everything below z_mid + 5
            slice_cut = upper_cut.slice_plane(plane_origin=[0, 0, z_mid + 5], plane_normal=[0, 0, -1])
            if slice_cut and slice_cut.vertices.shape[0] > 0:
                # Center the result at origin
                slice_bounds = slice_cut.bounds
                slice_center = (slice_bounds[0] + slice_bounds[1]) / 2
                slice_cut.apply_translation(-slice_center)
                
                output_file = output_dir / "wood_slice_middle_10mm_centered.stl"
                slice_cut.export(str(output_file))
                print(f"   [green]✓ Saved: {output_file.name} (centered at origin)[/green]")
                cuts_created += 1
            else:
                print("   [yellow]⚠ Empty result[/yellow]")
        else:
            print("   [yellow]⚠ First cut failed[/yellow]")

    except Exception as e:
        print(f"   [red]✗ Error: {e}[/red]")
    
    try:
        # 4. Corner cut (smaller box at corner) - centered at origin
        print("4. Creating corner sample cut centered at origin...")
        bounds = mesh.bounds
        extents = mesh.extents
        corner_pos = bounds[0] + extents * 0.2  # 20% from minimum corner
        corner_box = trimesh.creation.box(extents=[30, 30, 20])
        corner_box.apply_translation(corner_pos)
        corner_cut = mesh.intersection(corner_box)
        if corner_cut and corner_cut.vertices.shape[0] > 0:
            # Center the result at origin
            corner_bounds = corner_cut.bounds
            corner_center = (corner_bounds[0] + corner_bounds[1]) / 2
            corner_cut.apply_translation(-corner_center)
            
            output_file = output_dir / "wood_corner_sample_centered.stl"
            corner_cut.export(str(output_file))
            print(f"   [green]✓ Saved: {output_file.name} (centered at origin)[/green]")
            cuts_created += 1
        else:
            print("   [yellow]⚠ Empty result[/yellow]")

    except Exception as e:
        print(f"   [red]✗ Error: {e}[/red]")
    
    print(f"\n[green]✓ Demo completed! Created {cuts_created} cut files.[/green]")
    print(f"[blue]Output directory: {output_dir}[/blue]")
    
    return cuts_created

if __name__ == "__main__":
    demo_wood_grain_cuts()
