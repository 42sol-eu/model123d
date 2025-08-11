#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo script showing different STL centering methods
"""

from center_stl import center_mesh_to_origin, get_mesh_info, display_mesh_info
import trimesh
from pathlib import Path
from rich import print as rprint
import numpy as np

def demo_centering_methods():
    """Demonstrate different centering methods"""
    
    # Load a test mesh
    stl_path = Path(__file__).parent / "wood_grain_modifier.stl"
    
    if not stl_path.exists():
        rprint(f"[red]STL file not found: {stl_path}[/red]")
        return
    
    rprint("[blue]Loading original mesh...[/blue]")
    original_mesh = trimesh.load_mesh(str(stl_path))
    
    # Show original mesh info
    original_info = get_mesh_info(original_mesh)
    display_mesh_info(original_info, "Original Mesh")
    
    methods = ['geometric', 'mass', 'bounds']
    results = {}
    
    rprint("\n[yellow]Testing different centering methods...[/yellow]")
    
    for method in methods:
        rprint(f"\n[cyan]Method: {method}[/cyan]")
        
        # Center using this method
        centered_mesh, translation = center_mesh_to_origin(original_mesh, method)
        centered_info = get_mesh_info(centered_mesh)
        
        # Store results
        results[method] = {
            'mesh': centered_mesh,
            'translation': translation,
            'info': centered_info,
            'center_distance': np.linalg.norm(centered_info['center'])
        }
        
        rprint(f"  Translation: [{translation[0]:.3f}, {translation[1]:.3f}, {translation[2]:.3f}]")
        rprint(f"  New center: [{centered_info['center'][0]:.3f}, {centered_info['center'][1]:.3f}, {centered_info['center'][2]:.3f}]")
        rprint(f"  Distance from origin: {results[method]['center_distance']:.6f}")
        
        # Export result
        output_path = Path(__file__).parent / "_output" / f"wood_grain_centered_{method}.stl"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        centered_mesh.export(str(output_path))
        rprint(f"  [green]✓ Saved: {output_path.name}[/green]")
    
    # Summary table
    rprint("\n[blue]Centering Methods Comparison:[/blue]")
    print("─" * 70)
    print(f"{'Method':<12} {'Translation':<25} {'Distance from Origin':<20}")
    print("─" * 70)
    
    for method, result in results.items():
        trans = result['translation']
        distance = result['center_distance']
        trans_str = f"[{trans[0]:.1f}, {trans[1]:.1f}, {trans[2]:.1f}]"
        print(f"{method:<12} {trans_str:<25} {distance:.6f}")
    
    print("─" * 70)
    rprint("\n[green]All methods successfully created centered STL files![/green]")
    
    # Recommendations
    rprint("\n[blue]Method Recommendations:[/blue]")
    rprint("• [cyan]geometric[/cyan]: Best for most cases (centers geometric bounds)")
    rprint("• [cyan]mass[/cyan]: Use for physical simulations (centers center of mass)")  
    rprint("• [cyan]bounds[/cyan]: Use to align minimum corner to origin")

if __name__ == "__main__":
    demo_centering_methods()
